# CMNT Contract Fix
---
Diversas correciones sobre el módulo de contratos.

## Error 'bool' object has no attribute 'strftime'

- Si una línea de contrato ya ha finalizado, no calculará su fecha de fin de período.
con lo que fallará en la función de _insert_markers, a la cual se le pasa la fecha de última factura
que previamente se iguala al False que calculó la fecha de fin de período.