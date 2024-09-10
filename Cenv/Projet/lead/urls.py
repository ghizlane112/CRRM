from django.urls import path
from . import views
from .views import LeadListCreate, LeadDetail
from .views import lead_delete



urlpatterns = [
    path('', views.one, name='one'),
    path('two',views.two,name='two'),
    path('three',views.three,name='three'),
    path('four',views.four,name='four'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('leadlist', views.lead_list, name='lead_list'),
    path('lead/<int:pk>/', views.lead_detail, name='lead_detail'),
    path('lead/new/', views.lead_create, name='lead_create'),
    path('lead/import/', views.lead_import, name='lead_import'),
    path('lead/<int:lead_id>/interactions/', views.interaction_list, name='interaction_list'),
    path('lead/<int:lead_id>/interactions/add/', views.add_interaction, name='add_interaction'),
   # path('interaction_list/', views.interaction_list, name='interaction_list'),
    path('api/leads/', LeadListCreate.as_view(), name='lead-list-create'),
    path('lead/<int:pk>/edit/', views.lead_edit, name='lead_edit'),
   #path('lead/<int:id>/add-note/', views.add_note, name='add_note'),
    path('lead/<int:pk>/add-note/', views.add_note, name='add_note'),
   #path('lead/<int:pk>/history/', views.lead_history, name='lead_history'),
    path('lead/history/', views.lead_history, name='lead_history'),
    #path('lead/<int:pk>/history/', views.lead_history, name='lead_history'),
    path('lead/<int:pk>/delete/', lead_delete, name='lead_delete'),
    #path('search/', views.search_view, name='search'),
    path('lead/archive/<int:lead_id>/', views.archive_lead, name='archive_lead'),
    #path('lead/delete/<int:pk>/', views.lead_delete, name='lead_delete'),
    path('api/leads/<int:pk>/', LeadDetail.as_view(), name='lead-detail'),
    path('search/', views.search_view, name='search_view'),
    ]