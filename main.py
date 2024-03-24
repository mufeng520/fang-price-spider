from lib.spider import beike_spider,lianjia_spider
from lib.config.config import *
work = {
    LIANJIA_SPIDER:{
        XIAOQU:lianjia_spider.XiaoQuBaseSpider,
        LOUPAN:lianjia_spider.LouPanBaseSpider,
        ERSHOUFANG:lianjia_spider.ErShouSpider,
        ZUFANG:lianjia_spider.ZuFangBaseSpider
    },
    BEIKE_SPIDER: {
        XIAOQU:beike_spider.XiaoQuBaseSpider,
        LOUPAN:beike_spider.LouPanBaseSpider,
        ERSHOUFANG:beike_spider.ErShouSpider,
        ZUFANG:beike_spider.ZuFangBaseSpider
    },
}

if __name__ == "__main__":
    spider = work.get(SPIDER_NAME).get(CLASS_NAME)()
    spider.start()