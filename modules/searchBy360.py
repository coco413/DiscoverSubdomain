# -*- coding:utf-8 -*-
# !/usr/bin/env python

import re
import traceback
from lib.common import HttpReq


def get_subdomains(domain):
    subdomains = []
    try:
        url = 'http://webscan.360.cn/sub/index/?url={}'.format(domain)
        _, content = HttpReq(url)
        item = re.findall(r'\)">(.*?)</strong>', content)
        if len(item) > 0:
            subdomains = [item[i] for i in xrange(1, len(item))]
    except TypeError:
        pass
    except:
        traceback.print_exc()
    finally:
        return list(set(subdomains))
