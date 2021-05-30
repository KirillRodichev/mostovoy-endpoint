import numpy as np
from math import sqrt


class Stats:
    @array_function_dispatch(_mean_dispatcher)
    def mean(a, axis=None, dtype=None, out=None, keepdims=np._NoValue, *,where=np._NoValue):
        kwargs = {}
        if keepdims is not np._NoValue:
            kwargs['keepdims'] = keepdims
        if where is not np._NoValue:
            kwargs['where'] = where
        if type(a) is not mu.ndarray:
            try:
                mean = a.mean
            except AttributeError:
                pass
            else:
                return mean(axis=axis, dtype=dtype, out=out, **kwargs)

        return _methods._mean(a, axis=axis, dtype=dtype,out=out, **kwargs)

    @array_function_dispatch(_var_dispatcher)
    def var(a, axis=None, dtype=None, out=None, ddof=0, keepdims=np._NoValue, *,where=np._NoValue):
        kwargs = {}
        if keepdims is not np._NoValue:
            kwargs['keepdims'] = keepdims
        if where is not np._NoValue:
            kwargs['where'] = where

        if type(a) is not mu.ndarray:
            try:
                var = a.var

            except AttributeError:
                pass
            else:
                return var(axis=axis, dtype=dtype, out=out, ddof=ddof, **kwargs)

        return _methods._var(a, axis=axis, dtype=dtype, out=out, ddof=ddof, **kwargs)

    @staticmethod
    def get_avg(data_list):
        return np.mean(data_list)

    @staticmethod
    def get_standard_deviation(data_list):
        return sqrt(np.var(data_list))
