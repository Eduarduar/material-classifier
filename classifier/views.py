from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser

from utils.model_loader import predict
from utils.drive_service import upload_image_to_drive


class ClassifyView(APIView):
    """
    POST /api/classify/
    Body (multipart): image=<file>, label=<str opcional para datos de entrenamiento>
    """
    parser_classes = [MultiPartParser]

    def post(self, request):
        image_file = request.FILES.get('image')
        label = request.data.get('label', '')

        if not image_file:
            return Response(
                {'error': 'No se recibió ninguna imagen.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 1. Inferencia
        try:
            result = predict(image_file)
        except Exception as exc:
            return Response(
                {'error': f'Error al correr el modelo: {str(exc)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # 2. Subir a Google Drive
        try:
            drive_file_id = upload_image_to_drive(
                image_file=image_file,
                predicted_class=result['class'],
                human_label=label,
            )
        except Exception as exc:
            drive_file_id = None
            result['drive_warning'] = str(exc)

        result['drive_file_id'] = drive_file_id
        return Response(result, status=status.HTTP_200_OK)


class HealthView(APIView):
    """GET /api/health/"""

    def get(self, request):
        from utils.model_loader import is_model_loaded
        return Response({
            'status': 'ok',
            'model_loaded': is_model_loaded(),
        })
