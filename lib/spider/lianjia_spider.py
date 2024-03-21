import re
import threadpool
from bs4 import BeautifulSoup
from lib.item.dataObject import *
from lib.spider.base_spider import *
from lib.utility.date import *
from lib.zone.area import *
import math

class LouPanBaseSpider(BaseSpider):

    @staticmethod
    def get_loupan_info(city_name):
        """
        爬取页面获取城市新房楼盘信息
        :param city_name: 城市
        :return: 新房楼盘信息列表
        """
        total_page = 1
        loupan_list = list()
        page = 'http://{0}{1}'.format(city_name, LOUPAN_URL)
        print(page)
        headers = create_headers()
        response = requests.get(page, timeout=10, headers=headers)
        html = response.content
        soup = BeautifulSoup(html, "lxml")

        # 获得总的页数
        try:
            page_box = soup.find_all('div', class_='page-box')[0]
            matches = re.search('.*data-total-count="(\d+)".*', str(page_box))
            total_page = int(math.ceil(int(matches.group(1)) / 10))
        except Exception as e:
            print("\tWarning: only find one page for {0}".format(city_name))
            print(e)

        print(total_page)
        # 从第一页开始,一直遍历到最后一页
        headers = create_headers()
        for i in range(1, total_page + 1):
            page = 'http://{0}{1}pg{2}'.format(city_name, LOUPAN_URL, i)
            print(page)
            BaseSpider.random_delay()
            response = requests.get(page, timeout=10, headers=headers)
            html = response.content
            soup = BeautifulSoup(html, "lxml")

            # 获得有小区信息的panel
            house_elements = soup.find_all('li', class_="resblock-list")
            for house_elem in house_elements:
                price = house_elem.find('span', class_="number")
                total = house_elem.find('div', class_="second")
                loupan = house_elem.find('a', class_='name')

                # 继续清理数据
                try:
                    price = price.text.strip()
                except Exception as e:
                    price = '0'

                loupan = loupan.text.replace("\n", "")

                try:
                    total = total.text.strip().replace(u'总价', '')
                    total = total.replace(u'/套起', '')
                except Exception as e:
                    total = '0'

                print("{0} {1} {2} ".format(
                    loupan, price, total))

                # 作为对象保存
                loupan = LouPan(loupan, price, total)
                loupan_list.append(loupan)
        return loupan_list

    def start(self):

        t1 = time.time()  # 开始计时
        datas = self.get_loupan_info(self.city)
        self.collect_city_data(self.city, datas)
        t2 = time.time()  # 计时结束，统计结果

        print("Total crawl {0} loupan.".format(self.total_num))
        print("Total cost {0} second ".format(t2 - t1))

class XiaoQuBaseSpider(BaseSpider):

    @staticmethod
    def get_xiaoqu_info(city, area):
        total_page = 1
        district = area_dict.get(area, "")
        chinese_district = get_chinese_district(district)
        chinese_area = chinese_area_dict.get(area, "")
        xiaoqu_list = list()
        page = 'http://{0}{1}{2}/'.format(city, XIAOQU_URL, area)
        print(page)
        logger.info(page)

        headers = create_headers()
        response = requests.get(page, timeout=10, headers=headers)
        html = response.content
        soup = BeautifulSoup(html, "lxml")

        # 获得总的页数
        try:
            page_box = soup.find_all('div', class_='page-box')[0]
            matches = re.search('.*"totalPage":(\d+),.*', str(page_box))
            total_page = int(matches.group(1))
        except Exception as e:
            print("\tWarning: only find one page for {0}".format(area))
            print(e)

        # 从第一页开始,一直遍历到最后一页
        for i in range(1, total_page + 1):
            headers = create_headers()
            page = 'http://{0}{1}{2}/pg{3}'.format(city, XIAOQU_URL, area, i)
            print(page)  # 打印版块页面地址
            BaseSpider.random_delay()
            response = requests.get(page, timeout=10, headers=headers)
            html = response.content
            soup = BeautifulSoup(html, "lxml")

            # 获得有小区信息的panel
            house_elems = soup.find_all('li', class_="xiaoquListItem")
            for house_elem in house_elems:
                price = house_elem.find('div', class_="totalPrice")
                name = house_elem.find('div', class_='title')
                on_sale = house_elem.find('div', class_="xiaoquListItemSellCount")

                # 继续清理数据
                price = price.text.strip()
                name = name.text.replace("\n", "")
                on_sale = on_sale.text.replace("\n", "").strip()

                # 作为对象保存
                xiaoqu = XiaoQu(chinese_district, chinese_area, name, price, on_sale)
                xiaoqu_list.append(xiaoqu)
        return xiaoqu_list

    def start(self):

        t1 = time.time()  # 开始计时

        # 获得城市有多少区列表, district: 区县
        districts = get_districts(self.city)
        print('City: {0}'.format(self.city))
        print('Districts: {0}'.format(districts))
        # 获得每个区的板块, area: 板块
        areas = list()
        for district in districts:
            areas_of_district = get_areas(self.city, district)
            print('{0}: Area list:  {1}'.format(district, areas_of_district))
            if areas_of_district:
                # 用list的extend方法,L1.extend(L2)，该方法将参数L2的全部元素添加到L1的尾部
                areas.extend(areas_of_district)
                # 使用一个字典来存储区县和板块的对应关系, 例如{'beicai': 'pudongxinqu', }
                for area in areas_of_district:
                    area_dict[area] = district
            else:
                areas.append(district)
                area_dict[district] = district
        print("Area:", areas)
        print("District and areas:", area_dict)

        for area in areas:
            datas = self.get_xiaoqu_info(self.city, area)
            self.collect_city_data(self.city, datas)

        # 计时结束，统计结果
        t2 = time.time()
        print("Total crawl {0} areas.".format(len(areas)))
        print("Total cost {0} second to crawl {1} data items.".format(t2 - t1, self.total_num))

