from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from pathlib import Path
from PIL import Image
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las solicitudes de origen
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los encabezados
)

MODEL_PATH = "MyModel.keras"

# Cargar el modelo al iniciar el servidor
model = load_model(MODEL_PATH)
print("Modelo cargado exitosamente.")

UPLOAD_FOLDER = Path("uploads") # Define the folder where the files will be uploaded
UPLOAD_FOLDER.mkdir(exist_ok=True) # Create the folder if it doesn't exist

# Preprocesamiento de imágenes
IMG_SIZE = (224, 224)

def preprocess_image(img: Image.Image) -> np.ndarray:
    """
    Preprocesa la imagen para que sea compatible con el modelo.
    - Redimensiona la imagen.
    - Normaliza los valores de los píxeles entre 0 y 1.
    """
    img = img.resize(IMG_SIZE)  # Redimensionar
    img_array = np.array(img) / 255.0  # Normalizar
    if len(img_array.shape) == 2:  # Si es una imagen en blanco y negro
        img_array = np.stack((img_array,) * 3, axis=-1)  # Convertir a RGB
    img_array = np.expand_dims(img_array, axis=0)  # Añadir dimensión batch
    return img_array


LABELS = [
    'Manzana', 'Banano', 'Remolacha', 'Pimentón', 'Col', 'Ají', 'Zanahoria',
    'Coliflor', 'Chile', 'Maíz', 'Pepino', 'Berenjena', 'Ajo', 'Jengibre',
    'Uvas', 'Jalapeño', 'Kiwi', 'Limón', 'Lechuga', 'Mango', 'Cebolla',
    'Naranja', 'Páprika', 'Pera', 'Arvejas', 'Piña', 'Granada', 'Papa',
    'Rábano', 'Soya', 'Espinaca', 'Maíz dulce', 'Camote', 'Tomate',
    'Nabo', 'Sandía'
]


@app.post("/predict/")
async def upload_image(file: UploadFile = File(...)):
    valid_extensions = {".jpg", ".jpeg", ".png"}
    file_extension = Path(file.filename).suffix
    if file_extension not in valid_extensions:
        return {"error": "Formato de archivo no permitido. Usa JPG o PNG."}
    
    save_path = UPLOAD_FOLDER / file.filename # Define the path where the file will be saved

    with open(save_path, "wb") as buffer:
        buffer.write(file.file.read())

    try:
        img = Image.open(save_path)
        img_array = preprocess_image(img)
    except Exception as e:
        return {"error": f"No se pudo procesar la imagen: {str(e)}"}
    
    # Realizar la predicción
    try:
        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions, axis=1)[0]  # Clase con mayor probabilidad
        confidence = predictions[0][predicted_class]  # Confianza de la predicción
    except Exception as e:
        return {"error": f"No se pudo realizar la predicción: {str(e)}"}

    return {
        "class": LABELS[predicted_class],
        "confidence": float(confidence)
    }
    