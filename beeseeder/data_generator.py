from beeseeder.utils import ModelItem
import anthropic
from django.conf import settings
import json
import requests

class DataGenerator:
    BASE_API_URL = "http://localhost:8000"
    def __init__(self, model_items: list[ModelItem]) -> None:
        self.model_items = model_items
    
    
    def generate(self): 
        input_data = [model_item.model_schema for model_item in self.model_items]
       
        json_data = json.dumps(input_data, default=str)
        
        response = requests.post( f"{self.BASE_API_URL}/generator/generate/", json={
            "tables": json.loads(json_data)
        })
        if response.status_code == 200:
            response_data = response.json()
            print('Data generation initiated successfully, job_id:', response_data.get('data', {}).get("job_id"))
        else:
            print("Error generating data", response.text)

        
        independent_models = [] #models that dont have any foreign key relationships
        dependent_models = [] #models that have foreign key pointing to other models  
        # for model_item in self.model_items:
        #     if len(model_item.related_model_names) == 0:
        #         independent_models.append(model_item)
        #     else:
        #         dependent_models.append(model_item)
                
        # self.generate_independent_models_data(independent_models)
    
    def generate_independent_models_data(self, model_items: list[ModelItem]):
        print("Preparing prompt for independent models data")
        model = "claude-sonnet-4-20250514"
        client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

        system_prompt = """
            You are an expert Django database architect and seed data generator. Your task is to create realistic, comprehensive, and production-ready seed data for Django applications that maintains referential integrity and follows best practices.
            
            Generate comprehensive JSON seed data for the provided Django models. Create exactly 20 records for each model, ensuring all relationships are properly maintained and data is realistic and diverse.
            
            Data Quality Standards:
            Realistic Data: Use authentic-sounding names, addresses, emails, dates, and descriptions
            Data Diversity: Ensure variety in all fields (geographical, temporal, categorical)
            Validation Compliance: All data must pass Django model field validation
            No Duplicates: Respect unique constraints and avoid duplicate values
            Professional Quality: Data should be suitable for demos, testing, and development
            
            Output Format:
            Provide the response as a single, valid JSON object structured as follows:
            {
                "model_name_1": [
                    {
                        "id": 1,
                        "field1": "value1",
                        "field2": "value2",
                        "foreign_key_field": 1,
                        "datetime_field": "2024-01-15T10:30:00Z"
                    }
                ],
                "model_name_2": [
                    {
                        "id": 1,
                        "field1": "value1",
                        "related_field": 1
                    }
                ]
            }
            
            Examples
            Input_data:
            [
                {'name': 'bookstore.Genre', 'fields': [{'type': 'BigAutoField', 'is_relation': False, 'name': 'id', 'null': False, 'blank': True, 'unique': True, 'help_text': ''}, {'type': 'CharField', 'is_relation': False, 'name': 'name', 'max_length': 100, 'null': False, 'blank': False, 'unique': True, 'help_text': ''}]},
                {'name': 'accounts.Country', 'fields': [{'type': 'BigAutoField', 'is_relation': False, 'name': 'id', 'null': False, 'blank': True, 'unique': True, 'help_text': ''}, {'type': 'CharField', 'is_relation': False, 'name': 'code', 'max_length': 3, 'null': False, 'blank': False, 'unique': True, 'help_text': ''}, {'type': 'CharField', 'is_relation': False, 'name': 'currency', 'max_length': 3, 'null': False, 'blank': False, 'unique': False, 'help_text': ''}, {'type': 'CharField', 'is_relation': False, 'name': 'flag', 'max_length': 200, 'null': True, 'blank': True, 'unique': False, 'help_text': ''}, {'type': 'CharField', 'is_relation': False, 'name': 'name', 'max_length': 255, 'null': False, 'blank': False, 'unique': False, 'help_text': ''}]}
            ]
            Output data:
            [
                {
                    "bookstore.Genre": [
                        {"id": 1, "name": "Fiction"},
                        {"id": 2, "name": "Science Fiction"},
                        {"id": 3, "name": "Fantasy"},
                        {"id": 4, "name": "Mystery"},
                        {"id": 5, "name": "Thriller"},
                        {"id": 6, "name": "Romance"},
                    ]
                },
                {
                    "accounts.Country": [
                        {"id": 1, "code": "USA", "currency": "USD", "flag": "https://example.com/usa.png", "name": "United States"},
                        {"id": 2, "code": "UK", "currency": "GBP", "flag": "https://example.com/uk.png", "name": "United Kingdom"},
                        {"id": 3, "code": "CA", "currency": "CAD", "flag": "https://example.com/ca.png", "name": "Canada"},
                        {"id": 4, "code": "AU", "currency": "AUD", "flag": "https://example.com/au.png", "name": "Australia"},
                        {"id": 5, "code": "NZ", "currency": "NZD", "flag": "https://example.com/nz.png", "name": "New Zealand"},
                    ]
                }
            ]
            Output data:
            Input data:
        """
        print("Preparing input data for independent models")
        input_data = [model_item.model_schema for model_item in model_items]
        
        print("Sending request to Claude")
        print(json.dumps(input_data))
        
        # response = client.messages.create(
        #     model=model,
        #     max_tokens=10000,
        #     system=system_prompt,
        #     messages=[
        #         {
        #             "role": "user",
        #             "content": json.dumps(input_data)
        #         }
        #     ]
        # )
        # response_text = response.content[0].text.replace("```json", "").replace("```", "")
        # print(response_text)
        # json_data = json.loads(response_text)
                
                