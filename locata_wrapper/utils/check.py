# -*- coding: utf-8 -*-
# Copyright 2019 Waseda University (Nelson Yalta)
# Apache 2.0  (http://www.apache.org/licenses/LICENSE-2.0)

import sys


def CheckResults(results, inputs, opts, log):
    if 'source' not in results.__dict__ or 'telapsed' not in results.__dict__:
        log.error('Invalid structure of results.')
        sys.exit(1)

    # Need to implement rest
    return