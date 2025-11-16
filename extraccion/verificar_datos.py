"""
Script de verificación de integridad de datos
Realiza chequeos exhaustivos de la base de datos
"""

import sqlite3
import pandas as pd
from datetime import datetime

DB_PATH = r"C:\Users\Hector\Desktop\Proyectos\AGENTE_POR_APRENDIZAJE\mt5_data.db"

def verificar_integridad():
    """Verifica la integridad de los datos en la BD"""
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("=" * 70)
    print("🔍 VERIFICACIÓN DE INTEGRIDAD DE DATOS")
    print("=" * 70)
    
    # 1. Verificar duplicados
    print("\n1️⃣  Verificando duplicados por timestamp...")
    cursor.execute("""
        SELECT time, COUNT(*) as count 
        FROM eurusd_h1 
        GROUP BY time 
        HAVING count > 1
    """)
    duplicates = cursor.fetchall()
    if len(duplicates) == 0:
        print("   ✅ No hay duplicados por timestamp")
    else:
        print(f"   ❌ Se encontraron {len(duplicates)} timestamps duplicados")
        for dup in duplicates[:5]:
            print(f"      Timestamp: {dup[0]}, Cantidad: {dup[1]}")
    
    # 2. Verificar duplicados por datetime
    print("\n2️⃣  Verificando duplicados por datetime...")
    cursor.execute("""
        SELECT datetime, COUNT(*) as count 
        FROM eurusd_h1 
        GROUP BY datetime 
        HAVING count > 1
    """)
    duplicates_dt = cursor.fetchall()
    if len(duplicates_dt) == 0:
        print("   ✅ No hay duplicados por datetime")
    else:
        print(f"   ❌ Se encontraron {len(duplicates_dt)} fechas duplicadas")
    
    # 3. Verificar valores nulos
    print("\n3️⃣  Verificando valores nulos en columnas críticas...")
    columns = ['open', 'high', 'low', 'close', 'tick_volume', 'spread']
    nulls_found = False
    for col in columns:
        cursor.execute(f"SELECT COUNT(*) FROM eurusd_h1 WHERE {col} IS NULL")
        null_count = cursor.fetchone()[0]
        if null_count > 0:
            print(f"   ❌ {col}: {null_count} valores nulos")
            nulls_found = True
    if not nulls_found:
        print("   ✅ No hay valores nulos en columnas críticas")
    
    # 4. Verificar consistencia OHLC (High >= Low, etc.)
    print("\n4️⃣  Verificando consistencia OHLC...")
    cursor.execute("""
        SELECT COUNT(*) FROM eurusd_h1 
        WHERE high < low OR high < open OR high < close OR low > open OR low > close
    """)
    inconsistent = cursor.fetchone()[0]
    if inconsistent == 0:
        print("   ✅ Todas las barras tienen OHLC consistente")
    else:
        print(f"   ❌ {inconsistent} barras tienen OHLC inconsistente")
    
    # 5. Verificar gaps temporales (horas faltantes)
    print("\n5️⃣  Verificando continuidad temporal...")
    df = pd.read_sql_query("""
        SELECT datetime FROM eurusd_h1 
        ORDER BY datetime
    """, conn)
    
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['time_diff'] = df['datetime'].diff()
    
    # Gaps mayores a 1 día (considerando fines de semana)
    large_gaps = df[df['time_diff'] > pd.Timedelta(days=3)]
    
    if len(large_gaps) == 0:
        print("   ✅ No hay gaps temporales significativos (>3 días)")
    else:
        print(f"   ⚠️  Se encontraron {len(large_gaps)} gaps temporales (>3 días)")
        print("      Nota: Esto puede ser normal en fines de semana largos o festivos")
        for idx, row in large_gaps.head(5).iterrows():
            print(f"      Gap en: {row['datetime']}, Duración: {row['time_diff']}")
    
    # 6. Verificar rangos de precios (detectar outliers obvios)
    print("\n6️⃣  Verificando rangos de precios razonables...")
    cursor.execute("""
        SELECT 
            MIN(low) as min_price,
            MAX(high) as max_price,
            AVG(close) as avg_price,
            (MAX(high) - MIN(low)) as price_range
        FROM eurusd_h1
    """)
    min_p, max_p, avg_p, range_p = cursor.fetchone()
    
    print(f"   📊 Rango total: {min_p:.5f} - {max_p:.5f}")
    print(f"   📊 Promedio: {avg_p:.5f}")
    print(f"   📊 Amplitud: {range_p:.5f}")
    
    # Detectar precios extremos (más de 30% del promedio)
    cursor.execute(f"""
        SELECT COUNT(*) FROM eurusd_h1 
        WHERE close < {avg_p * 0.7} OR close > {avg_p * 1.3}
    """)
    outliers = cursor.fetchone()[0]
    if outliers == 0:
        print("   ✅ No hay precios extremos/outliers detectados")
    else:
        print(f"   ⚠️  {outliers} barras con precios fuera del rango normal (±30%)")
    
    # 7. Verificar distribución por día de la semana
    print("\n7️⃣  Verificando distribución por día de la semana...")
    cursor.execute("""
        SELECT 
            day_of_week,
            CASE day_of_week
                WHEN 0 THEN 'Lunes'
                WHEN 1 THEN 'Martes'
                WHEN 2 THEN 'Miércoles'
                WHEN 3 THEN 'Jueves'
                WHEN 4 THEN 'Viernes'
                WHEN 5 THEN 'Sábado'
                WHEN 6 THEN 'Domingo'
            END as dia,
            COUNT(*) as total
        FROM eurusd_h1
        GROUP BY day_of_week
        ORDER BY day_of_week
    """)
    
    for row in cursor.fetchall():
        day_num, day_name, total = row
        print(f"   {day_name:10s}: {total:6,} barras")
    
    # 8. Verificar distribución por hora
    print("\n8️⃣  Verificando distribución por hora del día...")
    cursor.execute("""
        SELECT hour, COUNT(*) as total
        FROM eurusd_h1
        GROUP BY hour
        ORDER BY hour
    """)
    
    hours_data = cursor.fetchall()
    # Mostrar solo horas con menos datos (posibles problemas)
    avg_per_hour = sum([h[1] for h in hours_data]) / len(hours_data)
    print(f"   Promedio por hora: {avg_per_hour:.0f} barras")
    
    low_hours = [h for h in hours_data if h[1] < avg_per_hour * 0.8]
    if low_hours:
        print(f"   ⚠️  Horas con menos datos (<80% del promedio):")
        for hour, count in low_hours:
            print(f"      Hora {hour:02d}:00: {count:,} barras ({count/avg_per_hour*100:.1f}%)")
    else:
        print("   ✅ Distribución uniforme por hora")
    
    # 9. Verificar spread (no debería ser negativo)
    print("\n9️⃣  Verificando spreads...")
    cursor.execute("SELECT COUNT(*) FROM eurusd_h1 WHERE spread < 0")
    negative_spreads = cursor.fetchone()[0]
    
    cursor.execute("SELECT MIN(spread), MAX(spread), AVG(spread) FROM eurusd_h1")
    min_s, max_s, avg_s = cursor.fetchone()
    
    if negative_spreads == 0:
        print("   ✅ No hay spreads negativos")
    else:
        print(f"   ❌ {negative_spreads} spreads negativos encontrados")
    
    print(f"   📊 Spread mín: {min_s}, máx: {max_s}, promedio: {avg_s:.2f}")
    
    # 10. Muestra de datos aleatorios
    print("\n🔟 Muestra aleatoria de 5 registros:")
    print("-" * 70)
    df_sample = pd.read_sql_query("""
        SELECT datetime, open, high, low, close, tick_volume, spread
        FROM eurusd_h1
        ORDER BY RANDOM()
        LIMIT 5
    """, conn)
    
    for idx, row in df_sample.iterrows():
        print(f"   {row['datetime']}: O={row['open']:.5f} H={row['high']:.5f} "
              f"L={row['low']:.5f} C={row['close']:.5f} V={row['tick_volume']:,} S={row['spread']}")
    
    conn.close()
    
    print("\n" + "=" * 70)
    print("✅ VERIFICACIÓN COMPLETADA")
    print("=" * 70)


if __name__ == "__main__":
    verificar_integridad()
