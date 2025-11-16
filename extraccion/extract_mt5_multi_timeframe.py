"""
Script para extraer datos OHLC de MT5 en múltiples timeframes y almacenarlos en SQLite
Extrae datos del par EURUSD de los últimos 10 años en timeframes: 1M, 5M, 15M, 1H
"""

import MetaTrader5 as mt5
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import time
import os

# ==================== CONFIGURACIÓN ====================
# Credenciales de MT5
MT5_LOGIN = 0  # Coloca tu número de cuenta aquí
MT5_PASSWORD = ""  # Coloca tu contraseña aquí
MT5_SERVER = "Pepperstone-Demo"  # o "Pepperstone-Live" según tu cuenta

# Configuración de extracción
SYMBOL = "EURUSD"
YEARS_TO_EXTRACT = 10
BATCH_SIZE = 10000  # Barras por lote

# Path de la base de datos
DB_PATH = r"C:\Users\Hector\Desktop\Proyectos\AGENTE_POR_APRENDIZAJE\mt5_data.db"

# Timeframes a extraer (nombre, constante MT5, nombre tabla)
TIMEFRAMES = [
    ("1 Minuto", mt5.TIMEFRAME_M1, "eurusd_m1"),
    ("5 Minutos", mt5.TIMEFRAME_M5, "eurusd_m5"),
    ("15 Minutos", mt5.TIMEFRAME_M15, "eurusd_m15"),
    ("1 Hora", mt5.TIMEFRAME_H1, "eurusd_h1"),
]

# ==================== FUNCIONES ====================

def initialize_mt5():
    """Inicializa la conexión con MT5"""
    print("=" * 60)
    print("🚀 INICIANDO CONEXIÓN CON MT5")
    print("=" * 60)
    
    if not mt5.initialize():
        print(f"❌ Error: No se pudo inicializar MT5. Error: {mt5.last_error()}")
        return False
    
    print(f"✅ MT5 inicializado correctamente")
    print(f"📊 Versión MT5: {mt5.version()}")
    
    # Login
    if MT5_LOGIN != 0 and MT5_PASSWORD != "":
        print(f"\n🔐 Intentando login con cuenta {MT5_LOGIN}...")
        authorized = mt5.login(MT5_LOGIN, password=MT5_PASSWORD, server=MT5_SERVER)
        if not authorized:
            print(f"❌ Error en login: {mt5.last_error()}")
            mt5.shutdown()
            return False
        print(f"✅ Login exitoso en servidor: {MT5_SERVER}")
    else:
        print("⚠️  Credenciales no configuradas. Usando cuenta activa en MT5.")
    
    return True


