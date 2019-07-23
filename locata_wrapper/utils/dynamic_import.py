# -*- coding: utf-8 -*-
# Copyright 2019 Waseda University (Nelson Yalta)
# Apache 2.0  (http://www.apache.org/licenses/LICENSE-2.0)

import importlib
import sys


def DynamicImport(import_path, alias=dict(), log=None):
    """dynamic import module and class

    :param str import_path: syntax 'module_name:class_name'
        e.g., 'locata_wrapper.utils.music:MUSIC'
    :param dict alias: shortcut for registered class
    :return: imported class
    """
    if import_path not in alias and ':' not in import_path:
        raise ValueError(
            'import_path should be one of {} or '
            'include ":", e.g. "locata_wrapper.utils.music:MUSIC" : '
            '{}'.format(set(alias), import_path))
    if ':' not in import_path:
        import_path = alias[import_path]

    module_name, objname = import_path.split(':')
    try:
        m = importlib.import_module(module_name)
    except Exception as e:  # NOQA
        log.error('Function specified by my_alg_name not found!')
        sys.exit(1)
    return getattr(m, objname)
