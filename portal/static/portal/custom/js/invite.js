function displayCurrentTime() {
    var months = [
      "Jan", "Feb", "Mar", "Apr", "May", "Jun",
      "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ];

    var currentDate = new Date();

    var day = currentDate.getDate();
    var month = months[currentDate.getMonth()];
    var hours = currentDate.getHours();
    var minutes = currentDate.getMinutes();
    var ampm = hours >= 12 ? 'pm' : 'am';

    // Convert hours to 12-hour format
    hours = hours % 12;
    hours = hours ? hours : 12;

    var formattedTime = day + " " + month + " " + hours + ":" +
      (minutes < 10 ? '0' : '') + minutes + " " + ampm;

    document.getElementById("current-time").innerText = formattedTime;
  }

  window.onload = function () {
    console.log("Invite js working")
    displayCurrentTime();
    setInterval(displayCurrentTime, 1000);
  };