 // Set today's date as the default value
 document.getElementById('todayDate').valueAsDate = new Date();
            
                
 document.addEventListener('DOMContentLoaded', function() {
         // Fetch data from the Flask endpoint
         fetch('/get_airlines_and_agents')
             .then(response => response.json())
             .then(data => {

                 
                 // Populate Airlines dropdown
                 var airlinesDropdown = document.getElementById('airlinesDropdown');

                 var defaultOption = document.createElement("option");
                 defaultOption.value = "";
                 defaultOption.text = "Select One"; // or any label you prefer
                 airlinesDropdown.add(defaultOption);


                 data.airlineName.forEach(agent => {
                     var option = document.createElement('option');
                     option.value = agent;
                     option.text = agent;
                     airlinesDropdown.add(option);
                 });

                 // Populate Travel Agents dropdown
                 var agentsDropdown = document.getElementById('agentsDropdown');
                 var defaultOption = document.createElement("option");
                 defaultOption.value = "";
                 defaultOption.text = "Select One"; // or any label you prefer
                 agentsDropdown.add(defaultOption);


                 data.travel_agents.forEach(agent => {
                     var option = document.createElement('option');
                     option.value = agent;
                     option.text = agent;
                     agentsDropdown.add(option);
                 });

                 // Populate Travel Flightnum dropdown
                 var flightNumbersDropdown = document.getElementById('flightNumbersDropdown');
                 var defaultOption = document.createElement("option");
                 defaultOption.value = "";
                 defaultOption.text = "Select One"; // or any label you prefer
                 flightNumbersDropdown.add(defaultOption);


                 data.flight_numbers.forEach(flightNum => {
                     var option = document.createElement('option');
                     option.value = flightNum;
                     option.text = flightNum;
                     flightNumbersDropdown.add(option);
                 });
             })
             .catch(error => console.error('Error fetching data:', error));
     });

