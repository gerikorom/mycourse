from django.urls import path
from . import views

from django.views.generic import TemplateView

app_name = 'proapp'

urlpatterns = [
    path('', views.kezdolap, name='kezdolap'),
    path('konyvek/', views.konyvek, name='konyvek'),
    path('konyvfelvetel/', views.konyvfelvetel, name='konyvfelvetel'),
    path('kolcsonzes/', views.kolcsonzes, name='kolcsonzes'),
    path('konyv/<int:id>/', views.konyv, name='konyv'),
    path('konyvar/<int:ar>/', views.konyvar, name='konyvar'),
    path('konyvlista/', views.KonyvListView.as_view(), name='konyvlista'),
    path('konyvhozzaadas/', views.KonyvCreateView.as_view(), name='konyvhozzaadas'),
    path('konyv2/<int:pk>/', views.KonyvDetailView.as_view(), name='konyvclass'),
    path('zoldseg/', views.zoldseg, name='zoldseg'),
    path('konyv-feltoltes/', views.book_upload_view, name='feltoltes'),
    path('excellekeres/', views.excel_lekeres, name='excellekeres'),
    path('wordlekeres/', views.word_lekeres, name='wordlekeres'),
    path('pdflekeres/', views.pdf_lekeres, name='pdflekeres'),
    path('estek/', views.estek, name='estek'),
    path('kapcsolat/', TemplateView.as_view(template_name='kapcsolat.html'), name='kapcsolat'),
    path('muzeum/', TemplateView.as_view(template_name='muzeum.html'), name='muzeum'),
    path('regisztracio/', views.regisztracio, name='regisztracio'),

]