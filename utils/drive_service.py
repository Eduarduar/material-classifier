"""
Sube imágenes a Google Drive usando OAuth2 con cuenta personal.
"""
import io
import os
import re
from datetime import datetime
from pathlib import Path

from django.conf import settings
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/drive']

CARPETAS_RECICLAJE = {
    "crushed_metal":   "1o5QQTB73Ku1FP6iWsVWt_eICs1JDbze_",
    "crushed_plastic": "1HjanmadCQertoGm-dIi1Jgid8UEy86Ux",
    "metal":           "10fzdmNTLTwjIFdu1ghUbcKejYYYlnByS",
    "no_reciclable":   "1rbLriyCKJWBLJW4f-vqzTFDijDEOBqFh",
    "plastic":         "1iGhD1qpPWo1VXOiQwXw__aAYObaS89QS",
}

def _get_service():
    creds = None
    token_path = str(settings.GOOGLE_OAUTH_TOKEN_FILE)

    if os.path.exists(token_path):
        try:
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        except ValueError as exc:
            raise RuntimeError(
                "El archivo de token es inválido. Ejecuta: python generate_token.py"
            ) from exc

    if not creds:
        raise RuntimeError(
            "Token inválido o inexistente. Ejecuta: python generate_token.py"
        )

    if creds.expired:
        if creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError as exc:
                raise RuntimeError(
                    "No se pudo refrescar el token. Ejecuta: python generate_token.py"
                ) from exc

            Path(token_path).parent.mkdir(parents=True, exist_ok=True)
            with open(token_path, 'w') as f:
                f.write(creds.to_json())
        else:
            raise RuntimeError(
                "Token inválido o inexistente. Ejecuta: python generate_token.py"
            )

    if not creds.valid:
        raise RuntimeError(
            "Token inválido. Ejecuta: python generate_token.py"
        )

    return build('drive', 'v3', credentials=creds)


def _sanitize(text: str) -> str:
    """Elimina caracteres no permitidos en nombres de archivo."""
    text = text.strip().lower()
    text = re.sub(r'[^\w\-]', '_', text, flags=re.UNICODE)
    text = re.sub(r'_+', '_', text)
    return text


def upload_image_to_drive(
    image_file,
    predicted_class: str,
    human_label: str = '',
    nombre: str = '',
    matricula: str = '',
) -> str:
    """
    Sube la imagen a Drive con el nombre:
      YYYYMMDD_HHMMSS_clase_nombre_matricula.ext

    Retorna el ID del archivo subido.
    """
    folder_key = human_label or predicted_class

    if folder_key not in CARPETAS_RECICLAJE:
        raise ValueError(
            f"Clase '{folder_key}' no válida. "
            f"Opciones: {list(CARPETAS_RECICLAJE.keys())}"
        )

    folder_id = CARPETAS_RECICLAJE[folder_key]
    service = _get_service()

    ts     = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    ext    = os.path.splitext(image_file.name)[-1] or '.jpg'
    nombre_safe    = _sanitize(nombre)
    suffix = f"_{matricula}" if matricula else ""
    filename = f"{ts}_{folder_key}_{nombre_safe}{suffix}{ext}"

    image_file.seek(0)
    content = image_file.read()
    media = MediaIoBaseUpload(io.BytesIO(content), mimetype='image/jpeg', resumable=False)

    file_meta = {'name': filename, 'parents': [folder_id]}
    uploaded = service.files().create(
        body=file_meta, media_body=media, fields='id'
    ).execute()

    return uploaded['id']


def move_and_relabel_image(file_id: str, new_class: str) -> str:
    """
    Mueve y renombra un archivo en Drive a la carpeta correspondiente a new_class.
    Reemplaza la clase en el nombre del archivo.

    Formato de nombre esperado:
    YYYYMMDD_HHMMSS_clase_nombre_matricula.ext

    Args:
        file_id: ID del archivo en Drive
        new_class: Nueva clase (debe estar en CARPETAS_RECICLAJE)

    Returns:
        El ID del archivo actualizado

    Raises:
        ValueError: Si new_class no es válida
        Exception: Si el archivo no existe o hay error en Drive
    """
    if new_class not in CARPETAS_RECICLAJE:
        raise ValueError(
            f"Clase '{new_class}' no válida. "
            f"Opciones: {list(CARPETAS_RECICLAJE.keys())}"
        )

    service = _get_service()
    new_folder_id = CARPETAS_RECICLAJE[new_class]

    # Obtener información actual del archivo
    file_meta = service.files().get(
        fileId=file_id,
        fields='name, parents'
    ).execute()

    current_name = file_meta.get('name', '')
    current_parents = file_meta.get('parents', [])

    # Convertir parents actuales a string separado por comas
    old_parents = ",".join(current_parents)

    # Parsear nombre:
    # YYYYMMDD_HHMMSS_clase_nombre_matricula.ext
    name_without_ext, ext = os.path.splitext(current_name)

    # máximo 4 partes:
    # [YYYYMMDD, HHMMSS, clase, resto]
    parts = name_without_ext.split('_', 3)

    if len(parts) >= 3:
        timestamp = f"{parts[0]}_{parts[1]}"
        rest = parts[3] if len(parts) > 3 else ""

        if rest:
            new_name = f"{timestamp}_{new_class}_{rest}{ext}"
        else:
            new_name = f"{timestamp}_{new_class}{ext}"
    else:
        # fallback si el formato no coincide
        new_name = current_name

    # Actualizar nombre y mover carpeta correctamente
    updated = service.files().update(
        fileId=file_id,
        addParents=new_folder_id,
        removeParents=old_parents,
        body={
            'name': new_name
        },
        fields='id'
    ).execute()

    return updated['id']