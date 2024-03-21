#!/usr/bin/env python
# coding=utf-8
# author: mufeng
# 此代码仅供学习与交流，请勿用于商业用途。
# 获得当前目录结构,创建目录结构


import inspect
import os
import sys


def get_root_path():
    file_path = os.path.abspath(inspect.getfile(sys.modules[__name__]))
    parent_path = os.path.dirname(file_path)
    lib_path = os.path.dirname(parent_path)
    root_path = os.path.dirname(lib_path)
    return root_path


def create_data_path():
    root_path = get_root_path()
    data_path = root_path + "/data"
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    return data_path


def create_site_path(site):
    data_path = create_data_path()
    site_path = data_path + "/" + site
    if not os.path.exists(site_path):
        os.makedirs(site_path)
    return site_path


def create_city_path(site, city):
    site_path = create_site_path(site)
    city_path = site_path + "/" + city
    if not os.path.exists(city_path):
        os.makedirs(city_path)
    return city_path

def create_type_path(site, city, type):
    city_path = create_city_path(site, city)
    type_path = city_path + "/" + type
    if not os.path.exists(type_path):
        os.makedirs(type_path)
    return type_path

def create_date_path(site, city, type, date):
    type_path = create_type_path(site, city, type)
    date_path = type_path + "/" + date
    if not os.path.exists(date_path):
        os.makedirs(date_path)
    return date_path


# const for path
ROOT_PATH = get_root_path()
DATA_PATH = ROOT_PATH + "/data"
SAMPLE_PATH = ROOT_PATH + "/sample"
LOG_PATH = ROOT_PATH + "/log"

if __name__ == "__main__":
    create_date_path("lianjia", "sh", "loupan", "20160912")
    create_date_path("anjuke", "bj", "xinfang", "20160912")
