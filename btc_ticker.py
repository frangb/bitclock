#!/usr/bin/python
# -*- coding:utf-8 -*-

from PIL import Image, ImageDraw, ImageFont
import datetime
import logging
import sys
import os
import requests
import pytz
import argparse
import random
import pause
import time

# check if current time is between certain range


def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.datetime.now().time()
    print(check_time)
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else:  # crosses midnight
        return check_time >= begin_time or check_time <= end_time


def get_price():
    try:
        response = requests.get(
            'http://api.coindesk.com/v1/bpi/currentprice.json')
        data = response.json()
        if args.sats:
            price = str(
                int(100000000 / float(data["bpi"][args.currency]["rate"].replace(",", ""))))
        else:
            price = str(
                int(float(data["bpi"][args.currency]["rate"].replace(",", ""))))
    except requests.exceptions.RequestException:
        price = "Err Prc"
        pass  # volveremos a intentar tras el intervalo
    return price


def get_block():
    try:
        response = requests.get('https://blockchain.info/latestblock')
        data = response.json()
        block = str(data['height'])
    except requests.exceptions.RequestException:
        block = "Err Blk"
        pass  # volveremos a intentar tras el intervalo
    return block


def get_fees():
    try:
        response = requests.get(
            'https://mempool.space/api/v1/fees/recommended')
        data = response.json()
        fee = "Fee: " + str(data['fastestFee']) + " / " + str(
            data['halfHourFee']) + " / " + str(data['hourFee']) + " sats/vByte"
    except requests.exceptions.RequestException:
        fee = "Err Fee"
        pass  # volvemos a intentar tras el intervalo
    return fee


parser = argparse.ArgumentParser(
    description="Muestra en la pantalla de tinta electrónica la información solicitada por el usuario")
parser.add_argument("-t", "--time",
                    help="Tiempo de refresco en segundos",
                    type=int,
                    default=60)

parser.add_argument("-c", "--currency",
                    help="Moneda para mostrar el precio de bitcoin (USD o EUR)",
                    type=str,
                    choices=["USD", "EUR"],
                    default="USD")

parser.add_argument("-d", "--display",
                    type=str,
                    help="Información a mostrar: PRICE, BLOCK, PRCBLK (alternar entre los dos) o QUOTES (mostrar pantallas con citas sobre bitcoin)",
                    choices=["PRICE", "BLOCK", "PRCBLK", "QUOTES"],
                    default="PRICE")

parser.add_argument("-tz", "--timezone",
                    type=str,
                    help="Zona horaria: ejemplo Europe/Madrid, America/Bogota, ... para ver las zonas disponibles, consultar en http://https://en.wikipedia.org/wiki/List_of_tz_database_time_zones",
                    default="Europe/Madrid")

parser.add_argument("-n", "--nightmode",
                    type=str,
                    help="Modo nocturno. El reloj dejará de actualizarse entre 00:00 y 7:00 para ahorrar refrescos de la pantalla de tinta electrónica",
                    choices=['yes', 'no'],
                    default='no')

parser.add_argument("-s", "--sats",
                    action='store_true',
                    help="Muestra el precio en sats en lugar de la moneda elegida",)

args = parser.parse_args()
tz = pytz.timezone(args.timezone)

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
screensdir = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), 'screens')

if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in13_V2
# Usaremos este driver ya que nuestra pantalla es la de 2'13 pulgadas
logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("btc ticker")
    epd = epd2in13_V2.EPD()
    logging.info("init and Clear")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)

    # Fonts
    font14 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 14)
    font16 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 16)
    font20 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 20)
    # Esta es la fuente que usaremos para el precio del BTC inferior a 100K
    fontprice = ImageFont.truetype(os.path.join(picdir, 'DS-DIGIT.TTF'), 60)
    # Esta es la fuente que usaremos para el precio del BTC superior a 100K
    fontprice100 = ImageFont.truetype(os.path.join(picdir, 'DS-DIGIT.TTF'), 50)
    # Esta para el bloque (mas pequeña porque hacen falta seis dígitos)
    fontblk = ImageFont.truetype(os.path.join(picdir, 'DS-DIGIT.TTF'), 50)

    epd.init(epd.FULL_UPDATE)

    displayblock = False
    while (True):
        now = datetime.datetime.now()

        if((args.nightmode == "yes") and is_time_between(datetime.time(0, 0), datetime.time(7, 0))):

            time_image = Image.new('1', (epd.height, epd.width), 255)
            time_draw = ImageDraw.Draw(time_image)
            time_draw.text((10, 45), "Night mode", font=font20, fill=0)
            epd.display(epd.getbuffer(time_image))
            pause.until(datetime.datetime(
                now.year, now.month, now.day, 7, 0, 0))
        else:
            time_image = Image.new('1', (epd.height, epd.width), 255)
            time_draw = ImageDraw.Draw(time_image)

            # obtenemos precio
            if((args.display == "PRICE") or (args.display == "PRCBLK")):
                price = get_price()

            # obtenemos bloque
            if((args.display == "BLOCK") or (args.display == "PRCBLK")):
                block = get_block()
                fee = get_fees()

            if(args.display == "QUOTES"):
                image = Image.open(os.path.join(screensdir, str(
                    random.randint(1, 14)).zfill(3) + '.bmp'))
                epd.display(epd.getbuffer(image))

            if(args.display == "PRICE"):
                if args.sats:
                    time_draw.text((20, 35), price, font=fontprice, fill=0)
                    time_draw.text((100, 105), "sats / " + args.currency,
                                   font=font16, fill=0)
                else:
                    if int(price) < 100000:
                        time_draw.text((3, 35), price, font=fontprice, fill=0)
                    else:
                        time_draw.text((2, 35), price, font=fontprice100, fill=0)
                    time_draw.text((100, 105), args.currency,
                                   font=font16, fill=0)

            elif(args.display == "BLOCK"):
                time_draw.text((5, 35), block, font=fontblk, fill=0)
                time_draw.text((15, 100), fee, font=font16, fill=0)

            elif(args.display == "PRCBLK"):
                if displayblock:
                    time_draw.text((5, 35), block, font=fontblk, fill=0)
                    time_draw.text((15, 100), fee, font=font16, fill=0)
                    displayblock = False
                else:
                    if args.sats:
                        time_draw.text((20, 35), price, font=fontprice, fill=0)
                        time_draw.text((100, 105), "sats / " + args.currency,
                                       font=font16, fill=0)
                    else:
                        if int(price) < 100000:
                            time_draw.text((3, 35), price, font=fontprice, fill=0)
                        else:
                            time_draw.text((2, 35), price, font=fontprice100, fill=0)
                        time_draw.text((100, 105), args.currency,
                                       font=font16, fill=0)
                    displayblock = True

            # escribimos la fecha y hora encima
            time_draw.text((5, 5), tz.localize(now).strftime(
                "%d/%m/%Y %H:%M:%S"), font=font14, fill=0)
            if args.display != "QUOTES":
                epd.display(epd.getbuffer(time_image))
            time.sleep(args.time)

    # # ed.Clear(0xFF)
    # logging.info("Clear...")
    # epd.init(epd.FULL_UPDATE)
    # epd.Clear(0xFF)

    # logging.info("Goto Sleep...")
    # epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in13_V2.epdconfig.module_exit()
    exit()
