#!/usr/bin/env python3

import client
import pathlib
import sys
    
if __name__ == '__main__':
    url = sys.argv[1]
    filename = pathlib.PurePath(sys.argv[2])

    client = client.Client(download_dir=filename.parent.as_posix())
    print(f"Downloading {url} to {filename}")
    client.get(url, filename.name)