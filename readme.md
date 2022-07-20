# developer-spider 帮助文档

<p align="center" class="flex justify-center">
    <a href="https://www.serverless-devs.com" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=developer-spider&type=packageType">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=developer-spider" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=developer-spider&type=packageVersion">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=developer-spider" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=developer-spider&type=packageDownload">
  </a>
</p>

<description>

> ***阿里云开发者社区爬虫***

</description>

<table>

## 前期准备
使用该项目，推荐您拥有以下的产品权限 / 策略：

| 服务/业务 | 服务名 |     
| --- |  --- |   
| 权限/策略 | 创建函数 |     


</table>

<codepre id="codepre">



</codepre>

<deploy>

## 部署 & 体验

<appcenter>

- :fire: 通过 [Serverless 应用中心](https://fcnext.console.aliyun.com/applications/create?template=developer-spider) ，
[![Deploy with Severless Devs](https://img.alicdn.com/imgextra/i1/O1CN01w5RFbX1v45s8TIXPz_!!6000000006118-55-tps-95-28.svg)](https://fcnext.console.aliyun.com/applications/create?template=developer-spider)  该应用。 

</appcenter>

- 通过 [Serverless Devs Cli](https://www.serverless-devs.com/serverless-devs/install) 进行部署：
    - [安装 Serverless Devs Cli 开发者工具](https://www.serverless-devs.com/serverless-devs/install) ，并进行[授权信息配置](https://www.serverless-devs.com/fc/config) ；
    - 初始化项目：`s init developer-spider -d developer-spider`   
    - 进入项目，并进行项目部署：`cd developer-spider && s deploy -y`

</deploy>

<appdetail id="flushContent">

# 应用详情

本应用是基于 Python 语言的爬虫案例，主要包括：
- 获取随机头
- 建立代理IP池
- 删除代理IP
- 获取代理IP     

## 获取随机头

通常情况下，反爬虫系统会校验请求头信息，在请求头信息中最常校验的就是`User-Agent`，所以在本方法中，会随即返回一个`User-Agent`。如果在使用过程中，已经列举的`User-Agent`无法满足需求，可以额外添加。

> tips：`User-Agent`不仅仅单纯的应对反爬虫的时候会有用，往往也会降低我们的数据采集难度，例如有一些网站手机端`User-Agent`请求时所触发的反爬虫策略等级会远小于电脑版，所以`User-Agent`在一定程度上也可以用来切换客户端类型。

## 代理相关

由于代理IP在一定程度上是需要付费进行使用的，所以本案例所采用的代理IP部分仅供学习和参考。

本案例的代理IP服务商来自阿里云云市场：https://market.aliyun.com/products/57126001/cmapi00037885.html

开发者可以根据自己的需求对这一部分的代理IP获取方法进行完善。

> tips：本文所采用的代理IP使用策略是，当前IP失效后，清理掉失效IP，再更换代理IP，当然这个策略并不一定适合全部的数据采集情况，例如某些网站的反爬虫策略是IP限频，那么此时如果想要突破频率，可以采用的是每次更换代理IP，或同一链路请求完成更换代理IP，代理IP不清理并且循环利用；

## 主方法的注意事项

###  循环条件

循环条件，此处案例1到10，用来进行页码的循环，但是在实际爬虫过程中可能有其他的方法：

1. 根据返回的数据页面进行循环；
2. 根据返回的数据个数，决定是否要继续循环操作；
3. 更具已有的列表决定是否要循环

当然还有其他的很多循环条件，此处可以根据实际需要自行修改

### 切换IP的判断条件

在代码中虚拟了一个逻辑分支，用于为用户铺垫切换IP/切换UA/删除IP的条件：例如 response 出现了某个指定的字符串，需要对现有的IP进行删除，并切换IP和UA

```
if 'xxxxx' in response:
    proxy = getProxy()
    headers["User-Agent"] = getUserAgent()
    response_status = False
    # 触发重试逻辑，进行重试
    continue
```

### 数据的下游处理

数据的下游处理方法在本文中并没有提及，通常情况下会将数据存放在MongoDB等数据库进行持久化，或将数据转到下游清洗逻辑进行数据清洗等相关的操作。

</appdetail>

<devgroup>

## 开发者社区

您如果有关于错误的反馈或者未来的期待，您可以在 [Serverless Devs repo Issues](https://github.com/serverless-devs/serverless-devs/issues) 中进行反馈和交流。如果您想要加入我们的讨论组或者了解 FC 组件的最新动态，您可以通过以下渠道进行：

<p align="center">

| <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407298906_20211028074819117230.png" width="130px" > | <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407044136_20211028074404326599.png" width="130px" > | <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407252200_20211028074732517533.png" width="130px" > |
|--- | --- | --- |
| <center>微信公众号：`serverless`</center> | <center>微信小助手：`xiaojiangwh`</center> | <center>钉钉交流群：`33947367`</center> | 

</p>

</devgroup>