# -*- coding: utf-8 -*-
import glob
import os

from locata_wrapper.utils.load_data import LoadLocataData


def ProcessTaskLocata(this_task, algorithm, opts, args, log):
    task_dir = os.path.join(args.data_dir, 'task{}'.format(this_task))

    # Create directory for this task in results directory:
    results_task_dir = os.path.join(args.results_dir,
                                    'task{}'.format(this_task))
    os.makedirs(results_task_dir, exist_ok=True)

    # Read all recording IDs available for this task:
    recordings = glob.glob(os.path.join(task_dir, '*'))

    # Parse through all recordings within this task:
    for this_recording in recordings:
        recording_id = int(this_recording.split('recording')[1])

        # Create directory for this recording in results directory:
        rec_dir = this_recording.replace(args.data_dir, args.results_dir)
        os.makedirs(rec_dir, exist_ok=True)

        # Read all recording IDs available for this task:
        array_names = glob.glob(os.path.join(this_recording, '*'))

        for this_array in array_names:
            array_id = os.path.basename(this_array)

            log.info('Processing task {}, recording {}, array {}.'.format(this_task, recording_id, array_id))

            # Load data

            # Load data from csv / wav files in database:
            if args.is_dev:
                audio_array, audio_source, position_array, position_source, required_time = LoadLocataData(
                    this_array, args, log)
            else:
                audio_array, position_array, required_time = LoadLocataData(this_array, args, log, is_dev=False)
