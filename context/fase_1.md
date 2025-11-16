# Fase 1 – Preparación de Datos para Entrenamiento del Modelo RL (sin LLM)

> Objetivo: terminar esta fase con **un dataset H1 limpio, consistente y documentado**, listo para ser consumido por el entorno de entrenamiento RL (gym + Stable-Baselines3), **sin** todavía meter LLM ni contexto avanzado.

---

## 1. Alcance de la Fase 1

**Incluye:**

- Definir qué datos necesitamos (símbolos, fechas, timeframe, campos).
- Diseñar el modelo de datos (tablas/archivos, formatos, particiones).
- Implementar la ingesta de datos históricos desde la fuente (MT5/proveedor).
- Limpiar, resamplear y enriquecer con indicadores básicos en H1.
- Definir el vector de estado que usará el futuro `Env` de gym.
- Generar splits de entrenamiento/validación/test.
- Documentar todo (diccionario de datos + guía de uso).

**No incluye (se hará en fases posteriores):**

- Integración con LLM (contexto diario, sentimiento, etc.).
- Entrenamiento de modelos RL (PPO, DQN, etc.).
- Implementación del `gym.Env`.
- Integración con MT5 en tiempo real.
- Capa de riesgo avanzada.

---

## 2. Entregables de la Fase 1

Propongo dividir esta fase en **4 entregables**:

1. **E1 – Especificación de datos y modelo de almacenamiento**
2. **E2 – Pipeline de ingesta de datos brutos (raw)**
3. **E3 – Pipeline de limpieza, resampleo H1 e indicadores**
4. **E4 – Dataset final para RL + validación y documentación**

Cada entregable se puede tratar como una “sub-fase” que se puede cerrar con criterios claros.

---

## 3. Detalle de Entregables y Tareas

### 3.1. Entregable 1 – Especificación de datos y modelo de almacenamiento

**Objetivo:**  
Tener definido y acordado **qué datos**, **de dónde**, **en qué formato** y **cómo se almacenan**, antes de escribir código serio.

**Criterios de aceptación:**

- Documento de especificación de datos aprobado (puede ser otro .md).
- Lista de símbolos, timeframe(s) y periodo histórico definidos.
- Campos mínimos definidos (OHLCV, spread, volumen, etc.).
- Decisión sobre formato de almacenamiento (Parquet/CSV) y particionado.
- Decisión de timezone y convenciones (ej. todo en UTC o TZ del broker).

**Tareas:**

| ID   | Tarea                                                                 | Descripción                                                                                                      | Dependencias      | Entregable |
|------|-----------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|-------------------|-----------|
| T1.1 | Definir símbolos y timeframe objetivo                                 | Lista de pares (e.g. EURUSD, GBPUSD…) y TF de entrenamiento (H1)                                               | Sin dependencias  | E1        |
| T1.2 | Definir periodo histórico y timezone                                  | Fechas de inicio/fin (ej. 2012–01–01 a hoy) y TZ estándar (ej. UTC o servidor broker)                           | Sin dependencias  | E1        |
| T1.3 | Definir campos mínimos requeridos                                     | OHLC, volumen, spread, tick_volume, etc.                                                                        | T1.1, T1.2        | E1        |
| T1.4 | Definir formato de almacenamiento y estructura de carpetas            | Decidir Parquet/CSV, particionado por `symbol/date`, estructura `/raw`, `/curated`, `/rl_ready`                | T1.3              | E1        |
| T1.5 | Redactar especificación de datos (documento)                          | Documento .md con todas las definiciones anteriores                                                             | T1.3, T1.4        | E1        |

---

### 3.2. Entregable 2 – Pipeline de ingesta de datos brutos (raw)

**Objetivo:**  
Contar con scripts reproducibles que descarguen / importen datos históricos, los normalicen mínimamente y los almacenen en `/raw` siguiendo la especificación.

**Criterios de aceptación:**

- Script(s) que se puedan ejecutar desde cero para regenerar `/raw`.
- Datos brutos normalizados de todos los símbolos y periodo definidos.
- Estructura de carpetas consistente con E1.

**Tareas:**

