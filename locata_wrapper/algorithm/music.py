# -*- coding: utf-8 -*-
# Copyright 2019 Waseda University (Nelson Yalta)
# Apache 2.0  (http://www.apache.org/licenses/LICENSE-2.0)
from argparse import Namespace
from collections import OrderedDict
import librosa
import logging
import numpy as np
from scipy.ndimage.filters import maximum_filter
from scipy.signal import find_peaks
import sys



def MUSIC(inputs, options, log=logging):
    """MUSIC

    implementation of Multiple SIgnal Classification (MUSIC) algorithm as described in [3].

    Inputs:
    in:
        in.array:               String containing array name: 'eigenmike', 'dicit', 'dummy', 'benchmark2'
        in.y:                   Data matrix
        in.fs:                  Sampling frequency [Hz]
        in.timestamps:          Vector of timestamps at which DoA estimates must be PROVIDED
        in.time:                6xT matrix of system clock times
        in.array.rotation:      Rotation matrix describing array orientation in 3D for each timestamp
        in.array.mic:           Matrix describing microphone positions for each timestamp
    opts:                     Settings structure generated by init()

    Outputs:
    out:
        out.source:             N x 1 struct array, one element for each N estimated sources. In this function: N = 1
                                (single-source)
        out.source(src_idx).azimuth:      Tx1 vector of azimuth estimates, where T is the number of timestamps
                                          in in.timestamps
        out.source(src_idx).elevation:    Tx1 vector of elevation estimates
        out.source(src_idx).time:         Tx1 vector of system time values of estimates (must be identical to in.time!)
        out.source(src_idx).timestamps:   Tx1 vector of timestamps of estimates (must be identical to in.timestamps!)

    References:
        [1]    J. Benesty, C. Jingdong, and I. Cohen, Design of Circular Differential Microphone Arrays.
               Springer, 2015.
        [2]    I. Cohen, J. Benesty, and S. Gannot, Speech Processing in Modern Communication, vol. 3. Berlin,
               Heidelberg: Springer Science & Business Media, 2009.
        [3]    H. L. Van Trees, Detection, Estimation, and Modulation Theory, Optimum Array Processing. John Wiley
               & Sons, 2004.
    """
    az = np.linspace(-np.pi, np.pi, 73)  # Resolution of azimuth: 5 dg
    el = np.linspace(0, np.pi, 19)  # Resolution of elevation: 10 dg

    if inputs.array_name == 'dicit':
        subarray = np.array([6, 7, 9])
        ref_mic = 1
    elif inputs.array_name == 'benchmark2':
        subarray = np.arange(12).astype(np.int)
        ref_mic = 1
    elif inputs.array_name == 'eigenmike':
        subarray = np.arange(32).astype(np.int)
        ref_mic = 1
    elif inputs.array_name == 'dummy':
        subarray = np.arange(4).astype(np.int)
        ref_mic = 1
    else:
        log.error('Array type {} does not exists'.format(inputs.array_name))
        sys.exit(1)

    # MUSIC
    numMic = subarray.shape[0]

    fftPoint = 1024
    frame_duration = 0.03
    frames_per_block = 100  # Number of frames per block
    block_step = 10

    frame_length = int(frame_duration * inputs.fs)

    # -> OptiTracker sampling rate

    # Unique timestamps:
    opti_timestamps, unique_idx = np.unique(inputs.timestamps, return_index=True)
    opti_rotation = inputs.array.rotation[:, unique_idx]
    opti_mics = inputs.array.mic[:, unique_idx]

    duration = inputs.y.shape[0]
    inputs.y = np.asfortranarray(inputs.y)

    # -> STFT
    X = np.stack([librosa.stft(inputs.y[:, ch],
                               n_fft=fftPoint,
                               hop_length=frame_length // 4,
                               win_length=fftPoint,
                               window='hamming',
                               pad_mode='reflect') for ch in subarray], axis=1)
    X = X.transpose(2, 0, 1)
    frame_timestamp = librosa.samples_to_time(np.arange(0, duration, frame_length // 4),
                                              sr=inputs.fs)
    fft_freq = librosa.fft_frequencies(sr=inputs.fs, n_fft=fftPoint)

    nframe = frame_timestamp.shape[0]

    # Check that the frame times and Optitracker times intersect:
    opti_timestamps = opti_timestamps[opti_timestamps < frame_timestamp[-1]]

    # -> MUSIC
    # Make blocks out of frames:
    frame_srt = np.arange(0, nframe - 1, block_step)
    frame_end = np.arange(frames_per_block, nframe, block_step)
    frame_end = np.pad(frame_end, (0, frame_srt.shape[0] - frame_end.shape[0]), 'constant', constant_values=nframe - 1)
    nblocks = frame_srt.shape[0]

    block_timestamps = np.mean([frame_timestamp[frame_srt], frame_timestamp[frame_end]], axis=0)
    # Bandlimit signals to avoid spatial aliasing / low freq effects:
    # NOTE: This is crucial for the DICIT array, the other arrays can be
    # evaluated for fullband signals.
    valid_freq_idx = (800 < fft_freq) * (fft_freq < 1400)
    valid_freq = fft_freq[valid_freq_idx]
    valid_X = X[:, valid_freq_idx]

    _power = np.zeros([fftPoint // 2 - 1, az.shape[0], el.shape[0], nblocks])
    for block_idx in range(nblocks):
        for freq_idx in range(valid_freq.shape[0]):  # fftPoint/2-1
            # Block of FFT frames:
            # print(freq_idx, block_idx)
            data_block = np.squeeze(valid_X[frame_srt[block_idx]:frame_end[block_idx], freq_idx, :])
            if data_block.shape[0] > 1:  # ensure svd does not result in empty U
                # Find nearest OptiTrac sample:
                _diff = block_timestamps[block_idx] - opti_timestamps
                closest_opti_idx = np.argmin(_diff)
                # Autocorrelation
                Rxx = np.dot(data_block.T, np.conj(data_block))

                # Rxx = U * S * U^H, see [3] eq. (9.32)
                U, _, _ = np.linalg.svd(Rxx)

                # [3] eq. (9.37), using spectral sparsity assumption:
                # Signal subspace is 1 dimensional if 1 source is active, hence D = 1
                Un = U[:, 1:]
                
                for a_idx in range(az.shape[0]):
                    for e_idx in range(el.shape[0]):
                        az_idx = az[a_idx]
                        el_idx = el[e_idx]
                        # [2] eq (8.35) modified s.th. az = 0 and el = pi/2 result in eta = [0 1 0],
                        #  i.e., pointing along y-axis:
                        eta = np.array([-np.sin(el_idx) * np.sin(az_idx), np.sin(el_idx) * np.cos(az_idx), np.cos(el_idx)])[:, None]
                        rot_eta = np.dot(np.squeeze(opti_rotation[:, closest_opti_idx, :]), eta)

                        # [2] eq (8.36) - TDoA:
                        tau = 1 / options.c * np.dot(rot_eta.T, np.squeeze(opti_mics[:, closest_opti_idx, subarray]) - 
                            np.repeat(opti_mics[:, closest_opti_idx:closest_opti_idx + 1, subarray[ref_mic]], numMic, axis=1))

                        # [2] eq (8.34) - Steering vector:
                        SV = np.exp(1j * 2 * np.pi * valid_freq[freq_idx] * tau).T

                        # [3] eq. (9.44):
                        _power[freq_idx, a_idx, e_idx, block_idx] = 1. / np.sum(
                            np.abs(np.linalg.multi_dot([SV.conj().T, Un, Un.conj().T, SV])))
    # Sum spectra over all frequencies:
    _spectrum = _power.sum(0).transpose(2, 0, 1)

    # -> Find DOA
    # NOTE: Single-source assumption
    azimuth = np.full([nblocks], np.nan)
    elevation = np.full([nblocks], np.nan)

    for block_idx in range(nblocks):
        if _spectrum.shape[2] == 1:
            # find_peak code for 1 elevation
            locs = find_peaks(_spectrum[block_idx, :])
            if len(locs) > 0:
                azimuth[block_idx] = az[locs[0]]
        else:
            mesh_spec = np.squeeze(_spectrum[block_idx, :, :])

            # Extract regional maxima:
            lm = maximum_filter(mesh_spec, 1)
            # Global maximum:
            loc = np.argmax(lm)
            loc_az, loc_el = np.unravel_index(loc, mesh_spec.shape)
            azimuth[block_idx] = az[loc_az]
            elevation[block_idx] = el[loc_el]

    # -> Interpolate estimates to OptiTracker timestamps
    # Interpolate MUSIC estimates to required time stamps:
    interp_azimuth = np.interp(inputs.timestamps, block_timestamps, azimuth, left=np.NaN)
    print(interp_azimuth)
    exit(1)
    interp_elevation = np.interp(inputs.timestamps, block_timestamps, elevation)

    # Output 1 - interpolated
    N_sources = 1
    out = Namespace()
    out.source = list()
    for src_idx in range(N_sources):
        results = dict(
            year=inputs.time.dt.year,
            month=inputs.time.dt.month,
            day=inputs.time.dt.day,
            hour=inputs.time.dt.hour,
            minute=inputs.time.dt.minute,
            second=inputs.time.dt.second + inputs.time.dt.microsecond / 1e6,
            timestamps=inputs.timestamps,
            azimuth=np.unwrap(interp_azimuth),
            elevation=np.unwrap(interp_elevation),
            )
        out.source.append(results)
    return out
