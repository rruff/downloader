#!/usr/bin/env python3

import pathlib
import logging
from urllib.parse import urljoin, urlparse, urlsplit

import bs4
import requests

from client import Client
from conf.config import configs
import re


""" 
Scrapes a web page for data based on provided CSS selectors and HTML attributes.
"""
class Scraper:
    def __init__(self, client, resp, **kwargs):
        self.client = client
        self.resp = resp
        self.selector = kwargs.get('selector')
        self.attr = kwargs.get('attr')
        self.host = kwargs.get('host')
        self.path_prefix = kwargs.get('prefix')
        self.path_index = kwargs.get('path_index')
        self.transform = kwargs.get('file_name_transform', {})
        self.pattern = re.compile(self.transform['pattern']) if 'pattern' in self.transform else None
        self.replacement = self.transform['replacement'] if 'replacement' in self.transform else None
        self.__transform_func = self.__transform_path if self.pattern and self.replacement else self.__null_transform

    def scrape(self):
        hrefs = filter(self.is_absolute, self.find_in_page(self.resp, self.selector, self.attr))
        logging.debug(f'hrefs={hrefs.__sizeof__()}')
        count = 0
        for href in hrefs:
            dl_url = self.dl_url(href)
            logging.debug(f'dl_url={dl_url}')
            filename = urlsplit(href).path.split('/')[-1]
            print(f'Downloading {dl_url}')
            saved = self.client.save(dl_url, filename)
            if saved: count += 1
        print(f'Downloaded {count} files')
    
    def is_absolute(self, url):
        logging.debug(f'{url=}')
        return bool(urlparse(url).netloc)

    def find_in_page(self, res, selector, attr=None):
        html = bs4.BeautifulSoup(res.text, 'html.parser')
        logging.debug(f'{html}')
        elems = html.select(selector)
        logging.debug(f'elems={elems}')
        if attr:
            return [e.get(attr) for e in elems]
        else:
            return elems

    def __transform_path(self, urlpath):
        parts = urlpath.split('/')
        filename = parts.pop()
        parts.append(self.pattern.sub(self.replacement, filename))
        return '/'.join(parts)
    
    def __null_transform(self, urlpath):
        return urlpath
    
    def dl_url(self, url):
        """ Computes the download URL. """
        u = urlparse(url)
        if self.host:
            base = f'{u.scheme}://{self.host}'
        else:
            base = f'{u.scheme}://{u.netloc}'

        if self.path_prefix:
            urlpath = self.__transform_func(u.path[self.path_index+1:])
            p = pathlib.PurePath(self.path_prefix).joinpath(urlpath)
        else:
            urlpath = self.__transform_func(u.path[self.path_index:])
            p = pathlib.PurePath(urlpath)

        return urljoin(base, p.as_posix())
