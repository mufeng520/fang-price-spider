#!/usr/bin/env python
# coding=utf-8
# author: mufeng
# 此代码仅供学习与交流，请勿用于商业用途。
# 页面元素的XPATH

from lib.config.config import *

if SPIDER_NAME == LIANJIA_SPIDER:
    ERSHOUFANG_QU_XPATH = '//*[@id="filter-options"]/dl[1]/dd/div/a'
    ERSHOUFANG_BANKUAI_XPATH = '//*[@id="filter-options"]/dl[1]/dd/div[2]/a'
    XIAOQU_QU_XPATH = '//*[@id="filter-options"]/dl[1]/dd/div/a'
    XIAOQU_BANKUAI_XPATH = '//*[@id="filter-options"]/dl[1]/dd/div[2]/a'
    DISTRICT_AREA_XPATH = '//div[3]/div[1]/dl[2]/dd/div/div[2]/a'
    CITY_DISTRICT_XPATH = '///div[3]/div[1]/dl[2]/dd/div/div/a'

    LOUPAN_URL = '.fang.lianjia.com/loupan/'
    XIAOQU_URL = '.lianjia.com/xiaoqu/'
    ERSHOU_URL = '.lianjia.com/ershoufang/'
    ZUFANG_URL = '.lianjia.com/zufang/'


elif SPIDER_NAME == BEIKE_SPIDER:
    ERSHOUFANG_QU_XPATH = '//*[@id="filter-options"]/dl[1]/dd/div/a'
    ERSHOUFANG_BANKUAI_XPATH = '//*[@id="filter-options"]/dl[1]/dd/div[2]/a'
    XIAOQU_QU_XPATH = '//*[@id="filter-options"]/dl[1]/dd/div/a'
    XIAOQU_BANKUAI_XPATH = '//*[@id="filter-options"]/dl[1]/dd/div[2]/a'
    DISTRICT_AREA_XPATH = '//div[3]/div[1]/dl[2]/dd/div/div[2]/a'
    CITY_DISTRICT_XPATH = '///div[3]/div[1]/dl[2]/dd/div/div/a'

    LOUPAN_URL = '.fang.ke.com/loupan/'
    XIAOQU_URL = '.ke.com/xiaoqu/'
    ERSHOU_URL = '.ke.com/ershoufang/'
    ZUFANG_URL = '.ke.com/zufang/'


elif SPIDER_NAME == FANGTIANXIA_SPIDER:
    ERSHOUFANG_QU_XPATH = '//*[@id="filter-options"]/dl[1]/dd/div/a'
    ERSHOUFANG_BANKUAI_XPATH = '//*[@id="filter-options"]/dl[1]/dd/div[2]/a'
    XIAOQU_QU_XPATH = '//*[@id="filter-options"]/dl[1]/dd/div/a'
    XIAOQU_BANKUAI_XPATH = '//*[@id="filter-options"]/dl[1]/dd/div[2]/a'
    DISTRICT_AREA_XPATH = '//div[3]/div[1]/dl[2]/dd/div/div[2]/a'
    CITY_DISTRICT_XPATH = '///div[3]/div[1]/dl[2]/dd/div/div/a'

    LOUPAN_URL = '.fang.ke.com/loupan/'
    XIAOQU_URL = '.ke.com/xiaoqu/'
    ERSHOU_URL = '.ke.com/ershoufang/'
    ZUFANG_URL = '.ke.com/zufang/'


elif SPIDER_NAME == FANGCHANCHAOSHI_SPIDER:
    ERSHOUFANG_QU_XPATH = '//*[@id="filter-options"]/dl[1]/dd/div/a'
    ERSHOUFANG_BANKUAI_XPATH = '//*[@id="filter-options"]/dl[1]/dd/div[2]/a'
    XIAOQU_QU_XPATH = '//*[@id="filter-options"]/dl[1]/dd/div/a'
    XIAOQU_BANKUAI_XPATH = '//*[@id="filter-options"]/dl[1]/dd/div[2]/a'
    DISTRICT_AREA_XPATH = '//div[3]/div[1]/dl[2]/dd/div/div[2]/a'
    CITY_DISTRICT_XPATH = '///div[3]/div[1]/dl[2]/dd/div/div/a'

    LOUPAN_URL = '.fccs.com/newhouse/'
    XIAOQU_URL = '.fccs.com/xiaoqu/'
    ERSHOU_URL = '.fccs.com/second/'
    ZUFANG_URL = '.fccs.com/rent/'
