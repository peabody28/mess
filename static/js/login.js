$('#form').submit(function(e){
    e.preventDefault();
    $.ajax({
        type: "POST",
        url: "/check",
        data: $('#form').serialize(),
        success: function(response) {
            let json = $.parseJSON(response);
            if (json.status === "OK")
                $(location).attr('href', "/messenger");
            else
                $('#message').html(json.message)
        },
        error: function (error) {
            console.log(error, "error in login.js")
        }
    });
});
