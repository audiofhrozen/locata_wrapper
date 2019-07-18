# -*- coding: utf-8 -*-
from argparse import Namespace
import h5py
import glob
import numpy as np
import os
import timeit

from locata_wrapper.utils.load_data import GetLocataTruth
from locata_wrapper.utils.load_data import LoadLocataData
from locata_wrapper.utils.check import CheckLocataResults


def ElapsedTime(time_array):
    n_steps = time_array.shape[0]
    elapsed_time = np.zeros([n_steps])
    for i in range(1, n_steps):
        elapsed_time[i] = (time_array[i] - time_array[i - 1]).total_seconds()
    return np.cumsum(elapsed_time)


def ProcessTaskLocata(this_task, algorithm, opts, args, log):
    task_dir = os.path.join(args.data_dir, 'task{}'.format(this_task))

    # Create directory for this task in results directory:
    # results_task_dir = os.path.join(args.results_dir,
    #                                 'task{}'.format(this_task))
    # os.makedirs(results_task_dir, exist_ok=True)

    # Read all recording IDs available for this task:
    recordings = sorted(glob.glob(os.path.join(task_dir, '*')))

    # Parse through all recordings within this task:
    for this_recording in recordings:
        recording_id = int(this_recording.split('recording')[1])

        # Create directory for this recording in results directory:
        # rec_dir = this_recording.replace(args.data_dir, args.results_dir)
        # os.makedirs(rec_dir, exist_ok=True)

        # Read all recording IDs available for this task:
        array_names = glob.glob(os.path.join(this_recording, '*'))

        for array_dir in array_names:
            this_array = os.path.basename(array_dir)

            log.info('Processing task {}, recording {}, array {}.'.format(this_task, recording_id, this_array))

            # Load data

            # Load data from csv / wav files in database:
            audio_array, audio_source, position_array, position_source, required_time = LoadLocataData(
                array_dir, args, log, args.is_dev)

            log.info('Processing Complete!')

            # Create directory for this array in results directory
            result_dir = array_dir.replace(args.data_dir, args.results_dir)
            os.makedirs(result_dir, exist_ok=True)

            # Load signal
            in_localization = Namespace()

            # Get number of mics and mic array geometry:
            in_localization.numMics = position_array.data[this_array].mic.shape[2]

            # Signal and sampling frequency:
            in_localization.y = audio_array.data[this_array]    # signal
            in_localization.fs = audio_array.fs                 # sampling freq

            # Users must provide estimates for each time stamp in in.timestamps

            # Time stamps required for evaluation
            in_localization.timestamps = ElapsedTime(required_time.time)[required_time.valid_flag]
            in_localization.time = required_time.time[required_time.valid_flag]

            # Extract ground truth

            # position_array stores all optitrack measurements.
            # Extract valid measurements only (specified by required_time.valid_flag).
            truth = GetLocataTruth(this_array, position_array, position_source, required_time, args.is_dev)

            in_localization.array = truth.array
            in_localization.array_name = this_array
            in_localization.mic_geom = truth.array.mic

            log.info('...Running localization using {}'.format(algorithm.__name__))
            start_time = timeit.default_timer()
            results = algorithm(in_localization, opts)

            results.telapsed = timeit.default_timer() - start_time

            # Check results structure is provided in correct format
            CheckLocataResults(results, in_localization, opts, log)
            # Plots & Save results to file

            print(results.telapsed)
            log.info('Localization Complete!')

            # Directory to save figures to:
            
            # with h5py.File('test.hdf5', 'w') as f:
            #   f.create_dataset('azimuth', data=results.source[0].azimuth)
            #    f.create_dataset('elevation', data=results.source[0].elevation)
            exit(1)
