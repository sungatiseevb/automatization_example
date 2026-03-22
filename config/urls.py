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
    dist_path = os.path.join(settings.BASE_DIR, 'tangem-project/dist')
    
    urlpatterns += static('/assets/', document_root=os.path.join(dist_path, 'assets'))
    
    urlpatterns += static('/', document_root=dist_path)