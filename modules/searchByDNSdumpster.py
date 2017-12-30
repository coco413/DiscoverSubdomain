# -*- coding:utf-8 -*-
# !/usr/bin/env python

import re
import traceback
import requests

session = requests.session()
subdomains = []


def req(req_method, url, params=None):
    global session
    params = params or {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/40.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'https://dnsdumpster.com'}

    try:
        if req_method == 'GET':
            resp = session.get(url, headers=headers, timeout=20)
        else:
            resp = session.post(url, data=params, headers=headers, timeout=20)
        if hasattr(resp, "text"):
            return resp.text
        else:
            return resp.content
    except:
        return None


def get_csrftoken(resp):
    csrf_regex = re.compile(
        "<input type='hidden' name='csrfmiddlewaretoken' value='(.*?)' />", re.S)
    token = csrf_regex.findall(resp)[0]
    return token.strip()


def extract_domains(resp, domain):
    global subdomains
    tbl_regex = re.compile(
        '<a name="hostanchor"><\/a>Host Records.*?<table.*?>(.*?)</table>', re.S)
    link_regex = re.compile('<td class="col-md-4">(.*?)<br>', re.S)
    links = []
    try:
        results_tbl = tbl_regex.findall(resp)[0]
    except IndexError:
        results_tbl = ''
    links_list = link_regex.findall(results_tbl)
    links = list(set(links_list))
    for link in links:
        subdomain = link.strip()
        if subdomain.endswith(domain):
            subdomains.append(subdomain.strip())
    return links


def get_subdomains(domain):
    global subdomains
    try:
        base_url = 'https://dnsdumpster.com'
        resp = req('GET', base_url)
        if resp:
            token = get_csrftoken(resp)
            params = {'csrfmiddlewaretoken': token, 'targetip': domain}
            post_resp = req('POST', base_url, params)
            if post_resp:
                extract_domains(post_resp, domain)
    except TypeError:
        pass
    except:
        traceback.print_exc()
    finally:
        return list(set(subdomains))
