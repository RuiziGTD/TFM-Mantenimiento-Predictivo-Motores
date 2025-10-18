# ✈️ TFM - Mantenimiento Predictivo de Motores de Aviación

Proyecto del **Trabajo Fin de Máster en Big Data e Inteligencia Artificial**, centrado en el desarrollo de un sistema de **mantenimiento predictivo** aplicado a motores de aviación mediante técnicas de **Machine Learning** y **Big Data**.

---

## 📘 Descripción general

El objetivo principal es **predecir la vida útil restante (RUL - Remaining Useful Life)** de motores de turbina a partir de datos de sensores, con el fin de **anticipar fallos y optimizar el mantenimiento**.

El proyecto utiliza el dataset **NASA C-MAPSS**, ampliamente reconocido en el ámbito de *prognostics & health management (PHM)*.  

---

## 📂 Estructura de directorios

TFM-Mantenimiento-Predictivo-Motores/
│
├── README.md
├── requirements.txt
├── .env.example
├── backlog.csv
│
├── docs/
│ ├── arquitectura_explicacion.md
│ └── diagramas/
│
├── src/
│ ├── ingest/
│ ├── model/
│ ├── api/
│ └── dashboard/
│
└── environment/

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
```

## 👥 Equipo

Autores: Gabriel Guzmán Puras Ruiz, Alvaro Ruiz Vallejo y Pablo Ruz Muñoz 

Tutor: José Miguel Ruiz Guevara

Institución: IFP - InNovación en Formación Profesional

Año: 2025

## 🔑 Licencia

Este proyecto se distribuye bajo la licencia MIT, permitiendo su libre uso con fines académicos y de investigación.