# -*- coding:utf-8 -*-
# !/usr/bin/env python

import re
import traceback
from lib.common import HttpReq


def get_subdomains(domain):
    subdomains = []
    try:
        url = 'https://www.virustotal.com/en/domain/{}/information/'.format(
            domain)
        _, content = HttpReq(url)
        regex = re.compile(
            '<div class="enum.*?">.*?<a target="_blank" href=".*?">(.*?)</a>', re.S)
        result = regex.findall(content)
        subdomains = [sub.strip() for sub in result if sub.strip().endswith(domain)]
    except TypeError:
        pass
    except:
        traceback.print_exc()
    finally:
        return list(set(subdomains))