class ErShouSpider(BaseSpider):

    @staticmethod
    def get_ershou_info(city_name, area_name):
        """
        通过爬取页面获得城市指定版块的二手房信息
        :param city_name: 城市
        :param area_name: 版块
        :return: 二手房数据列表
        """
        total_page = 1
        district_name = area_dict.get(area_name, "")
        # 中文区县
        chinese_district = get_chinese_district(district_name)
        # 中文版块
        chinese_area = chinese_area_dict.get(area_name, "")

        ershou_list = list()
        page = 'http://{0}{1}{2}/'.format(city_name, ERSHOU_URL, area_name)
        print(page)  # 打印版块页面地址
        headers = create_headers()
        response = requests.get(page, timeout=10, headers=headers)
        html = response.content
        soup = BeautifulSoup(html, "lxml")

        # 获得总的页数，通过查找总页码的元素信息
        try:
            page_box = soup.find_all('div', class_='page-box')[0]
            matches = re.search('.*"totalPage":(\d+),.*', str(page_box))
            total_page = int(matches.group(1))
        except Exception as e:
            print("\tWarning: only find one page for {0}".format(area_name))
            print(e)

        # 从第一页开始,一直遍历到最后一页
        for num in range(1, total_page + 1):
            page = 'http://{0}{1}{2}/pg{3}'.format(city_name, ERSHOU_URL, area_name, num)
            print(page)  # 打印每一页的地址
            headers = create_headers()
            BaseSpider.random_delay()
            response = requests.get(page, timeout=10, headers=headers)
            html = response.content
            soup = BeautifulSoup(html, "lxml")

            # 获得有小区信息的panel
            house_elements = soup.find_all('li', class_="clear")
            for house_elem in house_elements:
                price = house_elem.find('div', class_="totalPrice")
                unitPrice = house_elem.find('div', class_='unitPrice')
                name = house_elem.find('div', class_='title')
                xiaoqu = house_elem.find('div', class_='positionInfo')
                desc = house_elem.find('div', class_="houseInfo")
                pic = house_elem.find('a', class_="img").find('img', class_="lj-lazy")

                # 继续清理数据
                price = price.text.replace("\n","")
                unitPrice = unitPrice.text.replace("\n", "")
                name = name.text.replace("\n", "")
                xiaoqu = xiaoqu.text.replace("\n", "")
                desc = desc.text.replace("\n", "").replace(" ","")
                pic = pic.get('data-original').replace(" ","")
                # print(pic)

                # 作为对象保存
                ershou = ErShou(chinese_district, chinese_area, name, xiaoqu, price, unitPrice, desc, pic)
                ershou_list.append(ershou)
        return ershou_list

    def start(self):

        t1 = time.time()  # 开始计时

        # 获得城市有多少区列表, district: 区县
        districts = get_districts(self.city)
        print('City: {0}'.format(self.city))
        print('Districts: {0}'.format(districts))

        # 获得每个区的板块, area: 板块
        areas = list()
        for district in districts:
            areas_of_district = get_areas(self.city, district)
            print('{0}: Area list:  {1}'.format(district, areas_of_district))
            if areas_of_district:
                # 用list的extend方法,L1.extend(L2)，该方法将参数L2的全部元素添加到L1的尾部
                areas.extend(areas_of_district)
                # 使用一个字典来存储区县和板块的对应关系, 例如{'beicai': 'pudongxinqu', }
                for area in areas_of_district :
                    area_dict[area] = district
            else:
                areas.append(district)
                area_dict[district] = district
        print("Area:", areas)
        print("District and areas:", area_dict)

        for area in areas:
            datas = self.get_ershou_info(self.city, area)
            self.collect_city_data(self.city, datas)

        # 计时结束，统计结果
        t2 = time.time()
        print("Total crawl {0} areas.".format(len(areas)))
        print("Total cost {0} second to crawl {1} data items.".format(t2 - t1, self.total_num))

