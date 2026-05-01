from django.urls import path, include
from django.http import FileResponse
from django.conf import settings
from django.conf.urls.static import static
import mimetypes

FRONTEND_DIR = settings.BASE_DIR / 'staticfiles' / 'frontend'

def serve_frontend(request, path=''):
    # Intentar servir el archivo estático si existe
    file_path = FRONTEND_DIR / path
    if path and file_path.exists() and file_path.is_file():
        mime_type, _ = mimetypes.guess_type(str(file_path))
        return FileResponse(open(file_path, 'rb'), content_type=mime_type or 'application/octet-stream')
    # Si no existe, servir index.html (para rutas de Vue)
    index = FRONTEND_DIR / 'index.html'
    return FileResponse(open(index, 'rb'), content_type='text/html')

urlpatterns = [
    path('api/', include('classifier.urls')),
    path('', serve_frontend),
    path('<path:path>', serve_frontend),
]