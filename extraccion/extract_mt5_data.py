"""
Script para extraer datos OHLC de MT5 y almacenarlos en SQLite
Extrae datos del par EURUSD de los últimos 10 años en timeframe 1H
"""

import MetaTrader5 as mt5
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import time
import os

# ==================== CONFIGURACIÓN ====================
# Credenciales de MT5
MT5_LOGIN = 61409006  # Coloca tu número de cuenta aquí
MT5_PASSWORD = "V3n3zu3l@"  # Coloca tu contraseña aquí
MT5_SERVER = "Pepperstone-Demo"  # o "Pepperstone-Live" según tu cuenta

# Configuración de extracción
SYMBOL = "EURUSD"
TIMEFRAME = mt5.TIMEFRAME_H1  # 1 hora
YEARS_TO_EXTRACT = 10
BATCH_SIZE = 10000  # Barras por lote

# Path de la base de datos
DB_PATH = r"C:\Users\Hector\Desktop\Proyectos\AGENTE_POR_APRENDIZAJE\mt5_data.db"

# ==================== FUNCIONES ====================

def initialize_mt5():
    """Inicializa la conexión con MT5"""
    print("=" * 60)
    print("🚀 INICIANDO CONEXIÓN CON MT5")
    print("=" * 60)
    
    if not mt5.initialize():
        print(f"❌ Error: No se pudo inicializar MT5. Error: {mt5.last_error()}")
        print("\n💡 SOLUCIONES:")
        print("   1. Asegúrate de que MT5 esté ABIERTO")
        print("   2. Cierra completamente MT5 y vuélvelo a abrir")
        print("   3. Verifica que haya una cuenta conectada en MT5")
        return False
    
    print(f"✅ MT5 inicializado correctamente")
    print(f"📊 Versión MT5: {mt5.version()}")
    
    # Verificar si ya hay una cuenta activa
    account_info = mt5.account_info()
    if account_info is not None:
        print(f"✅ Cuenta ya conectada: {account_info.login} en {account_info.server}")
        print(f"💡 Usando cuenta activa (sin hacer login adicional)")
        return True
    
    # Si no hay cuenta activa, intentar login solo si hay credenciales
    if MT5_LOGIN != 0 and MT5_PASSWORD != "":
        print(f"\n🔐 Intentando login con cuenta {MT5_LOGIN}...")
        authorized = mt5.login(MT5_LOGIN, password=MT5_PASSWORD, server=MT5_SERVER)
        if not authorized:
            print(f"⚠️  Error en login: {mt5.last_error()}")
            print(f"💡 Continuaremos sin login. Asegúrate de conectar manualmente en MT5.")
            # No cerramos, continuamos sin login
        else:
            print(f"✅ Login exitoso en servidor: {MT5_SERVER}")
    else:
        print("⚠️  No hay credenciales. Asegúrate de tener una cuenta conectada en MT5.")
    
    return True


