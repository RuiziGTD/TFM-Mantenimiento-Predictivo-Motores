# ==========================================
#  TFM FASE 4 - ORQUESTADOR FINAL (DOCKER)
# ==========================================

.PHONY: all help install run-etl train-baseline train-lstm serve-docker run-all stop clean

# --- CONFIGURACIÓN ---
# Usamos el servicio 'trainer' para ejecutar scripts sin bloquear el Mac
DOCKER_RUN = docker-compose run --rm trainer

# --- 1. AYUDA ---
help:
	@echo "Comandos TFM:"
	@echo "  make install       - Construye la imagen Docker (Necesario la primera vez)"
	@echo "  make run-all       - EJECUTA TODO (ETL + Entreno + Web) Automáticamente"
	@echo "  make stop          - Detiene los contenedores (Mantiene datos)"
	@echo "  make clean         - Borra datos y contenedores"

install:
	@echo "🐳 Preparando el entorno blindado (Docker)..."
	docker-compose build trainer

# --- 2. COMANDOS INTERNOS (Corren en Docker automáticamente) ---
run-etl:
	@echo "🚀 [1/3] Procesando Datos (Ejecutando en contenedor seguro)..."
	$(DOCKER_RUN) python src/main.py

train-baseline:
	@echo "📈 [2/3] Entrenando Baseline (Ejecutando en contenedor seguro)..."
	$(DOCKER_RUN) python src/modelo_ia/train_baseline.py

train-lstm:
	@echo "🧠 [3/3] Entrenando LSTM (Ejecutando en contenedor seguro)..."
	$(DOCKER_RUN) python src/modelo_ia/modelo_2.py

# --- 3. DESPLIEGUE ---
serve-docker:
	@echo "🐳 Levantando Arquitectura Completa..."
	# Levantamos todos los servicios en segundo plano
	docker-compose up -d frontend api prometheus grafana
	@echo ""
	@echo "✅ SISTEMA ONLINE:"
	@echo "   -> 🖥️  Frontend App:       http://localhost:4200"
	@echo "   -> 📡 API Backend:        http://localhost:8000/docs"
	@echo "   -> 🔍 Prometheus Monitor: http://localhost:9090"
	@echo "   -> 📊 Grafana Dashboards: http://localhost:3000"

# --- 4. EL COMANDO MAESTRO ---
run-all:
	@echo "==================================================="
	@echo "   ✈️  TFM MANTENIMIENTO - MODO FULL DOCKER   ✈️"
	@echo "==================================================="
	
	@# 1. ETL
	@read -p "1️⃣  ¿Ejecutar pipeline de datos (ETL)? (s/n): " etl; \
	if [ "$$etl" = "s" ]; then \
		$(MAKE) run-etl; \
	else \
		echo "⏩ Saltando ETL..."; \
	fi

	@# 2. Baseline
	@read -p "2️⃣  ¿Entrenar Baseline? (s/n): " base; \
	if [ "$$base" = "s" ]; then \
		$(MAKE) train-baseline; \
	else \
		echo "⏩ Saltando Baseline..."; \
	fi

	@# 3. LSTM
	@read -p "3️⃣  ¿Entrenar LSTM? (s/n): " lstm; \
	if [ "$$lstm" = "s" ]; then \
		echo "☕ Entrenando modelo (Esto evitará bloqueos en tu Mac)..."; \
		$(MAKE) train-lstm; \
	else \
		echo "⏩ Saltando LSTM..."; \
	fi

	@echo ""
	@echo "🚀 Desplegando servicios..."
	$(MAKE) serve-docker

# --- 5. LIMPIEZA ---
stop:
	@echo "🛑 Deteniendo servicios..."
	docker-compose down

clean:
	rm -rf output/output_csv/*
	rm -rf models/*.keras models/*.save
	@echo "🧹 Limpieza completada."