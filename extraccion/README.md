# Extractor de Datos MT5 a SQLite

Sistema automatizado para extraer datos OHLC de MetaTrader 5 y almacenarlos en SQLite para backtesting.

## � Datos Disponibles en la Base de Datos

### Resumen por Timeframe (EURUSD)

| Timeframe | Registros | Fecha Inicio | Fecha Fin | Cobertura | Tamaño Aprox |
|-----------|-----------|--------------|-----------|-----------|--------------|
| **H1** (1 Hora) | 62,147 | 2015-11-19 00:00 | 2025-11-14 23:00 | **9.99 años** | ~8.7 MB |
| **M15** (15 Min) | 101,214 | 2021-10-22 03:15 | 2025-11-14 23:45 | **4.06 años** | ~14 MB |
| **M5** (5 Min) | 65,569 | 2024-12-31 00:10 | 2025-11-14 23:50 | **10.6 meses** | ~9 MB |
| **M1** (1 Min) | 50,296 | 2025-09-29 00:01 | 2025-11-14 23:54 | **1.5 meses** | ~7 MB |

**Total:** ~280,000 barras | **Tamaño BD:** ~39 MB

### ⚠️ Limitaciones del Broker (Pepperstone)

Los brokers tienen límites en cuántos datos históricos almacenan:

- **✅ H1 (1 Hora)**: Excelente cobertura - 10 años completos
- **⚠️ M15 (15 Min)**: Buena cobertura - 4 años (suficiente para la mayoría de backtests)
- **⚠️ M5 (5 Min)**: Cobertura limitada - Solo ~11 meses (limitación del broker)
- **❌ M1 (1 Min)**: Cobertura muy limitada - Solo ~1.5 meses (limitación del broker)

**Nota:** Estos son los datos máximos disponibles en Pepperstone. Para obtener más datos históricos en timeframes pequeños (M1, M5), necesitarías usar fuentes alternativas como DukasCopy o HistData.com.

### 📈 Distribución de Datos H1 por Año

| Año | Registros | Desde | Hasta |
|-----|-----------|-------|-------|
| 2015 | 713 | 2015-11-19 | 2015-12-31 |
| 2016 | 6,227 | 2016-01-04 | 2016-12-31 |
| 2017 | 6,211 | 2017-01-02 | 2017-12-29 |
| 2018 | 6,206 | 2018-01-02 | 2018-12-31 |
| 2019 | 6,216 | 2019-01-02 | 2019-12-31 |
| 2020 | 6,235 | 2020-01-02 | 2020-12-31 |
| 2021 | 6,238 | 2021-01-04 | 2021-12-31 |
| 2022 | 6,207 | 2022-01-03 | 2022-12-30 |
| 2023 | 6,214 | 2023-01-02 | 2023-12-29 |
| 2024 | 6,234 | 2024-01-02 | 2024-12-31 |
| 2025 | 5,446 | 2025-01-02 | 2025-11-14 |

### 💰 Estadísticas de Precios (EURUSD H1)

- **Precio Mínimo:** 0.95358
- **Precio Máximo:** 1.25556
- **Precio Promedio:** 1.11990
- **Rango de Precio:** 0.30198 (30,198 pips)

---

## �📋 Requisitos

```bash
pip install MetaTrader5 pandas
```

## ⚙️ Configuración

### 1. Editar credenciales en `extract_mt5_data.py`

```python
# Credenciales de MT5
MT5_LOGIN = 12345678  # Tu número de cuenta
MT5_PASSWORD = "tu_contraseña"  # Tu contraseña
MT5_SERVER = "Pepperstone-Demo"  # o "Pepperstone-Live"

# Path de la base de datos (opcional, ya está configurado)
DB_PATH = r"C:\Users\Hector\Desktop\Proyectos\AGENTE_POR_APRENDIZAJE\mt5_data.db"
```

### 2. Configuración adicional (opcional)

```python
SYMBOL = "EURUSD"  # Par a extraer
TIMEFRAME = mt5.TIMEFRAME_H1  # Timeframe (1H)
YEARS_TO_EXTRACT = 10  # Años hacia atrás
BATCH_SIZE = 10000  # Tamaño de lote
```

## 🚀 Uso

