from setuptools import setup, find_packages

setup(
    name="tfm-mantenimiento-predictivo",
    version="0.1.0",
    description="TFM - Mantenimiento Predictivo de Motores",
    author="Tu Nombre",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy", 
        "scikit-learn",
        "matplotlib",
        "python-dotenv",
        "tensorflow",
        "pyspark",
        "fastapi",
        "uvicorn",
        "python-dotenv",
        "pydantic",
        # JWT y seguridad
        "python-jose",
        "passlib[bcrypt]",
    ],
    python_requires=">=3.7",
)