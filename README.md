# ✈️ Sistema End-to-End de Mantenimiento Predictivo para Aviación (RUL Prediction)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker)
![TensorFlow/Keras](https://img.shields.io/badge/TensorFlow-FF6F00?style=flat&logo=tensorflow)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=flat&logo=grafana)
![Angular](https://img.shields.io/badge/Angular-DD0031?style=flat&logo=angular)

Proyecto integral del **Trabajo Fin de Máster (TFM) en Big Data e Inteligencia Artificial**, centrado en el desarrollo de un sistema de **mantenimiento predictivo** aplicado a motores de aviación mediante técnicas de Machine Learning y metodologías MLOps.

Este proyecto resuelve un problema crítico en la Industria 4.0: **predecir la Vida Útil Restante (RUL - Remaining Useful Life)** de motores de turbina a partir de datos de sensores, con el fin de anticipar fallos catastróficos, reducir tiempos de inactividad (downtime) y optimizar las ventanas de mantenimiento preventivo. Se ha utilizado el dataset **NASA C-MAPSS**, ampliamente reconocido en el ámbito de *Prognostics & Health Management (PHM)*.

---

## 🏗️ Arquitectura y Stack Tecnológico

El proyecto trasciende el modelado tradicional para ofrecer una arquitectura de despliegue completa (*End-to-End*):

* **Modelado (Data Science):** Redes Neuronales Recurrentes (LSTM + RNN) optimizadas para el procesamiento de series temporales de telemetría.
* **Backend & API:** Inferencia asíncrona servida a través de **FastAPI**.
* **Despliegue (MLOps):** Ciclo de vida automatizado y contenedorizado utilizando **Docker** y Make.
* **Observabilidad:** Monitorización de métricas en tiempo real mediante **Prometheus y Grafana**.
* **Frontend:** Dashboard interactivo construido en **Angular**.

![Arquitectura de Alto Nivel](./docs/arquitectura_alto_nivel.png)

---

## 📊 Resultados del Modelo y Métricas de Negocio

El modelo ha sido entrenado y validado superando los benchmarks estándar para entornos de seguridad crítica industrial:

* **RMSE (Root Mean Square Error):** 15.07
* **R2 Score:** 0.88
* **Impacto Operativo:** Capacidad demostrada para predecir la degradación del motor con alta fiabilidad, evitando el escenario de fallo catastrófico (*Run-to-Failure*) y reduciendo los costes asociados al mantenimiento correctivo no planificado.

---

## 📂 Estructura de Directorios

```text
TFM-Mantenimiento-Predictivo-Motores/
├── docs/
│   ├── README.md
│   ├── Fase1_Anteproyecto.pdf
│   ├── arquitectura_alto_nivel.png
│   └── backlog_fase1.csv
│
├── src/
│   └── README.md
│
├── environment/
│   ├── README.md
│   ├── requirements.txt
│   └── .env.example
│
├── .gitignore
├── LICENSE
├── README.md
└── CONTRIBUTING.md
```

## ⚙️ Instalación y ejecución 

```bash
# 1. Clonar el repositorio
git clone https://github.com/RuiziGTD/TFM-Mantenimiento-Predictivo-Motores.git
cd TFM-Mantenimiento-Predictivo-Motores

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate   # En Linux/macOS
venv\Scripts\activate      # En Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env

# 5. Levantar servicios con Docker si está configurado en el proyecto
docker-compose up --build
```

## 👥 Equipo

Autores: Gabriel Guzmán Puras Ruiz, Alvaro Ruiz Vallejo y Pablo Ruz Muñoz 

Tutor: José Miguel Ruiz Guevara

Institución: IFP - Innovación en Formación Profesional

Año: 2025

## 🔑 Licencia

Este proyecto se distribuye bajo la licencia MIT, permitiendo su libre uso con fines académicos y de investigación.