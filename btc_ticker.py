#!/usr/bin/python
# -*- coding:utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import traceback
import time
import logging
import sys
import os
import requests
from datetime import datetime
import pytz

if len(sys.argv) != 4:
	print("Son necesarios tres argumentos: tiempo de refresco (en segundos), zona horaria y moneda")
	sys.exit()

try:
	tz = pytz.timezone(sys.argv[2])
except pytz.UnknownTimeZoneError:
	print('la zona %s no existe' % sys.argv[2])
	sys.exit()

try:
	refresh_time = int(sys.argv[1])
except ValueError:
	print('El intervalo de refresco debe ser un numero entero (segundos)')
	sys.exit()

moneda = sys.argv[3]
if (moneda != 'USD') and (moneda != 'EUR'):
	print('La moneda debe ser USD o EUR')
	sys.exit()
	

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')

if os.path.exists(libdir):
	sys.path.append(libdir)

#Usaremos este driver ya que nuestra pantalla es la de 2'13 pulgadas
from waveshare_epd import epd2in13_V2

logging.basicConfig(level=logging.DEBUG)

try:
	logging.info("btc ticker")
	epd = epd2in13_V2.EPD()
	logging.info("init and Clear")
	epd.init(epd.FULL_UPDATE)
	epd.Clear(0xFF)

	# Fonts
	font14 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 14)
	# Esta es la fuente que usaremos para el precio del BTC
	font96 = ImageFont.truetype(os.path.join(picdir, 'DS-DIGIT.TTF'), 96)

	logging.info("Drawing on the image...")
	image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
	draw = ImageDraw.Draw(image)

	time.sleep(2)
	epd.init(epd.FULL_UPDATE)
	
	#get btc price from coindesk
	while (True):
		try:
			response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
			data = response.json()
			price = str(int(float(data["bpi"][moneda]["rate"].replace(",",""))))
		except requests.exceptions.RequestException:
			price = "Err"
			pass #volveremos a intentar tras el intervalo

		now = datetime.now()
		time_image = Image.new('1', (epd.height, epd.width), 255)
		time_draw = ImageDraw.Draw(time_image)
		#escribimos el precio
		time_draw.text((5, 20), price, font = font96, fill = 0)
		#escribimos la fecha y hora encima
		time_draw.text((5, 0), tz.localize(now).strftime("%d/%m/%Y %H:%M:%S"), font = font14, fill = 0)
		epd.display(epd.getbuffer(time_image))
		time.sleep(refresh_time)

	# ed.Clear(0xFF)
	logging.info("Clear...")
	epd.init(epd.FULL_UPDATE)
	epd.Clear(0xFF)
	
	logging.info("Goto Sleep...")
	epd.sleep()

except IOError as e:
	logging.info(e)
	
except KeyboardInterrupt:    
	logging.info("ctrl + c:")
	epd2in13_V2.epdconfig.module_exit()
	exit()
