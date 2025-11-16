# Organización de Tareas por Lotes - Fase 1

## 📋 Resumen Ejecutivo

Este documento describe la organización de las **21 tareas** de la Fase 1 en **12 lotes secuenciales**, optimizada para trabajo paralelo de hasta **4 agentes** simultáneos.

---

## 🎯 Estructura de Lotes

### LOTE 1 - Especificación Inicial (2 agentes en paralelo)
**Puede iniciar:** ✅ Inmediatamente

| Tarea | Agente | Descripción | Issue |
|-------|--------|-------------|-------|
| T1.1 | Agente 1 | Definir símbolos y timeframe objetivo | [Ver Issue](https://github.com/DVARGAS117/agente_por_aprendizaje/issues) |
| T1.2 | Agente 2 | Definir periodo histórico y timezone | [Ver Issue](https://github.com/DVARGAS117/agente_por_aprendizaje/issues) |

**Dependencias:** Ninguna

---

### LOTE 2 - Completar Especificación (2 agentes en paralelo)
**Puede iniciar:** ⏳ Cuando LOTE 1 esté completo

| Tarea | Agente | Descripción | Issue |
|-------|--------|-------------|-------|
| T1.3 | Agente 1 | Definir campos mínimos requeridos | [Ver Issue](https://github.com/DVARGAS117/agente_por_aprendizaje/issues) |
| T1.4 | Agente 2 | Definir formato de almacenamiento y estructura de carpetas | [Ver Issue](https://github.com/DVARGAS117/agente_por_aprendizaje/issues) |

**Dependencias:** T1.1, T1.2 (LOTE 1)

---

### LOTE 3 - Documentar Especificación (1 agente)
**Puede iniciar:** ⏳ Cuando LOTE 2 esté completo

| Tarea | Agente | Descripción | Issue |
|-------|--------|-------------|-------|
| T1.5 | Agente 1 | Redactar especificación de datos (documento) | [Ver Issue](https://github.com/DVARGAS117/agente_por_aprendizaje/issues) |

**Dependencias:** T1.3, T1.4 (LOTE 2)

---

### LOTE 4 - Pipeline de Ingesta - Parte 1 (2 agentes en paralelo)
**Puede iniciar:** ⏳ Cuando LOTE 1 esté completo

| Tarea | Agente | Descripción | Issue |
|-------|--------|-------------|-------|
| T2.1 | Agente 2 | Implementar exportación/descarga de histórico | [Ver Issue](https://github.com/DVARGAS117/agente_por_aprendizaje/issues) |
| T2.2 | Agente 3 | Normalizar nombres de columnas y tipos básicos | [Ver Issue](https://github.com/DVARGAS117/agente_por_aprendizaje/issues) |

**Dependencias:** T1.1, T1.2 (LOTE 1) + T1.3 (LOTE 2)

---

### LOTE 5 - Pipeline de Ingesta - Parte 2 (3 agentes en paralelo)
**Puede iniciar:** ⏳ Cuando LOTE 4 esté completo

| Tarea | Agente | Descripción | Issue |
|-------|--------|-------------|-------|
| T2.3 | Agente 1 | Unificar timezone | [Ver Issue](https://github.com/DVARGAS117/agente_por_aprendizaje/issues) |
| T2.4 | Agente 2 | Guardar datos brutos en /raw con particionado definido | [Ver Issue](https://github.com/DVARGAS117/agente_por_aprendizaje/issues) |
| T2.5 | Agente 3 | Pequeño script de verificación rápida de integridad | [Ver Issue](https://github.com/DVARGAS117/agente_por_aprendizaje/issues) |

**Dependencias:** T2.1, T2.2 (LOTE 4) + T1.2, T1.4 (LOTES anteriores)

---

### LOTE 6 - Limpieza Inicial (2 agentes en paralelo)
**Puede iniciar:** ⏳ Cuando LOTE 5 esté completo

| Tarea | Agente | Descripción | Issue |
|-------|--------|-------------|-------|
| T3.1 | Agente 1 | Implementar detección de huecos y datos corruptos | [Ver Issue](https://github.com/DVARGAS117/agente_por_aprendizaje/issues) |
| T3.2 | Agente 2 | Implementar resampleo a H1 | [Ver Issue](https://github.com/DVARGAS117/agente_por_aprendizaje/issues) |

**Dependencias:** T2.4 (LOTE 5)

---

### LOTE 7 - Procesamiento Paralelo (3 agentes en paralelo)
**Puede iniciar:** ⏳ Cuando LOTE 6 esté completo

| Tarea | Agente | Descripción | Issue |
|-------|--------|-------------|-------|
| T3.3 | Agente 1 | Definir y aplicar política de tratamiento de huecos | [Ver Issue](https://github.com/DVARGAS117/agente_por_aprendizaje/issues) |
| T3.4 | Agente 2 | Calcular indicadores técnicos básicos | [Ver Issue](https://github.com/DVARGAS117/agente_por_aprendizaje/issues) |
| T3.5 | Agente 3 | Etiquetar sesiones y features de calendario | [Ver Issue](https://github.com/DVARGAS117/agente_por_aprendizaje/issues) |

**Dependencias:** T3.1, T3.2 (LOTE 6)

---

### LOTE 8 - Consolidar Dataset Curado (1 agente)
**Puede iniciar:** ⏳ Cuando LOTE 7 esté completo

| Tarea | Agente | Descripción | Issue |
|-------|--------|-------------|-------|
| T3.6 | Agente 1 | Normalizar tipos y guardar dataset curado en /curated | [Ver Issue](https://github.com/DVARGAS117/agente_por_aprendizaje/issues) |

**Dependencias:** T3.3, T3.4, T3.5 (LOTE 7)

---

### LOTE 9 - Diseño RL (1 agente)
**Puede iniciar:** ⏳ Cuando LOTE 8 esté completo

| Tarea | Agente | Descripción | Issue |
|-------|--------|-------------|-------|
| T4.1 | Agente 4 | Diseñar el esquema del vector de estado para RL | [Ver Issue](https://github.com/DVARGAS117/agente_por_aprendizaje/issues) |

**Dependencias:** T3.6 (LOTE 8)

---

### LOTE 10 - Implementación RL - Parte 1 (1 agente)
**Puede iniciar:** ⏳ Cuando LOTE 9 esté completo

| Tarea | Agente | Descripción | Issue |
|-------|--------|-------------|-------|
| T4.2 | Agente 4 | Implementar mapper de columnas → vector de estado | [Ver Issue](https://github.com/DVARGAS117/agente_por_aprendizaje/issues) |

**Dependencias:** T4.1 (LOTE 9)

---

### LOTE 11 - Implementación RL - Parte 2 (2 agentes en paralelo)
**Puede iniciar:** ⏳ Cuando LOTE 10 esté completo

| Tarea | Agente | Descripción | Issue |
|-------|--------|-------------|-------|
| T4.3 | Agente 1 | Generar splits de train/valid/test por rangos temporales | [Ver Issue](https://github.com/DVARGAS117/agente_por_aprendizaje/issues) |
| T4.4 | Agente 2 | Validar distribuciones básicas y detectar outliers fuertes | [Ver Issue](https://github.com/DVARGAS117/agente_por_aprendizaje/issues) |

**Dependencias:** T4.2 (LOTE 10)

---

### LOTE 12 - Documentación y Export Final (2 agentes en paralelo)
**Puede iniciar:** ⏳ Cuando LOTE 11 esté completo

| Tarea | Agente | Descripción | Issue |
|-------|--------|-------------|-------|
| T4.5 | Agente 1 | Documentar diccionario de datos y guía de uso | [Ver Issue](https://github.com/DVARGAS117/agente_por_aprendizaje/issues) |
| T4.6 | Agente 2 | Exportar dataset final /rl_ready | [Ver Issue](https://github.com/DVARGAS117/agente_por_aprendizaje/issues) |

**Dependencias:** T4.1, T4.3, T4.4 (LOTES anteriores)

---

## 📊 Estadísticas de la Organización

- **Total de tareas:** 21
- **Total de lotes:** 12
- **Máximo de agentes en paralelo:** 3 (LOTE 5 y LOTE 7)
- **Cuellos de botella (1 agente):** LOTE 3, LOTE 8, LOTE 9, LOTE 10

### Distribución de carga por agente:

| Agente | Número de tareas asignadas |
|--------|---------------------------|
| Agente 1 | 8 tareas |
| Agente 2 | 8 tareas |
| Agente 3 | 3 tareas |
| Agente 4 | 2 tareas |

---

## 🎨 Sistema de Labels en GitHub

### Labels de Lotes
- `LOTE-1` a `LOTE-12`: Identifican el lote al que pertenece cada tarea

### Labels de Agentes
- `agente-1`, `agente-2`, `agente-3`, `agente-4`: Identifican quién debe trabajar la tarea

### Labels de Entregables
- `E1-especificacion`: Entregable 1
- `E2-ingesta`: Entregable 2
- `E3-limpieza`: Entregable 3
- `E4-rl`: Entregable 4

### Labels de Tipo
- `desarrollo`: Tarea de programación
- `documentacion`: Tarea de documentación
- `testing`: Tarea de validación
- `diseño`: Tarea de arquitectura

---

## 🚀 Cómo usar este sistema

### Para Agentes:

1. **Filtrar por tu agente**: En GitHub Issues, filtra por tu label (ej. `agente-1`)
2. **Ver solo tu lote actual**: Combina filtros (ej. `agente-1` + `LOTE-1`)
3. **Verificar dependencias**: Antes de iniciar, confirma que las dependencias del lote estén cerradas
4. **Actualizar progreso**: Comenta en el issue tu avance
5. **Cerrar al completar**: Marca el issue como completado cuando termines

### Para el Coordinador:

1. **Monitorear por lotes**: Usa el filtro `LOTE-X` para ver el estado de cada lote
2. **Verificar bloqueos**: Si un lote no puede iniciar, revisa las dependencias
3. **Balancear carga**: Si un agente termina antes, puede ayudar a otro
4. **Validar completitud**: Antes de pasar al siguiente lote, valida que todos los criterios de aceptación se cumplan

---

## 📈 Diagrama de Flujo de Lotes

```
INICIO
  ↓
LOTE 1 (2 agentes)  ← Puede iniciar inmediatamente
  ↓
LOTE 2 (2 agentes)  ← Espera LOTE 1
  ↓
LOTE 3 (1 agente)   ← Espera LOTE 2
  ↓
LOTE 4 (2 agentes)  ← Espera LOTE 1 y parte de LOTE 2
  ↓
LOTE 5 (3 agentes)  ← Espera LOTE 4
  ↓
LOTE 6 (2 agentes)  ← Espera LOTE 5
  ↓
LOTE 7 (3 agentes)  ← Espera LOTE 6
  ↓
LOTE 8 (1 agente)   ← Espera LOTE 7
  ↓
LOTE 9 (1 agente)   ← Espera LOTE 8
  ↓
LOTE 10 (1 agente)  ← Espera LOTE 9
  ↓
LOTE 11 (2 agentes) ← Espera LOTE 10
  ↓
LOTE 12 (2 agentes) ← Espera LOTE 11
  ↓
FIN - FASE 1 COMPLETADA ✅
```

---

## 🔗 Enlaces Útiles

- **Repositorio GitHub:** https://github.com/DVARGAS117/agente_por_aprendizaje
- **Issues:** https://github.com/DVARGAS117/agente_por_aprendizaje/issues
- **Documento Fase 1 completo:** [context/fase_1.md](../context/fase_1.md)

---

**Última actualización:** 15 de noviembre de 2025
