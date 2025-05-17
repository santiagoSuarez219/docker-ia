#  Implementación de un modelo de IA utilizando transfer learning para clasificar frutas y verduras 

El presente estudio explora la implementación de un modelo de inteligencia artificial basado en aprendizaje por transferencia para clasificar frutas y verduras, utilizando la arquitectura MobileNetV2. Se empleó un conjunto de datos público con 36 clases de frutas y verduras, organizadas en particiones para entrenamiento, validación y prueba, y se aplicaron técnicas de aumentación de datos para mejorar la diversidad y robustez del modelo. El modelo propuesto alcanzó un desempeño sobresaliente, con una precisión, recall y F1-score promedio ponderado de 96% en el conjunto de prueba. La combinación de MobileNetV2 con capas densas personalizadas y estrategias avanzadas de optimización, resultó fundamental para garantizar la estabilidad del modelo y prevenir el sobreajuste. A pesar de su efectividad global, el modelo mostró limitaciones en algunas clases específicas, lo que destaca la necesidad de expandir y diversificar los datos. 

## ¿Como esta estructurado este repositorio?
Este repositorio contiene el código y los datos necesarios para la implementación del modelo de IA y su despliegue. A continuación se detalla la estructura del mismo:

1. **model/**: Contiene todo el codigo relacionado con la creacion del modelo de IA.
   - **model.ipynb**: Notebook de Jupyter que contiene el código para la implementación del modelo de IA, incluyendo la carga de datos, preprocesamiento, entrenamiento y evaluación del modelo.
2. **backend/**: Contiene el código relacionado con la creación de la API con FastAPI.
3. **frontend/**: Contiene el código relacionado con la creación de la interfaz de usuario.

## Modelo
El modelo entrenado y validado en el archivo `model.ipynb` se encuentra en el siguiente enlace: [Modelo](https://drive.google.com/drive/folders/1QngzFDAgejn-WI0Tt02eI6RAv9EPXowh?usp=sharing). 

# Docker
Docker es una plataforma que permite crear, implementar y ejecutar aplicaciones en contenedores. Un contenedor es una unidad estandarizada de software que empaqueta el código y todas sus dependencias para que la aplicación se ejecute rápidamente y de manera confiable en diferentes entornos informáticos. Docker facilita la creación de entornos de desarrollo consistentes y escalables, lo que simplifica el proceso de implementación y mejora la portabilidad de las aplicaciones.

## 🔧 ¿Qué problema resuelve Docker? 
**Explicación con analogía**:
**Problema clásico**: “En mi máquina sí funciona”.
**Analogía:** Docker es como una "maleta" donde empacas tu aplicación con todo lo que necesita para funcionar (sistema operativo, dependencias, etc.).
**Ejemplo**: Cuando despliegas una app con versiones específicas de Python, Node, MySQL, etc., Docker te asegura que siempre funcionará igual.

Diferencia entre:

**Máquinas virtuales**: Pesadas, requieren sistema operativo completo.
**Contenedores**: Ligeros, comparten el kernel del sistema anfitrión.

## Comandos básicos de Docker
👉 Verifica que Docker está instalado:

```bash
docker --version
```
👉 Ejecuta un contenedor:

```bash
docker run hello-world
```
👉 Busca una imagen:

```bash
docker search nginx
```

👉 Descarga y corre una imagen:

```bash
docker run -d -p 8080:80 nginx # 
```

El comando anterior descarga la imagen de nginx y la ejecuta en segundo plano, mapeando el puerto 8080 del host al puerto 80 del contenedor.

👉 Lista contenedores:

```bash
docker ps     # activos
docker ps -a  # todos
```

👉 Detén y elimina:

```bash
docker stop <id>
docker rm <id>
docker rmi <imagen>
```

## Componetes clave de docker

| Componente | Explicación sencilla                       |
| ---------- | ------------------------------------------ |
| Imagen     | "Receta" o blueprint de una app            |
| Contenedor | Instancia en ejecución de una imagen       |
| Dockerfile | Script para construir imágenes             |
| Docker Hub | Repositorio público de imágenes            |
| Volumen    | Carpeta persistente compartida con el host |
| Red        | Para comunicar contenedores entre sí       |


## Dockerizando el backend
Inicialmente, se crea el archivo `Dockerfile` en la carpeta `backend/`, que contiene las instrucciones necesarias para construir la imagen de Docker que ejecutará la API. A continuación se presenta el `Dockerfile` básico para el backend de proyecto:

```dockerfile
 Usa una imagen base de Python
FROM python:3.12-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY requirements.txt . 
COPY MyModel.keras .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código al contenedor
COPY . .

# Expone el puerto 8000 para la API
EXPOSE 8000

# Comando para ejecutar la API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Luego, se construye la imagen de Docker utilizando el siguiente comando:

```bash
docker build -t backend . 
```

Una vez construida la imagen, se puede ejecutar el contenedor utilizando el siguiente comando:

```bash
docker run -d -p 8000:8000 backend
```
Esto ejecutará la API en el puerto 8000 del host, permitiendo acceder a ella a través de `http://localhost:8000/docs`.

## Dockerizando el frontend
De forma similar, se crea el archivo `Dockerfile` en la carpeta `frontend/`, que contiene las instrucciones necesarias para construir la imagen de Docker que ejecutará la interfaz de usuario. A continuación se presenta el `Dockerfile` básico para el frontend de proyecto:

```dockerfile
FROM nginx:alpine

COPY . /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```
Luego, desde la terminal y ubicado en la carpeta `frontend/` se construye la imagen de Docker utilizando el siguiente comando:

```bash
docker build -t frontend . 
```
Una vez construida la imagen, se puede ejecutar el contenedor utilizando el siguiente comando:

```bash
docker run -d -p 80:80 frontend
```

Esto ejecutará la interfaz de usuario en el puerto 80 del host, permitiendo acceder a ella a través de `http://localhost/`.

## Docker Compose
Docker Compose es una herramienta que permite definir y ejecutar aplicaciones Docker de múltiples contenedores. Con Docker Compose, puedes usar un archivo YAML para configurar los servicios de tu aplicación, redes y volúmenes, lo que facilita la gestión de aplicaciones complejas.

### ¿Por qué usar Docker Compose?
- **Simplicidad**: Define todos los servicios en un solo archivo YAML.
- **Facilidad de uso**: Con un solo comando, puedes iniciar o detener todos los servicios.
- **Escalabilidad**: Permite escalar servicios fácilmente.
- **Configuración**: Facilita la configuración de redes y volúmenes compartidos entre contenedores.

### Ejemplo de Docker Compose
A continuación se presenta un ejemplo básico de un archivo `docker-compose.yml` que define los servicios para el backend y el frontend del proyecto:

```yaml
version: '3.3'
services:
  backend:
    build: ./backend
    container_name: backend
    ports:
      - "8000:8000"

  frontend:
    build: ./frontend
    container_name: frontend
    ports:
      - "80:80"
   ```

### Comandos básicos de Docker Compose
- **Construir y ejecutar los servicios en segundo plano**:
```bash
docker-compose up -d --build
```
- **Detener los servicios**:
```bash
docker-compose down
```

