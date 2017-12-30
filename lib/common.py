# -*- coding:utf-8 -*-
# !/usr/bin/env python

import requests
import re
import tldextract
import logging
import time
import os
import dns.resolver
import traceback
import yagmail
import json
logging.basicConfig()
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

config = {'assets_func': True,
          'portlists':[80, 443, 22, 445, 8080, 3389, 3306],
          # 'Nmap_parameter': '-sV -p 80',

          'email_func': True,
          'seed_email_user': '646753606@qq.com',
          'seed_email_pass': 'jgzitqbrzjwqbcij',
          'seed_email_host': 'smtp.qq.com',
          'receive_email_user': 'coco413@sina.cn',

          'shodan_key': 'UNmOjxeFS2mPA3kmzm1sZwC0XjaTTksy',

          }

headers = {
    'User-Agent': "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
    'Accept': 'text/html,application/xhtml+xml, application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US;q=0.8,en;q=0.3',
    'Upgrade-Insecure-Requests': "1",
    'Connection': 'close'
}


def CheckDomainFormat(domain):
    try:
        hand = tldextract.extract(domain)
        root_domain = '.'.join(hand[1:])
        ip_regex = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}.$')
        domain_regex = re.compile(
            r'(?:[A-Z0-9_](?:[A-Z0-9-_]{0,247}[A-Z0-9])?\.)+(?:[A-Z]{2,6}|[A-Z0-9-]{2,}(?<!-))\Z',
            re.IGNORECASE)
        return root_domain if not ip_regex.match(root_domain) and domain_regex.match(root_domain) else False
    except:
        traceback.print_exc()


def Wildcard(domain):
    def parser(record):
        ips = []
        try:
            for _ in record.response.answer:
                for j in _:
                    ips.append(str(j))
        except:
            traceback.print_exc()
        finally:
            return ips
    try:
        ips = []
        test_domains = ['Dota1_{}.{}'.format(i, domain) for i in range(3)]
        for domain in test_domains:
            record = dns.resolver.query(domain, 'A')
            if record:
                ips.extend(parser(record))
        return True if len(set(ips)) > 1 else False
    except:
        return False


def Zonetransfer(domain):
    try:
        cmd_res = os.popen('nslookup -type=ns ' + domain).read()
        dns_servers = re.findall('nameserver = ([\w\.]+)', cmd_res)
        for server in dns_servers:
            if len(server) < 5:
                server += domain
            cmd_res = os.popen('dig @%s axfr %s' % (server, domain)).read()
            if cmd_res.find('Transfer failed.') < 0 and cmd_res.find('connection timed out') < 0 and cmd_res.find('XFR size') > 0:
                return True
            else:
                return False
    except:
        traceback.print_exc()


def CheckNet():
    teststatus = []
    try:
        # testurls = ['http://www.baidu.com','http://{}'.format(domain), 'http://www.google.com']
        testurls = ['http://www.baidu.com', 'http://www.google.com']
        for url in testurls:
            status, _ = HttpReq(url)
            teststatus.append(False) if status != 200 else teststatus.append(True)
    except:
        traceback.print_exc()
    finally:
        return teststatus


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
        except requests.exceptions.ChunkedEncodingError:
            pass
        except requests.exceptions.ContentDecodingError:
            pass
        except:
            traceback.print_exc()

    return status, content


def Email(file=None):
    """
    open email pop/stmp function and input right host、passwd.
    """
    try:
        yag = yagmail.SMTP(
            user=config['seed_email_user'],
            password=config['seed_email_pass'],
            host=config['seed_email_host']
        )
        body = 'God is a girl'
        yag.send(
            to=config['receive_email_user'],
            subject='Subdomains',
            contents=[body, file])
        print '[-] Send Email Success!!!'
    except:
        print '[-] Send Email Error!!!'


def SaveFile(content, domain, assets=False, email=False):
    try:
        timestamp = time.time()
        filename = domain.replace('.', '_') + '_' + str(timestamp) + '.json'
        data = json.dumps(content)
        with open(filename, 'w+') as fw:
            fw.write(data+'\n')
        print '[-] Save Local Success!!'
        if config['email_func']:
            Email(file=filename)
    except:
        traceback.print_exc()
