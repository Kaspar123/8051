package main;

/**
 * Created by kaspar on 16.04.18.
 */
public class Request {

    private String type;
    private byte bmRequestType;
    private byte bRequest;
    private int wValue;
    private int wIndex;
    private byte endpoint;
    private int length;
    private byte[] data;

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public byte getBmRequestType() {
        return bmRequestType;
    }

    public void setBmRequestType(byte bmRequestType) {
        this.bmRequestType = bmRequestType;
    }

    public byte getbRequest() {
        return bRequest;
    }

    public void setbRequest(byte bRequest) {
        this.bRequest = bRequest;
    }

    public int getwValue() {
        return wValue;
    }

    public void setwValue(int wValue) {
        this.wValue = wValue;
    }

    public int getwIndex() {
        return wIndex;
    }

    public void setwIndex(int wIndex) {
        this.wIndex = wIndex;
    }

    public byte getEndpoint() {
        return endpoint;
    }

    public void setEndpoint(byte endpoint) {
        this.endpoint = endpoint;
    }

    public int getLength() {
        return length;
    }

    public void setLength(int length) {
        this.length = length;
    }

    public byte[] getData() {
        return data;
    }

    public void setData(byte[] data) {
        this.data = data;
    }
}
