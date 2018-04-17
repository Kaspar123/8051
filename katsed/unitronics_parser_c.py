# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 21:58:47 2018

@author: kaspar
"""

BULK_TRANSFER = '0x03';
CONTROL_TRANSFER = '0x02';
BULK_TIMEOUT = 1000; # milliseconds
BUFFER_NAME = 'out_buffer';
READ_BUFFER_NAME = 'in_buffer';
ACTUAL_BYTES_COUNT_VARIABLE = '&actual';
DEVICE_VARIABLE = 'dev_handle';



def concatenate(l):
    l = [i[2:] for i in l]
    return '0x' + ''.join(l);
    
def dataline(l, counter, size):
    data = ', '.join(l);
    line = 'unsigned char ' + BUFFER_NAME + '_' + str(counter) + '[' + str(size) + '] = {' + '{0}'.format(data) + '};';
    print(line, end='\n');

def readFile():
    f = open('prev.h');
    lines = f.readlines();
    res = [];
    data = [];
    for line in lines:
        if 'static const unsigned char' in line:
            res.append(data);
            data = [];
            continue;
        if ('x' in line):
            data.append(line[:46].strip());
    res.append(data);
    return res;
    
if __name__ == '__main__':
    res = readFile();
    counter = 0;
    for i in res:
        if (i):
            l = ', '.join(i).split(', ')
            transfer_type = l[22]
            endpoint = int(l[21], 0)
            if (transfer_type == CONTROL_TRANSFER):
                bmRequestType = l[28];
                bRequest = l[29];
                wValue = concatenate(l[30:32][::-1]);
                wIndex = concatenate(l[32:34][::-1]);
                wLength = l[34];
                line = 'libusb_control_transfer({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7});'.format(DEVICE_VARIABLE, bmRequestType, bRequest, wValue, wIndex, READ_BUFFER_NAME, wLength, BULK_TIMEOUT);
                print(line, end='\n');
            elif (transfer_type == BULK_TRANSFER):
                length = int(l[23], 0)
                data = l[len(l) - length:];
                NAME = READ_BUFFER_NAME;
                if (length > 0):
                    NAME = BUFFER_NAME + "_" + str(counter);
                    dataline(data, counter, length);
                    counter += 1;
                line = 'libusb_bulk_transfer({0}, {1}, {2}, {3}, {4}, {5});'.format(DEVICE_VARIABLE, endpoint, NAME, length, ACTUAL_BYTES_COUNT_VARIABLE, BULK_TIMEOUT);
                print(line, end='\n');
