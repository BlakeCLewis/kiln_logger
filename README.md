# kiln_logger

Heat is dangerous! Evaluate the risk and make your go/no-go decision!

I have had issues with the thermocouple chip getting too hot when air temp is above 90F. It is in a metal box, 2' away from the kiln. Last firning, when the kiln was within 30C of cone 6, it started under reading. I added a computer muffin fan to cool the electronics.

Parts and pieces: I think it adds up to ~ $70 and some shipping.

- Raspberry pi: any of these will work, $10 Zero W is cheapest, but a Pi 3b runs much faster and will give a desktop.

		https://www.adafruit.com/product/3775

		https://www.adafruit.com/product/3055

		https://www.adafruit.com/product/4027

		https://www.adafruit.com/product/3400

- 5V power supply: for the Pi

		https://www.adafruit.com/product/1995

- MicroSD card: you will also need a way to write the image, e.g. usb adapter

		https://www.amazon.com/SanDisk-microSDHC-Standard-Packaging-SDSQUNC-032G-GN6MA/dp/B010Q57T02/ref=sr_1_14?keywords=micro+sd&qid=1552005480&s=gateway&sr=8-14

- MAX31856 thermocouple module:

		https://www.adafruit.com/product/3263

- Female <=> Female jumper wires:

		https://www.adafruit.com/product/266

- 20x4 LCD w/ i2c backpack: it will print to console too.

		https://www.amazon.com/gp/product/B01GPUMP9C/ref=oh_aui_detailpage_o01_s00?ie=UTF8&psc=1
		or
		https://www.adafruit.com/product/198
		https://www.adafruit.com/product/292

- High temperature (2372 F) type K thermocouple:

		https://www.amazon.com/Temperature-Thermocouple-Ceramic-connector-CR-06/dp/B0713X6XG3/ref=sr_1_25?keywords=k-type&qid=1551683054&s=gateway&sr=8-25


- Download Raspbien Stretch or newer and write it to the MicroSD:

		https://www.raspberrypi.org/downloads/raspbian/
		boot it up
		expand the partition, it ask on first boot
		configure network
		update software 'apt-get update' and 'apt-get upgrade'

Wiring:

- fritz: 'https://raw.githubusercontent.com/BlakeCLewis/kiln_logger/master/logger_bb.png'


- Pin-Out:

		Device	PI
		----------	-------
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


- Install project files:

		git clone git@github.com:BlakeCLewis/kiln_logger.git

- Install sqlite3:

		sudo apt-get install sqlite3

- Configure raspberry pi interfaces:

		sudo raspi-config
		#enable interfaces ssh, ic2 & spi

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

- create the database:

		sqlite3 ~/kiln_logger.sqlite3
		CREATE TABLE firelog(RunID number, datime datetime, t number);
		.schema
		.exit

- run the logger

		cd ~/kiln_logger
		./logger.py -i <intger Run_ID> -s <interval in seconds>

- access data:

		ssh pi@<pi ipaddres>
		sqlite3 kilnlog.sqlite3
		select * from firelog where runid=420 order by datime asc;
