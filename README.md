# canonical_interview_technical_assessment
This is a record of my solution of the technical assessment during Canonical interview of Linux Software Engineer - Ubuntu for Next-Gen Silicon (multiple roles and seniority levels)

## INSTRUCTIONS

Debian uses *deb packages to deploy and upgrade software. The packages are stored in repositories and each repository contains the so called "Contents index". The format of that file is well described here https://wiki.debian.org/RepositoryFormat#A.22Contents.22_indices


Your task is to develop a python command line tool that takes the architecture (amd64, arm64, mips etc.) as an argument and downloads the compressed Contents file associated with it from a Debian mirror. The program should parse the file and output the statistics of the top 10 packages that have the most files associated with them. An example output could be:

./package_statistics.py amd64

```bash
<package name 1>         <number of files>
<package name 2>         <number of files>
......

<package name 10>         <number of files>
```

# Debian Package Contents Statistics Command Line Tool

## Overview

This command-line tool downloads and analyzes the Debian package repository "Contents index" for a given architecture, and outputs the top 10 packages containing the most files.

## Approach

Main steps of the tool:

1. Download the Contents index file

2. Decompress the `.gz` file

3. Parse the file line by line

4. Count the number of files per package

5. Output the top 10 packages

## Considerations and Challenges

There are several aspects that need to be taken into account:

1. **Large file size**
   The Contents index file can be very large, so it should not be fully loaded into memory.  - A streaming approach should be used.

2. **Exception handling**
   Network issues such as connection failures and timeouts need to be handled. Parsing errors should also be considered and handled gracefully.  - Add error handling

3. **Performance of sorting**
   Sorting the entire dictionary of `[package: count]` may be inefficient.  - A more efficient approach should be used for selecting the top N results.

4. **Configurability**
   The value of N (top N packages) should be configurable via command-line arguments  - using `argparse`.

5. **Code quality and formatting**
   Code should follow standard formatting and linting practices  - using Flake8 and pylint.

## Usage

```bash
./package_statistics.py amd64
```

```bash
./package_statistics.py amd64 --top 20
```

## Example of output

```
 1.piglit                  54424
 2.acl2-books              20287
 3.esys-particle           18127
 4.libboost1.88-dev        16001
 5.libboost1.83-dev        15663
 6.racket                  12202
 7.libstarpu-dev           9652
 8.libtorch-dev            8673
 9.zoneminder              8162
10.paraview-dev            7039
```

## Summary

It took me around 3 to 4 hours, but it was not continuous as I was interrupted a few time.

