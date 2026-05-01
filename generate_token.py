"""
Ejecuta este script UNA SOLA VEZ para autorizar con tu cuenta de Google.
Abrirá el navegador, pide permiso, y guarda el token en credentials/token.json
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/drive']

flow = InstalledAppFlow.from_client_secrets_file(
    str(settings.GOOGLE_DRIVE_CREDENTIALS_FILE),
    SCOPES
)

creds = flow.run_local_server(port=0)

token_path = str(settings.GOOGLE_OAUTH_TOKEN_FILE)
with open(token_path, 'w') as f:
    f.write(creds.to_json())

print(f"✅ Token guardado en {token_path}")
print("Ya puedes correr el servidor normalmente.")