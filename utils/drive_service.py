"""
Sube imágenes a Google Drive usando OAuth2 con cuenta personal.
"""
import io
import os
import re
from datetime import datetime

from django.conf import settings
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/drive']

CARPETAS_RECICLAJE = {
    "crushed_metal":   "1o5QQTB73Ku1FP6iWsVWt_eICs1JDbze_",
    "crushed_plastic": "1HjanmadCQertoGm-dIi1Jgid8UEy86Ux",
    "metal":           "10fzdmNTLTwjIFdu1ghUbcKejYYYlnByS",
    "no_reciclable":   "1rbLriyCKJWBLJW4f-vqzTFDijDEOBqFh",
    "plastic":         "1iGhD1qpPWo1VXOiQwXw__aAYObaS89QS",
}

_service = None


def _get_service():
    global _service
    if _service:
        return _service

    creds = None
    token_path = str(settings.GOOGLE_OAUTH_TOKEN_FILE)
    credentials_path = str(settings.GOOGLE_DRIVE_CREDENTIALS_FILE)

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(token_path, 'w') as f:
                f.write(creds.to_json())
        else:
            raise RuntimeError(
                "No hay token de OAuth. Ejecuta: python generate_token.py"
            )

    _service = build('drive', 'v3', credentials=creds)
    return _service


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