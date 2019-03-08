# kiln_logger
raspberry pi kiln logging


Electricity and heat are dangerous! Evaluate the risk and make your go/no-go decision!


Raspberry pi 3b
- 20x4 LCD w/ i2c backpack

		https://www.amazon.com/gp/product/B01GPUMP9C/ref=oh_aui_detailpage_o01_s00?ie=UTF8&psc=1

- MAX31856 thermocouple module

		https://www.adafruit.com/product/3263

High temperature (2372 F) type K thermocouple

		https://www.amazon.com/Temperature-Thermocouple-Ceramic-connector-CR-06/dp/B0713X6XG3/ref=sr_1_25?keywords=k-type&qid=1551683054&s=gateway&sr=8-25




Stuff to get it to work:

- Pin-Out:

		RPLCD VCC:	5V
		RPLCD GND:	GND
		RPLCD SDA:	GPIO 2
		RPLCD SCL:	GPIO 3

		MAX31856 3vo:	3.3v
		MAX31856 GND:	GND
		MAX31856 SDO:	GPIO 9
		MAX31856 SDI:	GPIO 10
		MAX31856 CS:	GPIO 8
		MAX31856 SCK:	GPIO 11


- Install PiLN files in /home and create log directory:

		git clone git@github.com:BlakeCLewis/kiln_logger.git
		mkdir ./log

- Install sqlite3:

		sudo apt-get install sqlite3

- Configure raspberry pi interfaces:

		sudo raspi-config
		#enable interfaces ic2 & spi

- Instal RPLCD for the 20x4 lcd:

		sudo pip3 install RPLCD

- Install MAX31856 Module:

		cd
		sudo apt-get update
		sudo apt-get install build-essential python3-pip python3-dev python3-smbus git
		git clone https://github.com/adafruit/Adafruit_Python_GPIO.git
		cd Adafruit_Python_GPIO
		sudo python3 setup.py install
		cd
		git clone git@github.com:johnrbnsn/Adafruit_Python_MAX31856.git
		cd Adafruit_Python_MAX31856
		sudo python3 setup.py install
- test modules:

		cd ~/kiln_logger
		python3 display.py
		python3 max31856_test.py

- run the logger

		cd ~/kiln_logger
		./logger.py -i <intger Run_ID> -s <interval in seconds>


- access data
		sqlite3 /home/pi/kilnlog.sqlite3
		select * from firelog where runid=32 order by datime asc;
