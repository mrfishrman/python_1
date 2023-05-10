import serial

puerto_serie = serial.Serial('/dev/ttyACM1', 9600) #configurar el puerto serial

while True:
	datos = puerto_serie.readline().rstrip()
	print(datos) #imprimir datos recividos

