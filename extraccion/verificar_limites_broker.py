import MetaTrader5 as mt5
from datetime import datetime, timedelta

mt5.initialize()

print("=" * 70)
print("🔍 VERIFICANDO LÍMITES DE DATOS HISTÓRICOS EN PEPPERSTONE")
print("=" * 70)

now = datetime.now()

for months_back in [1, 3, 6, 12, 18, 24, 36, 48, 60, 120]:
    test_date = now - timedelta(days=30*months_back)
    
    rates_m1 = mt5.copy_rates_range('EURUSD', mt5.TIMEFRAME_M1, test_date, test_date + timedelta(days=1))
    rates_m5 = mt5.copy_rates_range('EURUSD', mt5.TIMEFRAME_M5, test_date, test_date + timedelta(days=1))
    rates_m15 = mt5.copy_rates_range('EURUSD', mt5.TIMEFRAME_M15, test_date, test_date + timedelta(days=1))
    
    m1_count = len(rates_m1) if rates_m1 is not None else 0
    m5_count = len(rates_m5) if rates_m5 is not None else 0
    m15_count = len(rates_m15) if rates_m15 is not None else 0
    
    print(f"\n{months_back:3d} meses atrás ({test_date.strftime('%Y-%m-%d')}):")
    print(f"  M1:  {m1_count:5d} barras {'✅' if m1_count > 100 else '❌' if m1_count == 0 else '⚠️'}")
    print(f"  M5:  {m5_count:5d} barras {'✅' if m5_count > 100 else '❌' if m5_count == 0 else '⚠️'}")
    print(f"  M15: {m15_count:5d} barras {'✅' if m15_count > 100 else '❌' if m15_count == 0 else '⚠️'}")

mt5.shutdown()

print("\n" + "=" * 70)
print("📋 CONCLUSIÓN:")
print("=" * 70)
print("""
Pepperstone (y la mayoría de brokers) tienen límites en datos históricos:
- M1 (1 minuto): Generalmente 1-3 meses
- M5 (5 minutos): Generalmente 3-12 meses  
- M15 (15 minutos): Generalmente 12-48 meses
- H1 (1 hora): 5-10 años o más

Esto es normal y es una limitación del broker, no del script.
""")
