#!/usr/bin/env python
# coding=utf-8
# author: mufeng
# 此代码仅供学习与交流，请勿用于商业用途。
# 处理后信息的数据结构


class ErShou(object):
    def __init__(self, district, area, name, xiaoqu, price, unitPrice, desc, pic):
        self.district = district
        self.area = area
        self.price = price
        self.name = name
        self.xiaoqu = xiaoqu
        self.unitPrice = unitPrice
        self.desc = desc
        self.pic = pic

    def text(self):
        return self.district + "," + \
                self.area + "," + \
                self.name + "," + \
                self.xiaoqu + "," + \
                self.price + "," + \
                self.unitPrice + "," + \
                self.desc + "," + \
                self.pic

class ZuFang(object):
    def __init__(self, district, area, xiaoqu, layout, size, price):
        self.district = district
        self.area = area
        self.xiaoqu = xiaoqu
        self.layout = layout
        self.size = size
        self.price = price

    def text(self):
        return self.district + "," + \
                self.area + "," + \
                self.xiaoqu + "," + \
                self.layout + "," + \
                self.size + "," + \
                self.price

class XiaoQu(object):
    def __init__(self, district, area, name, price, on_sale):
        self.district = district
        self.area = area
        self.price = price
        self.name = name
        self.on_sale = on_sale

    def text(self):
        return self.district + "," + \
                self.area + "," + \
                self.name + "," + \
                self.price + "," + \
                self.on_sale

class LouPan(object):
    def __init__(self, xiaoqu, price, total):
        # self.district = district
        # self.area = area
        self.xiaoqu = xiaoqu
        # self.address = address
        # self.size = size
        self.price = price
        self.total = total

    def text(self):
        return self.xiaoqu + "," + \
                self.price + "," + \
                self.total