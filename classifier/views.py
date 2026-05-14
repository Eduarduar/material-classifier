from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser

from utils.model_loader import predict
from utils.drive_service import upload_image_to_drive, move_and_relabel_image


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


class CorrectClassificationView(APIView):
    """
    POST /api/correct/
    Corrige la clasificación manual de una imagen ya cargada en Drive.
    
    Campos (JSON):
      - id    : ID del archivo en Drive (requerido)
      - type  : Nueva clase de clasificación (requerido)
    """

    def post(self, request):
        file_id = request.data.get('id', '').strip()
        new_class = request.data.get('type', '').strip()

        # Validaciones
        errors = {}

        if not file_id:
            errors['id'] = 'El ID del archivo es requerido.'

        if not new_class:
            errors['type'] = 'La clase de clasificación es requerida.'

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        # Validar que la clase exista
        from utils.drive_service import CARPETAS_RECICLAJE
        if new_class not in CARPETAS_RECICLAJE:
            return Response(
                {'type': f'Clase inválida. Opciones: {list(CARPETAS_RECICLAJE.keys())}'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Mover y renombrar el archivo en Drive
        try:
            updated_id = move_and_relabel_image(
                file_id=file_id,
                new_class=new_class,
            )
        except ValueError as exc:
            return Response(
                {'type': str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as exc:
            return Response(
                {'error': f'Error al corregir la clasificación: {str(exc)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response({
            'success': True,
            'message': f'Clasificación corregida a {new_class}',
            'file_id': updated_id,
        }, status=status.HTTP_200_OK)
