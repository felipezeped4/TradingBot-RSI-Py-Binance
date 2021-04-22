import websocket, json, pprint, talib, numpy
import config
import os
from binance.client import Client
from binance.enums import *

os.system("color")

# En la URL del SOCKET se modifica el symbol (ej THETABNB) y el kline_periodo (ej 1m) 
# https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md#klinecandlestick-streams

SOCKET = "wss://stream.binance.com:9443/ws/thetabnb@kline_1m"

### Parámetros para cálculo RSI y órdenes Compra/Venta
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = 'THETABNB'
TRADE_QUANTITY = 0.05

### Array de cierres closes
closes = []

### En posición de compra
in_posicion = False

### Client
client = Client(config.API_KEY, config.API_SECRET, tld='us')

### Función para enviar orden (compra/venta)
def order(symbol, side, quantity, order_type=ORDER_TYPE_MARKET):
    try:
        print("Enviando Orden")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        print(order)
    except Exception as e:
        return False

    return True

def on_open(ws):
    print('\x1b[0;31;43m' + 'System: [Openned Conecction]' + '\x1b[0m' '\n')

def on_close(ws):
    print('\n')
    print('\x1b[0;31;43m' + 'System: [Closed Conecction]' + '\x1b[0m')

def on_message(ws, message):
    global closes

    #print("received message")
    json_message = json.loads(message)
    #pprint.pprint(json_message)

    ###Candle logic
    candle = json_message['k']
    
    is_candle_closed = candle['x']
    close = candle['c']

    if is_candle_closed:
        print('\x1b[1;37;44m' + "Candle close at {}".format(close) + '\x1b[0m')
        closes.append(float(close))
        print("Closes")
        print(closes)
    
        ### Cálculo de RSI
        if len(closes) > RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            print('\x1b[1;37;44m' + "RSI Calculados" + '\x1b[0m')
            print(rsi)
            last_rsi = rsi[-1]
            print("El RSI actual es {}".format(last_rsi))

            if last_rsi > RSI_OVERBOUGHT:
                if in_posicion:
                    print('\x1b[5;37;42m' + "SELL, SELL, SELL" + '\x1b[0')
                    # Acá va lógica de venta
                    order_succeded = client.create_order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                    if order_succeded:
                        in_posicion = False
                else:
                    print("No hay nada que vender.")
            
            if last_rsi < RSI_OVERSOLD:
                if in_posicion:
                    print("Está oversold, pero ya está en posición, nada que hacer")
                else:
                    print('\x1b[5;37;41m' + "BUY, BUY, BUY" + '\x1b[0m')
                    # Acá va lógica de compra
                    order_succeded = client.create_order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                    if order_succeded:
                        in_posicion = True

ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()