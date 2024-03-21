
import threading
from lib.zone.city import cities,get_city
from lib.zone.district import area_dict
from lib.utility.date import *
from lib.utility.path import *
from lib.config.config import *
from lib.utility.log import logger
import random

class BaseSpider(object):
    @staticmethod
    def random_delay():# 具体时间可以修改random_delay()，由于多线程，建议数值大于10
        if RANDOM_DELAY:
            time.sleep(random.randint(0, 16))

    def __init__(self):
        self.cities = cities
        # 准备日期信息，爬到的数据存放到日期相关文件夹下
        self.date_string = get_date_string()
        print('Today date is: %s' % self.date_string)

        self.city = get_city()
        self.today_path = create_date_path(SPIDER_NAME, self.city, CLASS_NAME, self.date_string)

        self.total_num = 0  # 总的小区个数，用于统计
        print("Target site is {0}".format(SPIDER_NAME))
        self.mutex = threading.Lock()  # 创建锁
    def collect_city_data(self, city_name, datas, fmt="csv"):
        """
        将指定城市的新房楼盘数据存储下来，默认存为csv文件
        :param city_name: 城市
        :param fmt: 保存文件格式
        :return: None
        """
        csv_file = self.today_path + "/{0}.csv".format(city_name)
        with open(csv_file, "a+",encoding='utf-8') as f:
            # 开始获得需要的板块数据

            self.total_num = len(datas)
            if fmt == "csv":
                for data in datas:
                    f.write(self.date_string + "," + data.text() + "\n")
        print("Finish crawl: " + city_name + ", save data to : " + csv_file)


    def collect_area_threading_data(self, city_name, area_name, fmt="csv"):
        """
        对于每个板块,获得这个板块下所有小区的信息
        并且将这些信息写入文件保存
        :param city_name: 城市
        :param area_name: 板块
        :param fmt: 保存文件格式
        :return: None
        """
        district_name = area_dict.get(area_name, "")
        if area_name == district_name:
            csv_file = self.today_path + "/{0}.csv".format(district_name)
        else:
            csv_file = self.today_path + "/{0}_{1}.csv".format(district_name, area_name)
        with open(csv_file, "w",encoding='utf-8') as f:
            # 开始获得需要的板块数据
            xqs = self.get_xiaoqu_info(city_name, area_name)
            # 锁定
            if self.mutex.acquire(1):
                self.total_num += len(xqs)
                # 释放
                self.mutex.release()
            if fmt == "csv":
                for xiaoqu in xqs:
                    f.write(self.date_string + "," + xiaoqu.text() + "\n")
        print("Finish crawl area: " + area_name + ", save data to : " + csv_file)
        logger.info("Finish crawl area: " + area_name + ", save data to : " + csv_file)

    def create_prompt_text(self):
        """
        根据已有城市中英文对照表拼接选择提示信息
        :return: 拼接好的字串
        """
        city_info = list()
        count = 0
        for en_name, ch_name in self.cities.items():
            count += 1
            city_info.append(en_name)
            city_info.append(": ")
            city_info.append(ch_name)
            if count % 4 == 0:
                city_info.append("\n")
            else:
                city_info.append(", ")
        return 'Which city do you want to crawl?\n' + ''.join(city_info)

    def get_chinese_city(self, en):
        """
        拼音拼音名转中文城市名
        :param en: 拼音
        :return: 中文
        """
        return self.cities.get(en, None)
