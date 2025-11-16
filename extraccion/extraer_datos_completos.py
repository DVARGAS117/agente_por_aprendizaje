"""
Script mejorado para extraer TODOS los datos disponibles en MT5
Extrae desde la fecha más antigua disponible hasta hoy
"""

import MetaTrader5 as mt5
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import time
import os

# ==================== CONFIGURACIÓN ====================
SYMBOL = "EURUSD"
DB_PATH = r"C:\Users\Hector\Desktop\Proyectos\AGENTE_POR_APRENDIZAJE\mt5_data.db"

# Timeframes a extraer con tamaños de lote optimizados
TIMEFRAMES_CONFIG = [
    ("1 Minuto (M1)", mt5.TIMEFRAME_M1, "eurusd_m1", 50000, datetime(2010, 1, 1)),
    ("5 Minutos (M5)", mt5.TIMEFRAME_M5, "eurusd_m5", 50000, datetime(2010, 1, 1)),
    ("15 Minutos (M15)", mt5.TIMEFRAME_M15, "eurusd_m15", 50000, datetime(2010, 1, 1)),
]

# ==================== FUNCIONES ====================

def initialize_mt5():
    """Inicializa MT5"""
    if not mt5.initialize():
        print(f"❌ Error: {mt5.last_error()}")
        return False
    
    account_info = mt5.account_info()
    if account_info:
        print(f"✅ MT5 conectado - Cuenta: {account_info.login}")
    return True


def create_table(conn, table_name):
    """Crea tabla para timeframe"""
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            time INTEGER PRIMARY KEY,
            datetime TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            tick_volume INTEGER,
            spread INTEGER,
            real_volume INTEGER,
            year INTEGER,
            month INTEGER,
            day INTEGER,
            hour INTEGER,
            minute INTEGER,
            day_of_week INTEGER
        )
    """)
    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_datetime ON {table_name}(datetime)")
    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_year ON {table_name}(year)")
    conn.commit()


def find_oldest_available_date(symbol, timeframe):
    """Encuentra la fecha más antigua disponible en MT5 para un símbolo/timeframe"""
    print(f"   🔎 Buscando fecha inicial disponible...")
    
    # Probar fechas cada vez más antiguas
    test_years = [2005, 2008, 2010, 2012, 2014, 2015, 2016]
    oldest_found = None
    
    for year in test_years:
        test_date = datetime(year, 1, 1)
        rates = mt5.copy_rates_from(symbol, timeframe, test_date, 10)
        
        if rates is not None and len(rates) > 0:
            first_bar_time = pd.to_datetime(rates[0]['time'], unit='s')
            oldest_found = first_bar_time
            print(f"   ✓ Datos disponibles desde {year}: primera barra {first_bar_time}")
            break
    
    if oldest_found:
        return oldest_found
    else:
        # Si no encontramos nada, usar 3 años atrás como fallback
        return datetime.now() - timedelta(days=365*3)


def extract_all_available_data(tf_name, tf_constant, table_name, batch_size, start_from):
    """Extrae TODOS los datos disponibles desde la fecha más antigua"""
    print("\n" + "=" * 80)
    print(f"📥 EXTRAYENDO: {tf_name}")
    print("=" * 80)
    
    # Verificar símbolo
    if not mt5.symbol_select(SYMBOL, True):
        print(f"❌ Error seleccionando {SYMBOL}")
        return False
    
    # Buscar fecha más antigua
    oldest_date = find_oldest_available_date(SYMBOL, tf_constant)
    date_from = oldest_date
    date_to = datetime.now()
    
    print(f"   📅 Extrayendo desde: {date_from.strftime('%Y-%m-%d')}")
    print(f"   📅 Hasta: {date_to.strftime('%Y-%m-%d')}")
    print(f"   📊 Aproximadamente {(date_to - date_from).days} días de datos")
    
    # Base de datos
    conn = sqlite3.connect(DB_PATH)
    create_table(conn, table_name)
    cursor = conn.cursor()
    
    # Limpiar tabla existente para reextraer desde el inicio
    cursor.execute(f"DELETE FROM {table_name}")
    conn.commit()
    print(f"   🗑️  Tabla limpiada para reextracción completa")
    
    total_inserted = 0
    batch_num = 0
    current_date = date_from
    last_report_time = time.time()
    
    print(f"   🔄 Procesando en lotes de {batch_size:,} barras...\n")
    
    while current_date < date_to:
        batch_num += 1
        
        # Extraer lote grande
        rates = mt5.copy_rates_from(SYMBOL, tf_constant, current_date, batch_size)
        
        if rates is None or len(rates) == 0:
            # Avanzar si no hay datos
            current_date += timedelta(days=60)
            if current_date >= date_to:
                break
            continue
        
        # Convertir a DataFrame
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        
        # Filtrar rango
        df = df[(df['time'] >= pd.Timestamp(date_from)) & (df['time'] <= pd.Timestamp(date_to))]
        
        if len(df) == 0:
            current_date += timedelta(days=60)
            continue
        
        # Agregar columnas
        df['datetime'] = df['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
        df['year'] = df['time'].dt.year
        df['month'] = df['time'].dt.month
        df['day'] = df['time'].dt.day
        df['hour'] = df['time'].dt.hour
        df['minute'] = df['time'].dt.minute
        df['day_of_week'] = df['time'].dt.dayofweek
        df['time'] = (df['time'].astype('int64') // 10**9).astype('int64')
        
        # Insertar en bloque (más rápido)
        inserted = 0
        for _, row in df.iterrows():
            try:
                cursor.execute(f"""
                    INSERT OR IGNORE INTO {table_name}
                    (time, datetime, open, high, low, close, tick_volume, spread, real_volume, 
                     year, month, day, hour, minute, day_of_week)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    int(row['time']), row['datetime'], row['open'], row['high'], row['low'], 
                    row['close'], int(row['tick_volume']), int(row['spread']), int(row['real_volume']),
                    int(row['year']), int(row['month']), int(row['day']), 
                    int(row['hour']), int(row['minute']), int(row['day_of_week'])
                ))
                if cursor.rowcount > 0:
                    inserted += 1
            except:
                continue
        
        total_inserted += inserted
        
        # Actualizar fecha
        last_date = datetime.strptime(df['datetime'].iloc[-1], '%Y-%m-%d %H:%M:%S')
        current_date = last_date + timedelta(seconds=1)
        
        # Reportar progreso cada 5 segundos
        current_time = time.time()
        if current_time - last_report_time > 5:
            print(f"   Lote {batch_num:4d} | Total insertadas: {total_inserted:,} | "
                  f"Fecha actual: {df['datetime'].iloc[-1]}")
            last_report_time = current_time
        
        # Commit periódico
        if batch_num % 10 == 0:
            conn.commit()
        
        # Si obtuvimos menos barras de lo esperado, terminamos
        if len(rates) < batch_size:
            break
    
    conn.commit()
    conn.close()
    
    print(f"\n   ✅ Completado: {total_inserted:,} barras insertadas")
    return True


