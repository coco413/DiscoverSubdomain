# -*- coding:utf-8 -*-
# !/usr/bin/env python

import re
import traceback
from lib.common import HttpReq


def get_subdomains(domain):
    subdomains = []
    try:
        url = "http://{}/crossdomain.xml".format(domain)
        status, content = HttpReq(url)
        if status == 200:
            subdomains = re.findall('domain="([\w\.]+)"', content)
    except:
        traceback.print_exc()
    finally:
        return list(set(subdomains))
