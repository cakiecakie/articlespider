from scrapy.cmdline import execute #用于直接执行scrapy的脚本文件

import sys
import os
#获取当前项目目录
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
print(os.path.dirname(os.path.abspath(__file__)))

execute(["scrapy", "crawl", "jobbole"]) #执行命令 scrapy crawl jobbole


