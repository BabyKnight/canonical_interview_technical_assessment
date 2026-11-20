#!/usr/bin/env python3
"""
This module provides statistical analysis for Content index file.
It download the parse the .gz file and output the top 10 package
that have the most files associated with them.
"""

import argparse
import gzip
import heapq
from collections import defaultdict
import requests

DEBIAN_MIRROR = "http://ftp.uk.debian.org/debian/dists/stable/main"
DOWNLOAD_DIR = ""  # default as the same as script, modified if needed


def build_url(arch):
    """
    Build a complete URL using the CLI argument and predefined mirror address
    Args:
        arch (str): target architecture
    Return:
        str: complete morror url
    """
    return f"{DEBIAN_MIRROR}/Contents-{arch}.gz"


def download_file(url, local_file):
    """
    Download the Context index from the given url and save in local
    Args:
        url (str): complete context index url
        local_file (str): local file name for downloaded file
    """

    with requests.get(url, stream=True, timeout=30) as r:
        r.raise_for_status()
        with open(local_file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)


def process_file(file_path):
    """
    Process the downloaded Content index file
    decompress the gz file and parse each line to get the package name
    save the package name and total count into a dict
    Args:
        file_path (str): contents index file (.gz)
    Return:
        dict: {package_name: package_count}
    """
    pkg_count = defaultdict(int)  # save package name and total count

    with gzip.open(file_path, 'rt') as f:
        for line in f:
            pkg_list = parse_line(line)
            for pkg in pkg_list:
                pkg_count[pkg] += 1

    return pkg_count


def parse_line(line):
    """
    Parse each line and return the package name list
    Args:
        line (str): each line from the decompressed .gz file
    Return:
        list: package name list
    """
    # remove '\n' at the end of line
    line = line.strip()

    # deal with the empty line
    if not line:
        return []

    # when the package name appears, record it, but ignore the file path
    try:
        _, packages_str = line.rsplit(maxsplit=1)
    except ValueError:
        return []

    # packages_str may contains more than 1 split by "," e.g. pkg1,pkg2,pkg3
    # each package includes path e.g. admin/tboot
    packages = packages_str.split(",")

    return [pkg.split("/")[-1] for pkg in packages]


def main():
    """
    Parse command line arguments and start the analysis task
    This function is the script entry point, initializing the configuration
        and control the core logic.
    """
    # step 1: parse the command line argument
    parser = argparse.ArgumentParser()
    parser.add_argument("architecture",
                        help="Target architecture (e.g. amd64/arm64)")
    # reserved the top n argument for easy modify
    parser.add_argument("--top",
                        type=int,
                        default=10,
                        metavar="n",
                        help="Top n packages (default n is 10)")
    args = parser.parse_args()

    # step 2: build the url
    url = build_url(args.architecture)
    local_filename = f"Contents-{args.architecture}.gz"
    file_path = f"{DOWNLOAD_DIR}{local_filename}"

    # step 3: download the Content index file
    download_file(url, file_path)

    # step 4: decompress the gz file and process by parsing each line
    pkg_count = process_file(file_path)

    # step 5: get the top n packages
    top_n = heapq.nlargest(args.top, pkg_count, key=pkg_count.get)

    # step 6: output the result of top n packages
    max_pkg_name = max(len(pkg) for pkg in top_n)
    max_idx_len = len(str(args.top))

    for i, pkg in enumerate(top_n, 1):
        print(f"{i:>{max_idx_len}}.{pkg:<{max_pkg_name}}    {pkg_count[pkg]}")


if __name__ == "__main__":
    main()
