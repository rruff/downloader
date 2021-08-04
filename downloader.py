#!/usr/bin/env python3

import argparse
import client
import scraper
import pathlib
import sys


    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Scrapes a web page for links and downloads the targets.")
    parser.add_argument('url', metavar='URL', type=str, help='The URL of the web page to scrape')
    parser.add_argument('dir', metavar='DIR', type=str, help='The download directory')
    url = sys.argv[1]
    filename = pathlib.PurePath(sys.argv[2])

    client = client.Client(download_dir=filename.parent.as_posix())
    print(f"Downloading {url} to {filename}")
    client.save(url, filename.name)