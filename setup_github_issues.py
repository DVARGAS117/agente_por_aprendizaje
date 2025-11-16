#!/usr/bin/env python3
"""
Script para crear labels e issues organizados por lotes en GitHub
"""
import subprocess
import sys

def run_gh_command(command):
    """Ejecuta un comando de GitHub CLI"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def create_labels():
    """Crea todos los labels necesarios"""
    print("🏷️  Creando labels...")
    
    labels = [
        # Labels de Lotes
        ("LOTE-1", "Tareas del Lote 1 - Especificación Inicial", "0E8A16"),
        ("LOTE-2", "Tareas del Lote 2 - Completar Especificación", "1D76DB"),
        ("LOTE-3", "Tareas del Lote 3 - Documentar Especificación", "5319E7"),
        ("LOTE-4", "Tareas del Lote 4 - Pipeline Ingesta Parte 1", "FBCA04"),
        ("LOTE-5", "Tareas del Lote 5 - Pipeline Ingesta Parte 2", "FEF2C0"),
        ("LOTE-6", "Tareas del Lote 6 - Limpieza Inicial", "D93F0B"),
        ("LOTE-7", "Tareas del Lote 7 - Procesamiento Paralelo", "E99695"),
        ("LOTE-8", "Tareas del Lote 8 - Consolidar Dataset Curado", "C2E0C6"),
        ("LOTE-9", "Tareas del Lote 9 - Diseño RL", "006B75"),
        ("LOTE-10", "Tareas del Lote 10 - Implementación RL Parte 1", "BFD4F2"),
        ("LOTE-11", "Tareas del Lote 11 - Implementación RL Parte 2", "D4C5F9"),
        ("LOTE-12", "Tareas del Lote 12 - Documentación y Export Final", "F9D0C4"),
        
        # Labels de Agentes
        ("agente-1", "Asignado a Agente 1", "B60205"),
        ("agente-2", "Asignado a Agente 2", "D93F0B"),
        ("agente-3", "Asignado a Agente 3", "FBCA04"),
        ("agente-4", "Asignado a Agente 4", "0E8A16"),
        
        # Labels de Entregables
        ("E1-especificacion", "Entregable 1: Especificación", "1D76DB"),
        ("E2-ingesta", "Entregable 2: Ingesta de datos", "5319E7"),
        ("E3-limpieza", "Entregable 3: Limpieza e indicadores", "C5DEF5"),
        ("E4-rl", "Entregable 4: Dataset RL final", "BFD4F2"),
        
        # Labels de Tipo
        ("desarrollo", "Tarea de desarrollo", "0075CA"),
        ("documentacion", "Tarea de documentación", "D4C5F9"),
        ("testing", "Tarea de testing/validación", "E99695"),
        ("diseño", "Tarea de diseño/arquitectura", "C2E0C6"),
    ]
    
    for name, description, color in labels:
        cmd = f'gh label create "{name}" --description "{description}" --color "{color}" --force'
        success, output = run_gh_command(cmd)
        if success:
            print(f"  ✓ {name}")
    
    print("✅ Labels creados\n")

def create_issues():
    """Crea todos los issues organizados por lotes"""
    print("📝 Creando issues...")
    
    issues = [
        # LOTE 1
        {
            "title": "[LOTE 1] T1.1 - Definir símbolos y timeframe objetivo",
            "body": """**Entregable:** E1 - Especificación de datos y modelo de almacenamiento

**Agente asignado:** Agente 1

**Descripción:**
Lista de pares (e.g. EURUSD, GBPUSD…) y TF de entrenamiento (H1)

**Dependencias:** Sin dependencias

**Historia de Usuario:**
HU-DE-02: Como data engineer, quiero una definición clara de formato, particionado y timezone, para asegurar que todos los datos históricos son consistentes e integrables entre sí.

**Criterios de Aceptación:**
- [ ] Lista de pares de divisas definida
- [ ] Timeframe objetivo especificado (H1)
- [ ] Documentación inicial creada""",
            "labels": "LOTE-1,agente-1,E1-especificacion"
        },
        {
            "title": "[LOTE 1] T1.2 - Definir periodo histórico y timezone",
            "body": """**Entregable:** E1 - Especificación de datos y modelo de almacenamiento

