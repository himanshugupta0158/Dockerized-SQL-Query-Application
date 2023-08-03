import csv
import json
from decimal import Decimal, InvalidOperation

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import Countries_Info, Country_Coorinates, HousePricing


def assign_value_based_on_data_type(data_type):
    """
    Assign default values based on data type.

    Args:
        data_type (str): The data type to determine the default value for.

    Returns:
        Any: The default value based on the data type.
    """
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
    """
    Fetch data from a CSV file.

    Args:
        filename (str): The name of the CSV file.

    Returns:
        list: The list of data read from the CSV file.
    """
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
    """
    Save countries data to the database.

    Returns:
        str: A response message indicating the number of records saved and error count.
    """
    with open("data/countries_spacitial_data.json", "r") as json_file:
        countries_data = json.load(json_file)

    data_saved_counter = 0
    none_value_error_counter = 0

    for data in countries_data:
        print(
            "###############################||Countries Data||####################################"
        )
        print(data)
        print(
            "#####################################################################################"
        )
        try:
            country = data.get("country")
            capital = data.get("capital")
            coordinates = data.get("coordinates")
            area = data.get("area")

            # Handling missing or None values with default values based on data types
            country = country or "Unknown"
            capital = capital or "Unknown"
            # latitude = Decimal(latitude) if latitude is not None else Decimal(0)
            # longitude = Decimal(longitude) if longitude is not None else Decimal(0)
            area = int(area) if area is not None else 0

            # Create a new Countries_Info object and save it to the database
            country_info = Countries_Info(country=country, capital=capital, area=area)
            country_info.save()
            for coordinate in coordinates:
                latitude = (
                    Decimal(coordinate[0]) if coordinate[0] is not None else Decimal(0)
                )
                longitude = (
                    Decimal(coordinate[1]) if coordinate[1] is not None else Decimal(0)
                )
                Country_Coorinates.objects.create(
                    country=country_info,
                    latitude=latitude,
                    longitude=longitude,
                )

            data_saved_counter += 1

        except (KeyError, ValueError, TypeError) as e:
            none_value_error_counter += 1
            print(f"Error processing data: {e}")

    response_message = (
        f"{data_saved_counter} records saved. "
        f"{none_value_error_counter} records had NoneType or None value errors."
    )

    # return HttpResponse(response_message)
    return response_message


def SavingData(request):
    """
    Save data to the database from a CSV file.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        HttpResponse: A response message indicating the success or failure of data saving.
    """
    msg = ""
    exist = False
    if HousePricing.objects.all().exists():
        exist = True
        msg += "Data Already Exist : <br> - HousePricing"
    if Countries_Info.objects.all().exists():
        exist = True
        msg += "<br>- Countries Info "
    if Country_Coorinates.objects.all().exists():
        exist = True
        msg += "<br>- Countries Coordinates "
    print(msg)
    if exist:
        return HttpResponse(msg)

    csv_filename = "data/1553768847-housing.csv"
    csv_data = fetch_data_from_csv(csv_filename)

    # Display the fetched data
    for row in csv_data[1:]:
        print(
            "##################################||House Pricing||#################################"
        )
        print(row)
        print(
            "################################################################################"
        )
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

    data_save_response = (
        "Data Saved Successfully <br> - HousePricing Data Saved. <br> - "
        + save_countries_data()
    )

    return HttpResponse(data_save_response)
    # return redirect("homepage")


class SignupView(View):
    def get(self, request):
        """
        Render the signup.html template for GET requests.

        Returns:
            HttpResponse: Rendered template for signup page.
        """
        return render(request, "signup.html")

    def post(self, request):
        """
        Handle the user signup for POST requests.

        Args:
            request (HttpRequest): The POST request containing user signup data.

        Returns:
            HttpResponse: Redirects to the login page upon successful signup.
                        Rendered template with error message on failed signup.
        """
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm-password")
        if password == confirm_password:
            # Create a new user
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            # You may perform additional actions like sending a verification email, etc.
            return redirect(
                "login"
            )  # Replace 'login' with the URL name of your login page

        return render(request, "signup.html")


