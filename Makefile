# ==========================================
#  TFM FASE 4 - ORQUESTADOR FINAL
# ==========================================

.PHONY: all help install run-etl train-baseline train-lstm serve-docker run-all stop clean

# --- RUTAS ---
BACKEND_DIR = src
FRONTEND_DIR = frontend
REQ_FILE = environment/requirements.txt

# --- 1. COMANDOS BÁSICOS ---
help:
	@echo "Comandos TFM:"
	@echo "  make install       - Instala dependencias (Python)"
	@echo "  make run-all       - Ejecuta el flujo completo (ETL + Entreno + Docker)"
	@echo "  make stop          - Detiene los contenedores (Mantiene datos)"
	@echo "  make clean         - Limpieza total (Borra datos y contenedores)"

install:
	@echo "📦 Instalando dependencias..."
	pip install -r $(REQ_FILE)

# --- 2. EL FLUJO DE ENTRENAMIENTO (LOCAL) ---
run-etl:
	@echo "🚀 [1/3] Procesando Datos (ETL)..."
	# Configuración de compatibilidad para ejecución local en macOS
	OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES KMP_DUPLICATE_LIB_OK=True OMP_NUM_THREADS=1 python src/main.py

train-baseline:
	@echo "📈 [2/3] Entrenando Baseline (Regresión Lineal)..."
	python src/modelo_ia/train_baseline.py

train-lstm:
	@echo "🧠 [3/3] Entrenando LSTM (Red Neuronal)..."
	KMP_DUPLICATE_LIB_OK=True OMP_NUM_THREADS=1 python src/modelo_ia/modelo_2.py

# --- 3. DESPLIEGUE EN DOCKER ---
serve-docker:
	@echo "🐳 Levantando Arquitectura Completa..."
	docker-compose up -d --build --remove-orphans
	@echo ""
	@echo "✅ SISTEMA ONLINE:"
	@echo "   -> Frontend App:       http://localhost:4200"
	@echo "   -> API Backend:        http://localhost:8000/docs"
	@echo "   -> Prometheus Monitor: http://localhost:9090"
	@echo "   -> Grafana Dashboards: http://localhost:3000"

# --- 4. EJECUCIÓN MAESTRA ---
run-all:
	@echo "==================================================="
	@echo "   ✈️  TFM MANTENIMIENTO PREDICTIVO - FASE 4  ✈️"
	@echo "==================================================="
	
	@# 1. ETL
	@read -p "1️⃣  ¿Ejecutar pipeline de datos (ETL)? (s/n): " etl; \
	if [ "$$etl" = "s" ]; then \
		$(MAKE) run-etl; \
	else \
		echo "⏩ Saltando ETL..."; \
	fi

	@# 2. Baseline
	@read -p "2️⃣  ¿Entrenar modelo Baseline (Regresión)? (s/n): " base; \
	if [ "$$base" = "s" ]; then \
		$(MAKE) train-baseline; \
	else \
		echo "⏩ Saltando Baseline..."; \
	fi

	@# 3. LSTM
	@read -p "3️⃣  ¿Entrenar modelo LSTM? (s/n): " lstm; \
	if [ "$$lstm" = "s" ]; then \
		echo "☕ Iniciando entrenamiento de red neuronal..."; \
		$(MAKE) train-lstm; \
	else \
		echo "⏩ Saltando LSTM (Usando modelo pre-entrenado)..."; \
	fi

	@echo ""
	@echo "🚀 Desplegando infraestructura en Docker..."
	$(MAKE) serve-docker

# --- 5. PARADA SEGURA ---
stop:
	@echo "🛑 Deteniendo servicios..."
	docker-compose down
	@echo "✅ Sistema detenido correctamente."

# --- 6. LIMPIEZA TOTAL ---
clean:
	rm -rf output/output_csv/*
	rm -rf mlruns
	find . -type d -name "__pycache__" -exec rm -rf {} +
	-docker-compose down
	@echo "🧹 Entorno limpiado."