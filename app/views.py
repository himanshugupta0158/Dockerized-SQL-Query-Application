import csv
import json
from decimal import Decimal, InvalidOperation
import random
from django.conf import Settings, settings

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import psycopg2

from rest_framework.views import APIView

from .models import (
    Countries_Info,
    Country_Coorinates,
    HousePricing,
    Nyc_Coordinates,
    NycData,
    UploadFileData,
    UploadedSQLData,
)
from .shp_shx_extraction import shp_shx_data_extraction
from .sql_loading_script import Run_SQL_Script


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


# def insert_data_in_NYCCensusSociodata():
#     # Generate and insert 500 or 1000 rows of sample data
#     for _ in range(random.randint(500,1000)):  # Change to 1000 for 1000 rows
#         data = {
#             'tractid': str(random.randint(30000000000, 39999999999)),
#             'transit_total': random.randint(500, 5000),
#             'transit_private': random.randint(100, 1000),
#             'transit_public': random.randint(300, 2000),
#             'transit_walk': random.randint(10, 100),
#             'transit_other': random.randint(0, 50),
#             'transit_none': random.randint(0, 10),
#             'transit_time_mins': random.uniform(10, 120),
#             'family_count': random.randint(500, 5000),
#             'family_income_median': random.randint(10000, 50000),
#             'family_income_mean': random.randint(20000, 70000),
#             'family_income_aggregate': random.randint(1000000, 1000000000),
#             'edu_total': random.randint(1000, 10000),
#             'edu_no_highschool_dipl': random.randint(100, 1000),
#             'edu_highschool_dipl': random.randint(200, 1500),
#             'edu_college_dipl': random.randint(100, 1000),
#             'edu_graduate_dipl': random.randint(10, 100),
#         }
#         NYCCensusSociodata.objects.create(**data)

#     return str("Data Successfully saved in NYCCensusSociodata Table")


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
        msg += "Data Already Exist : \n - HousePricing"
    if Countries_Info.objects.all().exists():
        exist = True
        msg += "\n- Countries Info "
    if Country_Coorinates.objects.all().exists():
        exist = True
        msg += "\n- Countries Coordinates "
    # if NYCCensusSociodata.objects.all().exists():
    #     exist = True
    #     msg += "\n- NYCCensusSociodata "
    print(msg)
    if exist:
        # return HttpResponse(msg)
        return JsonResponse({"msg": msg}, status=409)

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

    msg1 = save_countries_data()
    # msg2 = insert_data_in_NYCCensusSociodata()
    data_save_response = (
        "Data Saved Successfully \n - HousePricing Data Saved. \n - " + msg1
    )

    return JsonResponse({"msg": data_save_response}, status=200)
    # return redirect("homepage")


class CreateSuperUserView(View):
    """
    View to create a superuser.

    Parameters:
        request: The HTTP request object.

    Returns:
        A redirect to the homepage.
    """

    def get(self, request):
        """
        Handles GET requests.

        Checks if the superuser already exists. If it does, prints a message.
        If it doesn't, creates the superuser and prints a message.

        Returns:
            A redirect to the homepage.
        """
        # Replace with your desired username, email, and password
        username = "admin"
        email = "admin@gmail.com"
        password = "1234"

        # Check if the superuser already exists
        if User.objects.filter(username=username).exists():
            print("Superuser already exists.")
        else:
            # Create the superuser
            User.objects.create_superuser(
                username=username, email=email, password=password
            )
            print("Superuser created successfully.")
        return redirect("homepage")


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


