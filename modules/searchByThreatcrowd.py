# -*- coding:utf-8 -*-
# !/usr/bin/env python

import json
import traceback
from lib.common import HttpReq, CheckDomainFormat


def get_subdomains(domain):
    subdomains = []
    try:
        url = "https://www.threatcrowd.org/searchApi/v2/domain/report/?domain={}".format(domain)
        _, content = HttpReq(url)
        subdomains = [sub for sub in json.loads(content).get('subdomains') if CheckDomainFormat(sub)]
    except TypeError:
        pass
    except:
        traceback.print_exc()
    finally:
        return list(set(subdomains))
