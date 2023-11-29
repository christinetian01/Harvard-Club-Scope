document.addEventListener('DOMContentLoaded', function(){

    const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    
    const currentDate = new Date();
    let selectedYear = currentDate.getFullYear();
    let selectedMonth = currentDate.getMonth();

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
            let cellDiv = document.createElement("div");
            cellDiv.className = "cell";
            cellDiv.innerHTML = i+1;

            if (i%7 == (7-firstDay)){
                nl = document.createElement("br");
                cal_days.appendChild(nl);
            }

            cal_days.appendChild(cellDiv);
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

    calendarGrid(selectedMonth, selectedYear);
})
