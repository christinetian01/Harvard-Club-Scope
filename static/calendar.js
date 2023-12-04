// 1. only run once the HTML is loaded
document.addEventListener('DOMContentLoaded', function(){

    const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    // 2. the default date for the calendar is the current date
    const currentDate = new Date();
    let selectedYear = currentDate.getFullYear();
    let selectedMonth = currentDate.getMonth();

    // 3. get the selected from the dropdown menus
    // selected date should be empty when the page is first opened
    let selectedDate = document.querySelector("#selected_date").innerHTML;

    // if selectedDate is not empty, then set the selected year and month to the value from the #selected_date element
    // defaults to current day if no day has been inputted yet
    if (selectedDate !=""){
        let newDate = new Date(selectedDate);
        selectedYear = newDate.getFullYear();
        selectedMonth = newDate.getMonth();
    }

    // 4. select element for the month
    const month_select = document.querySelector("#month")
    // select element for the year
    const year_select = document.querySelector("#year")
    
    function calendarGrid(month, year){
        // 5. change the headers to display the selected month and year
        document.getElementById("month_text").innerHTML = months[month];
        document.getElementById("year_text").innerHTML = year;
    
        // 6. select the div that is supposed to contain the actual calendar
        let cal_days = document.getElementById("calendar_days");

        // if the calendary body already has elements in it, remove them all to start fresh
        while (cal_days.hasChildNodes()){
            cal_days.removeChild(cal_days.firstChild);
        }

        // 7. the index of the first day of the month
        let firstDay = new Date(year, month, 1).getDay();
        // the number of days in a month
        let days = new Date(year, month+1, 0).getDate()
        
        // 8. making the filler cells
        for (let i = 0; i<firstDay; i++){
            let fillerDiv = document.createElement("div");
            fillerDiv.className = "filler";

            // append to the calendar body
            cal_days.appendChild(fillerDiv)
        }

        // 9. making the actual cells
        for (let i = 0; i<days; i++){
            // each cell is a form/button that should send a post request to the homepage when clicked
            // creating the form
            let cellDivForm = document.createElement("form")
            cellDivForm.action = "/"
            cellDivForm.className = "cell"
            cellDivForm.method = "post"

            // creating the button that will make up the cell
            let cellDiv = document.createElement("button");
            cellDiv.className = "cell";
            cellDiv.name = "cell";
            cellDiv.type = "submit";

            // 10. the value of the cell (button) will be the date that it corresponds to in the datetime format
            // datetime format: YYYY-MM-DD
            if ((""+(i+1)).length == 1){
                // need to add a zero if the day is only one digit
                cellDiv.value = "" + year + "-" + (month+1) + "-0" + (i+1);
            }
            else{
                cellDiv.value = "" + year + "-" + (month+1) + "-" + (i+1);
            }
            // display the day on the button    
            cellDiv.innerHTML = i+1;
            // add the button to the form
            cellDivForm.appendChild(cellDiv)

            // 11. if there are already 7 elements (including the filler divs) in one row, then add a break element to go to the next row
            if (i%7 == (7-firstDay)){
                nl = document.createElement("br");
                cal_days.appendChild(nl);
            }

            // 12.append the form to the calendary body
            cal_days.appendChild(cellDivForm);
        }
        
    }


    // 13. function that regenerates the calendar when the month is changed
    function changeMonth(event){
        if (event.target){
            // the month needs to be translated into an index
            selectedMonth = months.indexOf(event.target.value);
        }
        calendarGrid(selectedMonth, selectedYear)
    }

    // 14. function that regenerates the calendar when the year is changed
    function changeYear(event){
        if (event.target){
            selectedYear = event.target.value;
        }
        calendarGrid(selectedMonth, selectedYear)
    }

    // 15. adding event listeners to the dropdowns so that the calendar changes according to the month and year input
    month_select.addEventListener("change", changeMonth);
    year_select.addEventListener("change", changeYear);

    calendarGrid(selectedMonth, selectedYear);
})
