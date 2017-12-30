# -*- coding:utf-8 -*-
# !/usr/bin/env python
from lxml import etree
import traceback
from lib.common import HttpReq


def get_subdomains(domain, page=5):
    subdomains = []
    try:
        for i in xrange(1, page + 1):
            url = "https://dnstrails.com/#/list/domain/{}/type/hostname/page/{}".format(domain, i)
            _, content = HttpReq(url)
            selector = etree.HTML(content)
            content = selector.xpath("//li/div/a/text()")
            subdomains = [each for each in content]
    except:
        pass #maybe go wall
    finally:
        return list(set(subdomains))
