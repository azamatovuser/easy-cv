from rest_framework import serializers
from apps.cv.models import Cv, Contact
import openai
import os
from openai import OpenAI

# Set your OpenAI API key
client = OpenAI(
    api_key=os.environ.get("OPENAPI_KEY"),  # This is the default and can be omitted
)

def prompt(question):
    """
    Generate a professional resume based on user input.

    :param question: User-provided details for the resume.
    :return: Formatted resume as a string.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Use "gpt-4" or "gpt-3.5-turbo" as needed
            messages=[
                {
                    "role": "user",
                    "content": f"""Создай профессиональное резюме на основе следующих данных: {question}.
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
                        дополнительных комментариев. Не добавь от себя ничего, это важно! Если данные отсутствую какие то, то пропусти этот раздел"""
                }
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {e}"


def prompt_job_title(question):
    """
    Generate a concise job title based on user input.

    :param question: User-provided details for the job title.
    :return: A job title in the required format.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Use "gpt-4" or "gpt-3.5-turbo" as needed
            messages=[
                {
                    "role": "user",
                    "content": f"""Your task is to create a job title based on this data: {question}.
                        There should be max 2 words. If it is 2 words, then instead of a space between them, put + like
                        python+developer or software+engineer. Remember, just send the answer and no words more."""
                }
            ]
        )
        return response.choices[0].message.content.strip()
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