# urls.py
from django.urls import path
from .views import ApartmentCreateView, ApartmentListView, ApartmentDetailView, ApartmentUpdateView, \
    MyApartmentsListView

urlpatterns = [
    path('apartments/', ApartmentListView.as_view(), name='apartment-list'),
    path('my-apartments/', MyApartmentsListView.as_view(), name='my-apartments-list'),
    path('apartments/<int:pk>/update/', ApartmentUpdateView.as_view(), name='apartment-update'),
    path('apartments/create/', ApartmentCreateView.as_view(), name='apartment-create'),
    path('apartments/<int:pk>/', ApartmentDetailView.as_view(), name='apartment-detail'),
]
