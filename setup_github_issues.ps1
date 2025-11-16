# Script para crear labels y luego issues organizados por lotes

Write-Host "🏷️  Creando labels..." -ForegroundColor Cyan

# Labels de Lotes
gh label create "LOTE-1" --description "Tareas del Lote 1 - Especificación Inicial" --color "0E8A16" --force
gh label create "LOTE-2" --description "Tareas del Lote 2 - Completar Especificación" --color "1D76DB" --force
gh label create "LOTE-3" --description "Tareas del Lote 3 - Documentar Especificación" --color "5319E7" --force
gh label create "LOTE-4" --description "Tareas del Lote 4 - Pipeline Ingesta Parte 1" --color "FBCA04" --force
gh label create "LOTE-5" --description "Tareas del Lote 5 - Pipeline Ingesta Parte 2" --color "FEF2C0" --force
gh label create "LOTE-6" --description "Tareas del Lote 6 - Limpieza Inicial" --color "D93F0B" --force
gh label create "LOTE-7" --description "Tareas del Lote 7 - Procesamiento Paralelo" --color "E99695" --force
gh label create "LOTE-8" --description "Tareas del Lote 8 - Consolidar Dataset Curado" --color "C2E0C6" --force
gh label create "LOTE-9" --description "Tareas del Lote 9 - Diseño RL" --color "006B75" --force
gh label create "LOTE-10" --description "Tareas del Lote 10 - Implementación RL Parte 1" --color "BFD4F2" --force
gh label create "LOTE-11" --description "Tareas del Lote 11 - Implementación RL Parte 2" --color "D4C5F9" --force
gh label create "LOTE-12" --description "Tareas del Lote 12 - Documentación y Export Final" --color "F9D0C4" --force

# Labels de Agentes
gh label create "agente-1" --description "Asignado a Agente 1" --color "B60205" --force
gh label create "agente-2" --description "Asignado a Agente 2" --color "D93F0B" --force
gh label create "agente-3" --description "Asignado a Agente 3" --color "FBCA04" --force
gh label create "agente-4" --description "Asignado a Agente 4" --color "0E8A16" --force

# Labels de Entregables
gh label create "E1-especificacion" --description "Entregable 1: Especificación" --color "1D76DB" --force
gh label create "E2-ingesta" --description "Entregable 2: Ingesta de datos" --color "5319E7" --force
gh label create "E3-limpieza" --description "Entregable 3: Limpieza e indicadores" --color "C5DEF5" --force
gh label create "E4-rl" --description "Entregable 4: Dataset RL final" --color "BFD4F2" --force

# Labels de Tipo
gh label create "desarrollo" --description "Tarea de desarrollo" --color "0075CA" --force
gh label create "documentacion" --description "Tarea de documentación" --color "D4C5F9" --force
gh label create "testing" --description "Tarea de testing/validación" --color "E99695" --force
gh label create "diseño" --description "Tarea de diseño/arquitectura" --color "C2E0C6" --force

Write-Host "✅ Labels creados exitosamente" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Creando issues..." -ForegroundColor Cyan

# LOTE 1 - Especificación Inicial
gh issue create --title "[LOTE 1] T1.1 - Definir símbolos y timeframe objetivo" --body @"
**Entregable:** E1 - Especificación de datos y modelo de almacenamiento

**Agente asignado:** Agente 1

**Descripción:**
Lista de pares (e.g. EURUSD, GBPUSD…) y TF de entrenamiento (H1)

**Dependencias:** Sin dependencias

**Historia de Usuario:**
HU-DE-02: Como data engineer, quiero una definición clara de formato, particionado y timezone, para asegurar que todos los datos históricos son consistentes e integrables entre sí.

**Criterios de Aceptación:**
- [ ] Lista de pares de divisas definida
- [ ] Timeframe objetivo especificado (H1)
- [ ] Documentación inicial creada
"@ --label "LOTE-1,agente-1,E1-especificacion"

gh issue create --title "[LOTE 1] T1.2 - Definir periodo histórico y timezone" --body @"
**Entregable:** E1 - Especificación de datos y modelo de almacenamiento

**Agente asignado:** Agente 2

**Descripción:**
Fechas de inicio/fin (ej. 2012-01-01 a hoy) y TZ estándar (ej. UTC o servidor broker)

**Dependencias:** Sin dependencias

**Historia de Usuario:**
HU-DE-02: Como data engineer, quiero una definición clara de formato, particionado y timezone, para asegurar que todos los datos históricos son consistentes e integrables entre sí.

**Criterios de Aceptación:**
- [ ] Periodo histórico definido (fecha inicio y fin)
- [ ] Timezone estándar especificado
- [ ] Documentación de convenciones temporales
"@ --label "LOTE-1,agente-2,E1-especificacion"

