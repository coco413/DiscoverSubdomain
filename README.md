### 0x00 简介
尽可能花更少的时间,使用All in one工具收集更多的信息-子域名
### 0x01 安装使用
___
- 1.下载
```
git git@github.com:coco413/DiscoverSubdomain.git
cd DiscoverSubdomain
pip install -r requirements.txt
```

- 2.配置
```
vim lib/common.py
config = {'assets_func': True,  #默认开启资产检测功能

          'email_func': True, #默认开启发送邮箱功能
          'seed_email_user': 'xxxx@qq.com',
          'seed_email_pass': 'xxxx',
          'seed_email_host': 'xxx.qq.com',
          'receive_email_user': 'xxx@xxx.con',

          'shodan_key': 'UNmOjxeFS2mPA3kmzm1sZwC0XjaTTksy', 
          }
```

- 3.运行
```
usage: DiscoverSubdomain -t 100 -f True -d target.com

AutoInfoDetect of subdomain

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -d DOMAIN, --domain DOMAIN
                        DomainName of scan target
  -t THREAD, --thread THREAD
                        Number of scan threads(default:100)
  -f FULL, --full FULL  Full dict files to brute(default:False)
```
- 4.
```
open steam/dota2
```

### 0x02 运行截图
___
- 自检阶段
![](http://p4.cdn.img9.top/ipfs/QmU5mDUWjdHdPEiCwhCYwmSJvCatengGvmuXz5FNXLWFRV?4.png)
- OSINT阶段
![](http://p1.cdn.img9.top/ipfs/QmUXmdiW5z67H4SciEEVVkb5vXAacaZEVPjVaLBN2Wx7Q2?1.png)
- 枚举阶段
![](http://p4.cdn.img9.top/ipfs/QmP5cGchx7ryzghhZowDXnCmvmNtE35UtCKd6ETefknoWC?4.png)
- 资产阶段
![](http://p0.cdn.img9.top/ipfs/QmattMNYXZXbvYmwKQKf1WpfC6sHUVDhaxhT7Mwb7NzdL9?0.png)
- 保存结果
![](http://p4.cdn.img9.top/ipfs/QmYfN873q6M2QpCUBQjj1otDh5RYoseqSoqE3wcMo6CsgK?4.png)
- 发送邮件
![](http://p0.cdn.img9.top/ipfs/QmXwKPG1uH42MHVcVGWNhZ4jE8h2L9wZcbaACLQ2Dcb2wH?0.png)
- 测试结果
测试阿里子域名，使用lijiejie的大字典，用时4331s跑完的存放在目录文件aliyun_com_1514578637.88.json下。

### 0x03 可能问题
___
- 1.输出爆如下提醒:
```
WARNING:tldextract:unable to cache TLDs in file /Library/Python/2.7/site-packages/tldextract/.tld_set: [Errno 13] Permission denied: '/Library/Python/2.7/site-packages/tldextract/.tld_set'
```
[No handlers could be found for logger "tldextract"](https://github.com/infosec-au/altdns/issues/15),创目录给权限。

- 2.运行环境问题
`python2.7，windows的未测试`
- 3.searchByDnsTrails获取有时候为空
访问频繁或者需要代理。(有时候不翻墙能访问有时候不能。)
- 4.结果中偶尔会存在其他域名
这个主要是api采集的时候乱入的，由于很少所以我直接忽略了，如果不想要的话直接在最后结果时域名格式以及域名后缀判断下就行。
- 5.搜索引擎搜索内容有的偏少
默认只收集50页的，可以自定义，建议挂在vps上跑，也方便使用谷歌等。
- 6.从域名发现到资产再到保存这个流程如果出了异常跑的数据会不会丢失
这个基本不会，目录下cache.txt主要是为了防止后面的流程如果异常导致丢失的情况以及边出结果边扫，方便同时操作。

### 0x04 感谢
轮子造到一定程度后，觉得应该到了优化成自己顺手的自动化工具的过程了，方便平时的使用以及节约时间。
最后非常感谢以上工具的的开源精神(subDomainsBrute@lijiejie、wydomain2@zhuzhuxia、Teemo@bit4等)以及提供的参考帮助，此外吃了3天外卖写出来的代码肯定也很渣,大牛们轻喷,如果发现了bug、建议或者有好的API的接口可以通过gitgay提交,反正我也不会改。
