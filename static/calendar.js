document.addEventListener('DOMContentLoaded', function(){

    const currentDate = new Date();
    let month = document.getElementById('month').value;
    let year = document.getElementById('year').value;
    
    if (month=="" & year==""){
        year = currentDate.getFullYear();
        month = currentDate.getMonth();
    }

    console.log(month)
    console.log(year)

    const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    
    function calendarGrid(year, month){
    
        let cal_days = document.getElementById("calendar_days");

        let firstDay = new Date(year, month, 1).getDay();
        console.log(firstDay);
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

    let date_select = document.getElementById("set_date");
    date_select.addEventListener("submit", function(){
        month = document.getElementById('month').value;
        year = document.getElementById('year').value;
    })
    
    calendarGrid(year, month)
})
