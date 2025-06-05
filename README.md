# Sistema Inteligente para el Análisis de Electrocardiogramas (ECG)

Este proyecto consiste en una plataforma web para el análisis automático de electrocardiogramas (ECG) utilizando procesamiento de señales e imágenes. Fue desarrollado como parte de un proyecto de investigacion para apoyar el diagnóstico de enfermedades cardíacas.

## 🛠 Tecnologías usadas
- Python
- OpenCV (`cv2`) para el procesamiento de imágenes de los ECG
- SciPy (`scipy.signal`) para análisis de señales
- Streamlit para la interfaz web
- MongoDB + PyMongo para la base de datos de pacientes e historiales

## ⚙️ Funcionalidades
- Carga de imágenes de ECG (formatos .jpg, .png)
- Procesamiento de la señal e identificación de picos (P, QRS, T)
- Generación automática de reportes con resultados
- Historial médico vinculado al paciente
- Interfaz web interactiva y responsiva
