# -*- coding:utf-8 -*-
# !/usr/bin/env python

import sys
import traceback
import re
import json


reload(sys)
sys.setdefaultencoding("utf-8")


class HelpSubdomain(object):
    def __init__(self):
        self.LayerPath = "weibo.com子域名列表_Layer.txt"
        self.FuzzDomainPath = "fdomain.txt"
        self.file1 = ''
        self.file2 = ''
        self.result = 'result.txt'

    def LayerFormat(self):
        """
        @Layer提取数据格式化
        {
          'domain': 'apps.weibo.com',
          'ip': '180.149.134.249',
          'port': '80,443',
          'service': 'Apache',
          'title': '80:\xe6\xad\xa3\xe5\xb8\xb8\xe8\xae\xbf\xe9\x97\xae\r\n'
        }
        """
        LayerDomains = []
        try:
            with open(self.LayerPath) as fr:
                LayerDomains = [{'domain': _.split('\t')[0], 'ip':_.split('\t')[1], 'port':_.split('\t')[
                    2], 'service':_.split('\t')[3], 'banner':_.split('\t')[4]} for _ in fr if '域名' not in _]
        except:
            traceback.print_exc()
        finally:
            print LayerDomains
            return LayerDomains

    def IPtoCsegment(self, ip):
        """
        @ip > C段
        """
        c_ips = []
        import pyping
        try:

            ip_regex = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}.$')
            if ip_regex.match(ip):
                ip_head = '.'.join(ip.split('.')[:3])
                for i in xrange(1, 255):
                    ip = ip_head + '.' + str(_)
                    handler = pyping.ping(ip)
                    if handler.packet_lost == 0:
                        print 'Alive:', ip
                        c_ips.append(ip)

        except:
            traceback.print_exc()
        finally:
            print c_ips
            return c_ips

    def GetSingleElement(self):
        """
        @取单一元素,全ip、全域名
        """
        Element = []
        try:
            with open(self.result) as fr:
                for _ in fr:
                    ip = json.loads(_)['ip']
                    Element.append(ip)
        except:
            traceback.print_exc()
        finally:
            print Element
            return Element

    def RemoveListSpecialChar(self, lists):
        """
        @清除换行
        """
        try:
            return filter(lambda x: x, map(lambda x: x.strip(), lists))
        except:
            traceback.print_exc()

    def merge2file(self):
        """
        @域名合并去重
        """
        def removesame(files):
            source_lines = len(files)
            data = sorted(set(files), key=files.index)
            with open('removesame.txt', 'a+') as fw:
                for each in data:
                    fw.write(each + '\n')
            print 'merge and remove success,and remove {} lines'.format(source_lines - len(data))
        try:
            files = []
            with open(self.file1) as fr1, open(self.file2) as fr2:
                for _ in fr1:
                    files.append(_.strip())
                for _ in fr2:
                    files.append(_.strip())
            removesame(files)
        except:
            traceback.print_exc()

    def main(self):
        pass


if __name__ == "__main__":
    main = HelpSubdomain()
    main.main()
