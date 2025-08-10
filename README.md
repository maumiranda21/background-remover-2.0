Aplicación para Eliminar Fondos de Imágenes

Esta es una aplicación web creada con Streamlit que permite a los usuarios eliminar el fondo de una o varias imágenes de forma automática.
Características

    Eliminación precisa: Utiliza el modelo U-2-Net para obtener recortes de alta calidad sin halos blancos.

    Procesamiento por lotes: Sube múltiples imágenes y procésalas todas a la vez.

    Exportación a ZIP: Descarga todas las imágenes procesadas en un único archivo ZIP.

    Conservación de nombres: Opción para mantener los nombres de archivo originales.

Cómo desplegar en Streamlit Cloud

    Crea un nuevo repositorio en GitHub (puede ser público o privado).

    Sube los siguientes archivos a tu repositorio:

        app.py

        requirements.txt

        README.md (opcional)

    Ve a Streamlit Cloud.

    Haz clic en "New app" y conecta tu cuenta de GitHub.

    Selecciona el repositorio que acabas de crear.

    Asegúrate de que el "Main file path" apunte a app.py.

    ¡Haz clic en "Deploy!" y espera a que tu aplicación esté en línea!
