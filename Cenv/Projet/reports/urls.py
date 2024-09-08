from django.urls import path
from . import views
from .views import export_data


urlpatterns = [
    path('reports/', views.report_view, name='report_dashboard'),
    path('reports/<int:report_id>/', views.report_view, name='report_detail'),
    path('export/<str:format>/', export_data, name='export_data'),
     path('reports/history/', views.report_view, name='report_history'),
]