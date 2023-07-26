from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from .models import HousePricing
import csv
from decimal import Decimal, InvalidOperation


def assign_value_based_on_data_type(data_type):
    if data_type == "decimal":
        return Decimal(0)
    elif data_type == "integer":
        return 0
    elif data_type == "string":
        return ""
    elif data_type == "boolean":
        return False
    else:
        return None


def fetch_data_from_csv(filename):
    data = []

    with open(filename, "r") as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Get the headers from the first row
        data_types = []  # Store the data types for each column

        for row in reader:
            filtered_row = []
            for i, item in enumerate(row):
                if item.strip() == "":
                    data_type = data_types[i] if i < len(data_types) else None
                    filtered_row.append(assign_value_based_on_data_type(data_type))
                else:
                    try:
                        item_as_decimal = Decimal(item)
                        filtered_row.append(item_as_decimal)
                        data_types.append("decimal")
                    except (ValueError, InvalidOperation):
                        try:
                            item_as_integer = int(item)
                            filtered_row.append(item_as_integer)
                            data_types.append("integer")
                        except ValueError:
                            filtered_row.append(item)
                            data_types.append("string")
            data.append(filtered_row)

    return data


def SavingData(request):
    csv_filename = "1553768847-housing.csv"
    csv_data = fetch_data_from_csv(csv_filename)

    # Display the fetched data
    for row in csv_data[1:]:
        print(row)
        data = {
            "longitude": row[0],
            "latitude": row[1],
            "housing_median": row[2],
            "total_rooms": row[3],
            "total_bedrooms": row[4],
            "population": row[5],
            "households": row[6],
            "median_income": row[7],
            "ocean_proximity": str(row[8]),
            "median_house_value": row[9],
        }
        print(data)
        HousePricing.objects.create(
            longitude=row[0],
            latitude=row[1],
            housing_median=row[2],
            total_rooms=row[3],
            total_bedrooms=row[4],
            population=row[5],
            households=row[6],
            median_income=row[7],
            ocean_proximity=str(row[8]),
            median_house_value=row[9],
        )
    return HttpResponse("Data Saved Successfully")


class SignupView(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        if password == confirm_password:
            # Create a new user
            user = User.objects.create_user(username=username, email=email, password=password)
            # You may perform additional actions like sending a verification email, etc.
            return redirect('login')  # Replace 'login' with the URL name of your login page

        return render(request, 'signup.html')

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('homepage')  # Replace 'home' with the URL name of your home page
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('homepage')  # Replace 'home' with the URL name of your home page

class homepage(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        data = HousePricing.objects.all()
        return render(request, "homepage.html", {"data": data[:10]})


class getdata(View):
    def get(self, request):
        data = HousePricing.objects.all().values()
        return JsonResponse(list(data[:10]), safe=False)


class sendQuery(View):
    def get(self, request):
        return redirect("homepage")

    # @csrf_exempt
    def post(self, request):
        query = request.POST.get("query")
        if "app_housepricing" in query :
            request.session["query"] = str(query)
            request.session["query_error"] = ""
        else:
            request.session["query_error"] = "Use correct table name for query : '"+str(query)+"'"
            request.session["query"] = ""
        return redirect("homepage")


class QueryResult(View):
    def get(self, request):
        try:
            query = str(request.session["query"])
        except:
            return JsonResponse({"error": "No Query"}, safe=False)
        cursor = connection.cursor()
        query_data = []
        if not query or query == None or query == "":
            return JsonResponse({"error": "No Query"}, safe=False)
        try:
            cursor.execute(query)
            data = cursor.fetchall()
            column_name = []
            for row in cursor.description:
                column_name.append(str(row.name))
                
            for row in data:
                d = dict()
                for i in range(len(column_name)):
                    d[str(column_name[i])] = row[i]
                query_data.append(d)
            return JsonResponse(query_data, safe=False)
        except Exception as e:
            cursor.close
            return JsonResponse({"error": "Unsuccessful Query"}, safe=False)
