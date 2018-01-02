### 0x00 简介
尽可能花更少的时间,使用All in one工具收集更多的信息-子域名

### 0x01 起因

之所以选择在已经有很多工具情况下再造轮子，是因为平时收集子域名这块浪费不少时间、几款工具收集后格式上的不统一还要脚本处理去重等，
其次工具多选择也麻烦，并且有的工具在调用API不能输出显示或者API地址失效等原因给我一种收集不全的感觉。因此想实现只要运行一个工具就能尽可能多的子域名，并且能方便自由定制的顺手工具，于是浏览对比了如下几款工具，根据他们的优缺点总结出一份个人合适的子域名工具需求:

 

1.Subdomains

2.wydomain

3.Teemo

4.knock 

5.subdomain3

6.Sublist3r

7.dnsmaper

8.domain_seeke

9.SubDomainSniper

10.dnsrecon 

11.DomainSeeker

12.dnscan 

13.dnsbrute 

14.GSDF

15.subbrute 

16.orangescan 

17.aquatone 

18.fierce-domain-scanner 

- 需求一: 对泛解析自动识别过滤
解决:通过SelfCheck检测提醒用户 + 调用lijiejie subdomain爆破脚本(自带泛解析过滤)

- 需求二:对域名格式能自动调整(有些工具只允许输入根域名带上协议等就报错不是很人性化)
解决:通过正则验证域名格式以及自动转换域名成根域名,带不带协议都无所谓。

- 需求三:收集方式尽可能的全，并且如果哪些接口没查询到能直观告诉我，方便验证找到问题。
解决:使用18个接口,包含API、搜索引擎、证书等方式进行在线查询整合子域名信息(具体的可以再module目录查看);在使用过程中直接输出收集条数，如果对于收集为0的可以方便的去验证问题。(对于一些需要key或者打码的接口这部分没加以及一些觉得重复率比较高的接口比如雅虎搜索等也没加)

- 需求四:避免不必要的访问性错误，能自适应网络(有的工具调用谷歌,但不翻墙运行只会耗时间或者异常)
解决:通过SelfCheck检测网络情况自动选择API接口。

- 需求五:接口的扩展性要方便，方便添加新接口以及方便调整匹配策略。
解决:想加入新的或者删除API接口，只需要两步骤，module目录添加脚本，self.apis添加名称。

- 需求六:域传送泄露、domain.xml泄露
解决:域传送放在selfcheck中进行自检、domain.xml泄露当做一个接口放在module中。

- 需求七:一种一键getshell的感觉(工具多，运行参数多，选择麻烦，不多用几个总有错觉收集不全)
解决:只选取了线程、字典等作为运行参数,其余无关紧要或者修改频率较低的都使用配置进行一劳永逸。参考了同类工具，统一了以上工具中调用的api接口以及对爆破字典进行了去重过滤(放在dict/backup目录中)，对于爆破脚本调用的是liejiejie的subdomain。所以在有比较全的API，如果遇到扫的不是很全的话，正常情况下只需要更换backup目录中更大的字典。

- 需求八:高效字典和全部字典优化
解决:收集了如上工具的字典以及github有两个子域名字典库的字典，把他们合并去重排序，根据频率优先级进行存放。

- 需求九:端口、服务等基本信息。
解决:刚开始用的libnmap模块进行探测这些信息，但是效果不佳，既过多增大时间也没有很实质性的探测信息
因此还是直接用socket接口去探测，这部分端口的话默认只检测[80, 443, 22, 445, 8080, 3389, 3306](可在common.py config中自定义修改)，以及banner只检测80端口的，之所以没有根据http识别端口后再进行检测主要觉得这部分信息探测更多的是域名，其他的一些附属资产微探测只是为了更方便的直观看下，接下来收集到端口或者ip等时再深度收集。包括参考以上工具时候发现有的也会对CDN或者状态码等进行收集，没加进去也是不想增加过多的时间在这部分。

- 需求十:输出格式化统一(每次实用其他工具输出内容都还要小脚本进行整合去重等操作。) 
解决:以Json和TxT进行统一格式化输出，为接下来调用这些结果格式化处理更加方便点。对于用其他工具，如Layer结果输出提出去重等小工具放在了tools目录下，方便跟其他工具的结果进行合并。

- 需求十一:邮件提醒 
解决:平时跑子域名挂在vps上跑一晚后有时候都会忘了，所以加了个邮箱提醒。(邮箱要设置开通smtp/pop3功能)

- 需求十二:日志记录，方便debug 
解决:为了方便debug以及运行记录的，这部分没有加logging等记录代码主要平时要么本地直接输出屏幕跑要么都是vps nohup跑，所以直接看屏幕或者nohup日志即可。

### 0x03 安装使用
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

### 0x04 运行截图
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
测试百度的子域名结果存放在根目录,使用Layer进行结果比对(运行的字典等不一致以及未对结果全部进行验证，所以只能简单参考)
DiscoverSubdomain使用的lijiejie的大字典发现5148个子域名;Layer发现百度2590个子域名;


### 0x05 可能问题
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

### 0x06 感谢
轮子造到一定程度后，觉得应该到了优化成自己顺手的自动化工具的过程了，方便平时的使用以及节约时间。
最后非常感谢以上工具的的开源精神(subDomainsBrute@lijiejie、wydomain2@zhuzhuxia、Teemo@bit4等)以及提供的参考帮助，此外吃了3天外卖写出来的代码肯定也很渣,大牛们轻喷,如果发现了bug、建议或者有好的API的接口可以通过gitgay提交,反正我也不会改。