def main():
    """Función principal"""
    print("=" * 80)
    print("📊 EXTRACCIÓN COMPLETA DE DATOS HISTÓRICOS MT5")
    print("=" * 80)
    
    if not initialize_mt5():
        return
    
    start_time = time.time()
    
    try:
        for tf_name, tf_constant, table_name, batch_size, _ in TIMEFRAMES_CONFIG:
            extract_all_available_data(tf_name, tf_constant, table_name, batch_size, None)
        
        # Estadísticas finales
        print("\n" + "=" * 80)
        print("📈 RESUMEN FINAL")
        print("=" * 80)
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'eurusd_%'")
        tables = cursor.fetchall()
        
        for (table,) in tables:
            cursor.execute(f"SELECT COUNT(*), MIN(datetime), MAX(datetime) FROM {table}")
            count, min_d, max_d = cursor.fetchone()
            
            if count > 0:
                tf = table.replace('eurusd_', '').upper()
                days = (pd.to_datetime(max_d) - pd.to_datetime(min_d)).days
                years = days / 365.25
                
                print(f"\n{tf}:")
                print(f"  Registros: {count:,}")
                print(f"  Desde: {min_d}")
                print(f"  Hasta: {max_d}")
                print(f"  Cobertura: {years:.2f} años ({days} días)")
        
        db_size = os.path.getsize(DB_PATH) / (1024 * 1024)
        print(f"\n💾 Tamaño BD: {db_size:.2f} MB")
        
        conn.close()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrumpido")
    finally:
        mt5.shutdown()
        elapsed = time.time() - start_time
        print(f"\n⏱️  Tiempo total: {int(elapsed//60)}m {int(elapsed%60)}s")


if __name__ == "__main__":
    main()
