#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
# Copyright (C) 2015 Daniel Rodriguez
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import metaframe as mf


class FrameTest(mf.MetaFrameBase):
    _KEY = 'ft'
    _VAL = True

    @classmethod
    def _new_pre(cls, *args, **kwargs):
        # Insert a kwarg
        kwargs[cls._KEY] = cls._VAL
        return cls, args, kwargs

    @classmethod
    def _init_pre(cls, obj, *args, **kwargs):
        # Remove the kwarg
        kwargs.pop(cls._KEY)
        return obj, args, kwargs

    def __init__(self, *args, **kwargs):
        self._val = kwargs.get(self._KEY, False)


def test_run(main=False):
    ft = FrameTest()
    check = ft._VAL == ft._val
    if not main:
        assert not check  # param has been removed
    else:
        print('ft._val == ft._VAL:', check)


if __name__ == '__main__':
    test_run(main=True)
