#!/usr/bin/env python
# coding=utf-8
# author: mufeng
# 此代码仅供学习与交流，请勿用于商业用途。


thread_pool_size = 50

# 防止爬虫被禁，随机延迟设定
# 如果不想delay，就设定False，
# 具体时间可以修改random_delay()，由于多线程，建议数值大于10
RANDOM_DELAY = False
LIANJIA_SPIDER = "链家"
BEIKE_SPIDER = "贝壳"
FANGTIANXIA_SPIDER = "房天下"
FANGCHANCHAOSHI_SPIDER = "房产超市"

# SPIDER_NAME = LIANJIA_SPIDER
# SPIDER_NAME = BEIKE_SPIDER
# SPIDER_NAME = FANGTIANXIA_SPIDER
SPIDER_NAME = FANGCHANCHAOSHI_SPIDER

XIAOQU = "小区"
ERSHOUFANG = "二手房"
LOUPAN = "楼盘"
ZUFANG = "租房"

CLASS_NAME =XIAOQU
# CLASS_NAME = ERSHOUFANG
# CLASS_NAME = LOUPAN
# CLASS_NAME = ZUFANG