# -*- coding: utf-8 -*-
import sys


def CheckLocataResults(results, inputs, opts, log):
    if 'source' not in results.__dict__ or 'telapsed' not in results.__dict__:
        log.error('Invalid structure of results.')
        sys.exit(1)

    # Need to implement rest
    return