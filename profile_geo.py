# Copyright (C) 2019-2020 Zilliz. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pyarrow
import pandas
from osgeo import ogr
import arctern

rows = 10000000
func_name = 0
execute_times = 1

import time
output_path = "./output.txt"

def timmer(fun1):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = fun1(*args, **kwargs)
        stop_time = time.time()
        dur = stop_time - start_time
        with open(output_path, 'a') as f:
            f.write(fun1.__name__ + " " + str(dur) + "\n")
        return res
    return wrapper


def _trans(data):
    ret = pandas.Series([data])
    ret = arctern.ST_GeomFromText(ret)
    ret = [ret[0]]* rows
    ret = pandas.Series(ret)
    return ret

def _trans2(data):
    data_array = [data]*rows
    data = pandas.Series(data_array)
    print("HEHE\n")
    #data = arctern.ST_GeomFromText(data)
    return data



def gen_st_envelope_data():
    data = _trans('LINESTRING(77.29 29.07,77.42 29.26,77.27 29.31,77.29 29.07)')
    return data


def gen_st_geomfromtxt():
    data = _trans2("POLYGON ((113.66220266388723 22.39277623851494, 114.58136061218778 22.39277623851494, 114.58136061218778 22.92800492531275 ,113.66220266388723 22.92800492531275, 113.66220266388723 22.39277623851494))")
    return data


def gen_st_length_data():
    data = _trans('LINESTRING(743238 2967416,743238 2967450,743265 2967450, 743265.625 2967416,743238 2967416)')
    return data


def gen_st_area_data():
    #data1 = _trans('POLYGON((10 20,10 30,20 30,20 20,10 20))')
    data1 = _trans('POLYGON((2.99 6.04, 3.20 3.43, 1.02 4.03,  1.01 0.61 , 6.79 0.80 ,  8.01 2.52 ,  6.98 5.20 ,  5.32 3.40 ))')
    return data1


def gen_within_data():
    data1 = _trans("POINT(5 5)")
    data2 = _trans('POLYGON((1 1, 8 1, 8 7, 1 7, 1 1))')
    return data1, data2


def gen_st_point_data():
    data1 = [1.3, 2.5] * rows
    data1 = pandas.Series(data1)
    data2 = [3.8, 4.9] * rows
    data2 = pandas.Series(data2)
    return data1, data2


def gen_st_distance_data():
    data1 = _trans("POINT(1 1)")
    data2 = _trans('POINT(5 2.1)')
    return data1, data2


@timmer
def test_ST_GeomFromTxt():
    string_ptr =arctern.ST_GeomFromText(data_geom)

@timmer
def test_ST_Point():
    string_ptr = arctern.ST_Point(data_st_point1, data_st_point2)

@timmer
def test_ST_Within():
    rst = arctern.ST_Within(data_within1, data_within2)

@timmer
def test_ST_Distance():
    rst = arctern.ST_Distance(data_st_dis1, data_st_dis2)

@timmer
def test_ST_Area():
    rst = arctern.ST_Area(data_st_area)

@timmer
def test_ST_Length():
    rst = arctern.ST_Length(data_length)

@timmer
def test_ST_Envelope():
    rst = arctern.ST_Envelope(data_envelope)

def parse_args(argv):
    import sys, getopt
    try:
        opts, args = getopt.getopt(argv, "rf:", ["unf function name"])
    except getopt.GetoptError:
        print('profile_geo.py -r <rows>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('profile_geo.py -r <rows> -f <udf function name>')
            sys.exit()
        elif opt in ("-r", "--rows"):
            global rows
            rows = int(arg)
        elif opt in ("-f", "--udf"):
            global func_name
            func_name = int(arg)


if __name__ == "__main__":
    import sys
    parse_args(sys.argv[1:])
    funcs = [
        test_ST_Distance,
        test_ST_Point,
        test_ST_Within,
        test_ST_Area,
        test_ST_Length,
        test_ST_Envelope,
        test_ST_GeomFromTxt,
        ]

    if func_name == 6:
        data_geom = gen_st_geomfromtxt()

    if func_name == 5:
        data_envelope = gen_st_envelope_data()

    if func_name == 4:
        data_length = gen_st_length_data()

    if func_name == 3:
        data_st_area = gen_st_area_data()

    if func_name == 2:
        data_within1, data_within2 = gen_within_data()

    if func_name == 1:
        data_st_point1, data_st_point2 = gen_st_point_data()

    if func_name == 0:
        data_st_dis1, data_st_dis2 = gen_st_distance_data()

    for j in range(execute_times):
        funcs[func_name]()

#    for i in range(6):
#        for j in range(execute_times):
#            funcs[i]()
#    funcs[func_name]()
