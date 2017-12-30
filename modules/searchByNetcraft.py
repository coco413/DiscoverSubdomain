# -*- coding:utf-8 -*-
# !/usr/bin/env python

import re
import traceback
import requests
import hashlib
import urllib
import urlparse

subdomains = []
session = requests.Session()


def req(url, cookies=None):
    global session
    cookies = cookies or {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/40.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
    }
    try:
        resp = session.get(url, headers=headers, timeout=20, cookies=cookies)
    except requests.ReadTimeout:
        pass
    except:
        traceback.print_exc()
        resp = None
    return resp


def get_response(response):
    if response is None:
        return None
    if hasattr(response, "text"):
        return response.text
    else:
        return response.content


def get_next(resp, domain):
    link_regx = re.compile('<A href="(.*?)"><b>Next page</b></a>')
    link = link_regx.findall(resp)
    link = re.sub('host=.*?%s' % domain, 'host=%s' % domain, link[0])
    url = 'http://searchdns.netcraft.com' + link
    return url


def create_cookies(cookie):
    cookies = dict()
    cookies_list = cookie[0:cookie.find(';')].split("=")
    cookies[cookies_list[0]] = cookies_list[1]
    cookies['netcraft_js_verification_response'] = hashlib.sha1(
        urllib.unquote(cookies_list[1])).hexdigest()
    return cookies


def get_cookies(headers):
    if 'set-cookie' in headers:
        cookies = create_cookies(headers['set-cookie'])
    else:
        cookies = {}
    return cookies


def extract_domains(resp, domain):
    global subdomains
    link_regx = re.compile(
        '<a href="http://toolbar.netcraft.com/site_report\?url=(.*)">')
    try:
        links_list = link_regx.findall(resp)
        for link in links_list:
            subdomain = urlparse.urlparse(link).netloc
            if subdomain.endswith(domain):
                subdomains.append(subdomain.strip())
    except:
        traceback.print_exc()


def get_subdomains(domain):
    global subdomains
    try:
        url = 'http://searchdns.netcraft.com/?restriction=site+ends+with&host={}'.format(
            'example.com')
        hand = req(url)
        cookies = get_cookies(hand.headers)
        nurl = 'http://searchdns.netcraft.com/?restriction=site+ends+with&host={}'.format(
            domain)
        while True:
            resp = get_response(req(nurl, cookies))
            extract_domains(resp, domain)
            if 'Next page' not in resp:
                break
            get_next(resp, domain)
    except TypeError:
        pass
    except:
        traceback.print_exc()
    finally:
        return list(set(subdomains))