**Agente asignado:** Agente 2

**Descripción:**
Fechas de inicio/fin (ej. 2012-01-01 a hoy) y TZ estándar (ej. UTC o servidor broker)

**Dependencias:** Sin dependencias

**Historia de Usuario:**
HU-DE-02: Como data engineer, quiero una definición clara de formato, particionado y timezone, para asegurar que todos los datos históricos son consistentes e integrables entre sí.

**Criterios de Aceptación:**
- [ ] Periodo histórico definido (fecha inicio y fin)
- [ ] Timezone estándar especificado
- [ ] Documentación de convenciones temporales""",
            "labels": "LOTE-1,agente-2,E1-especificacion"
        },
        
        # LOTE 2
        {
            "title": "[LOTE 2] T1.3 - Definir campos mínimos requeridos",
            "body": """**Entregable:** E1 - Especificación de datos y modelo de almacenamiento

**Agente asignado:** Agente 1

**Descripción:**
OHLC, volumen, spread, tick_volume, etc.

**Dependencias:** T1.1, T1.2

**Historia de Usuario:**
HU-DE-02: Como data engineer, quiero una definición clara de formato, particionado y timezone, para asegurar que todos los datos históricos son consistentes e integrables entre sí.

**Criterios de Aceptación:**
- [ ] Lista completa de campos OHLC
- [ ] Campos adicionales especificados (spread, volumen, tick_volume)
- [ ] Tipos de datos definidos para cada campo""",
            "labels": "LOTE-2,agente-1,E1-especificacion"
        },
        {
            "title": "[LOTE 2] T1.4 - Definir formato de almacenamiento y estructura de carpetas",
            "body": """**Entregable:** E1 - Especificación de datos y modelo de almacenamiento

**Agente asignado:** Agente 2

**Descripción:**
Decidir Parquet/CSV, particionado por symbol/date, estructura /raw, /curated, /rl_ready

**Dependencias:** T1.3

**Historia de Usuario:**
HU-DE-02: Como data engineer, quiero una definición clara de formato, particionado y timezone, para asegurar que todos los datos históricos son consistentes e integrables entre sí.

**Criterios de Aceptación:**
- [ ] Formato de almacenamiento elegido (Parquet/CSV)
- [ ] Estrategia de particionado definida
- [ ] Estructura de carpetas /raw, /curated, /rl_ready especificada""",
            "labels": "LOTE-2,agente-2,E1-especificacion"
        },
        
        # LOTE 3
        {
            "title": "[LOTE 3] T1.5 - Redactar especificación de datos (documento)",
            "body": """**Entregable:** E1 - Especificación de datos y modelo de almacenamiento

**Agente asignado:** Agente 1

**Descripción:**
Documento .md con todas las definiciones anteriores

**Dependencias:** T1.3, T1.4

**Historia de Usuario:**
HU-PM-02: Como PM, quiero documentación clara de qué contiene cada entregable (/raw, /curated, /rl_ready), para facilitar el onboarding de nuevos desarrolladores y evitar dependencias en conocimiento tácito.

**Criterios de Aceptación:**
- [ ] Documento especificacion_datos.md creado
- [ ] Incluye todos los símbolos, periodos, campos y formatos
- [ ] Revisado y aprobado por el equipo""",
            "labels": "LOTE-3,agente-1,E1-especificacion,documentacion"
        },
        
        # LOTE 4
        {
            "title": "[LOTE 4] T2.1 - Implementar exportación/descarga de histórico",
            "body": """**Entregable:** E2 - Pipeline de ingesta de datos brutos (raw)

**Agente asignado:** Agente 2

**Descripción:**
Script Python que extrae datos de MT5/proveedor en el TF nativo

**Dependencias:** T1.1, T1.2

**Historia de Usuario:**
HU-DE-01: Como data engineer, quiero tener scripts reproducibles para descargar y normalizar datos históricos a /raw, para poder regenerar el dataset cuando cambie el rango de fechas o los símbolos, sin trabajo manual.

