'''
Input is two paths to directories that contain files.
This module compares the mdsums of files with common
names, and looks at the md5sums of files with same
names, and compares them pairwise.
'''

import hashlib
import sys
import os


def calculatemd5FromFile(filepath):
    '''calculate md5sum of a file in filepath.
        do the calculation in chunks of 4096
        bytes as a memory efficiency consideration.'''
    hash_md5 = hashlib.md5()
    with open(filepath, 'rb') as f:
        for token in iter(lambda: f.read(4096), b""):
            hash_md5.update(token)
    return hash_md5.hexdigest()


def getAbsolutePath(dirname):
    return os.path.abspath(dirname)


def main():
    dir_1_abspath = getAbsolutePath(sys.argv[1])
    dir_2_abspath = getAbsolutePath(sys.argv[2])
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
        md5_1 = calculatemd5FromFile(name1)
        md5_2 = calculatemd5FromFile(name2)
        equality = 'equal' if md5_1 == md5_2 else 'not equal'
        print '%s md5 sum is %s' % (name1, md5_1)
        print '%s md5 sum is %s' % (name2, md5_2)
        print 'md5 sums are %s' % equality


if __name__ == "__main__":
    main()