| ID   | Tarea                                                                 | Descripción                                                                                                   | Dependencias      | Entregable |
|------|-----------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|-------------------|-----------|
| T2.1 | Implementar exportación/descarga de histórico                         | Script Python que extrae datos de MT5/proveedor en el TF nativo                                              | T1.1, T1.2        | E2        |
| T2.2 | Normalizar nombres de columnas y tipos básicos                        | Homogeneizar nombres (`time`, `open`, `high`, `low`, `close`, `volume`, etc.) y tipos (float, datetime)      | T2.1, T1.3        | E2        |
| T2.3 | Unificar timezone                                                     | Convertir timestamps a TZ estándar definida en E1                                                             | T2.2, T1.2        | E2        |
| T2.4 | Guardar datos brutos en `/raw` con particionado definido              | Guardar en formato elegido (Parquet/CSV), particionando por símbolo/fecha                                   | T2.3, T1.4        | E2        |
| T2.5 | Pequeño script de verificación rápida de integridad                   | Chequear que no haya archivos vacíos, columnas faltantes, etc.                                              | T2.4              | E2        |

> Nota: T2.1 y T2.5 se pueden iterar en paralelo con ajustes menores mientras se estabiliza T2.2–T2.4.

---

### 3.3. Entregable 3 – Limpieza, resampleo H1 e indicadores

**Objetivo:**  
Transformar `/raw` en un dataset “curado” en H1 con indicadores básicos listos para RL.

**Criterios de aceptación:**

- Dataset H1 consistente por símbolo en `/curated`.
- Huecos detectados y tratados (según política acordada).
- Indicadores básicos calculados (retornos, ATR, RSI, rangos, spread_pct, etc.).
- Sesiones de mercado etiquetadas (Asia, London, NY o similar).

**Tareas:**

| ID   | Tarea                                                                 | Descripción                                                                                                     | Dependencias      | Entregable |
|------|-----------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------|-------------------|-----------|
| T3.1 | Implementar detección de huecos y datos corruptos                     | Script que detecta gaps de tiempo anormales, NaNs, outliers extremos, etc.                                     | T2.4              | E3        |
| T3.2 | Implementar resampleo a H1 (si los datos no vienen ya en H1)         | Agregar/convertir datos al timeframe H1 con reglas claras (OHLC, volumen, etc.)                                | T2.4              | E3        |
| T3.3 | Definir y aplicar política de tratamiento de huecos                   | Rellenar, marcar, o excluir tramos, según reglas; guardarlo en flags si aplica                                 | T3.1, T3.2        | E3        |
| T3.4 | Calcular indicadores técnicos básicos                                 | ATR14, RSI14, retornos (1h, 4h, 24h), rango, spread_pct, etc.                                                  | T3.2 *(en paralelo con T3.3)* | E3        |
| T3.5 | Etiquetar sesiones y features de calendario                           | Marcar Asia/London/NY, hour_sin/cos, day_of_week_sin/cos                                                        | T3.2 *(en paralelo con T3.4)* | E3        |
| T3.6 | Normalizar tipos y guardar dataset “curado” en `/curated`            | Asegurar tipos consistentes y guardar tabla H1 enriquecida por símbolo                                          | T3.3, T3.4, T3.5  | E3        |

> Notas de paralelismo:
> - T3.4 puede implementarse en paralelo a T3.3 una vez tengas H1 (T3.2).
> - T3.5 también puede ir en paralelo a T3.3 y T3.4 tras T3.2.

---

### 3.4. Entregable 4 – Dataset final para RL + validación y documentación

**Objetivo:**  
Definir el vector de estado para el entono RL, empaquetar los datos en el formato esperado y validar que esté listo para ser usado en entrenamiento.

**Criterios de aceptación:**

- Definición clara del vector de estado: orden, tipos, rangos esperados.
- Dataset `/rl_ready` con columnas estrictamente alineadas a ese estado.
- Splits train/valid/test generados y documentados.
- Diccionario de datos y guía de consumo para el equipo de RL.

**Tareas:**

| ID   | Tarea                                                                 | Descripción                                                                                                     | Dependencias      | Entregable |
|------|-----------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------|-------------------|-----------|
| T4.1 | Diseñar el esquema del vector de estado para RL                       | Definir qué columnas entran al `state`: precios, retornos, indicadores, calendario, flags, etc.                | T3.6              | E4        |
| T4.2 | Implementar mapper de columnas → vector de estado                     | Script que toma `/curated` y genera matrices/vectores listos para el `Env` (ej. numpy/Parquet estructurado)    | T4.1              | E4        |
| T4.3 | Generar splits de train/valid/test por rangos temporales              | Definir reglas (ej. train 2012–2018, valid 2019–2021, test 2022–2024) y etiquetar cada fila                    | T4.2              | E4        |
| T4.4 | Validar distribuciones básicas y detectar outliers fuertes            | Estadísticas descriptivas, histos, percentiles, para asegurar que el dataset es razonable                       | T4.2, T4.3        | E4        |
| T4.5 | Documentar diccionario de datos y guía de uso                        | Especificar para cada feature: significado, unidad, rango típico, tipo, y cómo se mapea al `Env`               | T4.1, T4.4        | E4        |
| T4.6 | Exportar dataset final `/rl_ready`                                    | Guardar versión final aprobada, lista para que el equipo de RL la consuma                                      | T4.3, T4.4        | E4        |

