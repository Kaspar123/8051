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

MAPPING = {
'0x1E': 'CP210X_SET_BAUDRATE', 
'0x04': 'CP210X_GET_LINE_CTL', 
'0x12': 'CP210X_PURGE', 
'0x19': 'CP210X_SET_CHARS', 
'0x0A': 'CP210X_SET_XOFF', 
'0x05': 'CP210X_SET_BREAK', 
'0x03': 'CP210X_SET_LINE_CTL', 
'0x06': 'CP210X_IMM_CHAR', 
'0x0F': 'CP210X_GET_PROPS', 
'0x15': 'CP210X_EMBED_EVENTS', 
'0x13': 'CP210X_SET_FLOW', 
'0x00': 'CP210X_IFC_ENABLE', 
'0x01': 'CP210X_SET_BAUDDIV', 
'0x11': 'CP210X_RESET', 
'0x16': 'CP210X_GET_EVENTSTATE', 
'0x0C': 'CP210X_GET_EVENTMASK', 
'0x1D': 'CP210X_GET_BAUDRATE', 
'0xc0': 'REQTYPE_DEVICE_TO_HOST', 
'0x40': 'REQTYPE_HOST_TO_DEVICE', 
'0x07': 'CP210X_SET_MHS', 
'0x08': 'CP210X_GET_MDMSTS', 
'0x0B': 'CP210X_SET_EVENTMASK', 
'0x09': 'CP210X_SET_XON', 
'0x0E': 'CP210X_GET_CHARS', 
'0x14': 'CP210X_GET_FLOW', 
'0x02': 'CP210X_GET_BAUDDIV', 
'0xc1': 'REQTYPE_INTERFACE_TO_HOST', 
'0x10': 'CP210X_GET_COMM_STATUS', 
'0x0D': 'CP210X_SET_CHAR', 
'0x41': 'REQTYPE_HOST_TO_INTERFACE', 
'0xFF': 'CP210X_VENDOR_SPECIFIC'
}

def concatenate(l):
    l = [i[2:] for i in l]
    return '0x' + ''.join(l);
    
def dataline(l, counter, size):
    data = ', '.join(l);
    line = 'unsigned char ' + BUFFER_NAME + '_' + str(counter) + '[' + str(size) + '] = {' + '{0}'.format(data) + '};';
    print(line, end='\n');

def readFile():
    f = open('CONNECT.h');
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
                bRequest = str(l[29]).upper().replace('X', 'x');
                wValue = concatenate(l[30:32][::-1]);
                wIndex = concatenate(l[32:34][::-1]);
                wLength = l[34];
                line = 'libusb_control_transfer({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7});'.format(DEVICE_VARIABLE, bmRequestType, MAPPING[bRequest], wValue, wIndex, READ_BUFFER_NAME, wLength, BULK_TIMEOUT);
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
