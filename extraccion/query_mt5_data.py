"""
Script para consultar y analizar los datos extraídos de MT5
Ejemplos de consultas útiles para backtesting
"""

import sqlite3
import pandas as pd
from datetime import datetime

# ==================== CONFIGURACIÓN ====================
DB_PATH = r"C:\Users\Hector\Desktop\Proyectos\AGENTE_POR_APRENDIZAJE\mt5_data.db"

# ==================== FUNCIONES DE CONSULTA ====================

def get_data_by_date_range(start_date, end_date):
    """
    Obtiene datos entre dos fechas
    
    Args:
        start_date: Fecha inicial (formato: 'YYYY-MM-DD' o 'YYYY-MM-DD HH:MM:SS')
        end_date: Fecha final (formato: 'YYYY-MM-DD' o 'YYYY-MM-DD HH:MM:SS')
    
    Returns:
        DataFrame con los datos
    """
    conn = sqlite3.connect(DB_PATH)
    
    query = """
        SELECT * FROM eurusd_h1 
        WHERE datetime BETWEEN ? AND ?
        ORDER BY datetime
    """
    
    df = pd.read_sql_query(query, conn, params=(start_date, end_date))
    conn.close()
    
    return df


def get_data_by_year(year):
    """Obtiene todos los datos de un año específico"""
    conn = sqlite3.connect(DB_PATH)
    
    query = """
        SELECT * FROM eurusd_h1 
        WHERE year = ?
        ORDER BY datetime
    """
    
    df = pd.read_sql_query(query, conn, params=(year,))
    conn.close()
    
    return df


def get_recent_data(hours=100):
    """Obtiene las últimas N horas de datos"""
    conn = sqlite3.connect(DB_PATH)
    
    query = f"""
        SELECT * FROM eurusd_h1 
        ORDER BY datetime DESC
        LIMIT ?
    """
    
    df = pd.read_sql_query(query, conn, params=(hours,))
    df = df.sort_values('datetime')  # Ordenar ascendente
    conn.close()
    
    return df


def get_data_by_hour_of_day(hour):
    """
    Obtiene todos los datos de una hora específica del día
    Útil para analizar patrones por hora
    
    Args:
        hour: Hora del día (0-23)
    """
    conn = sqlite3.connect(DB_PATH)
    
    query = """
        SELECT * FROM eurusd_h1 
        WHERE hour = ?
        ORDER BY datetime
    """
    
    df = pd.read_sql_query(query, conn, params=(hour,))
    conn.close()
    
    return df


def get_data_by_day_of_week(day):
    """
    Obtiene datos de un día específico de la semana
    
    Args:
        day: 0=Lunes, 1=Martes, ..., 6=Domingo
    """
    conn = sqlite3.connect(DB_PATH)
    
    query = """
        SELECT * FROM eurusd_h1 
        WHERE day_of_week = ?
        ORDER BY datetime
    """
    
    df = pd.read_sql_query(query, conn, params=(day,))
    conn.close()
    
    return df


def calculate_statistics(df):
    """Calcula estadísticas básicas de un DataFrame"""
    if df.empty:
        print("❌ No hay datos para calcular estadísticas")
        return
    
    print("\n" + "=" * 60)
    print("📊 ESTADÍSTICAS")
    print("=" * 60)
    print(f"Total de barras: {len(df):,}")
    print(f"Fecha inicial: {df['datetime'].iloc[0]}")
    print(f"Fecha final: {df['datetime'].iloc[-1]}")
    print(f"\n💰 Precios:")
    print(f"   Open  - Min: {df['open'].min():.5f} | Max: {df['open'].max():.5f} | Avg: {df['open'].mean():.5f}")
    print(f"   High  - Min: {df['high'].min():.5f} | Max: {df['high'].max():.5f} | Avg: {df['high'].mean():.5f}")
    print(f"   Low   - Min: {df['low'].min():.5f} | Max: {df['low'].max():.5f} | Avg: {df['low'].mean():.5f}")
    print(f"   Close - Min: {df['close'].min():.5f} | Max: {df['close'].max():.5f} | Avg: {df['close'].mean():.5f}")
    print(f"\n📊 Volumen:")
    print(f"   Tick Volume - Min: {df['tick_volume'].min():,} | Max: {df['tick_volume'].max():,} | Avg: {df['tick_volume'].mean():.0f}")
    print(f"   Spread      - Min: {df['spread'].min()} | Max: {df['spread'].max()} | Avg: {df['spread'].mean():.1f}")


def export_to_csv(df, filename):
    """Exporta un DataFrame a CSV"""
    df.to_csv(filename, index=False)
    print(f"✅ Datos exportados a: {filename}")


# ==================== EJEMPLOS DE USO ====================

if __name__ == "__main__":
    print("=" * 60)
    print("🔍 CONSULTAS A LA BASE DE DATOS MT5")
    print("=" * 60)
    
    # Ejemplo 1: Datos del último mes
    print("\n📅 Ejemplo 1: Datos del último mes")
    df_recent = get_recent_data(hours=720)  # 30 días aprox
    calculate_statistics(df_recent)
    
    # Ejemplo 2: Datos de un año específico
    print("\n\n📅 Ejemplo 2: Datos del año 2023")
    df_2023 = get_data_by_year(2023)
    calculate_statistics(df_2023)
    
    # Ejemplo 3: Datos de un rango específico
    print("\n\n📅 Ejemplo 3: Datos entre dos fechas")
    df_range = get_data_by_date_range('2024-01-01', '2024-03-31')
    calculate_statistics(df_range)
    
    # Ejemplo 4: Patrones por hora del día (ej: 14:00 UTC)
    print("\n\n📅 Ejemplo 4: Todos los datos de las 14:00 horas")
    df_14h = get_data_by_hour_of_day(14)
    if not df_14h.empty:
        print(f"Total de barras a las 14:00: {len(df_14h):,}")
        print(f"Precio promedio de cierre a las 14:00: {df_14h['close'].mean():.5f}")
    
    # Ejemplo 5: Datos de los lunes
    print("\n\n📅 Ejemplo 5: Todos los datos de los lunes")
    df_monday = get_data_by_day_of_week(0)
    if not df_monday.empty:
        print(f"Total de barras los lunes: {len(df_monday):,}")
        print(f"Volatilidad promedio (high-low): {(df_monday['high'] - df_monday['low']).mean():.5f}")
    
    # Ejemplo 6: Exportar datos a CSV
    print("\n\n💾 Exportando datos recientes a CSV...")
    export_to_csv(df_recent, "eurusd_recent.csv")
    
    print("\n" + "=" * 60)
    print("✅ Ejemplos completados")
    print("=" * 60)
    print("\nPuedes modificar este script para hacer tus propias consultas")
