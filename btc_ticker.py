#!/usr/bin/python
# -*- coding:utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import traceback
import time
import logging
import sys
import os
import requests
import pytz
import argparse

parser = argparse.ArgumentParser(description="Muestra en la pantalla de tinta electrónica la información solicitada por el usuario")
parser.add_argument("-t", "--time",
					help="tiempo de refresco en segundos",
					type=int,
					default=60)

parser.add_argument("-c", "--currency",
					help="Moneda para mostrar el precio de bitcoin (USD o EUR)", 
					type=str, 
					choices=["USD", "EUR"], 
					default="USD")

parser.add_argument("-d", "--display",
					type=str,
					help="Información a mostrar: PRICE, BLOCK o PRCBLK (alternar entre los dos)",
					choices=["PRICE", "BLOCK", "PRCBLK"],
					default="PRICE")

parser.add_argument("-tz", "--timezone",
					type=str,
					help="zona horaria: ejemplo Europe/Madrid, America/Bogota, ... ",
					default="Europe/Madrid")

args = parser.parse_args()
tz = pytz.timezone(args.timezone)

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
	font20 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 20)
	# Esta es la fuente que usaremos para el precio del BTC
	fontprice = ImageFont.truetype(os.path.join(picdir, 'DS-DIGIT.TTF'), 96)
	# Esta para el bloque (mas pequeña porque hacen falta seis dígitos)
	fontblk = ImageFont.truetype(os.path.join(picdir, 'DS-DIGIT.TTF'), 80)

	logging.info("Drawing on the image...")
	image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
	draw = ImageDraw.Draw(image)

	time.sleep(2)
	epd.init(epd.FULL_UPDATE)
	
	#get btc price from coindesk
	displayblock = False
	while (True):
		now = datetime.now()
		time_image = Image.new('1', (epd.height, epd.width), 255)
		time_draw = ImageDraw.Draw(time_image)
		
		#obtenemos precio
		if((args.display == "PRICE") or (args.display == "PRCBLK")):
			try:
				response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
				data = response.json()
				price = str(int(float(data["bpi"][args.currency]["rate"].replace(",",""))))
			except requests.exceptions.RequestException:
				price = "Err"
				pass #volveremos a intentar tras el intervalo
		
		#obtenemos bloque
		if((args.display == "BLOCK") or (args.display == "PRCBLK")):
			try:
				response = requests.get('https://blockchain.info/latestblock')
				data = response.json()
				block =  str(data['height'])
			except requests.exceptions.RequestException:
				block = "Err Blk"
				pass #volveremos a intentar tras el intervalo
		
		if(args.display == "PRICE"):
			time_draw.text((5, 20), price, font = fontprice, fill = 0)
			time_draw.text((95, 100), args.currency, font = font14, fill = 0)
   
		elif(args.display == "BLOCK"):
			time_draw.text((5, 20), block, font = fontblk, fill = 0)
			time_draw.text((95, 100), "BLOCK", font = font14, fill = 0)
   
		elif(args.display == "PRCBLK"):
			if displayblock:
				time_draw.text((5, 20), block, font = fontblk, fill = 0)
				time_draw.text((95, 100), "BLOCK", font = font14, fill = 0)
				displayblock = False
			else:
				time_draw.text((5, 20), price, font = fontprice, fill = 0)
				time_draw.text((95, 100), args.currency, font = font14, fill = 0)
				displayblock = True
    
		#escribimos la fecha y hora encima
		time_draw.text((5, 0), tz.localize(now).strftime("%d/%m/%Y %H:%M:%S"), font = font14, fill = 0)
		epd.display(epd.getbuffer(time_image))
		time.sleep(args.time)

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
