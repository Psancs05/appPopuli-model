# Usa la imagen base de Ubuntu
FROM ubuntu

# Expone el puerto 8080
EXPOSE 8080

# Establece el directorio de trabajo en HOME
WORKDIR /home

# Actualiza e instala dependencias
RUN apt update && \
    apt install -y python3-pip cron git ffmpeg libxext6 libsm6 wget && \
    apt update --fix-missing

# Crea el directorio de la aplicación y la estructura para el modelo
RUN mkdir -p AppPopuli/data/models
WORKDIR /home/AppPopuli

# Copia los archivos necesarios (excluyendo el modelo)
COPY ./requirements.txt .
COPY ./src ./src

# Instala las dependencias de Python
RUN pip install -r requirements.txt

# Descarga el modelo usando wget
# Reemplaza la URL según tus necesidades
RUN wget https://huggingface.co/Jsancs/appPopuli/resolve/main/modelo.h5 -O ./data/models/modelo.h5

# Configura variables de entorno para Flask
ENV FLASK_APP=src/backend.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# Comando para iniciar la aplicación
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
