# -*- coding:utf-8 -*-
# !/usr/bin/env python

from lxml import etree
import traceback
from lib.common import HttpReq, CheckDomainFormat


def get_subdomains(domain):
    subdomains = []
    try:
        url = 'http://ptrarchive.com/tools/search.htm?label={}'.format(domain)
        _, content = HttpReq(url)
        selector = etree.HTML(content)
        content = selector.xpath("//td[3]/text()")
        subdomains = [each.split(' ')[0] for each in content if CheckDomainFormat(each.split(' ')[0])]
    except TypeError:
        pass
    except:
        traceback.print_exc()
    finally:
        return list(set(subdomains))
