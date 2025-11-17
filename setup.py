from setuptools import setup, find_packages

setup(
    name="tfm-mantenimiento-predictivo",
    version="0.1.0",
    description="TFM - Mantenimiento Predictivo de Motores",
    author="Tu Nombre",
    packages=find_packages(),
    install_requires=[
        # Lista de dependencias - puedes leerlas de requirements.txt
        "pandas",
        "numpy", 
        "scikit-learn",
        "matplotlib",
        "python-dotenv",
        "tensorflow",
        # añade otras que uses
    ],
    python_requires=">=3.7",
)