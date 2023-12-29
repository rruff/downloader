import logging
from requests.models import HTTPError
from requests.exceptions import ConnectionError
import progressbar
import os
import requests

"""
A simple HTTP download client.

@params:
    download_dir    - Optional  :   base directory for downloads--if not provided a full path is expected for filenames

"""
class Client:
    def __init__(self, download_dir=None):
        self.download_dir = download_dir

    def save(self, url, filename):
        try:
            resp = self._get(url)
            self._save(filename, resp)
            return True
        except HTTPError as e:
            logging.error(f'Error downloading {url}: {e}')
            return False
        except ConnectionError as e:
            logging.error('A connection error occurred for URL %s: %s', url, e)
            return False

    
    def _get(self, url):
        response = requests.get(url, stream=True)
        response.raise_for_status()
        return response

    def _save(self, fname, r):
        if self.download_dir:
            if not os.path.exists(self.download_dir):
                os.makedirs(self.download_dir)
            fname = os.path.join(self.download_dir, fname)
        
        pbar = self._init_pbar(r)
        with open(fname, 'wb') as f:
            progress = 0
            for chunk in r.iter_content(1024):
                progress += len(chunk)
                pbar.update(progress)
                f.write(chunk)
    
    def _init_pbar(self, response):
        total = int(response.headers.get('content-length', 0))
        return progressbar.ProgressBar(total)