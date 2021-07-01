import pathlib
import progressbar
import requests

"""
A simple HTTP download client.

@params:
    download_dir    - Optional  :   base directory for downloads--if not provided a full path is expected for filenames

"""
class Client:
    def __init__(self, download_dir=None):
        try:
            self.download_dir = pathlib.PurePath(download_dir)
        except TypeError:
            self.download_dir = download_dir

    def get(self, url, filename):
        resp = self._get_file(url)
        self._save(filename, resp)
    
    def _get_file(self, url):
        response = requests.get(url, stream=True)
        response.raise_for_status()
        return response

    def _save(self, fname, r):
        if self.download_dir:
            fname = self.download_dir.joinpath(fname)
        
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