**Criterios de Aceptación:**
- [ ] Script de extracción de MT5 implementado
- [ ] Maneja múltiples símbolos
- [ ] Maneja rango de fechas configurable
- [ ] Logs de progreso implementados""",
            "labels": "LOTE-4,agente-2,E2-ingesta,desarrollo"
        },
        {
            "title": "[LOTE 4] T2.2 - Normalizar nombres de columnas y tipos básicos",
            "body": """**Entregable:** E2 - Pipeline de ingesta de datos brutos (raw)

**Agente asignado:** Agente 3

**Descripción:**
Homogeneizar nombres (time, open, high, low, close, volume, etc.) y tipos (float, datetime)

**Dependencias:** T2.1, T1.3

**Historia de Usuario:**
HU-DE-01: Como data engineer, quiero tener scripts reproducibles para descargar y normalizar datos históricos a /raw, para poder regenerar el dataset cuando cambie el rango de fechas o los símbolos, sin trabajo manual.

**Criterios de Aceptación:**
- [ ] Nombres de columnas estandarizados
- [ ] Tipos de datos normalizados
- [ ] Función de normalización reutilizable
- [ ] Tests unitarios básicos""",
            "labels": "LOTE-4,agente-3,E2-ingesta,desarrollo"
        },
        
        # LOTE 5
        {
            "title": "[LOTE 5] T2.3 - Unificar timezone",
            "body": """**Entregable:** E2 - Pipeline de ingesta de datos brutos (raw)

**Agente asignado:** Agente 1

**Descripción:**
Convertir timestamps a TZ estándar definida en E1

**Dependencias:** T2.2, T1.2

**Historia de Usuario:**
HU-DE-02: Como data engineer, quiero una definición clara de formato, particionado y timezone, para asegurar que todos los datos históricos son consistentes e integrables entre sí.

**Criterios de Aceptación:**
- [ ] Conversión de timezone implementada
- [ ] Todos los timestamps en formato estándar
- [ ] Validación de conversión correcta""",
            "labels": "LOTE-5,agente-1,E2-ingesta,desarrollo"
        },
        {
            "title": "[LOTE 5] T2.4 - Guardar datos brutos en /raw con particionado definido",
            "body": """**Entregable:** E2 - Pipeline de ingesta de datos brutos (raw)

**Agente asignado:** Agente 2

**Descripción:**
Guardar en formato elegido (Parquet/CSV), particionando por símbolo/fecha

**Dependencias:** T2.3, T1.4

**Historia de Usuario:**
HU-DE-01: Como data engineer, quiero tener scripts reproducibles para descargar y normalizar datos históricos a /raw, para poder regenerar el dataset cuando cambie el rango de fechas o los símbolos, sin trabajo manual.

**Criterios de Aceptación:**
- [ ] Datos guardados en /raw
- [ ] Particionado implementado correctamente
- [ ] Estructura de carpetas consistente
- [ ] Metadata de particiones documentada""",
            "labels": "LOTE-5,agente-2,E2-ingesta,desarrollo"
        },
        {
            "title": "[LOTE 5] T2.5 - Pequeño script de verificación rápida de integridad",
            "body": """**Entregable:** E2 - Pipeline de ingesta de datos brutos (raw)

**Agente asignado:** Agente 3

**Descripción:**
Chequear que no haya archivos vacíos, columnas faltantes, etc.

**Dependencias:** T2.4

**Historia de Usuario:**
HU-DE-01: Como data engineer, quiero tener scripts reproducibles para descargar y normalizar datos históricos a /raw, para poder regenerar el dataset cuando cambie el rango de fechas o los símbolos, sin trabajo manual.

**Criterios de Aceptación:**
- [ ] Script de verificación implementado
- [ ] Detecta archivos vacíos
- [ ] Valida columnas requeridas
- [ ] Genera reporte de integridad""",
            "labels": "LOTE-5,agente-3,E2-ingesta,testing"
        },
        
        # LOTE 6
        {
            "title": "[LOTE 6] T3.1 - Implementar detección de huecos y datos corruptos",
            "body": """**Entregable:** E3 - Pipeline de limpieza, resampleo H1 e indicadores

**Agente asignado:** Agente 1

**Descripción:**
Script que detecta gaps de tiempo anormales, NaNs, outliers extremos, etc.

