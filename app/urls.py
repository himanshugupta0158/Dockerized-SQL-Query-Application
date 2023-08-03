from django.urls import path

from .views import (GetSampleData, LoginView, LogoutView, QueryResult,
                    SavingData, SignupView, Homepage, save_countries_data,
                    sendQuery)

urlpatterns = [
    path('save_db_data',SavingData, name="save_db_data"), # Saving data into database model using CSV file from kaggle
    # path('save_countries',save_countries_data, name="save_countries"), # Saving data into database model using CSV file from kaggle
    path('',Homepage.as_view(), name="homepage"),
    # path('getdata',getdata.as_view(), name="getdata"),
    path('query',sendQuery.as_view(), name="query"),
    path('query_result',QueryResult.as_view(), name="query_result"),
    path('sample_data',GetSampleData.as_view(), name="sample_data"),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
