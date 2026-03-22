from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import os

urlpatterns = [
    path('admin/', admin.site.urls),  
    path('', include('dashboard.urls')),
]



if settings.DEBUG:
    # Путь к вашей папке dist
    dist_path = os.path.join(settings.BASE_DIR, 'tangem-project/dist')
    
    # 1. Позволяем Django отдавать статику (картинки, стили) по путям без /static/
    urlpatterns += static('/assets/', document_root=os.path.join(dist_path, 'assets'))
    
    # 2. На всякий случай разрешаем корень dist
    urlpatterns += static('/', document_root=dist_path)