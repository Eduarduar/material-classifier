from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser

from utils.model_loader import predict
from utils.drive_service import upload_image_to_drive


class ClassifyView(APIView):
    """
    POST /api/classify/
    Campos (multipart):
      - image      : archivo de imagen (requerido)
      - nombre     : nombre de la persona (requerido)
      - matricula  : número de 8 a 10 dígitos (opcional)
      - label      : clase manual (opcional, para corregir la predicción)
    """
    parser_classes = [MultiPartParser]

    def post(self, request):
        image_file = request.FILES.get('image')
        nombre    = request.data.get('nombre', '').strip()
        matricula = request.data.get('matricula', '').strip()
        label     = request.data.get('label', '').strip()

        # Validaciones
        errors = {}

        if not image_file:
            errors['image'] = 'La imagen es requerida.'

        if not nombre:
            errors['nombre'] = 'El nombre es requerido.'

        # Matrícula es opcional, pero si se manda debe ser válida
        if matricula:
            if not matricula.isdigit():
                errors['matricula'] = 'La matrícula debe contener solo números.'
            elif not (8 <= len(matricula) <= 10):
                errors['matricula'] = 'La matrícula debe tener entre 8 y 10 dígitos.'

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        # Inferencia
        try:
            result = predict(image_file)
        except Exception as exc:
            return Response(
                {'error': f'Error al correr el modelo: {str(exc)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Subir a Drive
        try:
            drive_file_id = upload_image_to_drive(
                image_file=image_file,
                predicted_class=result['class'],
                human_label=label,
                nombre=nombre,
                matricula=matricula,
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