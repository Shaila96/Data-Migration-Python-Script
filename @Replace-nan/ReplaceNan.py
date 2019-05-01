import pandas as pd
import math
import os
import numpy as np
import simplejson


from os import listdir
from fnmatch import fnmatch



def replaceNone(data_dict, v, rv):
    for key in data_dict.keys():
        # print(type(data_dict[key]))
        # print(data_dict[key])
        # print(type(v))
        # print(v)
        # print(data_dict[key] is v)
        if data_dict[key] is v:
            data_dict[key] = rv
        elif type(data_dict[key]) is dict:
            replaceNone(data_dict[key], v, rv)


def replace_nan():
    dict = {'HR_z': np.nan, 'Time': 4714}
    print(dict)

    replaceNone(dict, np.nan, '')
    print(dict)

    # print(simplejson.dumps(dict, ignore_nan=True, default='d'))
    # print(dict)



####STARTING OF THE SCRIPT####
replace_nan()



