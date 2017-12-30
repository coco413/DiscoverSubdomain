# -*- coding:utf-8 -*-
# !/usr/bin/env python
# 待修改
import re
import time
import traceback
import urllib2


def get_subdomains(domain):
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'HTTPS': '1',
        'Referer': 'https://www.google.com.tw/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36'
    }
    i = 0
    subdomains = []
    try:
        while True: # this use while, if  effect bad to change
            time.sleep(1)
            start = i * 10
            url = "https://www.google.com.tw/search?q=site:%s&start=%d&hl=en&filter=0" % (
                domain, start)
            i = i + 1
            req = urllib2.Request(url, headers=header)
            code = urllib2.urlopen(req).read()
            res = re.findall(
                'http://([\w\d\.-]{0,256}?\.?%s).*?".onmousedown' %
                domain, code, re.I)
            for name in res:
                if name not in subdomains:
                    subdomains.append(name)
            if code.find("Next") == -1:
                break
    except TypeError:
        pass
    except:
        traceback.print_exc()
    finally:
        return list(set(subdomains))
