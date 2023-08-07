

  // function SampleData2() {
  //   var table = document.getElementById("table_body");
  // var request = new XMLHttpRequest();
  // request.open("GET", "/getdata");
  //   request.send();
  //   request.onload = () => {
  //     if (request.status == 200){
  //       data = JSON.parse(request.response);
  //       console.log(data);
  //       console.log("Data refreshed successfully.")
  //       var html = "";
  //       for (let i = 0; i < data.length; i++) {
          
  //         html += "<tr>";
  //         html += "<td>"+data[i].id+"</td>";
  //         html += "<td>"+data[i].longitude+"</td>";
  //         html += "<td>"+data[i].latitude+"</td>";
  //         html += "<td>"+data[i].housing_median+"</td>";
  //         html += "<td>"+data[i].total_rooms+"</td>";
  //         html += "<td>"+data[i].total_bedrooms+"</td>";
  //         html += "<td>"+data[i].population+"</td>";
  //         html += "<td>"+data[i].households+"</td>";
  //         html += "<td>"+data[i].median_income+"</td>";
  //         html += "<td>"+data[i].ocean_proximity+"</td>";
  //         html += "<td>"+data[i].median_house_value+"</td>";
  //         html += "</tr>";

  //         }
  //         table.innerHTML = html;
  //     }
  //   }
  // }

  function Load_Data() {
    // Create a new XMLHttpRequest object
    var request = new XMLHttpRequest();

    // Start loader
    showLoader();

    // Configure the GET request
    request.open('GET', '/save_db_data', true);

    // Set up a callback function for a successful request
    request.onload = function() {
      hideLoader();
      var homePageUrl = "/"; // The URL of your home page (e.g., / or /home/)
      var response = JSON.parse(request.responseText);
      // console.log(response["msg"]);
      window.location.href = homePageUrl;

      // Redirect to the home page URL
      if (request.status == 200 ) {
        // Request was successful
        // Process the response data here (e.g., display or manipulate data)
        // alert('Request successful! ' + response["msg"]);
        console.log('Request successful! ' + response["msg"]);
      } 
      else if (request.status == 409 ){
        // trigger on when status 409 = Data already exist (Conflict).
        // alert(response["msg"]);
        console.log(response["msg"]);
      }
      else {
        // Process the response data here (e.g., display or manipulate data)
        // Request was unsuccessful (e.g., 404, 500, etc.)
        alert('Error: Request failed with status ' + request.status);
      }
    };

    // Set up a callback function for handling errors
    request.onerror = function() {
      // Error occurred during the request
      alert('Error: There was a network error or the request could not be completed.');
    };

    // Send the GET request
    request.send();
  }

function showLoader() {
// Create the loader container and loader element
const loaderContainer = document.createElement('div');
loaderContainer.classList.add('loader-container');

const loader = document.createElement('div');
loader.classList.add('loader');

// Append the loader to the container
loaderContainer.appendChild(loader);

// Append the loader container to the body
document.body.appendChild(loaderContainer);
}

function hideLoader() {
// Remove the loader container from the body
const loaderContainer = document.querySelector('.loader-container');
if (loaderContainer) {
  loaderContainer.remove();
}
}


function SampleData() {
  var table = document.getElementById("sample_table_body");
  var table_header = document.getElementById("sample_table_header");
var request = new XMLHttpRequest();
request.open("GET", "/sample_data");
  request.send();
  request.onload = () => {
    if (request.status == 200){
      data = JSON.parse(request.response);
      var column_names = Object.keys(data[0]);
      console.log("Data refreshed successfully.")

      // For result table Header
      var html = "<tr>";
      for (let i = 0; i < column_names.length; i++) {
        html += "<th scope='col'>"+column_names[i]+"</th>";
      }
      html += "</tr>";
      table_header.innerHTML = html;

      // For Result Table body
      html = "";
      for (let i = 0; i < data.length; i++) {
        var val = Object.values(data[i]);
        html += "<tr>";
          for (let i = 0; i < val.length; i++) {
            html += "<td>"+val[i]+"</td>";
          }
        html += "</tr>";

        }
        table.innerHTML = html;
    }
  }
}

function QueryResult() {
  var table = document.getElementById("Query_result_body");
  var table_header = document.getElementById("Query_result_header");
var request = new XMLHttpRequest();
request.open("GET", "/query_result");
  request.send();
  request.onload = () => {
    if (request.status == 200){
      data = JSON.parse(request.response);
      var column_names = Object.keys(data[0]);
      console.log("Data refreshed successfully.")

      // For result table Header
      var html = "<tr>";
      for (let i = 0; i < column_names.length; i++) {
        html += "<th scope='col'>"+column_names[i]+"</th>";
      }
      html += "</tr>";
      table_header.innerHTML = html;

      // For Result Table body
      html = "";
      for (let i = 0; i < data.length; i++) {
        var val = Object.values(data[i]);
        html += "<tr>";
          for (let i = 0; i < val.length; i++) {
            html += "<td>"+val[i]+"</td>";
          }
        html += "</tr>";

        }
        table.innerHTML = html;
    }
  }
}

// Function to reload the page once
function reloadOnce() {
  // Reload the page
  location.reload();

  // Remove the event listener to prevent further reloads
  window.removeEventListener('load', reloadOnce);
}

var count = true;
SampleData()
QueryResult()

