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
  function addItem(text) {
    // Create a new div element
    var newItem = document.getElementById('reply');
    // Set the inner text
    newItem.innerText = text;
    // Append the new item to the container
    document.getElementById('replies').appendChild(newItem);
}

  window.onload = function () {
    displayCurrentTime();
    setInterval(displayCurrentTime, 1000);
  };

  document.addEventListener("DOMContentLoaded", () => {
    let form = document.getElementById("mail-form")
    let reply_div = document.getElementById("reply")
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      let email = document.getElementById("email").value
      email_data = { template: "invite", subject: "Invitation to the Ark Junior School", email: email, user: "{{ request.user }}" }
      fetch("", {

        method: 'POST',
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(email_data)
      })
        // .then((response) => response.json())
        .then((response) => (response.json()))
        .then((data) => {
          if (data.message)
          {
            reply_div.style.display = "block"
            toastr.success("Invite has been sent")
          }
          else
          {
            toastr.warning("Invite not sent, please try again later")
          }


        })
        .catch((err) => {
          console.log(err)
          toastr.warning("Request failed, try again later")
        })

    })
  })
