# -*- coding:utf-8 -*-
# !/usr/bin/env python

import traceback
import requests


def get_subdomains(domain):
    subdomains = []
    try:
        for page in xrange(10):
            url = "http://api.chaxun.la/toolsAPI/getDomain/?k={}&page={}&order=default&sort=desc&action=moreson".format(
                domain, page)
            r = requests.get(url)
            if domain in r.text:
                subdomains.extend([each['domain'] for each in r.json()["data"]])
            else:
                break
    except TypeError:
        pass
    except:
        traceback.print_exc()
    finally:
        return list(set(subdomains))
