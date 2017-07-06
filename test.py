import os
import fnmatch

from pds4_tools import pds4_read

#struct_list = pds4_read('./data/ldex_20161118/data_calibrated/collection_ldex_data_calibrated.xml')
#struct_list = pds4_read('./data/ldex_20161118/bundle_ladee_ldex.xml')

path = './data/ldex_20161118/'
for dirpath, dirname, files in os.walk(path):
    for filepath in fnmatch.filter(files, '*.xml'):
        fullpath = os.path.join(dirpath, filepath)
        struct_list = pds4_read(fullpath)

        for struct in struct_list:
            print '*' * 80
            print struct
            print struct.info()
