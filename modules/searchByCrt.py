# -*- coding:utf-8 -*-
# !/usr/bin/env python

from lxml import etree
import traceback
from lib.common import HttpReq


def get_subdomains(domain):
    subdomains = []
    try:
        url = 'https://crt.sh/?q=%25.{}'.format(domain)
        _, content = HttpReq(url)
        if content:
            selector = etree.HTML(content)
            content = selector.xpath("//tr/td[4]/text()")
            for each in content:
                if '*.' in each:
                    each = each.replace('*.', '')
                subdomains.append(each)
    except TypeError:
        pass
    except:
        traceback.print_exc()
    finally:
        return list(set(subdomains))
