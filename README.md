# Agente por Aprendizaje - Sistema de Trading con RL

Sistema de trading automatizado basado en Aprendizaje por Refuerzo (Reinforcement Learning) para operar en mercados Forex.

## 🎯 Objetivo del Proyecto

Desarrollar un agente de trading que aprenda estrategias óptimas mediante técnicas de RL, utilizando datos históricos de MT5 y entrenándose en un entorno simulado (gym + Stable-Baselines3).

## 📋 Fase Actual: Fase 1 - Preparación de Datos

Actualmente en desarrollo de la **Fase 1**, enfocada en la preparación, limpieza y estructuración de datos históricos para entrenamiento del modelo RL.

### Estado del Proyecto

- ✅ Repositorio creado
- ✅ Issues organizados por lotes (21 tareas en 12 lotes)
- ✅ Sistema de labels configurado
- ⏳ En proceso: LOTE 1 (Especificación Inicial)

## 📂 Estructura del Proyecto

```
agente_por_aprendizaje/
├── context/
│   ├── fase_1.md              # Especificación completa Fase 1
│   ├── organizacion_lotes.md  # Organización de tareas por lotes
│   └── agents.md              # Información sobre agentes
├── extraccion/
│   ├── extract_mt5_data.py    # Script de extracción MT5
│   └── requirements.txt       # Dependencias Python
└── README.md                  # Este archivo
```

## 🏗️ Entregables de la Fase 1

La Fase 1 está dividida en **4 entregables**:

1. **E1 - Especificación de datos y modelo de almacenamiento**
2. **E2 - Pipeline de ingesta de datos brutos (raw)**
3. **E3 - Pipeline de limpieza, resampleo H1 e indicadores**
4. **E4 - Dataset final para RL + validación y documentación**

## 🎨 Sistema de Organización

### Lotes de Trabajo

Las 21 tareas están organizadas en **12 lotes secuenciales** que permiten trabajo paralelo de hasta 3 agentes simultáneamente.

Ver detalles completos en: [context/organizacion_lotes.md](context/organizacion_lotes.md)

### Agentes de Desarrollo

- **Agente 1**: Arquitecto de Datos / Diseño (8 tareas)
- **Agente 2**: Ingeniero de Ingesta / Desarrollo (8 tareas)
- **Agente 3**: Ingeniero de Features (3 tareas)
- **Agente 4**: Ingeniero RL/Validación (2 tareas)

## 📊 Issues en GitHub

Todos los issues están etiquetados con:

- **Lote**: `LOTE-1` a `LOTE-12`
- **Agente**: `agente-1` a `agente-4`
- **Entregable**: `E1-especificacion`, `E2-ingesta`, `E3-limpieza`, `E4-rl`
- **Tipo**: `desarrollo`, `documentacion`, `testing`, `diseño`

🔗 **Ver Issues:** https://github.com/DVARGAS117/agente_por_aprendizaje/issues

## 🚀 Inicio Rápido

### Prerrequisitos

- Python 3.8+
- MetaTrader 5 instalado
- Git

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/DVARGAS117/agente_por_aprendizaje.git
cd agente_por_aprendizaje

# Crear entorno virtual
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependencias
cd extraccion
pip install -r requirements.txt
```

### Configuración

1. Asegúrate de tener MetaTrader 5 instalado y corriendo
2. Configura tu cuenta demo/real en MT5
3. Ajusta los parámetros en los scripts de extracción según necesites

## 📖 Documentación

- [Fase 1 - Especificación Completa](context/fase_1.md)
- [Organización de Lotes](context/organizacion_lotes.md)
- [Información de Agentes](context/agents.md)

## 🤝 Contribución

Este proyecto está organizado por lotes secuenciales. Para contribuir:

1. Revisa los issues abiertos filtrados por tu agente
2. Verifica que el lote anterior esté completo
3. Asigna el issue a ti mismo
4. Desarrolla siguiendo los criterios de aceptación
5. Crea un PR cuando esté listo

## 📝 Roadmap

### Fase 1 (Actual) - Preparación de Datos
- [ ] E1: Especificación de datos
- [ ] E2: Pipeline de ingesta
- [ ] E3: Limpieza e indicadores
- [ ] E4: Dataset final RL

### Fases Futuras
- Fase 2: Desarrollo del entorno gym
- Fase 3: Entrenamiento de modelos RL
- Fase 4: Backtesting y validación
- Fase 5: Integración con MT5 en tiempo real
- Fase 6: Capa de gestión de riesgo

## 👥 Equipo

- **DVARGAS117** - Desarrollador Principal

## 📄 Licencia

[Especificar licencia]

## 📞 Contacto

- GitHub: [@DVARGAS117](https://github.com/DVARGAS117)
- Repositorio: https://github.com/DVARGAS117/agente_por_aprendizaje

---

**Última actualización:** 15 de noviembre de 2025
