from django.urls import path
from apps.cv.views import VacanciesListAPIView, CvCreateAPIView, CvListAPIView, ContactCreateAPIView


urlpatterns = [
    path('vacanies/<int:cv_id>/', VacanciesListAPIView.as_view()),
    path('cv_create/', CvCreateAPIView.as_view()),
    path('cv_list/', CvListAPIView.as_view()),
    path('contact_create/', ContactCreateAPIView.as_view()),
]