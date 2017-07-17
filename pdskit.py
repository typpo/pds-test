import os
import fnmatch

import numpy as np
from astropy.io import fits
from pds4_tools import pds4_read
from pds4_tools.reader.table_objects import TableStructure

def load_hierarchy(path):
    xml_paths = []
    for dirpath, dirname, files in os.walk(path):
        for filepath in fnmatch.filter(files, '*.xml'):
            xml_paths.append(os.path.join(dirpath, filepath))

    print 'Processing', len(xml_paths), 'XML files'
    num_records = 0
    for xml_path in xml_paths:
        struct_list = pds4_read(xml_path)

        print '*' * 80
        print xml_path
        print 'Processing', len(struct_list), 'structs'
        # See SBN dev wiki for pds4_read usage:
        # http://sbndev.astro.umd.edu/wiki/Python_PDS4_Tools#pds4_read
        for struct in struct_list:
            print '-' * 80
            if type(struct) != TableStructure:
                print 'Unknown struct type encountered:', type(struct)
                continue

            # xpath tester: https://codebeautify.org/Xpath-Tester#
            fields = [elt.text for elt in struct.label.findall('.//Field_Character/name')]
            formats = [elt.text for elt in struct.label.findall('.//Field_Character/field_format')]

            # See astropy docs for writing fits tables:
            # http://docs.astropy.org/en/stable/io/fits/#creating-a-new-table-file
            cols = []
            for field, fmt in zip(fields, formats):
                try:
                    cols.append(fits.Column(name=field, format='E', array=struct[field]))
                except ValueError:
                    pass

            if len(cols) < 1:
                continue

            print 'Writing fits file...'
            coldef = fits.ColDefs(cols)
            tbhdu = fits.BinTableHDU.from_columns(coldef)

            prihdr = fits.Header()
            prihdr['COMMENT'] = 'Converted by PDSKit from %s' % xml_path
            prihdu = fits.PrimaryHDU(header=prihdr)

            thdulist = fits.HDUList([prihdu, tbhdu])

            out_dirpath = './out/%s' % os.path.dirname(xml_path)
            if not os.path.exists(out_dirpath):
                os.makedirs(out_dirpath)

            out_filename = os.path.basename(xml_path).split('.')[0]
            out_path = '%s.fits' % os.path.join(out_dirpath, out_filename)
            if not os.path.exists(out_path):
                thdulist.writeto(out_path)

            num_records += len(struct.data)
    print 'Total number of records:', num_records

if __name__ == '__main__':
    load_hierarchy('./data/ldex_20161118/')
