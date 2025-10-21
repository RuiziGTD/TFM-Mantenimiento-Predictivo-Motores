# Guía de Contribución

Gracias por tu interés en contribuir al proyecto **TFM - Mantenimiento Predictivo de Motores de Aviación**.  
Este documento describe las normas básicas para colaborar y mantener un flujo de trabajo ordenado.

---

## 🧩 Flujo de trabajo con Git

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/<usuario>/TFM-Mantenimiento-Predictivo-Motores.git
   cd TFM-Mantenimiento-Predictivo-Motores
   ```
2. **Crear una rama para cada cambio o funcionalidad a añadir**
   ```bash
   git checkout -b feature/feature-name
   ```
3. **Realizar commits claros y congruentes**
   ```bash
   git commit -m "feat: add data ingestion pipeline"
   ```
4. **Si el cambio realiza cambios en la estructura del proyecto, realizar tambien cambios en los README.md necesarios**
5. **Subir los cambios a la rama**
   ```bash
   git push origin feature/modelo-predictivo
   ```

---

## ✍️ Formato commit

El formato utilizado de cara a la realización de los commits será **Conventional Commits**:

| Tipo       | Descripción                             |
| ---------- | --------------------------------------- |
| `feat`     | Nueva funcionalidad                     |
| `fix`      | Corrección de errores                   |
| `docs`     | Cambios en documentación                |
| `style`    | Cambios de formato o estilo             |
| `refactor` | Mejora interna sin cambiar la lógica    |
| `test`     | Tests añadidos o modificados            |
| `chore`    | Mantenimiento o tareas menores          |
| `init`     | Inicialización de proyecto o estructura |

Añadir tambien el número del issue al commit

Ejemplos de commits:

```bash
docs (#12): add architecture diagram and explanation
chore (#1): add requirements.txt and environment setup
feat (#112): implement RUL model training pipeline
fix (#92): correct bug in preprocessing step
```

---

## 🧱 Estructura del proyecto

 - **/docs** → Documentación y diagramas

 - **/src** → Código fuente (ingesta, modelado, API, dashboard...)

 - **/environment** → Configuración de entorno y dependencias

Cada carpeta contiene un README.md que explica el proposito del directorio y de cada fichero interno

---

## 🌐 Requisitos de entorno

Instalar dependencias desde:

```bash
pip install -r environment/requirements.txt
```

Utilizar variables de entorno:

```bash
cp environment/.env.example environment/.env
```

---

## ✅ Definition of Done (DoD)

Un cambio se considera **hecho** cuando:

  1. El código corre sin errores.
  2. Las métricas del modelo se registran en MLflow (si aplica).
  3. Los archivos/documentación están actualizados.
  4. El commit sigue las convenciones.
  5. Las dependencias están probadas.

---

## 👁️ Ética y cumplimiento

Este proyecto **no debe incluir datos personales ni sensibles**.
Todo dataset debe estar anonimizado conforme a las políticas del TFM y la normativa de protección de datos (GDPR).