### Extraer datos de MT5

```bash
python extract_mt5_data.py
```

El script:
- ✅ Se conecta a MT5 automáticamente
- ✅ Extrae datos en lotes (evita límites de MT5)
- ✅ Muestra progreso en tiempo real
- ✅ Evita duplicados automáticamente
- ✅ Guarda todo en SQLite con índices optimizados

### Consultar datos

```bash
python query_mt5_data.py
```

Incluye ejemplos de:
- Consultas por rango de fechas
- Consultas por año
- Datos recientes
- Patrones por hora del día
- Patrones por día de la semana
- Exportación a CSV

## 📊 Estructura de la Base de Datos

Tabla: `eurusd_h1`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| time | INTEGER | Timestamp Unix (PRIMARY KEY) |
| datetime | TEXT | Fecha y hora legible |
| open | REAL | Precio de apertura |
| high | REAL | Precio máximo |
| low | REAL | Precio mínimo |
| close | REAL | Precio de cierre |
| tick_volume | INTEGER | Volumen de ticks |
| spread | INTEGER | Spread en puntos |
| real_volume | INTEGER | Volumen real |
| year | INTEGER | Año (para filtros) |
| month | INTEGER | Mes (para filtros) |
| day | INTEGER | Día (para filtros) |
| hour | INTEGER | Hora (para filtros) |
| day_of_week | INTEGER | Día de la semana (0=Lun, 6=Dom) |

## 💡 Ejemplos de Consultas SQL

### Obtener datos de un mes específico
```sql
SELECT * FROM eurusd_h1 
WHERE year = 2024 AND month = 10
ORDER BY datetime;
```

### Obtener datos de las 14:00 horas
```sql
SELECT * FROM eurusd_h1 
WHERE hour = 14
ORDER BY datetime;
```

### Calcular volatilidad promedio por día de la semana
```sql
SELECT day_of_week, AVG(high - low) as avg_volatility
FROM eurusd_h1
GROUP BY day_of_week
ORDER BY day_of_week;
```

### Obtener datos entre dos fechas
```sql
SELECT * FROM eurusd_h1
WHERE datetime BETWEEN '2024-01-01' AND '2024-12-31'
ORDER BY datetime;
```

## 📦 Archivos del Proyecto

- `extract_mt5_data.py` - Script principal de extracción
- `query_mt5_data.py` - Script de consultas y ejemplos
- `mt5_data.db` - Base de datos SQLite (se crea automáticamente)
- `README.md` - Este archivo

## ⚠️ Notas Importantes

1. **MT5 debe estar abierto** durante la extracción
2. El script descarga en lotes de 10,000 barras para evitar límites de MT5
3. Los duplicados se omiten automáticamente
4. Si la extracción se interrumpe, puedes volver a ejecutar el script y continuará donde se quedó
5. La base de datos tiene índices optimizados para consultas rápidas

## 🔧 Solución de Problemas

### Error: "No se pudo inicializar MT5"
- Asegúrate de que MT5 esté abierto
- Verifica que la biblioteca MetaTrader5 esté instalada

### Error en login
- Verifica tus credenciales (LOGIN, PASSWORD, SERVER)
- Para cuentas Demo: usar "Pepperstone-Demo"
- Para cuentas Live: usar "Pepperstone-Live"

### Sin credenciales
- Si dejas las credenciales vacías, usará la cuenta activa en MT5

### Datos incompletos
- El script descarga todos los datos disponibles
- MT5 puede no tener datos completos de 10 años para todos los símbolos
- Verifica en MT5 cuántos datos históricos tiene tu broker

## 📈 Uso para Backtesting

```python
import sqlite3
import pandas as pd

# Conectar a la BD
conn = sqlite3.connect('mt5_data.db')

# Cargar datos para backtesting
df = pd.read_sql_query("""
    SELECT * FROM eurusd_h1 
    WHERE datetime BETWEEN '2023-01-01' AND '2023-12-31'
    ORDER BY datetime
""", conn)

# Tu estrategia de backtesting aquí
# ...

conn.close()
```

## 📞 Soporte

Para modificar el script según tus necesidades, edita las variables de configuración al inicio de `extract_mt5_data.py`.