# LOTE 2 - Completar Especificación
gh issue create --title "[LOTE 2] T1.3 - Definir campos mínimos requeridos" --body @"
**Entregable:** E1 - Especificación de datos y modelo de almacenamiento

**Agente asignado:** Agente 1

**Descripción:**
OHLC, volumen, spread, tick_volume, etc.

**Dependencias:** T1.1, T1.2

**Historia de Usuario:**
HU-DE-02: Como data engineer, quiero una definición clara de formato, particionado y timezone, para asegurar que todos los datos históricos son consistentes e integrables entre sí.

**Criterios de Aceptación:**
- [ ] Lista completa de campos OHLC
- [ ] Campos adicionales especificados (spread, volumen, tick_volume)
- [ ] Tipos de datos definidos para cada campo
"@ --label "LOTE-2,agente-1,E1-especificacion"

gh issue create --title "[LOTE 2] T1.4 - Definir formato de almacenamiento y estructura de carpetas" --body @"
**Entregable:** E1 - Especificación de datos y modelo de almacenamiento

**Agente asignado:** Agente 2

**Descripción:**
Decidir Parquet/CSV, particionado por symbol/date, estructura /raw, /curated, /rl_ready

**Dependencias:** T1.3

**Historia de Usuario:**
HU-DE-02: Como data engineer, quiero una definición clara de formato, particionado y timezone, para asegurar que todos los datos históricos son consistentes e integrables entre sí.

**Criterios de Aceptación:**
- [ ] Formato de almacenamiento elegido (Parquet/CSV)
- [ ] Estrategia de particionado definida
- [ ] Estructura de carpetas /raw, /curated, /rl_ready especificada
"@ --label "LOTE-2,agente-2,E1-especificacion"

# LOTE 3 - Documentar Especificación
gh issue create --title "[LOTE 3] T1.5 - Redactar especificación de datos (documento)" --body @"
**Entregable:** E1 - Especificación de datos y modelo de almacenamiento

**Agente asignado:** Agente 1

**Descripción:**
Documento .md con todas las definiciones anteriores

**Dependencias:** T1.3, T1.4

**Historia de Usuario:**
HU-PM-02: Como PM, quiero documentación clara de qué contiene cada entregable (/raw, /curated, /rl_ready), para facilitar el onboarding de nuevos desarrolladores y evitar dependencias en conocimiento tácito.

**Criterios de Aceptación:**
- [ ] Documento especificacion_datos.md creado
- [ ] Incluye todos los símbolos, periodos, campos y formatos
- [ ] Revisado y aprobado por el equipo
"@ --label "LOTE-3,agente-1,E1-especificacion,documentacion"

# LOTE 4 - Pipeline de Ingesta - Parte 1
gh issue create --title "[LOTE 4] T2.1 - Implementar exportación/descarga de histórico" --body @"
**Entregable:** E2 - Pipeline de ingesta de datos brutos (raw)

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
- [ ] Logs de progreso implementados
"@ --label "LOTE-4,agente-2,E2-ingesta,desarrollo"

gh issue create --title "[LOTE 4] T2.2 - Normalizar nombres de columnas y tipos básicos" --body @"
**Entregable:** E2 - Pipeline de ingesta de datos brutos (raw)

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
- [ ] Tests unitarios básicos
"@ --label "LOTE-4,agente-3,E2-ingesta,desarrollo"

# LOTE 5 - Pipeline de Ingesta - Parte 2
gh issue create --title "[LOTE 5] T2.3 - Unificar timezone" --body @"
**Entregable:** E2 - Pipeline de ingesta de datos brutos (raw)

**Agente asignado:** Agente 1

**Descripción:**
Convertir timestamps a TZ estándar definida en E1

**Dependencias:** T2.2, T1.2

**Historia de Usuario:**
HU-DE-02: Como data engineer, quiero una definición clara de formato, particionado y timezone, para asegurar que todos los datos históricos son consistentes e integrables entre sí.

**Criterios de Aceptación:**
- [ ] Conversión de timezone implementada
- [ ] Todos los timestamps en formato estándar
- [ ] Validación de conversión correcta
"@ --label "LOTE-5,agente-1,E2-ingesta,desarrollo"

gh issue create --title "[LOTE 5] T2.4 - Guardar datos brutos en /raw con particionado definido" --body @"
**Entregable:** E2 - Pipeline de ingesta de datos brutos (raw)

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
- [ ] Metadata de particiones documentada
"@ --label "LOTE-5,agente-2,E2-ingesta,desarrollo"