class LoginView(View):
    def get(self, request):
        """
        Render the login.html template for GET requests.

        Returns:
            HttpResponse: Rendered template for login page.
        """
        return render(request, "login.html")

    def post(self, request):
        """
        Handle user login for POST requests.

        Args:
            request (HttpRequest): The POST request containing user login data.

        Returns:
            HttpResponse: Redirects to the homepage upon successful login.
                        Rendered template with error message on failed login.
        """
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(
                "homepage"
            )  # Replace 'home' with the URL name of your home page
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})


class LogoutView(View):
    def get(self, request):
        """
        Handle user logout for GET requests.

        Args:
            request (HttpRequest): The GET request for user logout.

        Returns:
            HttpResponse: Redirects to the homepage after logout.
        """
        logout(request)
        return redirect(
            "homepage"
        )  # Replace 'home' with the URL name of your home page


class Homepage(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        """
        Dispatch method to enforce login_required decorator for the view.

        Args:
            *args: Arguments passed to the dispatch method.
            **kwargs: Keyword arguments passed to the dispatch method.

        Returns:
            HttpResponse: Rendered template for the homepage.
        """
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        """
        Render the homepage.html template for GET requests.

        Returns:
            HttpResponse: Rendered template for the homepage.
        """
        # data = HousePricing.objects.all()
        # return render(request, "homepage.html", {"data": data[:10]})
        return render(request, "homepage.html")


class sendQuery(View):
    def get(self, request):
        """
        Process the GET request for this view.

        Args:
            request (HttpRequest): The HTTP request.

        Returns:
            HttpResponseRedirect: Redirects to the homepage.
        """
        return redirect("homepage")

    def post(self, request):
        """
        Process the POST request containing a database query.

        Args:
            request (HttpRequest): The HTTP request containing the query.

        Returns:
            HttpResponseRedirect: Redirects to the homepage.
        """
        query = request.POST.get("query")
        user = self.request.user
        request.session["query"] = str(query)
        request.session["query_error"] = ""
        request.session["query_alert"] = ""

        # Define different levels of database query commands
        staff_level = ["Create", "INSERT", "Update", "Alter"]
        admin_level = ["Delete", "Drop", "Remove", "Truncate", "Grant", "Revoke", "@"]

        # Convert the query into a list of capitalized words
        query_lst = [str(i).capitalize() for i in str(query).split(" ")]
        print(query_lst)
        is_staff_lvl = False
        is_admin_lvl = False

        # Check if the query contains staff-level commands
        for i in staff_level:
            if i in query_lst:
                is_staff_lvl = True
                print("Staff True")
                break

        if is_staff_lvl:
            # Check if the user is a staff member and has permission for staff-level commands
            for i in admin_level:  # Check if the query contains admin-level commands
                if i in query_lst:
                    is_admin_lvl = True
                    break

        if is_staff_lvl:
            if not user.is_staff:
                # User is not a staff member, raise a permission error
                request.session[
                    "query_error"
                ] = "Permission Error: You do not have access to Create, Add, Update, or Alter table data"
                request.session["query_alert"] = ""
                request.session["query"] = ""
                # return render(request, "homepage.html", {"error" : "Permission Error: You do not have access to Create, Add, Update, or Alter table data"})

        if is_admin_lvl:
            if not user.is_superuser:
                # User is not an admin, raise a permission error
                request.session[
                    "query_error"
                ] = "Permission Error: You do not have access to Delete, Remove, or perform User Privileges queries to table data"
                request.session["query_alert"] = ""
                request.session["query"] = ""
                # return render(request, "homepage.html", {"error" : "Permission Error: You do not have access to Delete, Remove, or perform User Privileges queries to table data"})

        return redirect("homepage")


class GetSampleData(View):
    def get(self, request):
        """
        Process the GET request to fetch sample data (10 Rows) from the database.

        Args:
            request (HttpRequest): The HTTP request.

        Returns:
            JsonResponse: JSON response containing sample data fetched from the database.
        """
        query = "select * from app_housepricing limit 10;"
        cursor = connection.cursor()
        query_data = []
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
        """
        Process the GET request to fetch query results from the database.

        Args:
            request (HttpRequest): The HTTP request containing the database query.

        Returns:
            JsonResponse: JSON response containing query results fetched from the database.
        """
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

def load_nyc_census_sociodata(request):
    pass