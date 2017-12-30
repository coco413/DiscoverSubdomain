#!/usr/bin/env python
# -*- coding: utf-8 -*-

from termcolor import colored
from importlib import import_module
from lib.common import *
from lib.simple_assets import AssetsScan
from brute.subDomainsBrute import SubNameBrute
import sys
import argparse
import time


reload(sys)
sys.setdefaultencoding('utf-8')


class SubDomains(object):
    def __init__(self, domain, thread, mode=False):
        self.domain = domain
        self.thread = thread
        self.mode = mode
        self.assets = config['assets_func']
        self.result = []
        self.apipath = 'modules.'
        self.cachefile ='cache.txt'
        self.apis = [
            'searchBy360',
            'searchByBing',
            'searchByBaidu',
            'searchByChaxunla',
            'searchByChinaz',
            'searchByCrossDomainXml',
            'searchByCrt',
            'searchByDNSdumpster',
            'searchByDnsTrails',
            'searchByNetcraft',
            'searchByOShaDan',
            'searchByShodan',
            'searchByThreaminer',
            'searchByThreatcrowd',
            'serachByPtrarchive',
            'serachByVirustotal',
            'searchByGoogle',
            'searchCertificateByGoogle']

    def CheckSelf(self):
        test_Insidenet, test_Outsidenet, test_Zonetransfer, test_Wildcard = True, False, False, False
        try:
            print colored('*' * 10 + 'Wait for SelfCheck' + '*' * 10, 'yellow')
            self.domain = CheckDomainFormat(self.domain)
            if self.domain:
                test_Wildcard = Wildcard(self.domain)
                test_Zonetransfer = Zonetransfer(self.domain)
                test_Insidenet, test_Outsidenet = CheckNet()
                if not test_Outsidenet:
                    del self.apis[-2:]
                print colored("[-] Check-Result: Format:{}  InsideNet:{}\n[-] OutsideNet:{}  Zonetransfer:{}  Wildcard:{}".format(True, test_Insidenet, test_Outsidenet, test_Zonetransfer, test_Wildcard), "blue")
                return True if test_Insidenet else False
        except:
            return False

    def searchByApi(self, apiname=None):
        try:
            handler = import_module(self.apipath + apiname)
            if apiname and apiname in self.apis:
                domains = handler.get_subdomains(self.domain)
                if domains:
                    self.result.extend(domains)
                print colored("[-] {} found {} subdomains!!".format(apiname, len(domains)), 'blue')
            else:
                print colored("[-] Not Found API", 'red')
        except:
            traceback.print_exc()

    def main(self):
        try:
            if self.CheckSelf():
                print colored('*' * 10 + 'OSINT Discover Mode' + '*' * 10, 'yellow')
                for api in self.apis:
                    self.searchByApi(api)

                print colored('*' * 10 + 'Enumerate Discover Mode' + '*' * 10, 'yellow')
                domains = SubNameBrute(target=self.domain, threads=self.thread, mode=self.mode).run()
                print colored("\n[-] searchByEnumerate found {} subdomains!!".format(len(domains)), 'blue')
                self.result.extend(domains)

                with open(self.cachefile, 'w+') as fw:
                    for _ in list(set(self.result)):fw.write(_+'\n') # cache subdomains prevent asset error

                if self.assets:
                    print colored('*' * 10 + 'Assets Discover Mode' + '*' * 10, 'yellow')
                    result = AssetsScan(list(set(self.result)))
                    SaveFile(content=result, domain=self.domain)
                else:
                    SaveFile(content=list(set(self.result)), domain=self.domain)
            else:
                print colored('[-] Error: Please check domain or network is not normal', 'red')
        except:
            traceback.print_exc()


if __name__ == "__main__":
    print """   
                   _         _                       _       
         ___ _   _| |__   __| | ___  _ __ ___   __ _(_)_ __  
        / __| | | | '_ \ / _` |/ _ \| '_ ` _ \ / _` | | '_ \ 
        \__ \ |_| | |_) | (_| | (_) | | | | | | (_| | | | | |
        |___/\__,_|_.__/ \__,_|\___/|_| |_| |_|\__,_|_|_| |_|
     　 　                     Coded By Coco413 (v1.0 RELEASE)
        """
    parser = argparse.ArgumentParser(description='AutoInfoDetect of subdomain', version='v1.0 RELEASE', prog='DiscoverSubdomain', usage='%(prog)s -t 100 -f True -d target.com')
    parser.add_argument('-d', "--domain", help="DomainName of scan target")
    parser.add_argument('-t', '--thread', default=100, help='Number of scan threads(default:100)')
    parser.add_argument('-f', '--full', default=False, help="Full dict files to brute(default:False)")

    args = parser.parse_args()
    try:
        start_time = time.time()
        if args.domain:
            Discover = SubDomains(domain=args.domain, thread=args.thread, mode=args.full)
            Discover.main()
            print '[-] All Done in %.1f s' % (time.time() - start_time)
        else:
            print colored('[-] Error: Please input -h to help', 'red')
    except KeyboardInterrupt:
        logging.info("Ctrl C - Stopping Client")
        sys.exit(1)