**Dependencias:** T2.4

**Historia de Usuario:**
HU-QU-01: Como quant, quiero un dataset H1 curado con OHLCV, spread, indicadores básicos y flags de sesión, para poder explorar y validar hipótesis de trading sin preocuparme por la calidad de los datos.

**Criterios de Aceptación:**
- [ ] Detección de gaps temporales
- [ ] Detección de NaNs
- [ ] Detección de outliers extremos
- [ ] Reporte de anomalías generado""",
            "labels": "LOTE-6,agente-1,E3-limpieza,desarrollo"
        },
        {
            "title": "[LOTE 6] T3.2 - Implementar resampleo a H1",
            "body": """**Entregable:** E3 - Pipeline de limpieza, resampleo H1 e indicadores

**Agente asignado:** Agente 2

**Descripción:**
Agregar/convertir datos al timeframe H1 con reglas claras (OHLC, volumen, etc.)

**Dependencias:** T2.4

**Historia de Usuario:**
HU-QU-01: Como quant, quiero un dataset H1 curado con OHLCV, spread, indicadores básicos y flags de sesión, para poder explorar y validar hipótesis de trading sin preocuparme por la calidad de los datos.

**Criterios de Aceptación:**
- [ ] Algoritmo de resampleo a H1 implementado
- [ ] Reglas OHLC correctamente aplicadas
- [ ] Volumen agregado apropiadamente
- [ ] Tests de validación de resampleo""",
            "labels": "LOTE-6,agente-2,E3-limpieza,desarrollo"
        },
        
        # LOTE 7
        {
            "title": "[LOTE 7] T3.3 - Definir y aplicar política de tratamiento de huecos",
            "body": """**Entregable:** E3 - Pipeline de limpieza, resampleo H1 e indicadores

**Agente asignado:** Agente 1

**Descripción:**
Rellenar, marcar, o excluir tramos, según reglas; guardarlo en flags si aplica

**Dependencias:** T3.1, T3.2

**Historia de Usuario:**
HU-QU-01: Como quant, quiero un dataset H1 curado con OHLCV, spread, indicadores básicos y flags de sesión, para poder explorar y validar hipótesis de trading sin preocuparme por la calidad de los datos.

**Criterios de Aceptación:**
- [ ] Política de huecos documentada
- [ ] Implementación de rellenado/marcado
- [ ] Flags de calidad de datos creados
- [ ] Validación de política aplicada""",
            "labels": "LOTE-7,agente-1,E3-limpieza,desarrollo"
        },
        {
            "title": "[LOTE 7] T3.4 - Calcular indicadores técnicos básicos",
            "body": """**Entregable:** E3 - Pipeline de limpieza, resampleo H1 e indicadores

**Agente asignado:** Agente 2

**Descripción:**
ATR14, RSI14, retornos (1h, 4h, 24h), rango, spread_pct, etc.

**Dependencias:** T3.2

**Historia de Usuario:**
HU-QU-01: Como quant, quiero un dataset H1 curado con OHLCV, spread, indicadores básicos y flags de sesión, para poder explorar y validar hipótesis de trading sin preocuparme por la calidad de los datos.

**Criterios de Aceptación:**
- [ ] ATR14 calculado
- [ ] RSI14 calculado
- [ ] Retornos multi-periodo calculados
- [ ] Spread_pct calculado
- [ ] Librería de indicadores documentada""",
            "labels": "LOTE-7,agente-2,E3-limpieza,desarrollo"
        },
        {
            "title": "[LOTE 7] T3.5 - Etiquetar sesiones y features de calendario",
            "body": """**Entregable:** E3 - Pipeline de limpieza, resampleo H1 e indicadores

**Agente asignado:** Agente 3

**Descripción:**
Marcar Asia/London/NY, hour_sin/cos, day_of_week_sin/cos

**Dependencias:** T3.2

**Historia de Usuario:**
HU-QU-01: Como quant, quiero un dataset H1 curado con OHLCV, spread, indicadores básicos y flags de sesión, para poder explorar y validar hipótesis de trading sin preocuparme por la calidad de los datos.

