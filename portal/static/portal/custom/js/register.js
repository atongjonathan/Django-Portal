$(function () {
    $('#quickForm').validate({
      rules: {
        email: {
          required: true,
          email: true,
        },
        password: {
          minlength: 5
        },
        confirm_password: {
          minlength: 5,
          equalTo: "#password"
        },
      },
      messages: {
        email: {
          required: "Please enter a email address",
          email: "Please enter a valid email address"
        },
        password: {
          required: "Please provide a password",
          minlength: "Your password must be at least 5 characters long"
        },
        confirm_password: {
          required: "Please confirm your password",
          equalTo: "Please enter the same password again."
        },
      },
      errorElement: 'span',
      errorPlacement: function (error, element) {
        error.addClass('invalid-feedback');
        element.closest('.form-group').append(error);
      },
      highlight: function (element, errorClass, validClass) {
        $(element).addClass('is-invalid');
      },
      unhighlight: function (element, errorClass, validClass) {
        $(element).removeClass('is-invalid');
      }
    });
  });
