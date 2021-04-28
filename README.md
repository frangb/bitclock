# bitclock
bitclock es un proyecto para mostrar información relativa a bitcoin en una raspberry Pi zero W con pantalla de tinta electrónica
<img src="https://github.com/frangb/raspi-blockclock/blob/master/raspi-blockclock.jpg" alt="raspi-blockclock" width="300"/>


## Lista de la compra.
Necesitaremos el siguiente material. Dejo los enlaces de Aliexpress de lo que he comprado yo, pero en realidad lo podéis comprar donde queráis (amazon, etc...)
- 1 x Raspberry Pi Zero W, si puede ser con el pin header ya montado, esto te facilitará las cosas [enlace](https://es.aliexpress.com/item/4000693620101.html?spm=a2g0s.9042311.0.0.5d5363c0IMK1H6)
- 1 x cable micro hdmi a hdmi (o un adaptador micro hdmi a hdmi si ya tienes cable) [enlace](https://es.aliexpress.com/item/10000404075798.html?spm=a2g0s.9042311.0.0.5d5363c0IMK1H6)
- 1 x fuente alimentación para raspberry pi zero (si la necesitas. En caso que tengas alguna regleta donde conectarla por USB con salida de 5V no sería necesaria)
- 1 x pantalla waveshare e-ink de 2'13 pulgadas [enlace](https://es.aliexpress.com/item/4001261285356.html?spm=a2g0s.9042311.0.0.5d5363c0IMK1H6)
- 1 x teclado USB (puedes usar cualquier teclado que tengas por casa, ya que va a ser solo un momento) y un adaptador USB a mini-USB para poder conectarlo [enlace](https://es.aliexpress.com/item/1005001894830612.html?spm=a2g0o.productlist.0.0.3e52645fcWv8zN&algo_pvid=e53fb4cd-43b2-458f-9b1c-6b3fcd091c48&algo_expid=e53fb4cd-43b2-458f-9b1c-6b3fcd091c48-4&btsid=2100bde116178130299921634edfcd&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_)
- 1 x tarjeta microSD de 8 GB o superior

## Montaje
Si hemos comprado la Raspberry Pi Zero w con el pin header ya montado, no habrá ninguna complicación. Simplemente encajaremos la pantalla en el puerto GPIO de la raspberry y listo.

## Sistema operativo de la raspberry pi zero
Descargar el sistema operativo Raspberry Pi OS Lite de la siguiente dirección oficial
https://www.raspberrypi.org/software/operating-systems/

Debemos grabar el Sistema Operativo en una tarjeta SD de tamaño suficiente (con una pequeña de 1 GB debe bastar). Para grabar la imagen yo personalmente uso le aplicación Etcher. Es multiplataforma y la podéis descargar [aqui](https://www.balena.io/etcher/)

## Configuración y primeros pasos
Insertamos la tarjeta SD en la raspberry pi zero, conectamos el cable hdmi al monitor, un teclado y conectamos a la corriente.
Nos conectamos con el `user: pi` , `password: raspberry`, y ejecutamos el siguiente comando:
```
sudo raspi-config
```
En el menú configuración que aparece realizamos los siguientes cambios

**Configurar wifi**
    System options / Wireless LAN: conectar al wifi de casa (escribir el nombre de la red y la contraseña)

**Activar SSH**
    Interface options / SSH / enable

**Activar SPI**
    Interface options / SPI / enable

Una vez hecho esto, ya podríamos en teoría desconectar monitor y teclado de nuestra Raspberry Pi y continuar todo el proceso desde un terminal SSH que abriríamos desde algún ordenador que tengamos en la misma red. Para ello necesitamos primero obtener la dirección IP de la raspberry:
```
ifconfig
```
tras la ejecución de este comando obtendremos una salida como la siguiente

```
lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

wlan0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.136  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::a21:977c:c3f5:8fee  prefixlen 64  scopeid 0x20<link>
        ether b8:27:eb:ec:d7:d8  txqueuelen 1000  (Ethernet)
        RX packets 22986  bytes 17167770 (16.3 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 7194  bytes 1042225 (1017.7 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```
Debemos anotar la dirección que aparece en el interfaz wlan0, en el caso del ejemplo sería ```inet 192.168.1.136```

Ahora, para conectar a nuestra Raspberry Pi desde cualquier otro ordenador que se encuentre en la red local, abriremos un terminal en dicho ordenador (En windows, con el comando cmd, en Mac y linux abriendo un terminal) y ejecutaremos:
```
ssh pi@<dirección ip de la raspberry>
```
El sistema nos pedira la contraseña del usuario ```pi```. Escribiremos ```raspberry```

## Instalar herramientas y dependencias
```
sudo apt-get update
sudo apt-get install git
sudo apt-get install python3-pip
sudo apt-get install python3-pil
sudo apt-get install libatlas-base-dev
```

## Descarga del código del script
Descargamos el proyecto desde github
```
sudo git clone https://github.com/frangb/bitclock
```
Instalamos los paquetes requeridos
```
cd bitclock
sudo pip3 install -r requirements.txt
```

## Ejecución del script
Uso:
```
python3 btc_ticker.py [-h] [-t TIME] [-c {USD,EUR}] [-d {PRICE,BLOCK,PRCBLK}] [-tz TIMEZONE]
```

Disponemos de los siguientes argumentos opcionales:

**-h, --help**: Muestra un mensaje de ayuda explicando el uso de cada uno de los parámetros opcionales.

**-t, --time**: tiempo de refresco (en segundos) tras el que queremos que actualice el precio. Te recomiendo no usar un intervalo muy corto ya que la página desde donde se obtienen los datos podría bloquear tu IP. Un intervalo de 5 (300) o 10 (600) minutos debe funcionar bien. Si no se indica nada, por defecto se tomarán 60 segundos.

**-c, --currency**: indicar USD o EUR segun la moneda que queramos utilizar. Si no se indica nada, por defecto se mostrará en USD.

**-d, --display**: información que mostraremos en la pantalla. Indicar PRICE si queremos unicamente mostrar el precio, BLOCK si queremos mostrar la altura del bloque actual y las fees estimadas para confirmación inmediata / 30 min / 1 hora, o PRCBLK si queremos alternar entre ambos modos. Si no se indica nada, por defecto se mostrará el precio.

**-tz, --timezone**: esto se usa para que aparezca correctamente la hora de la ultima actualización en la parte superior de la pantalla. Puedes consultar las zonas horarias disponibles [aqui](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones). Elige una de las zonas de la columna "TZ database name", por ejemplo "Europe/Madrid". Si no se indica nada, por defecto se usará la zona "Europe/Madrid".

a) Si queremos que se inicie automáticamente al enchufar la Raspberry Pi Zero, debemos añadir la siguiente linea al archivo rc.local
```
sudo nano /etc/rc.local
```
Al final del archivo, antes de la linea ```exit 0``` añadimos el siguiente comando
```
sudo python3 btc_ticker.py -t 300 -c USD -d PRICE -tz Europe/Madrid &
```
*En este ejemplo he utilizado como intervalo de refresco 5 minutos (300 segundos) y como zona horaria Europe/Madrid, pero puedes cambiar estos parámetros a tu conveniencia*

b) Si queremos poner en marcha el script nosotros manualmente debemos ejecutarlo con de la siguiente forma, para que el proceso no se pare cuando cerremos la sesión de SSH
```
nohup python3 /home/pi/raspi-blockclock/btc_ticker.py -t 300 -c USD -d PRICE -tz Europe/Madrid
```

## Opcional
Si la luz verde del LED de la Raspberry Pi Zero W nos parece molesto, podemos desactivarlo con el siguiente comando
```
echo none | sudo tee /sys/class/leds/led0/trigger
```

## ¿Cómo actualizar?
Si el proyecto ha sufrido algún cambio y necesitas actualizarlo, únicamente tienes que acceder por ssh a tu raspberry pi zero, borrar el directorio de la aplicación mediante el comando:
```
rm -rf bitclock
```

y a continuación volver a descargar el repositorio mediante el comando:
```
git clone https://github.com/frangb/raspi-blockclock
```
