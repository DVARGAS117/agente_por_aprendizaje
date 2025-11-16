"""
Script simplificado para extraer timeframes adicionales (M1, M5, M15)
Requiere que MT5 esté abierto y con una cuenta activa
"""

import MetaTrader5 as mt5
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import time
import os

# ==================== CONFIGURACIÓN ====================
SYMBOL = "EURUSD"
YEARS_TO_EXTRACT = 10
DB_PATH = r"C:\Users\Hector\Desktop\Proyectos\AGENTE_POR_APRENDIZAJE\mt5_data.db"

# Timeframes pendientes de extraer
TIMEFRAMES_TO_EXTRACT = [
    ("1 Minuto (M1)", mt5.TIMEFRAME_M1, "eurusd_m1", 5000),   # Lotes más pequeños por cantidad
    ("5 Minutos (M5)", mt5.TIMEFRAME_M5, "eurusd_m5", 10000),
    ("15 Minutos (M15)", mt5.TIMEFRAME_M15, "eurusd_m15", 10000),
]

# ==================== FUNCIONES ====================

def initialize_mt5():
    """Inicializa MT5"""
    print("🚀 Inicializando MT5...")
    
    if not mt5.initialize():
        error = mt5.last_error()
        print(f"\n❌ Error al inicializar MT5: {error}")
        print("\n💡 SOLUCIONES:")
        print("   1. Asegúrate de que MT5 esté ABIERTO")
        print("   2. Verifica que tengas una cuenta activa/conectada en MT5")
        print("   3. Cierra y vuelve a abrir MT5")
        return False
    
    print(f"✅ MT5 conectado - Versión: {mt5.version()}")
    
    # Verificar cuenta activa
    account_info = mt5.account_info()
    if account_info is None:
        print("⚠️  No hay cuenta conectada, pero continuaremos...")
    else:
        print(f"✅ Cuenta activa: {account_info.login} ({account_info.server})")
    
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
    
    # Índices
    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_datetime ON {table_name}(datetime)")
    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_year ON {table_name}(year)")
    
    conn.commit()


def extract_timeframe(tf_name, tf_constant, table_name, batch_size):
    """Extrae datos de un timeframe"""
    print("\n" + "=" * 70)
    print(f"📥 EXTRAYENDO: {tf_name}")
    print("=" * 70)
    
    # Verificar símbolo
    if not mt5.symbol_select(SYMBOL, True):
        print(f"❌ Error seleccionando símbolo {SYMBOL}")
        return False
    
    print(f"✅ Símbolo {SYMBOL} listo")
    
    # Fechas
    date_to = datetime.now()
    date_from = date_to - timedelta(days=365 * YEARS_TO_EXTRACT)
    
    print(f"📅 Período: {date_from.strftime('%Y-%m-%d')} → {date_to.strftime('%Y-%m-%d')}")
    
    # Base de datos
    conn = sqlite3.connect(DB_PATH)
    create_table(conn, table_name)
    cursor = conn.cursor()
    
    # Verificar datos existentes
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    existing = cursor.fetchone()[0]
    if existing > 0:
        print(f"⚠️  Ya existen {existing:,} registros. Se agregarán solo nuevos datos.")
    
    total_extracted = 0
    total_inserted = 0
    batch_num = 0
    current_date = date_from
    
    print(f"🔄 Procesando en lotes de {batch_size:,} barras...")
    print("-" * 70)
    
    while current_date < date_to:
        batch_num += 1
        
        # Calcular fecha fin del lote
        batch_end = current_date + timedelta(hours=batch_size)
        if batch_end > date_to:
            batch_end = date_to
        
        # Extraer datos
        rates = mt5.copy_rates_range(SYMBOL, tf_constant, current_date, batch_end)
        
        if rates is None or len(rates) == 0:
            # Avanzar si no hay datos
            current_date += timedelta(days=30)
            if current_date >= date_to:
                break
            continue
        
        # Convertir a DataFrame
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        
        # Filtrar rango
        df = df[(df['time'] >= pd.Timestamp(date_from)) & (df['time'] <= pd.Timestamp(date_to))]
        
        if len(df) == 0:
            current_date = batch_end
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
        
        # Insertar
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
        
        total_extracted += len(df)
        total_inserted += inserted
        
        # Actualizar fecha
        last_date = datetime.strptime(df['datetime'].iloc[-1], '%Y-%m-%d %H:%M:%S')
        current_date = last_date + timedelta(seconds=1)
        
        # Mostrar progreso
        if batch_num % 5 == 0 or inserted > 100:
            print(f"Lote {batch_num:4d}: {len(df):7,} barras | "
                  f"{df['datetime'].iloc[0]} → {df['datetime'].iloc[-1]} | "
                  f"Nuevas: {inserted:7,}")
        
        # Commit periódico
        if batch_num % 20 == 0:
            conn.commit()
            print(f"   💾 Guardado intermedio... Total insertadas: {total_inserted:,}")
        
        time.sleep(0.01)
    
    conn.commit()
    conn.close()
    
    print("-" * 70)
    print(f"✅ {tf_name} completado:")
    print(f"   Extraídas: {total_extracted:,}")
    print(f"   Insertadas: {total_inserted:,}")
    print(f"   Duplicados omitidos: {total_extracted - total_inserted:,}")
    
    return True


def main():
    """Función principal"""
    print("=" * 70)
    print("📊 EXTRACCIÓN MULTI-TIMEFRAME PARA EURUSD")
    print("=" * 70)
    
    # Inicializar MT5
    if not initialize_mt5():
        print("\n⏸️  Proceso detenido. Abre MT5 y vuelve a intentar.")
        return
    
    print(f"\n📋 Timeframes a extraer:")
    for tf_name, _, table_name, _ in TIMEFRAMES_TO_EXTRACT:
        print(f"   • {tf_name} → {table_name}")
    
    start_time = time.time()
    
    try:
        # Extraer cada timeframe
        for tf_name, tf_constant, table_name, batch_size in TIMEFRAMES_TO_EXTRACT:
            success = extract_timeframe(tf_name, tf_constant, table_name, batch_size)
            if not success:
                print(f"⚠️  Error en {tf_name}, continuando...")
        
        # Estadísticas finales
        print("\n" + "=" * 70)
        print("📈 ESTADÍSTICAS FINALES")
        print("=" * 70)
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'eurusd_%'")
        tables = cursor.fetchall()
        
        for (table,) in tables:
            cursor.execute(f"SELECT COUNT(*), MIN(datetime), MAX(datetime) FROM {table}")
            count, min_d, max_d = cursor.fetchone()
            tf = table.replace('eurusd_', '').upper()
            print(f"\n{tf}:")
            print(f"  Registros: {count:,}")
            print(f"  Desde: {min_d}")
            print(f"  Hasta: {max_d}")
        
        # Tamaño BD
        db_size = os.path.getsize(DB_PATH) / (1024 * 1024)
        print(f"\n💾 Tamaño BD: {db_size:.2f} MB")
        
        conn.close()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrumpido. Puedes continuar ejecutando nuevamente el script.")
    finally:
        mt5.shutdown()
        elapsed = time.time() - start_time
        print(f"\n⏱️  Tiempo total: {int(elapsed//60)}m {int(elapsed%60)}s")
        print("\n✅ Proceso finalizado")


if __name__ == "__main__":
    main()
