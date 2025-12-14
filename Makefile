run-all: install run-etl train-baseline train-modelo-2

install:
	pip install -r environment/requirements.txt

run-etl:
	@echo "🚀 Ejecutando Pipeline de Datos..."
	python src/main.py

train-baseline:
	@echo "📈 Entrenando Baseline..."
	python src/modelo_ia/train_baseline.py

#train-lstm:
#@echo "🧠 Entrenando LSTM..."
#python src/modelo_ia/modelo_2.py
# KMP_DUPLICATE_LIB_OK=True OMP_NUM_THREADS=1 

train-modelo-2:
	@echo "Entrenando Modelo 2"
	python src/modelo_ia/modelo_2.py

clean:

	rm -rf output/output_csv/*
	rm -rf mlruns
	find . -type d -name "__pycache__" -exec rm -rf {} +