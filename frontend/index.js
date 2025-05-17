const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("fileInput");
const resultDiv = document.getElementById("response");
let selectedFile = null;

// Abrir el selector de archivos al hacer clic en el área de arrastre
dropZone.addEventListener("click", () => fileInput.click());

fileInput.addEventListener('change', () => {
    selectedFile = fileInput.files[0];
    dropZone.querySelector('p').textContent = `Archivo seleccionado: ${selectedFile.name}`;

    if (selectedFile) {
        dropZone.querySelector('p').textContent = `Archivo seleccionado: ${selectedFile.name}`;

        // Previsualización de la imagen
        const reader = new FileReader();
        reader.onload = function (e) {
            preview.src = e.target.result; // Establece el contenido de la imagen
            document.querySelector('.preview-container').style.display = "block"; // Muestra la imagen
        };
        reader.readAsDataURL(selectedFile); // Lee el archivo como Data URL
    } else {
        document.querySelector('.preview-container').style.display = "none"; // Oculta la imagen si no hay archivo seleccionado
        dropZone.querySelector('p').textContent = "haz clic para seleccionar una imagen";
    }
});

document.getElementById("upload-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];
    if (!file) {
        resultDiv.textContent = "Por favor, selecciona una imagen.";
        resultDiv.className = "error-message";
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("http://localhost:8000/predict/", {
            method: "POST",
            body: formData,
        });

        const result = await response.json();
        const probability = (result.confidence * 100).toFixed(2); // Convertir a porcentaje
        resultDiv.innerHTML = `<strong>Predicción:</strong> ${result.class} <br> 
                                <strong>Probabilidad:</strong> ${probability}%`;
        resultDiv.className = "success-message"; // Clase para mensajes exitosos
    } catch (error) {
        console.error("Error al subir el archivo:", error);
        resultDiv.textContent = "Error al subir el archivo.";
    }

});