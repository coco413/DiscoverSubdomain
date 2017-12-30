# -*- coding:utf-8 -*-
# !/usr/bin/env python

import re
import traceback
from lib.common import HttpReq,CheckDomainFormat


def get_subdomains(domain):
    subdomains = []
    try:
        url = "https://www.threatminer.org/getData.php?e=subdomains_container&q={}&t=0&rt=10&p=1".format(domain)
        _, content = HttpReq(url)
        regex = re.compile(r'(?<=<a  href\="domain.php\?q=).*?(?=">)')
        result = regex.findall(content)
        subdomains = [sub for sub in result if CheckDomainFormat(sub)]
    except TypeError:
        pass
    except:
        traceback.print_exc()
    finally:
        return list(set(subdomains))
