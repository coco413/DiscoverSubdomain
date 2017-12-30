# -*- coding:utf-8 -*-
# !/usr/bin/env python

import traceback
import json
import requests
from lib.common import HttpReq


def get_page(page):
    j_data = {}
    try:
        url = "https://transparencyreport.google.com/transparencyreport/api/v3/httpsreport/ct/certsearch/page?p={page}"
        r = requests.get(url.format(page=page))
        data = r.text[6:]
        j_data = json.loads(data)
    except:
        traceback.print_exc()
    finally:
        return j_data


def HttpReq(url='', data='', headers={}):
    status, content = '', ''
    if data:
        try:
            r = requests.post(
                url,
                data=data,
                headers=headers,
                verify=False,
                timeout=20)

            status, content = r.status_code, r.text
            r.close()
        except requests.exceptions.ConnectionError:
            pass
        except:
            traceback.print_exc()
    else:
        try:
            r = requests.get(url, headers=headers, verify=False, timeout=20)
            status, content = r.status_code, r.text
            r.close()
        except requests.exceptions.ConnectionError:
            pass
        except:
            traceback.print_exc()
    return status, content


def get_subdomains(domain):
    subdomains = []
    try:
        url = "https://transparencyreport.google.com/transparencyreport/api/v3/httpsreport/ct/certsearch?include_expired=true&include_subdomains=true&domain={}".format(
            domain)
        r = requests.get(url)
        content = r.text[6:]
        data = json.loads(content)
        if data[0][1] == []:
            return subdomains
        tmp = map(lambda x: x[1], data[0][1])
        for target in tmp:
            if str(target).endswith(domain):
                subdomains.append(str(target).strip())
        pages = data[0][3]

        while pages[3] != pages[4]:
            j_data = get_page(pages[1])
            pages = j_data[0][3]
            tmp = map(lambda x: x[1], j_data[0][1])
            for target in tmp:
                if str(target).endswith(domain):
                    subdomains.append(str(target).strip())
    except TypeError:
        pass
    except:
        traceback.print_exc()
    finally:
        return list(set(subdomains))
