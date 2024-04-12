var currentDate = new Date();

var day = currentDate.getDate();
var month = currentDate.getMonth();
var year = currentDate.getFullYear();
document.getElementById("date").innerText = `${day}/${month+1}/${year}`;