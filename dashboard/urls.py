from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('docs/', views.documentation, name='docs'),
    path('export/', views.export_excel, name='export'),
    path('export/pdf/', views.export_pdf, name='export_pdf'),
]