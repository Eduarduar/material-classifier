# Setup del proyecto — Material Classifier

## 1. Entorno virtual

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Variables de entorno

```bash
cp .env.example .env
# Edita .env con tus valores reales
```

## 3. Coloca tu modelo

```
model/model.keras
```

## 4. Google Drive — Service Account

1. Ve a [Google Cloud Console](https://console.cloud.google.com/) → IAM → Service Accounts
2. Crea una cuenta de servicio → descarga el JSON de credenciales
3. Guárdalo en: `credentials/service_account.json`
4. Comparte tu carpeta de Drive con el email de la service account (rol: Editor)
5. Copia el ID de la carpeta en `GOOGLE_DRIVE_FOLDER_ID` del `.env`
   - El ID es la última parte de la URL: `drive.google.com/drive/folders/<ESTE_ES_EL_ID>`

## 5. Correr el servidor

```bash
python manage.py runserver
```

## Endpoints

| Método | URL | Descripción |
|--------|-----|-------------|
| POST | `/api/classify/` | Envía imagen → predicción + sube a Drive |
| GET  | `/api/health/`   | Verifica que servidor y modelo estén listos |

### Ejemplo con curl

```bash
curl -X POST http://localhost:8000/api/classify/ \
  -F "image=@mi_foto.jpg" \
  -F "label=plastico"
```

### Respuesta esperada

```json
{
  "class": "plastico",
  "confidence": 0.9231,
  "scores": {
    "plastico": 0.9231,
    "metal": 0.0412,
    "vidrio": 0.0357
  },
  "drive_file_id": "1ABCxyz..."
}
```

## Estructura en Drive

```
📁 Tu carpeta raíz (GOOGLE_DRIVE_FOLDER_ID)
  📁 plastico/
    🖼 20240501_120000_plastico.jpg
  📁 metal/
    🖼 20240501_120100_metal.jpg
  📁 vidrio/
    ...
```
