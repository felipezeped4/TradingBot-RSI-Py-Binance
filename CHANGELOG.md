# CHANGELOG

A continuación se indican los cambios realizados en el Bot RSI Binance

## Unreleased

- Se añadirán registros json de RSI calculados y de las órdenes emitidas, para mejor lectura. La idea es dejar registros y limpiar los outputs en consola.

## Versión 0.2

### Added
- Se incluye archivo **CHANGELOG.md**
- Colores para destacar eventos importantes (Conexión iniciada, finalizada, compra y venta)
- Sonidos para notificar eventos importantes (Conexión iniciada, compra y venta)
- Se genera registro json de los puntos de cierre (closes) en directorio: data/closes/closes.json. Esto con motivo de facilitar lectura de eventos en consola.

### Changed

-  Se corrige error en envío de órdenes de compra.
- 

## Versión 0.1

### Added

- Archivo **README.md** incluye forma de uso e instalación.
- Se incluye archivo **requirements.txt**, con los paquetes que utiliza el bot.