def create_database():
    """Crea la base de datos y tabla si no existen"""
    print("\n" + "=" * 60)
    print("💾 CONFIGURANDO BASE DE DATOS")
    print("=" * 60)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS eurusd_h1 (
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
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_datetime ON eurusd_h1(datetime)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_year ON eurusd_h1(year)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_year_month ON eurusd_h1(year, month)")
    
    conn.commit()
    
    # Verificar si ya hay datos
    cursor.execute("SELECT COUNT(*) FROM eurusd_h1")
    existing_records = cursor.fetchone()[0]
    
    if existing_records > 0:
        cursor.execute("SELECT MIN(datetime), MAX(datetime) FROM eurusd_h1")
        min_date, max_date = cursor.fetchone()
        print(f"📊 Registros existentes: {existing_records:,}")
        print(f"📅 Rango de fechas: {min_date} a {max_date}")
    else:
        print(f"📊 Base de datos vacía. Se crearán nuevos registros.")
    
    conn.close()
    print(f"✅ Base de datos lista: {DB_PATH}")
    return existing_records


def extract_data_in_batches():
    """Extrae datos de MT5 en lotes y los guarda en SQLite"""
    print("\n" + "=" * 60)
    print(f"📥 EXTRAYENDO DATOS DE {SYMBOL}")
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
    
    print(f"✅ Símbolo {SYMBOL} verificado")
    print(f"📊 Spread actual: {symbol_info.spread} puntos")
    
    # Calcular fechas
    date_to = datetime.now()
    date_from = date_to - timedelta(days=365 * YEARS_TO_EXTRACT)
    
    print(f"\n📅 Período de extracción:")
    print(f"   Desde: {date_from.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Hasta: {date_to.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Timeframe: 1 Hora (H1)")
    
    # Conectar a la base de datos
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    total_extracted = 0
    total_inserted = 0
    batch_num = 0
    current_date_from = date_from
    
    print(f"\n🔄 Iniciando extracción en lotes de {BATCH_SIZE:,} barras...")
    print("-" * 60)
    
    while current_date_from < date_to:
        batch_num += 1
        
        # Calcular fecha final del lote
        # Aproximadamente BATCH_SIZE horas hacia adelante, pero no más allá de date_to
        batch_date_to = current_date_from + timedelta(hours=BATCH_SIZE)
        if batch_date_to > date_to:
            batch_date_to = date_to
        
        # Extraer lote usando rango de fechas
        rates = mt5.copy_rates_range(SYMBOL, TIMEFRAME, current_date_from, batch_date_to)
        
        if rates is None or len(rates) == 0:
            print(f"⚠️  Lote {batch_num}: No hay datos disponibles entre {current_date_from} y {batch_date_to}")
            # Avanzar 30 días para buscar datos más adelante
            current_date_from += timedelta(days=30)
            continue
        
        # Convertir a DataFrame
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        
        # Filtrar solo datos dentro del rango solicitado (por seguridad)
        df = df[(df['time'] >= pd.Timestamp(date_from)) & (df['time'] <= pd.Timestamp(date_to))]
        
        if len(df) == 0:
            current_date_from = batch_date_to
            continue
        
        # Agregar columnas adicionales para análisis
        df['datetime'] = df['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
        df['year'] = df['time'].dt.year
        df['month'] = df['time'].dt.month
        df['day'] = df['time'].dt.day
        df['hour'] = df['time'].dt.hour
        df['day_of_week'] = df['time'].dt.dayofweek  # 0=Lunes, 6=Domingo
        
        # Convertir time a timestamp para usar como PRIMARY KEY
        df['time'] = (df['time'].astype('int64') // 10**9).astype('int64')
        
        # Insertar en la base de datos usando INSERT OR IGNORE para manejar duplicados
        inserted = 0
        for _, row in df.iterrows():
            try:
                cursor.execute("""
                    INSERT OR IGNORE INTO eurusd_h1 
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
                print(f"⚠️  Error insertando registro: {e}")
                continue
        
        total_extracted += len(df)
        total_inserted += inserted
        
        # Actualizar fecha para el siguiente lote
        last_date = df['datetime'].iloc[-1]
        last_datetime = datetime.strptime(last_date, '%Y-%m-%d %H:%M:%S')
        current_date_from = last_datetime + timedelta(hours=1)
        
        # Mostrar progreso
        print(f"✓ Lote {batch_num:3d}: {len(df):5,} barras | "
              f"Desde {df['datetime'].iloc[0]} | "
              f"Hasta {df['datetime'].iloc[-1]} | "
              f"Nuevas: {inserted:5,} | Duplicados: {len(df)-inserted:5,}")
        
        # Commit periódico
        if batch_num % 10 == 0:
            conn.commit()
        
        # Si recibimos menos barras de las esperadas, podríamos estar cerca del final
        if len(rates) < BATCH_SIZE / 2:
            # Intentar avanzar pero con cautela
            if current_date_from >= date_to:
                print(f"\n✅ Fecha final alcanzada")
                break
        
        # Pequeña pausa para no sobrecargar
        time.sleep(0.05)
    
    conn.commit()
    conn.close()
    
    print("-" * 60)
    print(f"\n📊 RESUMEN DE EXTRACCIÓN:")
    print(f"   Total de barras extraídas: {total_extracted:,}")
    print(f"   Total de barras insertadas: {total_inserted:,}")
    print(f"   Duplicados omitidos: {total_extracted - total_inserted:,}")
    
    return True


def show_database_stats():
    """Muestra estadísticas de la base de datos"""
    print("\n" + "=" * 60)
    print("📈 ESTADÍSTICAS DE LA BASE DE DATOS")
    print("=" * 60)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Total de registros
    cursor.execute("SELECT COUNT(*) FROM eurusd_h1")
    total = cursor.fetchone()[0]
    print(f"📊 Total de registros: {total:,}")
    
    # Rango de fechas
    cursor.execute("SELECT MIN(datetime), MAX(datetime) FROM eurusd_h1")
    min_date, max_date = cursor.fetchone()
    print(f"📅 Primer registro: {min_date}")
    print(f"📅 Último registro: {max_date}")
    
    # Estadísticas por año
    cursor.execute("""
        SELECT year, COUNT(*) as records, 
               MIN(datetime) as first_date, 
               MAX(datetime) as last_date
        FROM eurusd_h1 
        GROUP BY year 
        ORDER BY year
    """)
    
    print(f"\n📊 Registros por año:")
    print("-" * 60)
    for row in cursor.fetchall():
        year, records, first_date, last_date = row
        print(f"   {year}: {records:6,} registros | {first_date} a {last_date}")
    
    # Precios
    cursor.execute("""
        SELECT 
            MIN(low) as min_price,
            MAX(high) as max_price,
            AVG(close) as avg_price
        FROM eurusd_h1
    """)
    min_price, max_price, avg_price = cursor.fetchone()
    print(f"\n💰 Estadísticas de precio:")
    print(f"   Precio mínimo: {min_price:.5f}")
    print(f"   Precio máximo: {max_price:.5f}")
    print(f"   Precio promedio: {avg_price:.5f}")
    
    # Tamaño de la base de datos
    db_size = os.path.getsize(DB_PATH) / (1024 * 1024)  # MB
    print(f"\n💾 Tamaño de la BD: {db_size:.2f} MB")
    
    conn.close()


def shutdown_mt5():
    """Cierra la conexión con MT5"""
    mt5.shutdown()
    print("\n" + "=" * 60)
    print("✅ PROCESO COMPLETADO")
    print("=" * 60)
    print(f"💾 Base de datos guardada en: {DB_PATH}")
    print(f"📊 Ya puedes usar los datos para backtesting y análisis")


# ==================== PROGRAMA PRINCIPAL ====================

def main():
    """Función principal"""
    start_time = time.time()
    
    try:
        # 1. Inicializar MT5
        if not initialize_mt5():
            return
        
        # 2. Crear/verificar base de datos
        create_database()
        
        # 3. Extraer datos
        if not extract_data_in_batches():
            print("❌ Error durante la extracción de datos")
            return
        
        # 4. Mostrar estadísticas
        show_database_stats()
        
        # 5. Cerrar MT5
        shutdown_mt5()
        
        # Tiempo total
        elapsed_time = time.time() - start_time
        print(f"\n⏱️  Tiempo total de ejecución: {elapsed_time:.2f} segundos")
        
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        if mt5.initialize():
            mt5.shutdown()


if __name__ == "__main__":
    main()
