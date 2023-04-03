from django.urls import path
from .views import UploadCSV

urlpatterns = [
    path('download-csv/', UploadCSV.as_view(), name='upload_csv'),
]