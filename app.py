import streamlit as st
from rembg import remove
from PIL import Image
import io
import zipfile

# --- Configuración de la página ---
st.set_page_config(
    page_title="Eliminador de Fondos Pro",
    page_icon="✂️",
    layout="centered",
    initial_sidebar_state="auto",
)

# --- Estilos CSS para mejorar la apariencia ---
st.markdown("""
<style>
    .stApp {
        background-color: #f0f2f6;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 20px;
        border: 1px solid #4CAF50;
        padding: 10px 24px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: white;
        color: #4CAF50;
        border: 1px solid #4CAF50;
    }
    .stFileUploader label {
        font-size: 1.1rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- Funciones auxiliares ---

def process_image(image_file):
    """
    Elimina el fondo de una sola imagen.
    Args:
        image_file: El archivo de imagen subido por el usuario.
    Returns:
        Un objeto de imagen de Pillow sin fondo.
    """
    input_image = Image.open(image_file)
    # El modelo 'u2net' es excelente para recortes precisos y detallados.
    output_image = remove(input_image, model='u2net')
    return output_image

def create_zip(images, filenames):
    """
    Crea un archivo ZIP en memoria con las imágenes procesadas.
    Args:
        images: Una lista de objetos de imagen de Pillow.
        filenames: Una lista de nombres para los archivos de imagen.
    Returns:
        Los bytes del archivo ZIP.
    """
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for i, image in enumerate(images):
            # Guardar la imagen en un buffer de bytes en formato PNG
            img_buffer = io.BytesIO()
            image.save(img_buffer, format="PNG")
            # Añadir el archivo al ZIP
            zip_file.writestr(filenames[i], img_buffer.getvalue())
    
    return zip_buffer.getvalue()

# --- Interfaz de la aplicación ---

st.title("✂️ Eliminador de Fondos Profesional")
st.markdown("Sube una o varias imágenes para quitarles el fondo de forma automática y precisa.")

# --- Carga de archivos ---
uploaded_files = st.file_uploader(
    "Selecciona tus imágenes (PNG, JPG, JPEG)",
    accept_multiple_files=True,
    type=['png', 'jpg', 'jpeg']
)

# --- Opciones ---
if uploaded_files:
    st.info(f"Has subido {len(uploaded_files)} imágen(es).")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        keep_filenames = st.checkbox("Mantener nombres de archivo originales", value=True)
    
    # --- Botón de procesamiento ---
    if st.button("✨ ¡Quitar Fondos!"):
        if not uploaded_files:
            st.warning("Por favor, sube al menos una imagen antes de procesar.")
        else:
            with st.spinner('Procesando... Esto puede tardar un momento...'):
                processed_images = []
                processed_filenames = []

                for uploaded_file in uploaded_files:
                    # Procesar cada imagen
                    result_image = process_image(uploaded_file)
                    processed_images.append(result_image)
                    
                    # Determinar el nombre del archivo
                    if keep_filenames:
                        # Eliminar la extensión original y añadir .png
                        base_name = uploaded_file.name.rsplit('.', 1)[0]
                        new_name = f"{base_name}_sin_fondo.png"
                    else:
                        new_name = f"imagen_{len(processed_filenames) + 1}_sin_fondo.png"
                    processed_filenames.append(new_name)
            
            st.success("¡Proceso completado con éxito!")

            # --- Lógica de descarga ---
            if len(processed_images) == 1:
                st.subheader("Resultado")
                
                # Convertir la imagen para la descarga
                img_byte_arr = io.BytesIO()
                processed_images[0].save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()

                st.image(img_byte_arr, caption="Vista previa de la imagen sin fondo.")
                
                st.download_button(
                    label="📥 Descargar Imagen",
                    data=img_byte_arr,
                    file_name=processed_filenames[0],
                    mime="image/png"
                )
            else:
                st.subheader("Descargar Todo")
                st.markdown("Todas tus imágenes procesadas están listas en un archivo ZIP.")
                
                zip_data = create_zip(processed_images, processed_filenames)
                
                st.download_button(
                    label="📥 Descargar ZIP con todas las imágenes",
                    data=zip_data,
                    file_name="imagenes_sin_fondo.zip",
                    mime="application/zip"
                )

# --- Pie de página ---
st.markdown("---")
st.markdown("Creado con ❤️ usando [Streamlit](https://streamlit.io) y [rembg](https://github.com/danielgatis/rembg).")
