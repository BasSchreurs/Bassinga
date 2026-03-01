from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),             # Home page
    path('selection/', views.selection_view, name='selection'),  # Song/scale selection
    path('tuner/', views.tuner_view, name='tuner'),     # Tuner/app page
    path('get-note/', views.get_note, name='get_current_note'),
    path('get-tab/<int:tab_id>/', views.get_tab, name='get_tab'),
]