**Criterios de Aceptación:**
- [ ] Sesiones de mercado etiquetadas (Asia/London/NY)
- [ ] Features cíclicas de hora implementadas
- [ ] Features cíclicas de día de semana
- [ ] Validación de etiquetas correctas""",
            "labels": "LOTE-7,agente-3,E3-limpieza,desarrollo"
        },
        
        # LOTE 8
        {
            "title": "[LOTE 8] T3.6 - Normalizar tipos y guardar dataset curado en /curated",
            "body": """**Entregable:** E3 - Pipeline de limpieza, resampleo H1 e indicadores

**Agente asignado:** Agente 1

**Descripción:**
Asegurar tipos consistentes y guardar tabla H1 enriquecida por símbolo

**Dependencias:** T3.3, T3.4, T3.5

**Historia de Usuario:**
HU-QU-01: Como quant, quiero un dataset H1 curado con OHLCV, spread, indicadores básicos y flags de sesión, para poder explorar y validar hipótesis de trading sin preocuparme por la calidad de los datos.

**Criterios de Aceptación:**
- [ ] Tipos de datos normalizados
- [ ] Dataset guardado en /curated
- [ ] Estructura consistente por símbolo
- [ ] Metadata del dataset documentada""",
            "labels": "LOTE-8,agente-1,E3-limpieza,desarrollo"
        },
        
        # LOTE 9
        {
            "title": "[LOTE 9] T4.1 - Diseñar el esquema del vector de estado para RL",
            "body": """**Entregable:** E4 - Dataset final para RL + validación y documentación

**Agente asignado:** Agente 4

**Descripción:**
Definir qué columnas entran al state: precios, retornos, indicadores, calendario, flags, etc.

**Dependencias:** T3.6

**Historia de Usuario:**
HU-RL-01: Como desarrollador del entorno RL, quiero un vector de estado bien definido (orden de features, tipos, rangos), para poder implementar el gym.Env sin ambigüedades ni hacks.

**Criterios de Aceptación:**
- [ ] Esquema del vector de estado documentado
- [ ] Orden de features definido
- [ ] Tipos y rangos especificados
- [ ] Justificación de features incluidas""",
            "labels": "LOTE-9,agente-4,E4-rl,diseño"
        },
        
        # LOTE 10
        {
            "title": "[LOTE 10] T4.2 - Implementar mapper de columnas → vector de estado",
            "body": """**Entregable:** E4 - Dataset final para RL + validación y documentación

**Agente asignado:** Agente 4

**Descripción:**
Script que toma /curated y genera matrices/vectores listos para el Env (ej. numpy/Parquet estructurado)

**Dependencias:** T4.1

**Historia de Usuario:**
HU-RL-02: Como desarrollador del entorno RL, quiero que el dataset /rl_ready ya venga en un formato eficiente (ej. Parquet/numpy) y alineado con el vector de estado, para poder entrenar modelos en Colab sin tener que rehacer la transformación de datos cada vez.

**Criterios de Aceptación:**
- [ ] Mapper implementado
- [ ] Conversión a formato eficiente (numpy/Parquet)
- [ ] Validación de dimensiones correctas
- [ ] Tests unitarios""",
            "labels": "LOTE-10,agente-4,E4-rl,desarrollo"
        },
        
        # LOTE 11
        {
            "title": "[LOTE 11] T4.3 - Generar splits de train/valid/test por rangos temporales",
            "body": """**Entregable:** E4 - Dataset final para RL + validación y documentación

**Agente asignado:** Agente 1

**Descripción:**
Definir reglas (ej. train 2012–2018, valid 2019–2021, test 2022–2024) y etiquetar cada fila

**Dependencias:** T4.2

**Historia de Usuario:**
HU-QU-03: Como quant, quiero que los datos estén ya divididos en train/valid/test por periodos temporales, para evaluar modelos sin riesgo de mezclar información de futuro en el entrenamiento.

**Criterios de Aceptación:**
- [ ] Rangos temporales definidos
- [ ] Splits implementados correctamente
- [ ] Etiquetas de split asignadas
- [ ] Validación de no-fuga temporal""",
            "labels": "LOTE-11,agente-1,E4-rl,desarrollo"
        },
        {
            "title": "[LOTE 11] T4.4 - Validar distribuciones básicas y detectar outliers fuertes",
            "body": """**Entregable:** E4 - Dataset final para RL + validación y documentación

