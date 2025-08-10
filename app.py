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
    initial_sidebar_state="expanded",
)

# --- Gestión del Tema (Día/Noche) ---
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False # Por defecto, modo día

# --- Barra Lateral ---
with st.sidebar:
    st.header("🎨 Configuración")
    # El toggle actualiza el estado de la sesión directamente
    st.session_state.dark_mode = st.toggle(
        "Activar Modo Noche", 
        value=st.session_state.dark_mode, 
        key="theme_toggle"
    )
    st.markdown("---")
    st.info("Sube una o varias imágenes en el área principal para empezar.")
    st.markdown("---")


# --- Estilos CSS Dinámicos ---
light_theme = """
<style>
    /* --- TEMA CLARO --- */
    .stApp {
        background-color: #f0f2f6;
        color: #31333F;
    }
    .st-emotion-cache-1y4p8pa { /* Encabezado y títulos */
        color: #31333F;
    }
    .st-emotion-cache-16txtl3 { /* Texto normal */
        color: #31333F;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 30px;
        border: 2px solid #4CAF50;
        padding: 10px 24px;
        transition: all 0.3s;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: white;
        color: #4CAF50;
    }
    .stFileUploader {
        background-color: #ffffff;
        border: 2px dashed #4CAF50;
        border-radius: 30px;
        padding: 25px;
    }
    .stDownloadButton>button {
       background-color: #008CBA;
       color: white;
       border-radius: 30px;
       border: 2px solid #008CBA;
       padding: 10px 24px;
       transition: all 0.3s;
       font-weight: bold;
    }
    .stDownloadButton>button:hover {
       background-color: white;
       color: #008CBA;
    }
    .results-container {
        background-color: #ffffff;
        border-radius: 30px;
        padding: 1.5rem;
        margin-top: 1rem;
        border: 1px solid #ddd;
    }
</style>
"""

dark_theme = """
<style>
    /* --- TEMA OSCURO --- */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    .st-emotion-cache-1y4p8pa { /* Encabezado y títulos */
        color: #fafafa;
    }
    .st-emotion-cache-16txtl3 { /* Texto normal */
        color: #fafafa;
    }
    .stButton>button {
        background-color: #2E8B57; /* SeaGreen */
        color: white;
        border-radius: 30px;
        border: 2px solid #2E8B57;
        padding: 10px 24px;
        transition: all 0.3s;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #0e1117;
        color: #2E8B57;
    }
    .stFileUploader {
        background-color: #262730;
        border: 2px dashed #2E8B57;
        border-radius: 30px;
        padding: 25px;
    }
    .stDownloadButton>button {
       background-color: #1E90FF; /* DodgerBlue */
       color: white;
       border-radius: 30px;
       border: 2px solid #1E90FF;
       padding: 10px 24px;
       transition: all 0.3s;
       font-weight: bold;
    }
    .stDownloadButton>button:hover {
       background-color: #262730;
       color: #1E90FF;
    }
    .results-container {
        background-color: #262730;
        border-radius: 30px;
        padding: 1.5rem;
        margin-top: 1rem;
        border: 1px solid #444;
    }
</style>
"""

# Aplicar el tema seleccionado
st.markdown(dark_theme if st.session_state.dark_mode else light_theme, unsafe_allow_html=True)


# --- Funciones auxiliares ---
def process_image(image_file):
    input_image = Image.open(image_file)
    output_image = remove(input_image, model='u2net')
    return output_image

def create_zip(images, filenames):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for i, image in enumerate(images):
            img_buffer = io.BytesIO()
            image.save(img_buffer, format="PNG")
            zip_file.writestr(filenames[i], img_buffer.getvalue())
    return zip_buffer.getvalue()

# --- Interfaz Principal ---
st.title("✂️ Eliminador de Fondos Profesional")
st.markdown("Sube una o varias imágenes para quitarles el fondo de forma automática y precisa.")

# --- Carga de archivos ---
uploaded_files = st.file_uploader(
    "Selecciona tus imágenes (PNG, JPG, JPEG)",
    accept_multiple_files=True,
    type=['png', 'jpg', 'jpeg']
)

if uploaded_files:
    st.info(f"Has subido {len(uploaded_files)} imágen(es).")
    
    keep_filenames = st.checkbox("Mantener nombres de archivo originales", value=True)
    
    if st.button("✨ ¡Quitar Fondos!"):
        with st.spinner('Procesando... Esto puede tardar un momento...'):
            processed_images = []
            processed_filenames = []

            for uploaded_file in uploaded_files:
                result_image = process_image(uploaded_file)
                processed_images.append(result_image)
                
                if keep_filenames:
                    base_name = uploaded_file.name.rsplit('.', 1)[0]
                    new_name = f"{base_name}_sin_fondo.png"
                else:
                    new_name = f"imagen_{len(processed_filenames) + 1}_sin_fondo.png"
                processed_filenames.append(new_name)
        
        st.success("¡Proceso completado con éxito!")

        # Contenedor para los resultados con el estilo aplicado
        st.markdown('<div class="results-container">', unsafe_allow_html=True)
        
        if len(processed_images) == 1:
            st.subheader("Resultado")
            img_byte_arr = io.BytesIO()
            processed_images[0].save(img_byte_arr, format='PNG')
            st.image(img_byte_arr.getvalue(), caption="Vista previa de la imagen sin fondo.")
            
            st.download_button(
                label="📥 Descargar Imagen",
                data=img_byte_arr.getvalue(),
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
        
        st.markdown('</div>', unsafe_allow_html=True)

# --- Pie de página ---
st.markdown("---")
st.markdown("Creado con ❤️ usando [Streamlit](https://streamlit.io) y [rembg](https://github.com/danielgatis/rembg).")
