from rest_framework import serializers
from apps.cv.models import Cv
import g4f


def prompt(question):
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4o,
        messages=[{"role": "user", "content": f"""Your task is to create a cv base on this data: {question}. 
                   Cv should have 4 sections: About me/Contact, Education, Experience, Skills.
                   The CV should be in russian language. Result should be only cv. If there is missing data,
                   just skip or based on given data fill it"""}]
    )
    
    return response


def prompt_job_title(question):
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4o,
        messages=[{"role": "user", "content": f"""Your task is to create a job title basde on this data: {question}.
                   There should be max 2 words. If it is 2 words than instead of space between them put + like
                   python+developer or software+engineer"""}]
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
        validated_data['cv'] = "default_cv.pdf"
        validated_data['cv_text'] = prompt(validated_data['prompt'])

        return super().create(validated_data)