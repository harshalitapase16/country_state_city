from django.urls import path
from .views import *

urlpatterns = [
    path('',Index.as_view(), name='index'),

    path('country/',CountryView.as_view(), name='country'),
    path('country/<int:id>/',CountryView.as_view(), name='country'),
    path('countryupdate/<int:id>/',UpdateCountry.as_view(), name='countryupdate'),
    

    path('state/',StateView.as_view(), name='state'),
    path('stateupdate/<int:id>/',UpdateState.as_view(), name='stateupdate'),
    path('deletestate/<int:id>/',DeleteState.as_view(), name='deletestate'),


    path('city/',CityView.as_view(), name='city'),
    path('cityupdate/<int:city_id>',CityUpdateView.as_view(), name='cityupdate'),
    path('citydelete/<int:city_id>/', CityDeleteView.as_view(), name='citydelete'),
    path('getstate/',get_state, name='getstate')

    
] 