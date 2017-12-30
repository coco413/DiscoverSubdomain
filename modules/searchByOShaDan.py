# -*- coding:utf-8 -*-
# !/usr/bin/env python
import json
import traceback
from lib.common import HttpReq
import requests



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
        headers ={
                'User-Agent': "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
                'Accept': 'text/html,application/xhtml+xml, application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US;q=0.8,en;q=0.3',
                'Upgrade-Insecure-Requests': "1",
                'X-Requested-With':'XMLHttpRequest',
                'Referer':'https://www.oshadan.com/toolkit',
        }
        data = {"site": domain, "page": "1"}
        url = 'https://www.oshadan.com/anoipdomain?info={}'.format(json.dumps(data))
        _, content = HttpReq(url=url, headers=headers)
        formatdata = json.loads(content)['data']
        result = [i.keys()[0] for i in formatdata]
        subdomains = [i.split('|')[1] for i in result]
    except TypeError:
        pass
    except:
        traceback.print_exc()
    finally:
        return list(set(subdomains))
