import jssc.*;

/**
 * Created by kaspar on 23.04.18.
 */
public class Main {

    public static void main(String[] args) throws InterruptedException {
        /**String[] ports = SerialPortList.getPortNames();
        for (String port : ports) {
            System.out.println(port);
        }**/
        final SerialPort serialPort = new SerialPort("/dev/ttyUSB0");
        try {
            serialPort.openPort();
            serialPort.setParams(SerialPort.BAUDRATE_9600,
                                 SerialPort.DATABITS_8,
                                 SerialPort.STOPBITS_1,
                                 SerialPort.PARITY_NONE);
            serialPort.setFlowControlMode(SerialPort.FLOWCONTROL_RTSCTS_IN |
                                            SerialPort.FLOWCONTROL_RTSCTS_OUT);
            byte[] data = {0x2f, 0x30, 0x30, 0x49, 0x44, 0x45, 0x44, 0x0d};
            //serialPort.purgePort(SerialPort.PURGE_RXABORT | SerialPort.PURGE_RXCLEAR);
            serialPort.writeBytes(data);
            byte[] response = serialPort.readBytes();

        } catch (SerialPortException e) {
            e.printStackTrace();
        }
    }
}
