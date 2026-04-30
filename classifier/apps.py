from django.apps import AppConfig


class ClassifierConfig(AppConfig):
    name = 'classifier'
    verbose_name = 'Material Classifier'

    def ready(self):
        from utils.model_loader import load_model
        load_model()