**Agente asignado:** Agente 2

**Descripción:**
Estadísticas descriptivas, histos, percentiles, para asegurar que el dataset es razonable

**Dependencias:** T4.2, T4.3

**Historia de Usuario:**
HU-QU-02: Como quant, quiero disponer de estadísticas básicas y detección de outliers sobre el dataset final, para confiar en que los resultados del entrenamiento RL no se deben a datos corruptos.

**Criterios de Aceptación:**
- [ ] Estadísticas descriptivas calculadas
- [ ] Histogramas generados
- [ ] Outliers detectados y reportados
- [ ] Reporte de validación completo""",
            "labels": "LOTE-11,agente-2,E4-rl,testing"
        },
        
        # LOTE 12
        {
            "title": "[LOTE 12] T4.5 - Documentar diccionario de datos y guía de uso",
            "body": """**Entregable:** E4 - Dataset final para RL + validación y documentación

**Agente asignado:** Agente 1

**Descripción:**
Especificar para cada feature: significado, unidad, rango típico, tipo, y cómo se mapea al Env

**Dependencias:** T4.1, T4.4

**Historia de Usuario:**
HU-PM-02: Como PM, quiero documentación clara de qué contiene cada entregable (/raw, /curated, /rl_ready), para facilitar el onboarding de nuevos desarrolladores y evitar dependencias en conocimiento tácito.

**Criterios de Aceptación:**
- [ ] Diccionario de datos completo
- [ ] Guía de uso del dataset
- [ ] Ejemplos de código de consumo
- [ ] Documentación revisada""",
            "labels": "LOTE-12,agente-1,E4-rl,documentacion"
        },
        {
            "title": "[LOTE 12] T4.6 - Exportar dataset final /rl_ready",
            "body": """**Entregable:** E4 - Dataset final para RL + validación y documentación

**Agente asignado:** Agente 2

**Descripción:**
Guardar versión final aprobada, lista para que el equipo de RL la consuma

**Dependencias:** T4.3, T4.4

**Historia de Usuario:**
HU-RL-02: Como desarrollador del entorno RL, quiero que el dataset /rl_ready ya venga en un formato eficiente (ej. Parquet/numpy) y alineado con el vector de estado, para poder entrenar modelos en Colab sin tener que rehacer la transformación de datos cada vez.

**Criterios de Aceptación:**
- [ ] Dataset exportado a /rl_ready
- [ ] Formato optimizado para consumo RL
- [ ] Versión etiquetada y documentada
- [ ] Checksums y metadata incluidos""",
            "labels": "LOTE-12,agente-2,E4-rl,desarrollo"
        },
    ]
    
    created_count = 0
    for issue in issues:
        # Crear archivo temporal con el body
        with open('temp_issue_body.txt', 'w', encoding='utf-8') as f:
            f.write(issue['body'])
        
        cmd = f'gh issue create --title "{issue["title"]}" --body-file temp_issue_body.txt --label "{issue["labels"]}"'
        success, output = run_gh_command(cmd)
        
        if success:
            created_count += 1
            print(f"  ✓ {issue['title']}")
        else:
            print(f"  ✗ Error en {issue['title']}: {output}")
    
    # Limpiar archivo temporal
    import os
    if os.path.exists('temp_issue_body.txt'):
        os.remove('temp_issue_body.txt')
    
    print(f"\n✅ {created_count}/{len(issues)} issues creados exitosamente")
    print(f"🔗 Ver issues: https://github.com/DVARGAS117/agente_por_aprendizaje/issues")

def main():
    """Función principal"""
    print("=" * 70)
    print("  CONFIGURACIÓN DE GITHUB ISSUES - FASE 1")
    print("  Agente por Aprendizaje - Sistema de Trading RL")
    print("=" * 70)
    print()
    
    create_labels()
    create_issues()
    
    print("\n" + "=" * 70)
    print("  ✅ PROCESO COMPLETADO")
    print("=" * 70)

if __name__ == "__main__":
    main()
