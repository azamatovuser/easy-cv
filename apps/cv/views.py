import requests
from bs4 import BeautifulSoup
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from apps.cv.models import Cv
from apps.cv.serializers import CvSerializer


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
            
            # Extract title
            title_elem = card.find('span', {'data-qa': 'serp-item__title-text'})
            job_info['title'] = title_elem.text.strip() if title_elem else None
            
            # Extract company name
            company_elem = card.find('span', {'data-qa': 'vacancy-serp__vacancy-employer-text'})
            job_info['company'] = company_elem.text.strip() if company_elem else None
            
            # Extract salary
            salary_elem = card.find('span', {'class': 'magritte-text_typography-label-1-regular___pi3R-_3-0-19'})
            job_info['salary'] = salary_elem.text.strip() if salary_elem else None

            jobs_data.append(job_info)
        
        return jobs_data
        
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []


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