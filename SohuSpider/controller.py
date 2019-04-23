import os
import time
import subprocess

while 1 == 1:
    print("启动爬虫爬取新的数据")
    run = os.system("scrapy crawl sohu")
    print("等待一分钟")
    time.sleep(60)
