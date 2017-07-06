import os
import fnmatch

from pds4_tools import pds4_read

def load_hierarchy(path):
    for dirpath, dirname, files in os.walk(path):
        for filepath in fnmatch.filter(files, '*.xml'):
            fullpath = os.path.join(dirpath, filepath)
            struct_list = pds4_read(fullpath)

            print '*' * 80
            print fullpath
            for struct in struct_list:
                print '-' * 80
                print struct
                print struct.info()

if __name__ == '__main__':
    load_hierarchy('./data/ldex_20161118/')
