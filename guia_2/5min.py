import smbus
import time
import datetime

class MPU6050:
    def __init__(self, bus_num=1, address=0x68):
        self.bus = smbus.SMBus(bus_num)
        self.address = address
        
        # Registros de configuración del MPU6050
        self.PWR_MGMT_1 = 0x6B
        self.ACCEL_CONFIG = 0x1C
        self.GYRO_CONFIG = 0x1B
        
        # Escala de la aceleración y el giroscopio
        self.ACCEL_SCALE = 16384.0
        self.GYRO_SCALE = 131.0
        
        # Configura el MPU6050 para medir la aceleración y la velocidad angular
        self.bus.write_byte_data(self.address, self.PWR_MGMT_1, 0)
        self.bus.write_byte_data(self.address, self.ACCEL_CONFIG, 0x00)
        self.bus.write_byte_data(self.address, self.GYRO_CONFIG, 0x00)
    
    def read_word_2c(self, address):
        high = self.bus.read_byte_data(self.address, address)
        low = self.bus.read_byte_data(self.address, address + 1)
        value = (high << 8) + low
        if (value >= 0x8000):
            return -((65535 - value) + 1)
        else:
            return value
    
    def read_acceleration(self):
        accel_x = self.read_word_2c(0x3B) / self.ACCEL_SCALE
        accel_y = self.read_word_2c(0x3D) / self.ACCEL_SCALE
        accel_z = self.read_word_2c(0x3F) / self.ACCEL_SCALE
        return (accel_x * 9.81, accel_y * 9.81, accel_z * 9.81)
    
    def read_gyro(self):
        gyro_x = self.read_word_2c(0x43) / self.GYRO_SCALE
        gyro_y = self.read_word_2c(0x45) / self.GYRO_SCALE
        gyro_z = self.read_word_2c(0x47) / self.GYRO_SCALE
        return (gyro_x, gyro_y, gyro_z)


    def tomar_datos(self, duracion=300):
        datos = []
        t0 = time.time()
        while time.time() - t0 < duracion:
            accel_data = self.read_acceleration()
            gyro_data = self.read_gyro()
            datos.append((accel_data, gyro_data))
            timestamp = time.time()
            hora = time.strftime('%H:%M:%S', time.localtime(timestamp)) 
            print(f'Timestamp: {hora}')
            print('Aceleracion (m/s^2): X={0:.2f}, Y={1:.2f}, Z={2:.2f}'.format(*accel_data))
            print('Giroscopio (grados/s): X={0:.2f}, Y={1:.2f}, Z={2:.2f}'.format(*gyro_data))
            time.sleep(30)
        self.guardar_promedio(datos)
    
    def guardar_promedio(self, datos):
        acel_x = [d[0][0] for d in datos]
        acel_y = [d[0][1] for d in datos]
        acel_z = [d[0][2] for d in datos]
        gyro_x = [d[1][0] for d in datos]
        gyro_y = [d[1][1] for d in datos]
        gyro_z = [d[1][2] for d in datos]
        
        promedios = [sum(acel_x)/len(acel_x), sum(acel_y)/len(acel_y), sum(acel_z)/len(acel_z),
                     sum(gyro_x)/len(gyro_x), sum(gyro_y)/len(gyro_y), sum(gyro_z)/len(gyro_z)]
        
        timestamp = time.time()
        hora = time.strftime('%H:%M:%S', time.localtime(timestamp))
        with open('mpu.txt', 'a') as archivo:
            archivo.write(f'{hora} {promedios}\n')



if __name__ == '__main__':
    mpu = MPU6050()
    mpu.tomar_datos()