def DbTableList():
    """
    Functions Working :
    # This function retrieves a list of user tables from a PostgreSQL database's 'public' schema.
    # It filters out specific system-related table names.
    # The function doesn't take any explicit input parameters.
    # It returns a list containing the names of user tables and a status indicator (1 for success, 0 for failure).
    """

    try:
        # Create a cursor for database operations
        cursor = connection.cursor()

        # SQL query to fetch a list of tables in the 'public' schema
        query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public';
        """
        cursor.execute(query)
        tables = cursor.fetchall()

        # Initialize an empty list to store names of user tables
        db_tables = []

        # Iterate through the fetched tables
        for table in tables:
            # Exclude certain table names that are likely system-related
            if (
                "django" in str(table[0])
                or "auth" in str(table[0])
                or "app_uploadedsqldata" in str(table[0])
                or "app_shapefiledata" in str(table[0])
                or "app_uploadfiledata" in str(table[0])
            ):
                continue
            db_tables.append(table[0])  # Add the table name to the list

        # Commit the transaction to the database
        connection.commit()

        # Close the cursor if the database connection is open
        if connection:
            cursor.close()

        # Return a list of user tables and a success indicator
        return [db_tables, 1]

    except (Exception, psycopg2.Error) as error:
        # If an exception occurs, print an error message and return an error indicator
        print("Error:", error)
        return [error, 0]


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

        request.session["Sample_table_name"] = "app_housepricing"

        response = DbTableList()
        if response[1]:
            return render(request, "homepage.html", {"table_list": response[0]})
        else:
            return render(request, "homepage.html")

    def post(self, request):
        table_name = request.POST.get("Input_Table_Name")
        if table_name:
            print(table_name)
            request.session["Sample_table_name"] = str(table_name)
        else:
            request.session["Sample_table_name"] = "app_housepricing"

        response = DbTableList()
        if response[1]:
            return render(request, "homepage.html", {"table_list": response[0]})
        else:
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


# class GetSampleData(View):
class GetSampleData(APIView):
    def get(self, request):
        """
        Process the GET request to fetch sample data (10 Rows) from the database.

        Args:
            request (HttpRequest): The HTTP request.

        Returns:
            JsonResponse: JSON response containing sample data fetched from the database.
        """
        table_name = str(request.session.get("Sample_table_name"))
        # print(f"Table Name to show : {table_name}")
        query = f"select * from {table_name} limit 10;"
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
            print(row)
            return JsonResponse(query_data, safe=False)
        except Exception as e:
            print("Error occurred:", str(e))
            request.session["sample_query_error"] = str(e)
            # request.session["query_error"] = ""
            cursor.close
            return JsonResponse(
                {"error": f"Unsuccessful Query on table {table_name}"}, safe=False
            )


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


class PostFilesData(View):
    def get(self, request):
        """
        Handles HTTP GET requests for the PostFilesData view.

        Parameters:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: Renders the 'upload.html' template.
        """
        return render(request, "upload.html")

    def post(self, request):
        """
        Handles HTTP POST requests for the PostFilesData view.

        Parameters:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: Redirects to the 'load_shape_data' view after processing.
        """
        # Retrieve uploaded files and form data from the request
        dbf_file = request.FILES.get("dbf_file_input")
        shp_file = request.FILES.get("shp_file_input")
        shx_file = request.FILES.get("shx_file_input")
        db_selected = request.POST.get("db_selected")

        # print(request.FILES)

        # Create an UploadFileData object and save it to the database
        data = UploadFileData(
            dbf_file=dbf_file,
            shp_file=shp_file,
            shx_file=shx_file,
            database_name=db_selected,
        )

        data.save()

        # Store the ID of the uploaded shape data in the session
        request.session["shape_data_id_to_load_data"] = int(data.id)

        print(data)

        response = dict(
            {
                "shp_file": data.shp_file,
                "shx_file": data.shx_file,
                "database_name": data.database_name,
            }
        )
        print(response)
        return redirect("load_shape_data")


def LoadShapeData(request):
    """
    Working :
    # This function loads shape data from SHP and SHX files into the database.
    # It expects a session key "shape_data_id_to_load_data" to be set with the ID of the shape data to load.
    # The function iterates through the extracted features, creates NycData and Nyc_Coordinates objects,
    # and marks the shape data as loaded.
    # After processing, the function redirects to the "homepage".
    """
    try:
        # Extract the shape data's ID from the session and remove it from the session
        id = int(request.session["shape_data_id_to_load_data"])
        del request.session["shape_data_id_to_load_data"]

        # Retrieve the shape data object based on the extracted ID
        shape_data = UploadFileData.objects.get(id=id)

        # Define paths to the SHP and SHX files
        shp_file_path = "media/" + str(shape_data.shp_file)
        shx_file_path = "media/" + str(shape_data.shx_file)

        # Extract data from SHP and SHX files
        datas = shp_shx_data_extraction(
            shp_file_path=shp_file_path, shx_file_path=shx_file_path
        )

        # Iterate through extracted features and store data in the database
        for data in datas["features"]:

            # Create a new NycData object with extracted properties
            nyc_data = NycData.objects.create(
                BLKID=str(data["properties"]["BLKID"]),
                POPN_TOTAL=int(data["properties"]["POPN_TOTAL"]),
                POPN_WHITE=int(data["properties"]["POPN_WHITE"]),
                POPN_BLACK=int(data["properties"]["POPN_BLACK"]),
                POPN_NATIV=int(data["properties"]["POPN_NATIV"]),
                POPN_ASIAN=int(data["properties"]["POPN_ASIAN"]),
                POPN_OTHER=int(data["properties"]["POPN_OTHER"]),
                BORONAME=str(data["properties"]["BORONAME"]),
            )
            # print(nyc_data)

            # Iterate through coordinates and create Nyc_Coordinates objects
            for coord in data["geometry"]["coordinates"][0]:
                try:
                    coord = list(coord)
                    new_nyc_coord = Nyc_Coordinates(
                        nyc_data=nyc_data, x_coord=coord[0], y_coord=coord[1]
                    )
                    new_nyc_coord.save()
                except:
                    coord = list(coord[0])
                    new_nyc_coord = Nyc_Coordinates(
                        nyc_data=nyc_data, x_coord=coord[0], y_coord=coord[1]
                    )
                    new_nyc_coord.save()

                # print(coord)
            # Mark the shape data as loaded and save changes
            shape_data.is_loaded = True
            shape_data.save()
    except Exception as e:
        print(f"Error : {e}")

    # Redirect to the homepage after processing
    return redirect("homepage")


class SQLDumping(View):
    """
    WORKING :
    # This view class handles SQL dumping functionality in a Django web application.
    # It supports both GET and POST HTTP methods.
    # - For GET requests, it renders the 'sql_dumping.html' template.
    # - For POST requests, it processes an uploaded SQL file, runs its script, updates the database accordingly,
    #   and renders the 'sql_dumping.html' template with a message indicating the script execution result.
    """

    def get(self, request):
        """
        Handles HTTP GET requests for the SQLDumping view.

        Parameters:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: Renders the 'sql_dumping.html' template.
        """
        return render(request, "sql_dumping.html")

    def post(self, request):
        """
        Handles HTTP POST requests for the SQLDumping view.

        Parameters:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: Renders the 'sql_dumping.html' template with a message about the script execution.
        """
        # Retrieve the uploaded SQL file from the POST request
        sql_file = request.FILES.get("sql_file_input")

        # Create an UploadedSQLData object and get its associated data
        data = UploadedSQLData.objects.get(
            id=UploadedSQLData.objects.create(sql_file=sql_file).id
        )

        # Define the path to the uploaded SQL file
        sql_file_path = "media/" + str(data.sql_file)

        # Run the SQL script using a utility function
        response = Run_SQL_Script(sql_file_path)

        # Print the response for debugging purposes
        print(response)

        # Update the 'is_loaded' attribute of the UploadedSQLData object if the script executed successfully
        if response[1]:
            data.is_loaded = True

        # Render the 'sql_dumping.html' template with a message about the script execution
        return render(request, "sql_dumping.html", {"msg": response[0]})


""" ##################################### APIs ###############################################"""


