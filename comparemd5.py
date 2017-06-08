'''
comparemd5.py simple md5 comparison tool for python.
Copyright (C) 2017 Otto Jolanki

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import hashlib
import sys
import os
from threading import Thread
import argparse


EPILOG = '''
          Usage: python comparemd5.py <dir1> <dir2>
         '''


class Md5CalculatingThread(Thread):
    '''
    Thread that compares MD5 sums
    '''
    def __init__(self, fname1, fname2):
        '''
        Initialize thread
        '''
        Thread.__init__(self)
        self.fname1 = fname1
        self.fname2 = fname2

    def run(self):
        '''
        Run the thread
        '''
        md5_1 = calculatemd5FromFile(self.fname1)
        md5_2 = calculatemd5FromFile(self.fname2)
        base = os.path.basename(self.fname1)
        equality = 'equal' if md5_1 == md5_2 else 'not equal'
        print '%s md5 sum is %s' % (self.fname1, md5_1)
        print '%s md5 sum is %s' % (self.fname2, md5_2)
        print 'md5 sums are %s for file %s' % (equality, base)


def get_args():
    parser = argparse.ArgumentParser(epilog=EPILOG)
    parser.add_argument('dirs',
                        help='Two directories containing files to compare',
                        nargs=2)
    args = parser.parse_args()
    return args


def calculatemd5FromFile(filepath, chunksize=4096):
    '''calculate md5sum of a file in filepath.
        do the calculation in chunks of 4096
        bytes as a memory efficiency consideration.'''
    hash_md5 = hashlib.md5()
    with open(filepath, 'rb') as f:
        # Iter is calling f.read(chunksize) until it returns
        # the sentinel b''(empty bytes)
        for chunk in iter(lambda: f.read(chunksize), b''):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def getAbsolutePath(dirname):
    return os.path.abspath(dirname)


def main():
    args = get_args()
    dir_1_abspath = getAbsolutePath(args.dirs[0])
    dir_2_abspath = getAbsolutePath(args.dirs[1])
    print 'dir1 path: %s ' % dir_1_abspath
    print 'dir2 path: %s ' % dir_2_abspath
    # get basenames of files in both directories to find common ones
    dir_1_basenames = {os.path.basename(fname) for
                       fname in os.listdir(dir_1_abspath)
                       if os.path.isfile(os.path.join(dir_1_abspath, fname))}
    dir_2_basenames = {os.path.basename(fname) for
                       fname in os.listdir(dir_2_abspath)
                       if os.path.isfile(os.path.join(dir_2_abspath, fname))}
    # Make common_basenames a list to ensure order
    common_basenames = list(dir_1_basenames.intersection(dir_2_basenames))
    if not common_basenames:
        print "No common filenames were found"
        sys.exit(1)
    # Expand the basenames back into absolute paths
    common_names_in_dir1 = [os.path.join(dir_1_abspath, name) for
                            name in common_basenames]
    common_names_in_dir2 = [os.path.join(dir_2_abspath, name) for
                            name in common_basenames]
    # Do the actual comparison
    for name1, name2 in zip(common_names_in_dir1, common_names_in_dir2):
        thread = Md5CalculatingThread(name1, name2)
        thread.start()


if __name__ == "__main__":
    main()
