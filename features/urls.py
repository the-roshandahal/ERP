from django.urls import path
from . import views
from django.urls import re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static  

urlpatterns = [

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
