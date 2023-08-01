from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from .models import HousePricing, Countries_Info
import csv, json
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


def save_countries_data():
    with open("countries_data.json", "r") as json_file:
        countries_data = json.load(json_file)

    data_saved_counter = 0
    none_value_error_counter = 0

    for data in countries_data:
        try:
            country = data.get("country")
            capital = data.get("capital")
            latitude = data.get("latitude")
            longitude = data.get("longitude")
            area = data.get("area")

            # Handling missing or None values with default values based on data types
            country = country or "Unknown"
            capital = capital or "Unknown"
            latitude = Decimal(latitude) if latitude is not None else Decimal(0)
            longitude = Decimal(longitude) if longitude is not None else Decimal(0)
            area = int(area) if area is not None else 0

            # Create a new Countries_Info object and save it to the database
            Countries_Info.objects.create(
                country=country,
                capital=capital,
                latitude=latitude,
                longitude=longitude,
                area=area
            )
            data_saved_counter += 1

        except (KeyError, ValueError, TypeError) as e:
            none_value_error_counter += 1
            print(f"Error processing data: {e}")

    response_message = f"{data_saved_counter} records saved. " \
                       f"{none_value_error_counter} records had NoneType or None value errors."

    # return HttpResponse(response_message)
    return response_message

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
    
    data_save_response = "Data Saved Successfully <br> - HousePricing Data Saved. <br> - "+save_countries_data() 
    

    return HttpResponse(data_save_response)
    # return redirect("homepage")


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
        # data = HousePricing.objects.all()
        # return render(request, "homepage.html", {"data": data[:10]})
        return render(request, "homepage.html") 


# class getdata(View):
#     def get(self, request):
#         data = HousePricing.objects.all().values()
#         return JsonResponse(list(data[:10]), safe=False)


class sendQuery(View):
    def get(self, request):
        return redirect("homepage")

    # @csrf_exempt
    def post(self, request):
        query = request.POST.get("query")
        user = self.request.user
        request.session["query"] = str(query)
        request.session["query_error"] = ""
        request.session["query_alert"] = ""
        

        staff_level = ["Create","INSERT","Update", "Alter"]
        admin_level = ["Delete","Drop","Remove", "Truncate", "Grant", "Revoke","@"]
        query_lst = [str(i).capitalize() for i in str(query).split(" ")]
        print(query_lst)
        is_staff_lvl = False
        is_admin_lvl = False

        for i in staff_level:
            if i in query_lst:
                is_staff_lvl = True
                print("Staff True")
                break

        if is_staff_lvl:
            for i in admin_level:
                if i in query_lst:
                    is_admin_lvl = True
                    break

        if is_staff_lvl:
            if user.is_staff == False :
                request.session["query_error"] = "Permission Error : You Do not have access to Create, Add, Update or Alter table data"
                request.session["query_alert"] = ""
                request.session["query"] = ""
                # return render(request, "homepage.html", {"error" : "Permission Error : You Do not have access to Create, Add, Update or Alter table data"})

        if is_admin_lvl :
            if user.is_superuser == False :
                request.session["query_error"] = "Permission Error : You Do not have access to Delete, Remove or do User Privilages queries to table data"
                request.session["query_alert"] = ""
                request.session["query"] = ""
                # return render(request, "homepage.html", {"error" : "Permission Error : You Do not have access to Delete, Remove or do User Privilages queries to table data"})

        return redirect("homepage")



class GetSampleData(View):
    def get(self, request):
        try:
            query = "select * from app_housepricing limit 10;"
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
            print("Error occurred:", str(e))
            request.session["sample_query_error"] = str(e)
            # request.session["query_error"] = ""
            cursor.close
            return JsonResponse({"error": "Unsuccessful Query"}, safe=False)
        
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
            print("Error occurred:", str(e))
            request.session["query_alert"] = str(e)
            # request.session["query_error"] = ""
            cursor.close
            return JsonResponse({"error": "Unsuccessful Query"}, safe=False)
