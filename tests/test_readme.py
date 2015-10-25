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


from metaframe import MetaFrame

# First creating the class with MetaFrame as metaclass

class A(MetaFrame.as_metaclass(object)):

    @classmethod
    def _new_do(cls, *args, **kwargs):

        nkwargs = dict()
        for key, val in kwargs.items():

            # Remove any argument with a value of None
            if val is None:
                continue

            try:
                val = float(val)
            except:
                continue

            nkwargs[key] = val

        # The only nuisance being the cumbersome call to _new_do
        # super doesn't work
        obj, args, kwargs = cls.__class__._new_do(cls, *args, **nkwargs)
        return obj, args, kwargs

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            print('key, val, type', key, val, type(val))


a = A(p1=72, p2=None, p3='hello', p4=None, p5='72.5')


# Now with a subclassed MetaB from MetaFrame
# Here super can be applied to find the higher in the hierarchy _new_do

class MetaB(MetaFrame):

    def _new_do(cls, *args, **kwargs):

        nkwargs = dict()
        for key, val in kwargs.items():

            # Remove any argument with a value of None
            if val is None:
                continue

            try:
                val = float(val)
            except:
                continue

            nkwargs[key] = val

        # super can be called directly
        obj, args, kwargs = super(MetaB, cls)._new_do(*args, **nkwargs)
        return obj, args, kwargs


class B(MetaB.as_metaclass()):
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            print('key, val, type', key, val, type(val))


b = B(p1=27, p2=None, p3='olleh', p4=None, p5='5.27')
