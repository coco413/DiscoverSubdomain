# -*- coding:utf-8 -*-
# !/usr/bin/env python
import socket
import requests
import traceback
import re
import Queue
import threading
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from common import config
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import sys

reload(sys)
sys.setdefaultencoding("utf-8")

result = []
Q = Queue.Queue()


def GetBanner(domain, port=80):
    banner, server = '', ''
    try:
        url = 'http://' + domain if port == 80 else 'https: //' + domain
        r = requests.get(url, timeout=10, verify=False, allow_redirects=False)
        server = r.headers.get('Server')
        content = r.text
        m = re.search(r'<title>(.*)</title>', content, flags=re.I)
        if m:
            banner = m.group(1)
        r.close()
    except requests.exceptions.ConnectionError:
        pass
    except requests.exceptions.ChunkedEncodingError:
        pass
    except requests.TooManyRedirects:
        pass
    except requests.ReadTimeout:
        pass
    except:
        traceback.print_exc()
    finally:
        return banner, server


def GetPort(domain, portlists=config['portlists']):
    ports, ip = [], ''
    try:
        ip = socket.gethostbyname(domain)
        if ip:
            for port in portlists:
                s = socket.socket()
                s.settimeout(0.2)
                if s.connect_ex((domain, port)) == 0:
                    ports.append(port)
                s.close()
    except socket.gaierror:
        pass
    except:
        traceback.print_exc()
    finally:
        return ports, ip


def Scan():
    global result, Q
    banner, server = '', ''
    try:
        while not Q.empty():
            try:
                domain = Q.get(block=False)
            except:
                break
            ports, ip = GetPort(domain)
            if 80 in ports:
                banner, server = GetBanner(domain)
            data = {'domain': domain, 'ip': ip, 'ports': ports, 'banner': banner, 'server': server}
            print """
-------------
Doamin:{}
IP:{}
Port:{}
Server:{}
Banner:{}
      """.format(domain, ip, ports, server, banner)
            result.append(data)
            with open('cache_assets.txt', 'a+') as fw:
                fw.write(json.dumps(data) + '\n')

    except:
        traceback.print_exc()


def AssetsScan(domains):
    global Q
    try:
        # with open('3.txt') as fr:
        #     for domain in fr:
        for domain in domains:
            Q.put(domain.strip())
        threads = []
        for i in xrange(50):
            t = threading.Thread(target=Scan(), )
            t.start()
            threads.append(t)
        for i in threads:
            i.join()
    except:
        traceback.print_exc()
    finally:
        return result


# Main()
