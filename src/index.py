# -*- coding: utf-8 -*-
import os
import json
import random
import requests

proxies = []


# 获取随机头
def getUserAgent():
    return random.choice([
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
        'User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)'
    ])


# 建立代理ip池
def setProxiesPool():
    # 获取代理IP的方法有很多，此处使用的是阿里云云市场提供的代理ip获取接口：
    # https://market.aliyun.com/products/57126001/cmapi00037885.html
    url = 'http://zip.market.alicloudapi.com/devtoolservice/ipagency'
    data = {
        "IpPoolId": 2,
        "foreigntype": 0,
        "protocol": 0
    }
    headers = {
        "Authorization": 'APPCODE ' + os.environ['APPCODE']
    }
    global proxies
    proxies = proxies + [{
        eve_data["address"].split('://')[0]: eve_data["address"]
    } for eve_data in json.loads(requests.get(url, params=data, headers=headers).text)['result']]


# 删除代理ip
def deleteProxy(proxy):
    global proxies
    proxies.remove(proxy)

# 获取代理ip
def getProxy():
    global proxies
    if not proxies: setProxiesPool()
    return random.choice(proxies)


def handler(event, context):
    global proxies

    # 初始化地址
    url = 'https://developer.aliyun.com/developer/api/index/202109/listIndexItem'
    # 初始化代理
    proxy = getProxy()
    # 初始化header
    headers = {
        "User-Agent": getUserAgent()
    }

    # 循环条件，此处案例1到10，用来进行页码的循环，但是在实际爬虫过程中可能有其他的方法：
    # 1. 根据返回的数据页面进行循环；
    # 2. 根据返回的数据个数，决定是否要继续循环操作；
    # 3. 更具已有的列表决定是否要循环
    # 当然还有其他的很多循环条件，此处可以根据实际需要自行修改
    for i in range(1, 10):
        # 构建请求的数据结构
        data = {
            'type': 'recommend',
            'pageNum': i,
            'pageSize': '50'
        }
        response_status = True  # 对请求状态标记
        for times in range(0, 3):  # 构建重试逻辑，由于重试的前提可能是proxy/headers发生了变化，所以此处使用循环来进行重试
            response = requests.get(url=url, params=data, proxies=proxy, headers=headers).content.decode("utf-8")
            # 此处虚拟了一个逻辑分支，用于为用户铺垫切换IP/切换UA/删除IP的条件
            # 例如 response 出现了某个指定的字符串，需要对现有的IP进行删除，并切换IP和UA
            if 'xxxxx' in response:
                proxy = getProxy()
                headers["User-Agent"] = getUserAgent()
                response_status = False
                # 触发重试逻辑，进行重试
                continue
            else:
                # 没有预期的问题，退出重试
                response = json.loads(response)
                response_status = True
                break

        if not response_status:
            print("Error Url: ", url)
            continue
        else:
            print("Url %s. Result: " % url)
            for eve_item in response["data"]["list"]:
                # 获得到每条数据，可以将数据传到下游，此处仅以打印为例
                print(eve_item)