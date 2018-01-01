# -*- coding:utf-8 -*-
# !/usr/bin/env python

import traceback
import json
from lib.common import HttpReq, CheckDomainFormat, config


def get_subdomains(domain):
    subdomains = []
    try:
        url = "https://api.shodan.io/shodan/host/search?key=%s&query=hostname:%s&facets={facets}" % (
            config['shodan_key'], domain)
        _, content = HttpReq(url)
        data = json.loads(content)
        if isinstance(data, list) and data[1] == "INVALID_API":
            return subdomains
        else:
            if 'matches' in data.keys():
                subdomains = [
                    i['hostnames'][0].strip() for i in data['matches'] if CheckDomainFormat(
                        i['hostnames'][0].strip())]
                subdomains = [_ for _ in subdomains if _.endswith(domain)]
    except TypeError:
        pass
    except:
        traceback.print_exc()
    finally:
        return list(set(subdomains))
