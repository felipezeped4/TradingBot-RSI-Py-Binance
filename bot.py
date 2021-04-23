import websocket, json, pprint, talib, numpy
import config
from binance.client import Client
from binance.enums import *
import os

#Evita que pygame despliegue bienvenida en consola
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

os.system("color")

pygame.init()

#set de audios en variables
b = pygame.mixer.Sound("sounds/buy.mp3")
s = pygame.mixer.Sound("sounds/sell.mp3")

SOCKET = "wss://stream.binance.com:9443/ws/thetabnb@kline_1m"

### Parámetros para cálculo RSI y órdenes Compra/Venta
RSI_PERIOD = 2
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = 'THETABNB'
TRADE_QUANTITY = 0.05

### Array de cierres closes
closes = []

### En posición de compra
in_posicion = True

### Client
client = Client(config.API_KEY, config.API_SECRET)

### Función para enviar orden (compra/venta)
def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print("Enviando Orden")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        print(order)
    except Exception as e:
        print("Ha ocurrido un error al enviar la orden - {}".format(e))
        return False

    return True


def on_open(ws):
    print('\x1b[0;31;43m' + 'System: [Openned Conecction]' + '\x1b[0m' '\n')
    pygame.mixer.Sound.play(b)
    pygame.mixer.music.stop()

def on_close(ws):
    print('\n')
    print('\x1b[0;31;43m' + 'System: [Closed Conecction]' + '\x1b[0m')

def on_message(ws, message):
    global closes, in_posicion, b, s

    #print("received message")
    json_message = json.loads(message)
    #pprint.pprint(json_message)

    candle = json_message['k']
    
    is_candle_closed = candle['x']
    close = candle['c']

    if is_candle_closed:
        print("Candle close at {}".format(close))
        closes.append(float(close))
        json_closes = json.dumps(closes)
        closesFile = open("data/closes/closes.json", "w")
        closesFile.write(json_closes)
        closesFile.close()
    
        ### Cálculo de RSI
        if len(closes) > RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            print("RSI Calculados")
            print(rsi)
            last_rsi = rsi[-1]
            print("El RSI actual es {}".format(last_rsi))

            if last_rsi > RSI_OVERBOUGHT:
                if in_posicion:
                    print('\x1b[5;37;42m' + "#### VENDE ####" + '\x1b[0m')
                    # Acá va lógica de venta
                    order_succeeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                    pygame.mixer.Sound.play(s)
                    pygame.mixer.music.stop()
                    if order_succeeded:
                        in_posicion = False
                else:
                    print("Está Overbought pero ya vendiste.")
            
            if last_rsi < RSI_OVERSOLD:
                if in_posicion:
                    print("Está Oversold, pero ya compraste.")
                else:
                    print('\x1b[5;37;42m' + "#### COMPRA ####" + '\x1b[0m')
                    # Acá va lógica de compra
                    order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                    pygame.mixer.Sound.play(b)
                    pygame.mixer.music.stop()
                    if order_succeeded:
                        in_posicion = True

ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()