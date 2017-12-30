# -*- coding:utf-8 -*-
# !/usr/bin/env python
import re
import traceback
import urlparse
from lib.common import HttpReq


def get_subdomains(domain, page=50):
    subdomains = []
    try:
        for i in xrange(0, page * 50, 50):
            url = 'http://cn.bing.com/search?count=50&q=host:{}&first={}'.format(
                domain, str(i))
            _, content = HttpReq(url)
            match = re.findall('<cite>(.*?)<\/strong>', content)
            for each in match:
                if 'target="_blank"' not in each.replace('<strong>', ''):
                    url = each.replace('<strong>', '')
                    subdomains.append(urlparse.urlparse(url).netloc)
    except TypeError:
        pass
    except:
        traceback.print_exc()
    finally:
        return list(set(subdomains))