class ZuFangBaseSpider(BaseSpider):

    @staticmethod
    def get_zufang_info(city_name, area_name):
        matches = None
        """
        通过爬取页面获取城市指定版块的租房信息
        :param city_name: 城市
        :param area_name: 版块
        :return: 出租房信息列表
        """
        total_page = 1
        district_name = area_dict.get(area_name, "")
        chinese_district = get_chinese_district(district_name)
        chinese_area = chinese_area_dict.get(area_name, "")
        zufang_list = list()
        page = 'http://{0}{1}{2}/'.format(city_name, ZUFANG_URL, area_name)
        print(page)

        headers = create_headers()
        response = requests.get(page, timeout=10, headers=headers)
        html = response.content
        soup = BeautifulSoup(html, "lxml")

        # 获得总的页数
        try:
            page_box = soup.find_all('div', class_='content__pg')[0]
            matches = re.search('.*data-totalpage="(\d+)".*', str(page_box))
            total_page = int(matches.group(1))
        except Exception as e:
            print("\tWarning: only find one page for {0}".format(area_name))
            print(e)

        # 从第一页开始,一直遍历到最后一页
        headers = create_headers()
        for num in range(1, total_page + 1):
            page = 'http://{0}{1}{2}/pg{3}'.format(city_name, ZUFANG_URL, area_name, num)
            print(page)
            BaseSpider.random_delay()
            response = requests.get(page, timeout=10, headers=headers)
            html = response.content
            soup = BeautifulSoup(html, "lxml")

            # 获得有小区信息的panel

            ul_element = soup.find('div', class_="content__list")
            house_elements = ul_element.find_all('div', class_="content__list--item")

            if len(house_elements) == 0:
                continue
            # else:
            #     print(len(house_elements))

            for house_elem in house_elements:

                price = house_elem.find('span', class_="content__list--item-price")
                desc1 = house_elem.find('p', class_="content__list--item--title")
                desc2 = house_elem.find('p', class_="content__list--item--des")

                try:

                    # 继续清理数据
                    price = price.text.strip().replace(" ", "").replace("元/月", "")
                    # print(price)
                    desc1 = desc1.text.strip().replace("\n", "")
                    desc2 = desc2.text.strip().replace("\n", "").replace(" ", "")
                    # print(desc1)

                    infos = desc1.split(' ')
                    xiaoqu = infos[0]
                    layout = infos[1]
                    descs = desc2.split('/')
                    # print(descs[1])
                    size = descs[1].replace("㎡", "平米")
                    # print("{0} {1} {2} {3} {4} {5} {6}".format(
                    #     chinese_district, chinese_area, xiaoqu, layout, size, price))

                    # 作为对象保存
                    zufang = ZuFang(chinese_district, chinese_area, xiaoqu, layout, size, price)
                    zufang_list.append(zufang)
                except Exception as e:
                    print("=" * 20 + " page no data")
                    print(e)
                    print(page)
                    print("=" * 20)
        return zufang_list

    def start(self):

        t1 = time.time()  # 开始计时

        # 获得城市有多少区列表, district: 区县
        districts = get_districts(self.city)
        print('City: {0}'.format(self.city))
        print('Districts: {0}'.format(districts))

        # 获得每个区的板块, area: 板块
        areas = list()
        for district in districts:
            areas_of_district = get_areas(self.city, district)
            print('{0}: Area list:  {1}'.format(district, areas_of_district))
            if areas_of_district:
                # 用list的extend方法,L1.extend(L2)，该方法将参数L2的全部元素添加到L1的尾部
                areas.extend(areas_of_district)
                # 使用一个字典来存储区县和板块的对应关系, 例如{'beicai': 'pudongxinqu', }
                for area in areas_of_district:
                    area_dict[area] = district
            else:
                areas.append(district)
                area_dict[district] = district
        print("Area:", areas)
        print("District and areas:", area_dict)

        for area in areas:
            datas = self.get_zufang_info(self.city, area)
            self.collect_city_data(self.city, datas)

        # 计时结束，统计结果
        t2 = time.time()
        print("Total crawl {0} areas.".format(len(areas)))
        print("Total cost {0} second to crawl {1} data items.".format(t2 - t1, self.total_num))


if __name__ == '__main__':
    pass
