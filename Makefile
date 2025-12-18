run-all: install run-etl train-baseline train-lstm

install:
	pip install -r environment/requirements.txt

run-etl:
	@echo "🚀 Ejecutando Pipeline de Datos..."
	python src/main.py

train-baseline:
	@echo "📈 Entrenando Baseline..."
	python src/modelo_ia/train_baseline.py

train-lstm:
	@echo "🧠 Entrenando LSTM..."
	# Mantenemos las variables de Mac por seguridad, en Windows se ignoran o no hacen daño
	KMP_DUPLICATE_LIB_OK=True OMP_NUM_THREADS=1 python src/modelo_ia/modelo_1.py

clean:
	rm -rf output/output_csv/*
	rm -rf mlruns
	find . -type d -name "__pycache__" -exec rm -rf {} +