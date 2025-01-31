import requests
from rest_framework import serializers
from apps.cv.models import Cv, Contact

OLLAMA_API_URL = "http://localhost:11434/api/generate"

def prompt(question):
    """
    Generate a professional resume based on user input using Ollama.
    """
    try:
        data = {
            "model": "mistral",  # Change model if needed
            "prompt": f"""Создай профессиональное резюме на основе следующих данных: {question}.
                        Резюме должно содержать 4 раздела:
                        1. Контактная информация
                            Тут должно быть:
                            1. Имя  
                            2. Телефон
                            3. Почта
                        2. Обо мне
                            Краткое описание о человеке исходя из данных
                        3. Опыт работы
                            Тут должно быть:
                            1. Имя компании
                            2. Должность
                            3. Дата (пример Октябрь 2023 - Сейчас)
                            4. Описание чем занимался
                        4. Образование
                            Тут должно быть:
                            1. Имя университета
                            2. Направление
                        5. Навыки
                        И перед каждым разделом раздели их символом next. Между разделами будет только слово next и всё.
                        Текст должен быть на русском языке. Форматируй текст чётко и структурированно, чтобы резюме выглядело 
                        профессионально и готово к отправке работодателю. Ответ должен содержать только текст резюме, без 
                        дополнительных комментариев. Не добавь от себя ничего, это важно! Если данные отсутствуют какие-то, то пропусти этот раздел""",
            "stream": False
        }
        
        response = requests.post(OLLAMA_API_URL, json=data)
        
        if response.status_code == 200:
            return response.json().get("response", "").strip()
        else:
            return f"Error: {response.status_code} - {response.text}"
    
    except Exception as e:
        return f"An error occurred: {e}"

def prompt_job_title(question):
    """
    Generate a concise job title based on user input using Ollama.
    """
    try:
        data = {
            "model": "mistral",  # Change model if needed
            "prompt": f"""Your task is to create a job title based on this data: {question}.
                        There should be max 2 words. If it is 2 words, then instead of a space between them, put + like
                        python+developer or software+engineer. Remember, just send the answer and no words more.""",
            "stream": False
        }
        
        response = requests.post(OLLAMA_API_URL, json=data)
        
        if response.status_code == 200:
            return response.json().get("response", "").strip()
        else:
            return f"Error: {response.status_code} - {response.text}"
    
    except Exception as e:
        return f"An error occurred: {e}"

class CvSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    job_title = serializers.CharField(read_only=True)
    cv = serializers.FileField(read_only=True)
    cv_text = serializers.CharField(read_only=True)

    class Meta:
        model = Cv
        fields = ("id", "user", "job_title", "prompt", "cv_text", "cv")

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['job_title'] = prompt_job_title(validated_data['prompt'])
        validated_data['cv'] = None
        validated_data['cv_text'] = prompt(validated_data['prompt'])

        return super().create(validated_data)

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__" 