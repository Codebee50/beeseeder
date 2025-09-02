from django.core.management.base import BaseCommand
from django.apps import apps
from beeseeder.utils import ModelItem
from beeseeder.services import order_models_by_dependency






class Command(BaseCommand):
    def handle(self, *args, **options) -> str | None:
        print('"Seeding the database for you..')
        model_items = []
        field_items = []
        all_models = apps.get_models()
        for model in all_models:
            model_item = ModelItem(model)
            model_items.append(model_item)

            name = model_item.model_schema["name"]

            print(model_item.model_name, model_item.related_model_names)

        print("===================================")
        ordered_model_items = order_models_by_dependency(model_items)

        for model_item in ordered_model_items:
            # print(model_item.model_name, model_item.related_model_names)

            # print("=>>>>>>>")
            print(model_item.model_schema, end="\n\n")
            # print(json.dumps(model_item.model_schema, indent=4), end="\n\n")
