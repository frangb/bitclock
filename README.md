# raspi-blockclock
Blockclock para mostrar el precio actual del BTC en una raspberry Pi zero W con pantalla de tinta electrónica
<img src="https://github.com/frangb/raspi-blockclock/blob/main/raspi-blockclock.jpg" alt="raspi-blockclock" width="300"/>


## Lista de la compra.
Necesitaremos el siguiente material. Dejo los enlaces de Aliexpress de lo que he comprado yo, pero en realidad lo podéis comprar donde queráis (amazon, etc...)
- 1 x raspberry pi zero w, si puede ser con el pin header ya montado, esto te facilitará las cosas [enlace](https://es.aliexpress.com/item/4000693620101.html?spm=a2g0s.9042311.0.0.5d5363c0IMK1H6)
- 1 x cable micro hdmi a hdmi (o un adaptador micro hdmi a hdmi si ya tienes cable) [enlace](https://es.aliexpress.com/item/10000404075798.html?spm=a2g0s.9042311.0.0.5d5363c0IMK1H6)
- 1 x fuente alimentacion para raspberry pi zero (si la necesitas. En caso que tengas alguna regleta donde conectarla por USB con salida de 5V no sería necearia)
- 1 x pantalla waveshare e-ink de 2'13 pulgadas [enlace](https://es.aliexpress.com/item/4001261285356.html?spm=a2g0s.9042311.0.0.5d5363c0IMK1H6)
- 1 x teclado USB (puedes usar cualquier teclado que tengas por casa, ya que va a ser solo un momento) y un adaptador USB a mini-USB para poder conectarlo [enlace](https://es.aliexpress.com/item/1005001894830612.html?spm=a2g0o.productlist.0.0.3e52645fcWv8zN&algo_pvid=e53fb4cd-43b2-458f-9b1c-6b3fcd091c48&algo_expid=e53fb4cd-43b2-458f-9b1c-6b3fcd091c48-4&btsid=2100bde116178130299921634edfcd&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_)

## Montaje
Si hemos comprado la raspberry pi zero w con el pin header ya montado, no hay ninguna complicación, simplemente encajar la pantalla en el puerto GPIO de la raspberry

## Sistema operativo de la raspberry pi zero
Descargar el S.O. Raspberry Pi OS Lite de la siguiente dirección oficial
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
sudo apt-get install python3-pip
sudo apt-get install python3-pil
```

## Descarga del código del script
Descargamos el proyecto desde github
```
sudo git clone https://github.com/frangb/raspi-blockclock
```
Instalamos los paquetes requeridos
```
cd raspi-blockclock
pip3 install -r requirement.txt
```

## Ejecución del script
Uso:
```
python3 raspi-blockclock.py <intervalo> <zona-horaria> <moneda>
```
Donde:
- **intervalo**: intervalo (en segundos) tras el que queremos que actualice el precio. Te recomiendo no usar un intervalo muy corto ya que la página desde donde se obtienen los datos podría bloquear tu IP. Un intervalo de 5 (300) o 10 (600) minutos debe funcionar bien.
- **zona-horaria**: esto se usa para que aparezca correctamente la hora de la ultima actualización en la parte superior de la pantalla. 
- **moneda**: indicar USD o EUR segun la moneda que queramos utilizar

a) Si queremos que se inicie automáticamente al enchufar la Raspberry Pi Zero, debemos añadir la siguiente linea al archivo rc.local
```
sudo nano /etc/rc.local
```
Al final del archivo, antes de la linea ```exit 0``` añadimos el siguiente comando
```
sudo python3 /home/pi/raspi-blockclock/btc_ticker.py 300 Europe/Madrid USD &
```
*En este ejemplo he utilizado como intervalo de refresco 5 minutos (300 segundos) y como zona horaria Europe/Madrid, pero puedes cambiar estos parámetros a tu conveniencia*

b) Si queremos poner en marcha el script nosotros manualmente debemos ejecutarlo con de la siguiente forma, para que el proceso no se pare cuando cerremos la sesión de SSH
```
nohup python3 /home/pi/raspi-blockclock/btc_ticker.py 300 Europe/Madrid USD
```
## Opcional
Si la luz verde del LED de la Raspberry Pi Zero W nos parece molesto, podemos desactivarlo con el siguiente comando
```
echo none | sudo tee /sys/class/leds/led0/trigger
```
