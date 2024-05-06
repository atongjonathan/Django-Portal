
function resetBtn() {
  normal.style.display = "block"
  loading.style.display = "none"
}
function query(url) {
  fetch(url)
    .then((query_response) => (query_response.json()))
    .then((query_data) => {
      // console.log("Query ", query_data)
      if (query_data.ResponseCode == "0") {
        // console.log("Code is not successful", query_data.ResponseCode)
        if (query_data.ResultDesc == "The service request is processed successfully.") {
          toastr.success("The service request is processed successfully.")
          resetBtn()
        }
        else {
          // console.log("Code is not successful", query_data.ResponseCode)
          toastr.warning(query_data.ResultDesc)
          resetBtn()
        }
      }
      else if (query_data.errorCode) {
        setTimeout(() => {
          // console.log("Retrying")
          query(url)

        }, 5000)
      }
      else {
        // console.log("Code is not 0", query_data.ResultDesc)
        toastr.info(query_data.errorMessage)
        resetBtn()
      }
      
    })
    .catch((err) => {
      // console.log("An error occured on query")
      // console.log(err)
      toastr.error('Request failed, Try again Later')
      resetBtn()
    })
}
document.addEventListener("DOMContentLoaded", () => {
  $('input[data-mask]').inputmask();
  let form = document.getElementById("form")
  let url = window.location.href
  let loading = document.getElementById("loading")
  let normal = document.getElementById("normal")
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    normal.style.display = "none"
    loading.style.display = "block"
    let amount = document.getElementById("amount").value
    let number = document.getElementById("number").value
    let csrf_token = document.querySelectorAll("input")[1].value
    fetch("", {

      method: 'POST',
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf_token,
      },
      body: JSON.stringify({ 'amount': amount, "phone_no": number })
    })
      // .then((response) => response.json())
      .then((response) => (response.json()))
      .then((data) => {
        // console.log("STK ", data)
        if (data.success) {
          // console.log("Success")
          toastr.info('Request has been sent to your phone')
          let requestId = data.transaction_id
          setTimeout(() => {
            // console.log("Querying...")
            url = window.location.origin + "/query/" + requestId
            query(url)
          }, 5000);
        }
        else {
          // console.log("Data is not success")
          toastr.error('Request failed, Try again Later')
          resetBtn()
        }

      })
      .catch((err) => {
        // console.log("An error occurred on stk")
        // console.log(err)
        toastr.error('Request failed, Try again Later')
        resetBtn()
      })

  })

})

