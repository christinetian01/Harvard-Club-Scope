document.addEventListener('DOMContentLoaded', function(){

    const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    const currentDate = new Date();
    let selectedYear = currentDate.getFullYear();
    let selectedMonth = currentDate.getMonth();

    let selectedDate = document.querySelector("#selected_date").innerHTML;
    console.log(selectedDate);

    if (selectedDate !=""){
        let newDate = new Date(selectedDate);
        selectedYear = newDate.getFullYear();
        selectedMonth = newDate.getMonth();
    }
    console.log(selectedYear);
    console.log(selectedMonth);


    const month_select = document.querySelector("#month")
    const year_select = document.querySelector("#year")
    
    function calendarGrid(month, year){
        document.getElementById("month_text").innerHTML = months[month];
        document.getElementById("year_text").innerHTML = year;
    
        let cal_days = document.getElementById("calendar_days");

        while (cal_days.hasChildNodes()){
            cal_days.removeChild(cal_days.firstChild);
        }

        let firstDay = new Date(year, month, 1).getDay();
        let days = new Date(year, month+1, 0).getDate()
        
        // making the filler cells
        for (let i = 0; i<firstDay; i++){
            let fillerDiv = document.createElement("div");
            fillerDiv.className = "filler";

            cal_days.appendChild(fillerDiv)
        }

        // making the actual cells
        for (let i = 0; i<days; i++){
            let cellDivForm = document.createElement("form")
            cellDivForm.action = "/"
            cellDivForm.className = "cell"
            cellDivForm.method = "post"

            let cellDiv = document.createElement("button");
            cellDiv.className = "cell";
            cellDiv.name = "cell";
            cellDiv.type = "submit";
            if ((""+(i+1)).length == 1){
                cellDiv.value = "" + year + "-" + (month+1) + "-0" + (i+1);
            }
            else{
                cellDiv.value = "" + year + "-" + (month+1) + "-" + (i+1);
            }    
            cellDiv.innerHTML = i+1;
            cellDivForm.appendChild(cellDiv)

            if (i%7 == (7-firstDay)){
                nl = document.createElement("br");
                cal_days.appendChild(nl);
            }

            cal_days.appendChild(cellDivForm);
        }
        
    }


    function changeMonth(event){
        if (event.target){
            selectedMonth = months.indexOf(event.target.value);
        }
        calendarGrid(selectedMonth, selectedYear)
    }

    function changeYear(event){
        if (event.target){
            selectedYear = event.target.value;
        }
        calendarGrid(selectedMonth, selectedYear)
    }

    month_select.addEventListener("change", changeMonth);
    year_select.addEventListener("change", changeYear);


    sessionStorage.setItem(selectedYear, selectedYear);
    sessionStorage.setItem(selectedMonth, selectedMonth);

    calendarGrid(selectedMonth, selectedYear);
})
