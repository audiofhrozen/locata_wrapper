# -*- coding: utf-8 -*-
# Copyright 2019 Waseda University (Nelson Yalta)
# Apache 2.0  (http://www.apache.org/licenses/LICENSE-2.0)

from argparse import Namespace


class LocataInitalOptions(object):
    """InitalOptions

       set the parameters for the main function
       Outputs: struct opts with all settings and parameters for main

    """

    def __init__(self):
        super(LocataInitalOptions, self).__init__()
        # Field names used throughout code:
        self.valid_arrays = ['dummy', 'eigenmike', 'benchmark2', 'dicit']
        self.valid_sources = ['hendrik', 'christine', 'alex', 'heinrich',
                              'claas', 'loudspeaker1', 'loudspeaker2',
                              'loudspeaker3', 'loudspeaker4']
        self.valid_results = ['time', 'timestamps', 'broadside_angle',
                              'azimuth', 'elevation', 'range', 'x', 'y', 'z', 'ID']
        self.fields_position_array = ['rotation', 'position', 'ref_vec', 'mic',
                                      'valid_flags']
        self.fields_position_source = ['rotation', 'position', 'ref_vec',
                                       'valid_flags']
        self.fields_audio_source = ['time', 'fs', 'data', 'NS']
        self.fields_audio_array = ['time', 'fs', 'data']
        self.fields_table = ['year', 'month', 'day', 'hour', 'minute', 'second']
        self.columns_position_source = ['year', 'month', 'day', 'hour', 'minute',
                                        'second', 'ref_vec_x', 'ref_vec_y',
                                        'ref_vec_z', 'x', 'y', 'z']

        # Number of mics:
        self.dicit = Namespace(M=15)
        self.eigenmike = Namespace(M=32)
        self.benchmark2 = Namespace(M=12)
        self.dummy = Namespace(M=4)

        self.c = 340.0  # [m/s]


class DCASEInitalOptions(object):
    """InitalOptions

       set the parameters for the main function
       Outputs: struct opts with all settings and parameters for main

    """

    def __init__(self):
        super(DCASEInitalOptions, self).__init__()
        # Field names used throughout code:
        self.valid_arrays = ['dummy', 'eigenmike', 'benchmark2', 'dicit']
        self.valid_sources = ['hendrik', 'christine', 'alex', 'heinrich',
                              'claas', 'loudspeaker1', 'loudspeaker2',
                              'loudspeaker3', 'loudspeaker4']
        self.valid_results = ['time', 'timestamps', 'broadside_angle',
                              'azimuth', 'elevation', 'range', 'x', 'y', 'z', 'ID']
        self.fields_position_array = ['rotation', 'position', 'ref_vec', 'mic',
                                      'valid_flags']
        self.fields_position_source = ['rotation', 'position', 'ref_vec',
                                       'valid_flags']
        self.fields_audio_source = ['time', 'fs', 'data', 'NS']
        self.fields_audio_array = ['time', 'fs', 'data']
        self.fields_table = ['year', 'month', 'day', 'hour', 'minute', 'second']
        self.columns_position_source = ['year', 'month', 'day', 'hour', 'minute',
                                        'second', 'ref_vec_x', 'ref_vec_y',
                                        'ref_vec_z', 'x', 'y', 'z']

        # Number of mics:
        self.dicit = Namespace(M=15)
        self.eigenmike = Namespace(M=32)
        self.benchmark2 = Namespace(M=12)
        self.dummy = Namespace(M=4)

        self.c = 340.0  # [m/s]
