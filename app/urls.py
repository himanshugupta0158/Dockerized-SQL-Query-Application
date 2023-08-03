from django.urls import path

from .views import (
    GetSampleData, LoginView, LogoutView, QueryResult, SavingData, SignupView, Homepage, save_countries_data, sendQuery
)

urlpatterns = [
    # URL to save data into the database model using CSV file from Kaggle
    path('save_db_data/', SavingData, name="save_db_data"),

    # URL to save countries data only 
    # path('save_countries',save_countries_data, name="save_countries"),
    
    # Homepage URL
    path('', Homepage.as_view(), name="homepage"),

    # URL to execute a custom query and get the result
    path('query/', sendQuery.as_view(), name="query"),

    # URL to view the result of the executed query
    path('query_result/', QueryResult.as_view(), name="query_result"),

    # URL to fetch sample data from the database
    path('sample_data/', GetSampleData.as_view(), name="sample_data"),

    # URL for user registration/signup
    path('signup/', SignupView.as_view(), name='signup'),

    # URL for user login/signin
    path('login/', LoginView.as_view(), name='login'),

    # URL for user logout/signout
    path('logout/', LogoutView.as_view(), name='logout'),
]

