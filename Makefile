# Makefile para TFM Mantenimiento Predictivo

# Variables
# Usamos PYTHONPATH=. para que Python entienda que 'src' es un módulo
PYTHON = PYTHONPATH=. python
PIP = pip

# 1. Instalación de dependencias
# Usar archivo requeriments.txt en entorno Windows
install:
	$(PIP) install -r environment/requirements_docker.txt 
	@echo "Dependencias instaladas."

# 2. Ejecutar Pipeline de Datos (ETL)
pipeline:
	@echo "Ejecutando Pipeline de Datos..."
	$(PYTHON) src/main.py

# 3. Entrenar Modelo Base (Regresión Lineal)
train-baseline:
	@echo "Entrenando Baseline..."
	$(PYTHON) src/modelo_ia/train_baseline.py

# 4. Entrenar Modelo Avanzado (LSTM)
train-lstm:
	@echo "Entrenando LSTM..."
	KMP_DUPLICATE_LIB_OK=True OMP_NUM_THREADS=1 $(PYTHON) src/modelo_ia/modelo_1.py

# 5. COMANDO MAESTRO
run-all: install pipeline train-baseline train-lstm
	@echo "¡Ciclo completo finalizado! Revisa MLflow."

# Limpieza
clean:
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf src/modelo_ia/__pycache__
	rm -rf .pytest_cache