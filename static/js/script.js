document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('todayDate').valueAsDate = new Date();
    var codeInput = document.getElementById('code');
    codeInput.focus();
    var seatNumberInput = document.getElementById('seatNumber');

    // Attach an event listener to the blur event
    codeInput.addEventListener('blur', function() {
        // Clear the value of the input field
        codeInput.value = '';

        seatNumberInput.focus();
    });
    // Function to calculate amounts
    function calculateAmounts() {
        var currencyType = document.getElementById('currencyType').value;
        var adultPax = parseFloat(document.getElementById('adultPax').value) || 0;
        var kidPax = parseFloat(document.getElementById('kidPax').value) || 0;
        var adultrate = parseFloat(document.getElementById('adultrate').value) || 0;
        var kidrate = parseFloat(document.getElementById('kidrate').value) || 0;
        var adultrateMVR = parseFloat(document.getElementById('adultrateMVR').value) || 0;
        var kidrateMVR = parseFloat(document.getElementById('kidrateMVR').value) || 0;
        var givenAmount = parseFloat(document.getElementById('givenAmount').value) || 0;
        var GSTRate1 = parseFloat(document.getElementById('GSTRate1').value) || 0;
        var paymentType = document.getElementById('paymentType').value;
        var paymentTypeField = document.getElementById('paymentType');
        var currencyTypeField = document.getElementById('currencyType');
        var paxNameField = document.getElementById('paxName');
        var codeInput = document.getElementById('code');
        var airlineNameInput = document.getElementById('airlineName');
        var flightNumberInput = document.getElementById('flightNumber');
        var seatNumberInput = document.getElementById('seatNumber');
        

       
        //document.getElementById('airlineName').value = airline_Name;
        
                    // Get values from input fields
                  
        
        
        // Choose the appropriate rate based on the currencyType
        var lowerCurrencyType = currencyType.toLowerCase();
        var selectedRate = (lowerCurrencyType === 'mvr') ? adultrateMVR : adultrate;
        var selectedRatekID = (lowerCurrencyType === 'mvr') ? kidrateMVR : kidrate;
        

        // Calculate amounts
        var adultAmount = adultPax * selectedRate;
        var kidAmount = kidPax * selectedRatekID;
        //var adultAmount = adultPax * adultrate;
        //var kidAmount = kidPax * kidrate;

        // Update the corresponding input fields
        
        document.getElementById('adultAmount').value = adultAmount.toFixed(2);
        document.getElementById('kidAmount').value = kidAmount.toFixed(2);

        // Calculate and update the totalAmount
        var totalAmount = adultAmount + kidAmount;
        document.getElementById('totalAmount').value = totalAmount.toFixed(2);


         // Calculate and update adultGST
        var adultGST = (GSTRate1 / 100) * adultAmount;
        document.getElementById('adultGST').value = adultGST.toFixed(2);

        // Calculate and update KidGST
        var kidGST = (GSTRate1 / 100) * kidAmount;
        document.getElementById('kidGST').value = kidGST.toFixed(2);

        // Update the visibility of givenAmount and balanceAmount based on paymentType
        var givenAmountField = document.getElementById('givenAmount');
        var balanceAmountField = document.getElementById('balanceAmount');
       


        if (paymentType !== 'CASH') {
            givenAmountField.style.display = 'none';
            balanceAmountField.style.display = 'none';
           
        } else {
            givenAmountField.style.display = 'block';
            balanceAmountField.style.display = 'block';
            
        }

         // Calculate and update the balanceAmount
        var balanceAmount = givenAmount - totalAmount;
        document.getElementById('balanceAmount').value = balanceAmount.toFixed(2);


        

        // Convert paymentType to uppercase
        paymentTypeField.value = paymentType.toUpperCase();
        currencyTypeField.value = currencyType.toUpperCase();
        


    }

    function calculateAmounts1() {
        var paxNameField = document.getElementById('paxName');
        var codeInput = document.getElementById('code');
        var airlineNameInput = document.getElementById('airlineName');
        var flightNumberInput = document.getElementById('flightNumber');
        var seatNumberInput = document.getElementById('seatNumber');
        

        // Parse flight code
        var codeValue = codeInput.value;
        var code = codeValue.split(/\s{2,}/);
        var paxName = code[0].substring(2);
        var code1 = code[1];
        var code2 = code1.split(/\s+/);
        var flightNumber1 = code2[1] + code2[2];
        var flightNumber = flightNumber1.substring(6);
        var seatNumber = code2[3].slice(5, -4);
        var airlineName1 = code2[1].substring(6);
        
        // Update input fields with the extracted flight information
        paxNameField.value = paxName;
        flightNumberInput.value = flightNumber;
        seatNumberInput.value = seatNumber;

        var airlineName1Field = document.getElementById('airlineName1');
        var airlineName2 = airlineName1Field.value = airlineName1.toUpperCase();
        
        if (airlineName2 === "BA") {
            airlineNameInput.value = "BRITISH AIRWAYS";
        } else if (airlineName2 === "QR") {
            airlineNameInput.value = "QATAR AIRWAYS";
        } else if (airlineName2 === "SQ") {
            airlineNameInput.value = "SINGAPORE AIRLINES";
        } else if (airlineName2 === "AK") {
            airlineNameInput.value = "AIR ASIA";
        } else if (airlineName2 === "EK") {
            airlineNameInput.value = "EMIRATES";
        } else if (airlineName2 === "PG") {
            airlineNameInput.value = "BANGKOK AIRWAYS";
        } else if (airlineName2 === "GF") {
            airlineNameInput.value = "GULF AIR";
        } else if (airlineName2 === "VS") {
            airlineNameInput.value = "VIRGIN ATLANTIC";
        } else if (airlineName2 === "EY") {
            airlineNameInput.value = "ETIHAD AIRWAYS";
        } else if (airlineName2 === "WK") {
            airlineNameInput.value = "EDELWEISS";
        } else if (airlineName2 === "Q2") {
            airlineNameInput.value = "MALDIVIAN";
        } else if (airlineName2 === "UL") {
            airlineNameInput.value = "SRILANKAN AIRLINES";
        } else if (airlineName2 === "6E") {
            airlineNameInput.value = "INDIGO";
        } else if (airlineName2 === "WY") {
            airlineNameInput.value = "OMAN AIR";
        } else {
            airlineNameInput.value = "Unknown";
}

        // Determine airline name based on the airline code
        var paxNameField = document.getElementById('paxName');
        paxNameField.value = paxName.toUpperCase();
        var flightNumberField = document.getElementById('flightNumber');
        flightNumberField.value = flightNumber.toUpperCase();
        var seatNumberField = document.getElementById('seatNumber');
        seatNumberField.value = seatNumber.toUpperCase();
        var airlineNameField = document.getElementById('airlineName');
        airlineNameField.value = airlineName.toUpperCase();
        var codeInput = document.getElementById('code');
        // Attach an event listener to the blur event
        codeInput.addEventListener('blur', function() {
            // Clear the value of the input field
            codeInput.value = '';
        });


// ... (your code for calculateAmounts1 function)
}

    

    // Attach the calculateAmounts function to the change event of adultPax and kidPax fields
    document.getElementById('adultPax').addEventListener('input', calculateAmounts);
    document.getElementById('kidPax').addEventListener('input', calculateAmounts);
    document.getElementById('currencyType').addEventListener('input', calculateAmounts);
    document.getElementById('currencyType').addEventListener('change', calculateAmounts);
    document.getElementById('paymentType').addEventListener('change', calculateAmounts);
    document.getElementById('paymentType').addEventListener('input', calculateAmounts);
    document.getElementById('givenAmount').addEventListener('input', calculateAmounts);
    document.getElementById('paymentType').addEventListener('input', calculateAmounts);
    document.getElementById('code').addEventListener('input', calculateAmounts1);
    
    

// Call the function to calculate amounts initially
calculateAmounts();

});