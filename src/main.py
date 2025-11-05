from src.pipeline.pipeline import run_pipeline

open("logs/pipeline.log", "w").close()

if __name__ == "__main__":
    run_pipeline()