class Get_NYC_Data(View):
    """
    GET API to retrieve all NYC data.

    Returns:
    - JsonResponse: JSON response containing all country data.
    """

    def get(self, request):
        nycs = NycData.objects.all()
        data = []
        for nyc_info in nycs:
            nyc_data = {
                "BLKID": nyc_info.BLKID,
                "POPN_TOTAL": nyc_info.POPN_TOTAL,
                "POPN_WHITE": nyc_info.POPN_WHITE,
                "POPN_BLACK": nyc_info.POPN_BLACK,
                "POPN_NATIV": nyc_info.POPN_NATIV,
                "POPN_ASIAN": nyc_info.POPN_ASIAN,
                "POPN_OTHER": nyc_info.POPN_OTHER,
                "BORONAME": nyc_info.BORONAME,
                "coordinates": [],
            }
            coordinates = Nyc_Coordinates.objects.filter(nyc_data=nyc_info)
            for coordinate in coordinates:
                nyc_data["coordinates"].append([coordinate.x_coord, coordinate.y_coord])
            data.append(nyc_data)

        return JsonResponse(data, safe=False)


class Get_All_Country_Data(View):
    """
    GET API to retrieve all country data.

    Returns:
    - JsonResponse: JSON response containing all country data.
    """

    def get(self, request):
        countries = Countries_Info.objects.all()
        data = []
        for country_info in countries:
            country_data = {
                "country": country_info.country,
                "capital": country_info.capital,
                "area": country_info.area,
                "coordinates": [],
            }
            coordinates = Country_Coorinates.objects.filter(country=country_info)
            for coordinate in coordinates:
                country_data["coordinates"].append(
                    [coordinate.latitude, coordinate.longitude]
                )
            data.append(country_data)

        return JsonResponse(data, safe=False)


class Get_Country_Data(View):
    """
    GET API to retrieve specific country data based on the country name.

    Parameters passed in URL:
    - name (str): The name of the country.

    Returns:
    - JsonResponse: JSON response containing specific country data.
    """

    def get(self, request, name):
        try:
            country_info = Countries_Info.objects.get(country=name)
        except Countries_Info.DoesNotExist:
            return JsonResponse({"error": "Country not found"}, status=404)

        country_data = {
            "country": country_info.country,
            "capital": country_info.capital,
            "area": country_info.area,
            "coordinates": [],
        }
        coordinates = Country_Coorinates.objects.filter(country=country_info)
        for coordinate in coordinates:
            country_data["coordinates"].append(
                [coordinate.latitude, coordinate.longitude]
            )

        return JsonResponse(country_data, safe=False)
