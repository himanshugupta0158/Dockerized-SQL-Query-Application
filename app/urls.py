from django.urls import path
from .views import SavingData, SignupView, homepage, getdata, sendQuery, QueryResult, LoginView, LogoutView

urlpatterns = [
    # path('save_csv_data/',SavingData), # Saving data into database model using CSV file from kaggle
    path('',homepage.as_view(), name="homepage"),
    path('getdata',getdata.as_view(), name="getdata"),
    path('query',sendQuery.as_view(), name="query"),
    path('query_result',QueryResult.as_view(), name="query_result"),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
