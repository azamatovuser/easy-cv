from rest_framework import serializers
from apps.cv.models import Cv, Contact
import g4f


def prompt(question):
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4o,
        messages=[{"role": "user", "content": f"""Создай профессиональное резюме на основе следующих данных: {question}.
                                                Резюме должно содержать 4 раздела:
                                                1. О себе / Контактная информация  
                                                2. Образование  
                                                3. Опыт работы  
                                                4. Навыки  

                                                Текст должен быть на русском языке. Если какие-то данные отсутствуют, просто пропусти этот раздел.  
                                                Форматируй текст четко и структурированно, чтобы резюме выглядело профессионально и готово к отправке работодателю.  
                                                Ответ должен содержать только текст резюме, без дополнительных комментариев."""}]
    )
    return response


def prompt_job_title(question):
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4o,
        messages=[{"role": "user", "content": f"""Your task is to create a job title basde on this data: {question}.
                   There should be max 2 words. If it is 2 words than instead of space between them put + like
                   python+developer or software+engineer. Remember, just send the answer and no words more"""}]
    )
    
    return response


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