import serial


class SerialCommunication:
    def __init__(self, port='/dev/ttyACM0', baudrate=9600):
        self.serial = serial.Serial(port, baudrate)
    
    def read_data(self):
        if self.serial.in_waiting > 0:
            return self.serial.readline().decode().strip()
    
    def send_data(self, data):
        self.serial.write(data.encode())

if __name__ == '__main__':
    serial_comm = SerialCommunication()
    while True:
        data = serial_comm.read_data()
        if data:
            print(data)
            serial_comm.send_data(data)