---

## 4. Vista global de dependencias

- **E1** no depende de nada y se puede empezar ya.
- **E2** depende de E1 (porque necesita qué símbolos, periodo, campos, formato).
- **E3** depende de E2 (necesita `/raw` cargado).
- **E4** depende de E3 (necesita `/curated` limpio).

Dentro de cada entregable:

- Tareas marcadas como “sin dependencias” se pueden hacer desde el inicio.
- Tareas con la misma dependencia principal pueden ejecutarse **en paralelo** entre sí.

Esto permite tener, por ejemplo:

- Un dev de **data ingestion** en E2.
- Otro dev de **feature engineering** avanzando E3 en cuanto haya datos de ejemplo.
- Un dev más “cuant” preparando T4.1 (definición de estado) en cuanto haya una versión preliminar de `/curated`.

---

## 5. Historias de usuario (para guiar a los programadores)

### 5.1. Rol: Data Engineer

- **HU-DE-01**  
  *Como* **data engineer**,  
  *quiero* tener scripts reproducibles para descargar y normalizar datos históricos a `/raw`,  
  *para* poder regenerar el dataset cuando cambie el rango de fechas o los símbolos, sin trabajo manual.

- **HU-DE-02**  
  *Como* **data engineer**,  
  *quiero* una definición clara de formato, particionado y timezone,  
  *para* asegurar que todos los datos históricos son consistentes e integrables entre sí.

---

### 5.2. Rol: Quant / Científico de Datos

- **HU-QU-01**  
  *Como* **quant**,  
  *quiero* un dataset H1 “curado” con OHLCV, spread, indicadores básicos y flags de sesión,  
  *para* poder explorar y validar hipótesis de trading sin preocuparme por la calidad de los datos.

- **HU-QU-02**  
  *Como* **quant**,  
  *quiero* disponer de estadísticas básicas y detección de outliers sobre el dataset final,  
  *para* confiar en que los resultados del entrenamiento RL no se deben a datos corruptos.

- **HU-QU-03**  
  *Como* **quant**,  
  *quiero* que los datos estén ya divididos en train/valid/test por periodos temporales,  
  *para* evaluar modelos sin riesgo de mezclar información de futuro en el entrenamiento.

---

### 5.3. Rol: Desarrollador del entorno RL

- **HU-RL-01**  
  *Como* **desarrollador del entorno RL**,  
  *quiero* un vector de estado bien definido (orden de features, tipos, rangos),  
  *para* poder implementar el `gym.Env` sin ambigüedades ni hacks.

- **HU-RL-02**  
  *Como* **desarrollador del entorno RL**,  
  *quiero* que el dataset `/rl_ready` ya venga en un formato eficiente (ej. Parquet/numpy) y alineado con el vector de estado,  
  *para* poder entrenar modelos en Colab sin tener que rehacer la transformación de datos cada vez.

---

### 5.4. Rol: PM / Responsable del sistema de trading

- **HU-PM-01**  
  *Como* **PM del sistema de trading**,  
  *quiero* que el pipeline de datos sea determinista y reproducible,  
  *para* poder comparar versiones de modelos RL sabiendo que todas se entrenan sobre la misma versión de datos.

- **HU-PM-02**  
  *Como* **PM**,  
  *quiero* documentación clara de qué contiene cada entregable (`/raw`, `/curated`, `/rl_ready`),  
  *para* facilitar el onboarding de nuevos desarrolladores y evitar dependencias en conocimiento tácito.

---

## 6. Siguiente paso sugerido

Una vez aprobemos este diseño de Fase 1, el siguiente paso lógico sería:

- Cerrar **E1**: definir símbolos, periodo, campos, formato y TZ,  
- y crear el primer pequeño dataset de prueba `/raw` con unos pocos meses de datos,

para que en paralelo podamos:

- Empezar a implementar la ingesta (E2),
- y que otro dev empiece con el diseño del vector de estado preliminar (parte de T4.1) usando datos de ejemplo.

