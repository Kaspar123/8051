package main;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.usb4java.BufferUtils;
import org.usb4java.DeviceHandle;
import org.usb4java.LibUsb;
import org.usb4java.LibUsbException;

import java.io.File;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.IntBuffer;

public class BulkTransfer {

    private static final short VENDOR_ID = 0x0403;
    private static final short PRODUCT_ID = 0x6015;

    private static final int TIMEOUT = 5000;

    public static void write(DeviceHandle handle, Request request) {
        ByteBuffer buffer;
            // IN
        if ((request.getEndpoint() & 0x10) == 0x10) {
            buffer = BufferUtils.allocateByteBuffer(request.getLength()).order(ByteOrder.LITTLE_ENDIAN);
        } else {
            // OUT
            buffer = BufferUtils.allocateByteBuffer(request.getLength());
            buffer.put(request.getData());
        }
        IntBuffer transferred = BufferUtils.allocateIntBuffer();
        int result = LibUsb.bulkTransfer(handle, request.getEndpoint(), buffer, transferred, TIMEOUT);
//        if (result != LibUsb.SUCCESS) {
//            throw new LibUsbException("Unable to send data", result);
//        }
    }

    public static void controlTransfer(DeviceHandle handle, Request request) {
        ByteBuffer buffer;
        if (request.getData() != null) {
            buffer = BufferUtils.allocateByteBuffer(request.getData().length);
            buffer.put(request.getData());
        } else {
            buffer = BufferUtils.allocateByteBuffer(0);
        }
        int result = LibUsb.controlTransfer(
                handle,
                request.getBmRequestType(),
                request.getbRequest(),
                (short) request.getwValue(),
                (short) request.getwIndex(),
                buffer,
                TIMEOUT);
//        if (result != LibUsb.SUCCESS) {
//            throw new LibUsbException("Unable To make control Transfer", result);
//        }
    }

    public static void main(String[] args) throws IOException {
        int result = LibUsb.init(null);
        if (result != LibUsb.SUCCESS) throw new LibUsbException("Unable to initialize libusb", result);
        DeviceHandle handle = LibUsb.openDeviceWithVidPid(null, VENDOR_ID, PRODUCT_ID);
        if (handle == null) {
            System.out.println("Device not found.");
            return;
        }
        if (LibUsb.kernelDriverActive(handle, 0) != 0) {
            LibUsb.detachKernelDriver(handle, 0);
        }
        LibUsb.claimInterface(handle, 0);
        ObjectMapper mapper = new ObjectMapper();
        //Request[] requests = mapper.readValue(new File("/home/kaspar/Desktop/proov/src/main/java/data2.json"), Request[].class);
        Request[] requests = mapper.readValue(new File("/home/kaspar/Desktop/proov/src/main/java/data.json"), Request[].class);
        for (Request request : requests) {
            if (request.getType().equalsIgnoreCase("control")) controlTransfer(handle, request);
            else if (request.getType().equalsIgnoreCase("bulk")) write(handle, request);
        }
    }
}
