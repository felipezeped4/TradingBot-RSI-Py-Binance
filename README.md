# Bot Binance con RSI

* Este bot está diseñado para realizar trades en la plataforma Binance.
* Utiliza Python 3.5 o superior
* Actualmente utiliza el [indicador RSI](https://academy.binance.com/es/articles/what-is-the-rsi-indicator) para calcular si realiza o no un trade.
* No es de mi total autoría, está basado en otro desarrollo.. (En cuanto recuerde la documentación/video lo pondré)

## Disclaimer!

* Este bot fue hecho con propósitos de aprendizaje y si bien puede utilizarse para realizar trade, se recomienda hacerlo con cautela por los siguientes motivos:
1. No ha sido probado de manera extensa.
2. El indicador RSI por si solo, puede generar compras/ventas en puntos previos al máximo de cada período, por lo cual es ideal poder ocuparlo con otros indicadores

## Installation

Utilizar el administrador de paquetes PIP [pip](https://pip.pypa.io/en/stable/) para instalar los paquetes necesarios, que se encuentran en el archivo requirements.txt utilizando el siguiente comando

```powershell
    # Directament con PIP
    pip install -r requirements.txt

    # En caso de ambiente virtual o PIP no es variable de entorno invocar mediante python de alguna de las siguientes opciones:
    python -m pip install -r requirements.txt

    #O también
    py -m pip install -r requirements.txt
```

## Configuración de uso
* Esta versión 0.1 tiene pre-configurados los parámetros por defecto que utiliza el algoritmo RSI. En caso de requerir customización, se debe hacer en el código en los siguientes parámetros:

```python    
    RSI_PERIOD = 14
    RSI_OVERBOUGHT = 70
    RSI_OVERSOLD = 30
```

* Dependiendo del **símbolo** y del **tiempo** que se desee recolectar los datos, se debe modificar la siguiente línea con el parámetro indicado en la documentación:
1. Para el tiempo: Referir a la documentación de [Binance API](https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md#klinecandlestick-streams)
2. Para el símbolo de trade: Tomar de Binance según moneda en análisis. Ej: BNB/USDT se remueve el "/" y queda BNBUSDT 

```python
    SOCKET = "wss://stream.binance.com:9443/ws/SIMBOLO_DE_TRADE@kline__PONER_ACÁ_TIEMPO"

    #ejemplo
    SOCKET = "wss://stream.binance.com:9443/ws/BNBUSDT@kline_1m"
```

* Para el trade además deben ser configurados los siguientes parámetros:

```python
    TRADE_SYMBOL = 'ACÁ_VA_SÍMBOLO_DE_LA_MONEDA'
    TRADE_QUANTITY = 'ACÁ_VA_EL_MONTO_A_TRADEAR'
```

* En el archivo config.py se deben ingresar la ApiKey y ApiSecret, los cuales se deben obtener del sitio web de Binance siguiendo la documentación [¿Cómo crear una clave API?](https://www.binance.com/es/support/faq/360002502072)

```python
    API_KEY = "Entre estas comillas va tu API KEY"
    API_SECRET = "Entre estas comillas va tu API SECRET"
```

## Referencias
* [Binance Api]()
* [Indicador RSI](https://academy.binance.com/es/articles/what-is-the-rsi-indicator)
* [WebSocket Streams](https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md)