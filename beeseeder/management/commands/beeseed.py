from django.core.management.base import BaseCommand
from django.apps import apps
from beeseeder.data_generator import DataGenerator
from beeseeder.utils import ModelItem
from beeseeder.services import order_models_by_dependency
from django.conf import settings

SEED_APPS = settings.SEED_APPS


ASCII_ART = """
 ____  _____ _____ 
| __ )| ____| ____|
|  _ \|  _| |  _|  
| |_) | |___| |___ 
|____/|_____|_____|
                                          
"""


class Command(BaseCommand):
    def handle(self, *args, **options) -> str | None:
        print(ASCII_ART)
        print('"Seeding the database for you..')
        model_items = []
        all_models = apps.get_models()
        for model in all_models:
            if model._meta.app_label  in SEED_APPS:       
                model_item = ModelItem(model)
                model_items.append(model_item)

                print(model_item.model_name, model_item.related_model_names)

        print("===================================", end="\n\n")
        ordered_model_items = order_models_by_dependency(model_items)
        
        # for model_item in ordered_model_items:
        #     print(model_item.model_schema, end="\n\n")
        
        generator = DataGenerator(ordered_model_items)
        generator.generate()