#!/usr/bin/env python3

import requests
import sys

class Downloader:
    def __init__(self, requests):
        self.requests = requests

    def get(self, url, filename):
        resp = self._get_file(url)
        self._save(filename, resp)
    
    def _get_file(self, url):
        response = self.requests.get(url)
        response.raise_for_status()
        return response

    def _save(self, fname, request_data):
        with open(fname, 'wb') as f:
            for chunk in request_data.iter_content(100000):
                f.write(chunk)

if __name__ == '__main__':
    url = sys.argv[1]
    filename = sys.argv[2]

    downloader = Downloader(requests)
    print(f"Downloading {url} to {filename}")
    downloader.get(url, filename)