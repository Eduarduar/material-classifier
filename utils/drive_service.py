"""
Sube imágenes a Google Drive usando una Service Account.
Las carpetas destino están mapeadas directamente por su ID.
"""
import io
import os
from datetime import datetime

from django.conf import settings
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/drive']

# Mapa clase → ID de carpeta en Drive (fijo, sin búsquedas)
CARPETAS_RECICLAJE = {
    "crushed_metal":    "1yy4UT7kivg5Qt-1NJl7P9c_WIXbCrcQE",
    "crushed_plastic":  "1MCb-XO5xb6Xe1V25AvEMtczk84bhFdDg",
    "metal":            "1wYYdju6RC0jJ1MMN0tFoZ6vizx_OjzSD",
    "no_reciclable":    "1i4k3jy05AVgYh0VyhHH1uf9z9aGZHPYX",
    "plastic":          "1M6DdX5geeVsvms_B_j27X4zYyr83iIyZ"
}

_service = None


def _get_service():
    global _service
    if _service:
        return _service

    creds = service_account.Credentials.from_service_account_file(
        str(settings.GOOGLE_DRIVE_CREDENTIALS_FILE),
        scopes=SCOPES,
    )
    _service = build('drive', 'v3', credentials=creds)
    return _service


def upload_image_to_drive(image_file, predicted_class: str, human_label: str = '') -> str:
    """
    Sube la imagen a la carpeta de Drive correspondiente a la clase.

    - Si se manda `human_label` (corrección manual), se usa esa clase.
    - Si la clase no está en CARPETAS_RECICLAJE, lanza ValueError.

    Retorna el ID del archivo subido en Drive.
    """
    folder_key = human_label.strip() or predicted_class

    if folder_key not in CARPETAS_RECICLAJE:
        raise ValueError(
            f"Clase '{folder_key}' no tiene carpeta asignada. "
            f"Clases válidas: {list(CARPETAS_RECICLAJE.keys())}"
        )

    folder_id = CARPETAS_RECICLAJE[folder_key]
    service = _get_service()

    ts = datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')
    ext = os.path.splitext(image_file.name)[-1] or '.jpg'
    filename = f"{ts}_{folder_key}{ext}"

    image_file.seek(0)
    content = image_file.read()
    media = MediaIoBaseUpload(io.BytesIO(content), mimetype='image/jpeg', resumable=False)

    file_meta = {'name': filename, 'parents': [folder_id]}
    uploaded = service.files().create(
        body=file_meta, media_body=media, fields='id'
    ).execute()

    return uploaded['id']