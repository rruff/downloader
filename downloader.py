#!/usr/bin/env python3

import argparse
import logging
from client import Client
from conf.config import configs
from scraper import Scraper
import requests

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Scrapes a web page for links and downloads the targets.")
    parser.add_argument('-u-', '--url', metavar='URL', dest='url', type=str, help='The URL of the web page to scrape')
    parser.add_argument('-d', '--dir', metavar='DIR', dest='dl_dir', type=str, help='The download directory')
    parser.add_argument('-c', '--conf', metavar='CONF', dest='config_profile', type=str, help='The configuration profile to use')
    parser.add_argument('-D', '--debug',  metavar='DEBUG', dest='debug_on', type=bool, help='Turn on debugging')

    args = parser.parse_args()
    
    if args.debug_on:
        logging.basicConfig(level=logging.DEBUG)

    client = Client(args.dl_dir)
    page = requests.get(args.url, headers={'user-agent': USER_AGENT})
    scraper = Scraper(client, page, **configs[args.config_profile])
    scraper.scrape()