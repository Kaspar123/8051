import usb.core
import usb.util

import usb.control
import time
import sys

ID_VENDOR = 0x10c4
ID_PRODUCT = 0xea60

IN_EP = 0x82;
OUT_EP = 0x01;
SLEEP = 0.022;

def lenovo(dev):
    # dev, wLength, desc_type, desc_index, wIndex
    usb.control.get_descriptor(dev, 18, 0x01, 0x00);            # DEVICE
    usb.control.get_descriptor(dev, 9, 0x02, 0x00);             # CONFIGURATION
    usb.control.get_descriptor(dev, 59, 0x02, 0x00);            # CONFIGURATION again
    usb.control.get_descriptor(dev, 255, 0x03, 0x00);           # STRING
    usb.control.get_descriptor(dev, 255, 0x03, 0x01, 0x0409);   # STRING
    usb.control.get_descriptor(dev, 255, 0x03, 0x02, 0x0409);   # STRING
    usb.control.set_configuration(dev, 1)                       # SET CONFIGURATION
    dev.ctrl_transfer(0x21, 0x0a, 0x0000, 0, 0);                # SET IDLE
    
def arduino(dev):
     msg = '\x41\x98\x20';
     dev.write(0x02, msg);
     #time.sleep(SLEEP);
     #response = dev.read(0x02, 100);
     return None;
    
def android(dev):
    msg = '\x10\x00\x00\x00\x01\x00\x05\x10\xe7\x02\x00\x00\x01\x00\x01\x00';
    dev.write(0x01, msg)
    
def unitronics_identify(dev):
    msg = '\x2f\x30\x30\x49\x44\x45\x44\x0d';
    dev.write(OUT_EP, msg);
    time.sleep(SLEEP);
    #response = dev.read(IN_EP, 63, 100);
    return '';

def unitronics_run(dev):
    # TODO: validate identity response;
    response = unitronics_identify(dev);
    msg = '\x2f\x30\x30\x43\x43\x52\x33\x38\x0d';
    dev.write(OUT_EP, msg);
    time.sleep(SLEEP);
    response = dev.read(IN_EP, 9);
    return response

def unitronics_stop(dev):
    # TODO: validate identity response;
    response = unitronics_identify(dev);
    msg = '\x2f\x30\x30\x43\x43\x53\x33\x39\x0d';
    dev.write(OUT_EP, msg);
    time.sleep(SLEEP);
    response = dev.read(IN_EP, 9);
    return response;
    
def unitronics_reset(dev):
    #TODO: validate both identity responses;
    response = unitronics_identify(dev);
    response = unitronics_identify(dev);
    msg = '\x2f\x30\x30\x43\x43\x45\x32\x42\x0d';
    dev.write(OUT_EP, msg);
    time.sleep(SLEEP);
    response = dev.read(IN_EP, 9);
    return response;
    
def unitronics_status(dev):
    # TODO: validate identity response;
    response = unitronics_identify(dev);
    msg = '\x2f\x5f\x4f\x50\x4c\x43\x00\xfe\x01\x00\x00\x00\x07\x00\x00\x00\x00\x00\x6a\x00\x00\x00\xd4\xfc\x00\x00\x5c';
    dev.write(OUT_EP, msg);
    time.sleep(SLEEP);
    response = dev.read(IN_EP, 133);
    return response
    
    
def print_device_data(dev):
    print("bLength:\t\t{0}".format(dev.bLength));
    print("bNumConfigurations:\t{0}".format(dev.bNumConfigurations));
    print("bDeviceClass:\t\t{0}".format(dev.bDeviceClass));
    print("bDescriptorType:\t{0}".format(dev.bDescriptorType));
    print("bDeviceSubClass:\t{0}".format(dev.bDeviceSubClass));
    print("bDeviceProtocol:\t{0}".format(dev.bDeviceProtocol));
    print("bMaxPacketSize0:\t{0}".format(dev.bMaxPacketSize0));
    print("idVendor:\t\t{:02X}".format(dev.idVendor));
    print("idProduct:\t\t{:02X}".format(dev.idProduct));
    print("address:\t\t{0}".format(dev.address));
    print("bus:\t\t\t{0}".format(dev.bus));
    print("port_number:\t\t{0}".format(dev.port_number));
    print("speed:\t\t\t{0}".format(dev.speed));
    
def detach_kernel_driver(dev):
    res = [];
    for cfg in dev:
        for interface in cfg:
            if dev.is_kernel_driver_active(interface.bInterfaceNumber):
                try:
                    dev.detach_kernel_driver(interface.bInterfaceNumber);
                    res.append(interface.bInterfaceNumber);
                except usb.core.USBError as e:
                    sys.exit("Could not detach kernel driver from interface({0}): {1}".format(interface.bInterfaceNumber, str(e)));
    return res;
               
def main():
    dev = usb.core.find(idVendor=ID_VENDOR, idProduct=ID_PRODUCT);
    #dev.reset();
    if dev is None:
        raise ValueError('Device not found');
    # -------------
    print_device_data(dev);
    num = detach_kernel_driver(dev);
    
    unitronics_identify(dev);
    
    usb.util.dispose_resources(dev);
    
    [dev.attach_kernel_driver(x) for x in num if x != None];
    

if __name__ == '__main__':
    main();
