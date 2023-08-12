from django.urls import path

from .views import (
    CreateSuperUserView, Get_All_Country_Data, Get_NYC_Data, GetSampleData, LoadShapeData, LoginView, LogoutView, PostFilesData, QueryResult, SQLDumping, SavingData, SignupView, Homepage, save_countries_data, sendQuery, Get_Country_Data
)

urlpatterns = [
    # URL to save data into the database model using CSV file from Kaggle
    path('save_db_data/', SavingData, name="save_db_data"),

    # URL to create super User
    path('create_admin',CreateSuperUserView.as_view(), name="create_admin"),
    
    # URL to save countries data only 
    # path('save_countries',save_countries_data, name="save_countries"),

    # Get NYC Related DB datas
    path('get_nyc_data',Get_NYC_Data.as_view(), name="get_nyc_data"),
    
    # URL to get countries related data both Get and Post request
    path('get_all_country_data',Get_All_Country_Data.as_view(), name="get_country_data"),
    path('get_country_data/<str:name>',Get_Country_Data.as_view(), name="get_country_data"),
    
    # Homepage URL
    path('', Homepage.as_view(), name="homepage"),
    path('<str:table_name>', Homepage.as_view(), name="load_sample_data"),

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

    path('SendData/', PostFilesData.as_view(), name='SendData'),

    path('sql_dumping/', SQLDumping.as_view(), name='sql_dumping'),

    path('load_shape_data/', LoadShapeData, name='load_shape_data'),
]

