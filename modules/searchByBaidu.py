# -*- coding:utf-8 -*-
# !/usr/bin/env python

import re
import traceback
from lib.common import HttpReq, CheckDomainFormat


def get_subdomains(domain, page=50):
    subdomains, sites = [], []
    try:
        for i in xrange(0, page * 10, 10):
            url = 'http://www.baidu.com/s?wd=site:{}&pn={}'.format(
                domain, i)
            _, content = HttpReq(url)
            sites.extend(
                re.findall(
                    'style="text-decoration:none;">(.*?)/',
                    content))
        subdomains = [_.strip() for _ in sites if CheckDomainFormat(_.strip())]
    except TypeError:
        pass
    except:
        traceback.print_exc()
    finally:
        return list(set(subdomains))
