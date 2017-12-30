# -*- coding:utf-8 -*-
# !/usr/bin/env python

import re
import traceback
from lib.common import HttpReq, CheckDomainFormat


def get_subdomains(domain):
    subdomains = []
    try:
        url = 'http://alexa.chinaz.com/?domain={}'.format(domain)
        _, content = HttpReq(url)
        regex = re.compile(r'(?<="\>\r\n<li>).*?(?=</li>)')
        result = regex.findall(content)
        subdomains = [sub for sub in result if CheckDomainFormat(sub)]
    except TypeError:
        pass
    except:
        traceback.print_exc()
    finally:
        return list(set(subdomains))
