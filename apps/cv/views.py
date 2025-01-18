import requests
from bs4 import BeautifulSoup
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from apps.cv.models import Cv, Contact
from apps.cv.serializers import CvSerializer, ContactSerializer
import re


def parse_data_hh(job_title):
    print(job_title)
    # Format URL and make request
    url = f"https://hh.uz/search/vacancy?text={job_title}&area=2759&hhtmFrom=main&hhtmFromLabel=vacancy_search_line"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        jobs_data = []
        # Find all job cards
        job_cards = soup.find_all('div', {'data-qa': 'vacancy-serp__vacancy vacancy-serp__vacancy_standard_plus'})
        
        for card in job_cards:
            job_info = {}
            
            # Extract title and link
            title_elem = card.find('span', {'data-qa': 'serp-item__title-text'})
            link_elem = card.find('a', {'data-qa': 'serp-item__title'})
            job_info['title'] = title_elem.text.strip() if title_elem else None
            job_info['link'] = link_elem['href'] if link_elem else None  # Extract link
            
            # Extract company name
            company_elem = card.find('span', {'data-qa': 'vacancy-serp__vacancy-employer-text'})
            job_info['company'] = company_elem.text.strip() if company_elem else None
            
            # Extract salary
            salary_elem = card.find('span', {'class': 'magritte-text___pbpft_3-0-22 magritte-text_style-primary___AQ7MW_3-0-22 magritte-text_typography-label-1-regular___pi3R-_3-0-22'})
            job_info['salary'] = salary_elem.get_text(strip=True) if salary_elem else None  # Capture full salary text

            jobs_data.append(job_info)
        
        return jobs_data
        
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []


def parse_resume(text):
    # Extracting full name
    full_name = re.search(r"Имя: (.+)", text)
    full_name = full_name.group(1).strip() if full_name else ""  # Default to empty string if not found
    
    # Extracting phone number
    number = re.search(r"Телефон: ([+\d\s\-]+)", text)
    number = number.group(1).strip() if number else ""  # Default to empty string if not found
    
    # Extracting email
    email = re.search(r"Почта: (.+)", text)
    email = email.group(1).strip() if email else ""  # Default to empty string if not found
    
    # Extracting "about me" section
    about_me_match = re.search(r"Обо мне\s+(.+?)\s+next", text, re.DOTALL)
    about_me = about_me_match.group(1).strip() if about_me_match else ""  # Default to empty string if not found
    
    # Extracting job experience
    jobs = []
    for job_match in re.finditer(r"Имя компании: (.+?)\s+Должность: (.+?)\s+Дата: (.+?) - (.+?)\s+Описание: (.+?)\s+next", text, re.DOTALL):
        jobs.append({
            "name_company": job_match.group(1).strip(),
            "job_title": job_match.group(2).strip(),
            "from_date": job_match.group(3).strip(),
            "to_date": job_match.group(4).strip(),
            "job_description": job_match.group(5).strip()
        })
    
    # Extracting education
    education_match = re.search(r"Университет: (.+?)\s+Направление: (.+?)\s+next", text, re.DOTALL)
    education = {
        "university": education_match.group(1).strip(),
        "major": education_match.group(2).strip()
    } if education_match else {}
    
    # Extracting skills
    skills_match = re.search(r"Навыки\s+- (.+)", text, re.DOTALL)
    skills = [skill.strip() for skill in skills_match.group(1).split("\n- ")] if skills_match else []
    
    # Compiling the result
    return {
        "full_name": full_name,
        "number": number,
        "email": email,
        "about_me": about_me,
        "jobs": jobs,
        "education": education,
        "skills": skills
    }


class VacanciesListAPIView(APIView):
    def get(self, request, cv_id):
        job_title = Cv.objects.get(id=cv_id).job_title
        data = parse_data_hh(job_title)
        return Response(data)
    

class CvCreateAPIView(generics.CreateAPIView):
    queryset = Cv.objects.all()
    serializer_class = CvSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cv_instance = serializer.save()  # This will call the create method in the serializer
        return Response(serializer.data, status=201)
    

class CvListAPIView(generics.ListAPIView):
    queryset = Cv.objects.all()
    serializer_class = CvSerializer


class ContactCreateAPIView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class CvViewAPIView(APIView):
    def get(self, request, pk, *args, **kwargs):
        cv = Cv.objects.get(id=pk)
        response_data = parse_resume(cv.cv_text)

        return Response(response_data)