def create_table_for_timeframe(conn, table_name):
    """Crea una tabla para un timeframe específico"""
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
            day_of_week INTEGER
        )
    """)
    
    # Crear índices para consultas rápidas
    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_datetime ON {table_name}(datetime)")
    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_year ON {table_name}(year)")
    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_year_month ON {table_name}(year, month)")
    
    conn.commit()


def get_existing_records(conn, table_name):
    """Obtiene información sobre registros existentes"""
    cursor = conn.cursor()
    
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    existing_records = cursor.fetchone()[0]
    
    if existing_records > 0:
        cursor.execute(f"SELECT MIN(datetime), MAX(datetime) FROM {table_name}")
        min_date, max_date = cursor.fetchone()
        return existing_records, min_date, max_date
    
    return 0, None, None


def extract_timeframe_data(timeframe_name, timeframe_mt5, table_name):
    """Extrae datos de un timeframe específico"""
    print("\n" + "=" * 60)
    print(f"📥 EXTRAYENDO {timeframe_name.upper()}")
    print("=" * 60)
    
    # Verificar que el símbolo existe
    symbol_info = mt5.symbol_info(SYMBOL)
    if symbol_info is None:
        print(f"❌ Error: Símbolo {SYMBOL} no encontrado")
        return False
    
    if not symbol_info.visible:
        print(f"⚠️  Símbolo {SYMBOL} no visible. Habilitando...")
        if not mt5.symbol_select(SYMBOL, True):
            print(f"❌ Error al seleccionar símbolo: {mt5.last_error()}")
            return False
    
    # Calcular fechas
    date_to = datetime.now()
    date_from = date_to - timedelta(days=365 * YEARS_TO_EXTRACT)
    
    print(f"📅 Período: {date_from.strftime('%Y-%m-%d')} → {date_to.strftime('%Y-%m-%d')}")
    
    # Conectar a la base de datos
    conn = sqlite3.connect(DB_PATH)
    
    # Crear tabla si no existe
    create_table_for_timeframe(conn, table_name)
    
    # Verificar datos existentes
    existing_count, min_date, max_date = get_existing_records(conn, table_name)
    if existing_count > 0:
        print(f"⚠️  Tabla existente con {existing_count:,} registros ({min_date} → {max_date})")
        print(f"💡 Se agregarán solo registros nuevos")
    
    cursor = conn.cursor()
    
    total_extracted = 0
    total_inserted = 0
    batch_num = 0
    current_date_from = date_from
    
    print(f"🔄 Extrayendo en lotes de {BATCH_SIZE:,} barras...")
    print("-" * 60)
    
    while current_date_from < date_to:
        batch_num += 1
        
        # Calcular fecha final del lote
        batch_date_to = current_date_from + timedelta(hours=BATCH_SIZE)
        if batch_date_to > date_to:
            batch_date_to = date_to
        
        # Extraer lote usando rango de fechas
        rates = mt5.copy_rates_range(SYMBOL, timeframe_mt5, current_date_from, batch_date_to)
        
        if rates is None or len(rates) == 0:
            # Avanzar en el tiempo para buscar datos
            current_date_from += timedelta(days=30)
            if current_date_from >= date_to:
                break
            continue
        
        # Convertir a DataFrame
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        
        # Filtrar solo datos dentro del rango solicitado
        df = df[(df['time'] >= pd.Timestamp(date_from)) & (df['time'] <= pd.Timestamp(date_to))]
        
        if len(df) == 0:
            current_date_from = batch_date_to
            continue
        
        # Agregar columnas adicionales
        df['datetime'] = df['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
        df['year'] = df['time'].dt.year
        df['month'] = df['time'].dt.month
        df['day'] = df['time'].dt.day
        df['hour'] = df['time'].dt.hour
        df['day_of_week'] = df['time'].dt.dayofweek
        
        # Convertir time a timestamp
        df['time'] = df['time'].astype(int) // 10**9
        
        # Insertar en la base de datos
        inserted = 0
        for _, row in df.iterrows():
            try:
                cursor.execute(f"""
                    INSERT OR IGNORE INTO {table_name}
                    (time, datetime, open, high, low, close, tick_volume, spread, real_volume, 
                     year, month, day, hour, day_of_week)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    int(row['time']), row['datetime'], row['open'], row['high'], row['low'], 
                    row['close'], int(row['tick_volume']), int(row['spread']), int(row['real_volume']),
                    int(row['year']), int(row['month']), int(row['day']), int(row['hour']), int(row['day_of_week'])
                ))
                if cursor.rowcount > 0:
                    inserted += 1
            except Exception as e:
                continue
        
        total_extracted += len(df)
        total_inserted += inserted
        
        # Actualizar fecha para el siguiente lote
        last_date = df['datetime'].iloc[-1]
        last_datetime = datetime.strptime(last_date, '%Y-%m-%d %H:%M:%S')
        current_date_from = last_datetime + timedelta(seconds=1)
        
        # Mostrar progreso cada 10 lotes o si hay nuevos datos
        if batch_num % 10 == 0 or inserted > 0:
            print(f"✓ Lote {batch_num:3d}: {len(df):6,} barras | "
                  f"{df['datetime'].iloc[0]} → {df['datetime'].iloc[-1]} | "
                  f"Nuevas: {inserted:6,}")
        
        # Commit periódico
        if batch_num % 50 == 0:
            conn.commit()
        
        # Pequeña pausa
        time.sleep(0.02)
    
    conn.commit()
    conn.close()
    
    print("-" * 60)
    print(f"📊 Resumen {timeframe_name}:")
    print(f"   Extraídas: {total_extracted:,} barras")
    print(f"   Insertadas: {total_inserted:,} barras nuevas")
    print(f"   Duplicados: {total_extracted - total_inserted:,}")
    
    return True


def show_all_statistics():
    """Muestra estadísticas de todas las tablas"""
    print("\n" + "=" * 60)
    print("📈 ESTADÍSTICAS GENERALES")
    print("=" * 60)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Obtener todas las tablas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'eurusd_%'")
    tables = cursor.fetchall()
    
    for (table_name,) in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        total = cursor.fetchone()[0]
        
        if total > 0:
            cursor.execute(f"SELECT MIN(datetime), MAX(datetime) FROM {table_name}")
            min_date, max_date = cursor.fetchone()
            
            # Determinar timeframe por nombre
            tf_name = table_name.replace('eurusd_', '').upper()
            
            print(f"\n📊 {tf_name}:")
            print(f"   Registros: {total:,}")
            print(f"   Desde: {min_date}")
            print(f"   Hasta: {max_date}")
    
    # Tamaño de la base de datos
    db_size = os.path.getsize(DB_PATH) / (1024 * 1024)  # MB
    print(f"\n💾 Tamaño total de la BD: {db_size:.2f} MB")
    
    conn.close()


def shutdown_mt5():
    """Cierra la conexión con MT5"""
    mt5.shutdown()
    print("\n" + "=" * 60)
    print("✅ PROCESO COMPLETADO")
    print("=" * 60)
    print(f"💾 Base de datos: {DB_PATH}")


# ==================== PROGRAMA PRINCIPAL ====================

def main():
    """Función principal"""
    start_time = time.time()
    
    try:
        # 1. Inicializar MT5
        if not initialize_mt5():
            return
        
        print("\n" + "=" * 60)
        print("📋 TIMEFRAMES A EXTRAER:")
        print("=" * 60)
        for tf_name, _, table_name in TIMEFRAMES:
            print(f"   • {tf_name} → tabla: {table_name}")
        
        # 2. Extraer cada timeframe
        for tf_name, tf_mt5, table_name in TIMEFRAMES:
            success = extract_timeframe_data(tf_name, tf_mt5, table_name)
            if not success:
                print(f"⚠️  Error extrayendo {tf_name}, continuando con el siguiente...")
                continue
        
        # 3. Mostrar estadísticas
        show_all_statistics()
        
        # 4. Cerrar MT5
        shutdown_mt5()
        
        # Tiempo total
        elapsed_time = time.time() - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        print(f"\n⏱️  Tiempo total: {minutes}m {seconds}s")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Proceso interrumpido por el usuario")
        print("💡 Puedes ejecutar el script nuevamente para continuar")
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        if mt5.initialize():
            mt5.shutdown()


if __name__ == "__main__":
    main()
