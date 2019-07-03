#!/usr/bin/env python
# -*- coding: utf-8 -*-
from argparse import Namespace
import locata_wrapper.utils as locata_utils
import logging

import os
from sacred import Experiment
# from sacred.observers import MongoObserver

import sys


ex = Experiment()
logging.basicConfig(format='%(asctime)s (%(module)s:%(lineno)d) %(levelname)s: %(message)s')
logger = logging.getLogger('my_custom_logger')
ex.logger = logger
# ex.observers.append(MongoObserver.create())


@ex.config
def config_eval():
    """Inputs:

    data_dir:    String with directory path for the LOCATA/DCASE Dev or Eval database
    results_dir: String with directory path in which to save the results of this
                 function
    is_dev:      Kind of database specified by data_dir
                 False: Eval database
                 True: Dev database
    arrays:      List with array names which should be evaluated (optional)
                 LOCATA list {'benchmark2', 'eigenmike', 'dicit','dummy'} is taken
                 as default which contains all available arrays
                 DCASE list {'doa', 'foa'}
    tasks:       List with task(s) (optional)
                 LOCATA List [1,2,3,4,5,6] is taken as default which evaluates
                 over all available tasks
                 DCASE list [1 2 3 4]

    Outputs: N/A (saves results as csv files in save_dir)
    """
    # [locata or dcase]
    dataset = 'locata'  # NOQA
    data_dir = './data'  # NOQA
    results_dir = './results'  # NOQA
    is_dev = True  # NOQA
    arrays = ['benchmark2', 'eigenmike', 'dicit', 'dummy']  # NOQA
    tasks = [1, 2, 3, 4, 5, 6]  # NOQA
    algorithm = 'locata_wrapper.algorithm.music:MUSIC'  # NOQA
    processes = 1  # NOQA


@ex.main
def main_eval(_config, _log):
    args = Namespace(**_config)

    if args.dataset not in ['locata', 'dcase']:
        _log.error('This wrapper only supports LOCATA or DCASE datasets')
        sys.error(1)

    # Selection of the localisation algorithm

    # Enter the name of the PYTHON function of your localization algorithm.
    # The LOCATA organizers provided MUSIC here as an example for the required interface.
    # Check the documentation inside for contents of structures.
    my_alg_name = locata_utils.DynamicImport(args.algorithm, log=_log)

    # Check and process input arguments

    # Create directories if they do not exist already
    if not os.path.exists(args.results_dir):
        _log.warning('Directory for results not found. New directory created.')
        os.makedirs(args.results_dir)

    if not os.path.exists(args.data_dir):
        _log.error('Incorrect data path!')
        sys.exit(1)

    # Initialize settings required for these scripts:
    if args.dataset == 'locata':
        opts = locata_utils.LocataInitalOptions()
    else:
        opts = locata_utils.DCASEInitalOptions()

    # Check and process input arguments
    # check if input contains valid tasks
    if args.dataset == 'locata':
        error_tasks = [x for x in list(set(args.tasks)) if not 0 < x < 7]
    else:
        error_tasks = [x for x in list(set(args.tasks)) if not 0 < x < 5]
    if len(error_tasks) > 1:
        _log.error('Invalid input for task number(s)')
        sys.exit(1)

    # check if input contains valid arrays names
    if args.arrays is None:
        args.arrays = opts.valid_arrays
    else:
        error_arrays = [x for x in list(set(args.arrays))
                        if x not in opts.valid_arrays]
    if len(error_arrays) > 1:
        _log.error('Invalid input for array(s)')
        sys.exit(1)

    _log.info('Available tasks in the dev dataset in {}: {}'.format(
        args.data_dir, args.tasks))

    # Process
    # Parse through all specified task folders
    if args.dataset == 'locata':
        task_process = locata_utils.ProcessTaskLocata
    else:
        task_process = locata_utils.ProcessTaskDCASE

    # Multiprocessing
    if args.processes > 1:
        from pathos.multiprocessing import ProcessingPool
        pool = ProcessingPool(args.processes)

    for this_task in args.tasks:
        if args.processes > 1:
            pool.map(task_process, [my_alg_name], [this_task], [opts], [args], [_log])
        else:
            task_process(this_task, my_alg_name, opts, args, _log)
    if args.processes > 1:
        pool.close()
        pool.join()
    _log.info('Processing finished!')


if __name__ == '__main__':
    ex.run_commandline()