gh issue create --title "[LOTE 5] T2.5 - Pequeño script de verificación rápida de integridad" --body @"
**Entregable:** E2 - Pipeline de ingesta de datos brutos (raw)

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
- [ ] Genera reporte de integridad
"@ --label "LOTE-5,agente-3,E2-ingesta,testing"

# LOTE 6 - Limpieza Inicial
gh issue create --title "[LOTE 6] T3.1 - Implementar detección de huecos y datos corruptos" --body @"
**Entregable:** E3 - Pipeline de limpieza, resampleo H1 e indicadores

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
- [ ] Reporte de anomalías generado
"@ --label "LOTE-6,agente-1,E3-limpieza,desarrollo"

gh issue create --title "[LOTE 6] T3.2 - Implementar resampleo a H1" --body @"
**Entregable:** E3 - Pipeline de limpieza, resampleo H1 e indicadores

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
- [ ] Tests de validación de resampleo
"@ --label "LOTE-6,agente-2,E3-limpieza,desarrollo"

# LOTE 7 - Procesamiento Paralelo
gh issue create --title "[LOTE 7] T3.3 - Definir y aplicar política de tratamiento de huecos" --body @"
**Entregable:** E3 - Pipeline de limpieza, resampleo H1 e indicadores

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
- [ ] Validación de política aplicada
"@ --label "LOTE-7,agente-1,E3-limpieza,desarrollo"

gh issue create --title "[LOTE 7] T3.4 - Calcular indicadores técnicos básicos" --body @"
**Entregable:** E3 - Pipeline de limpieza, resampleo H1 e indicadores

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
- [ ] Librería de indicadores documentada
"@ --label "LOTE-7,agente-2,E3-limpieza,desarrollo"

gh issue create --title "[LOTE 7] T3.5 - Etiquetar sesiones y features de calendario" --body @"
**Entregable:** E3 - Pipeline de limpieza, resampleo H1 e indicadores

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
- [ ] Validación de etiquetas correctas
"@ --label "LOTE-7,agente-3,E3-limpieza,desarrollo"

# LOTE 8 - Consolidar Dataset Curado
gh issue create --title "[LOTE 8] T3.6 - Normalizar tipos y guardar dataset curado en /curated" --body @"
**Entregable:** E3 - Pipeline de limpieza, resampleo H1 e indicadores

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
- [ ] Metadata del dataset documentada
"@ --label "LOTE-8,agente-1,E3-limpieza,desarrollo"

# LOTE 9 - Diseño RL
gh issue create --title "[LOTE 9] T4.1 - Diseñar el esquema del vector de estado para RL" --body @"
**Entregable:** E4 - Dataset final para RL + validación y documentación

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
- [ ] Justificación de features incluidas
"@ --label "LOTE-9,agente-4,E4-rl,diseño"

# LOTE 10 - Implementación RL - Parte 1
gh issue create --title "[LOTE 10] T4.2 - Implementar mapper de columnas → vector de estado" --body @"
**Entregable:** E4 - Dataset final para RL + validación y documentación

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
- [ ] Tests unitarios
"@ --label "LOTE-10,agente-4,E4-rl,desarrollo"

# LOTE 11 - Implementación RL - Parte 2
gh issue create --title "[LOTE 11] T4.3 - Generar splits de train/valid/test por rangos temporales" --body @"
**Entregable:** E4 - Dataset final para RL + validación y documentación

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
- [ ] Validación de no-fuga temporal
"@ --label "LOTE-11,agente-1,E4-rl,desarrollo"

gh issue create --title "[LOTE 11] T4.4 - Validar distribuciones básicas y detectar outliers fuertes" --body @"
**Entregable:** E4 - Dataset final para RL + validación y documentación

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
- [ ] Reporte de validación completo
"@ --label "LOTE-11,agente-2,E4-rl,testing"

# LOTE 12 - Documentación y Export Final
gh issue create --title "[LOTE 12] T4.5 - Documentar diccionario de datos y guía de uso" --body @"
**Entregable:** E4 - Dataset final para RL + validación y documentación

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
- [ ] Documentación revisada
"@ --label "LOTE-12,agente-1,E4-rl,documentacion"

gh issue create --title "[LOTE 12] T4.6 - Exportar dataset final /rl_ready" --body @"
**Entregable:** E4 - Dataset final para RL + validación y documentación

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
- [ ] Checksums y metadata incluidos
"@ --label "LOTE-12,agente-2,E4-rl,desarrollo"

Write-Host ""
Write-Host "✅ Todos los issues han sido creados exitosamente" -ForegroundColor Green
Write-Host "🔗 Ver issues: https://github.com/DVARGAS117/agente_por_aprendizaje/issues" -ForegroundColor Cyan
