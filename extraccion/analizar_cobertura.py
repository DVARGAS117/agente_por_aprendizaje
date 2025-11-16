"""
Análisis de datos extraídos - Verificar cobertura temporal
"""

import sqlite3
import pandas as pd
from datetime import datetime

DB_PATH = r"C:\Users\Hector\Desktop\Proyectos\AGENTE_POR_APRENDIZAJE\mt5_data.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Obtener todas las tablas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'eurusd_%'")
tables = cursor.fetchall()

print("=" * 80)
print("📊 ANÁLISIS DE COBERTURA DE DATOS")
print("=" * 80)

for (table,) in tables:
    cursor.execute(f"SELECT COUNT(*), MIN(datetime), MAX(datetime) FROM {table}")
    count, min_d, max_d = cursor.fetchone()
    
    if count == 0:
        continue
    
    tf = table.replace('eurusd_', '').upper()
    
    min_date = pd.to_datetime(min_d)
    max_date = pd.to_datetime(max_d)
    
    dias_totales = (max_date - min_date).days
    años_totales = dias_totales / 365.25
    
    # Calcular cuántos registros DEBERÍAN haber
    if tf == 'H1':
        # 24 horas * 5 días laborables = 120 barras por semana aprox
        barras_esperadas_por_año = 24 * 5 * 52
    elif tf == 'M15':
        # 4 barras por hora * 24 horas * 5 días = 480 barras por semana aprox
        barras_esperadas_por_año = (60 // 15) * 24 * 5 * 52
    elif tf == 'M5':
        # 12 barras por hora * 24 horas * 5 días = 1440 barras por semana aprox
        barras_esperadas_por_año = (60 // 5) * 24 * 5 * 52
    elif tf == 'M1':
        # 60 barras por hora * 24 horas * 5 días = 7200 barras por semana aprox
        barras_esperadas_por_año = 60 * 24 * 5 * 52
    
    barras_esperadas_totales = int(barras_esperadas_por_año * años_totales)
    porcentaje_cobertura = (count / barras_esperadas_totales) * 100 if barras_esperadas_totales > 0 else 0
    
    print(f"\n📈 {tf}:")
    print(f"   Registros actuales: {count:,}")
    print(f"   Fecha inicial: {min_d}")
    print(f"   Fecha final: {max_d}")
    print(f"   Días cubiertos: {dias_totales:,} días")
    print(f"   Años cubiertos: {años_totales:.2f} años")
    print(f"   Barras esperadas (aprox): {barras_esperadas_totales:,}")
    print(f"   Cobertura: {porcentaje_cobertura:.1f}%")
    
    # Verificar gaps
    df = pd.read_sql_query(f"SELECT datetime FROM {table} ORDER BY datetime", conn)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['diff'] = df['datetime'].diff()
    
    # Gaps mayores a 7 días
    large_gaps = df[df['diff'] > pd.Timedelta(days=7)]
    
    if len(large_gaps) > 0:
        print(f"   ⚠️  Gaps grandes detectados: {len(large_gaps)}")
        for idx, row in large_gaps.head(3).iterrows():
            print(f"      - Gap en {row['datetime']}: {row['diff']}")

print("\n" + "=" * 80)
print("🔍 VERIFICANDO DISPONIBILIDAD EN MT5")
print("=" * 80)

# Intentar consultar datos más antiguos directamente de MT5
import MetaTrader5 as mt5

if mt5.initialize():
    print("✅ MT5 conectado")
    
    # Intentar obtener la barra más antigua disponible
    from datetime import datetime, timedelta
    
    # Probar fechas cada vez más antiguas
    test_dates = [
        datetime(2010, 1, 1),
        datetime(2012, 1, 1),
        datetime(2014, 1, 1),
        datetime(2015, 1, 1),
    ]
    
    print("\n📅 Probando disponibilidad de datos históricos en MT5:")
    for test_date in test_dates:
        rates = mt5.copy_rates_from("EURUSD", mt5.TIMEFRAME_H1, test_date, 1)
        if rates is not None and len(rates) > 0:
            first_bar = pd.to_datetime(rates[0]['time'], unit='s')
            print(f"   ✅ Desde {test_date.strftime('%Y-%m-%d')}: Datos disponibles (primera barra: {first_bar})")
        else:
            print(f"   ❌ Desde {test_date.strftime('%Y-%m-%d')}: No hay datos")
    
    # Obtener la barra más antigua posible
    print("\n🔎 Buscando la barra más antigua disponible...")
    rates = mt5.copy_rates_from("EURUSD", mt5.TIMEFRAME_H1, datetime(1970, 1, 1), 1)
    if rates is not None and len(rates) > 0:
        oldest_bar = pd.to_datetime(rates[0]['time'], unit='s')
        print(f"   📊 Barra más antigua en MT5: {oldest_bar}")
        
        # Comparar con lo que tenemos
        cursor.execute("SELECT MIN(datetime) FROM eurusd_h1")
        our_oldest = cursor.fetchone()[0]
        print(f"   📊 Nuestra barra más antigua: {our_oldest}")
        
        if oldest_bar < pd.to_datetime(our_oldest):
            diff_days = (pd.to_datetime(our_oldest) - oldest_bar).days
            print(f"   ⚠️  Nos faltan {diff_days} días de datos históricos!")
            print(f"   💡 Puedes extraer desde {oldest_bar} hasta {our_oldest}")
    
    mt5.shutdown()
else:
    print("❌ No se pudo conectar a MT5")

conn.close()

print("\n" + "=" * 80)
print("📋 CONCLUSIÓN")
print("=" * 80)
print("""
Si MT5 tiene datos más antiguos disponibles:
  1. Modifica YEARS_TO_EXTRACT en el script
  2. O usa una fecha de inicio específica más antigua
  
Si no hay más datos disponibles:
  - Pepperstone tiene un límite de datos históricos
  - Algunos brokers solo mantienen 2-3 años en timeframes pequeños (M1)
  - H1 suele tener más historia (5-10 años)
""")
