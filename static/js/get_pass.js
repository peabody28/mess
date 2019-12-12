function get_pass() {
    $.ajax({
        type: "POST",
        url: "/cp",
        data: $('form').serialize(),
        success: function(response) {
            let json = $.parseJSON(response);
            if (json.status === "OK"){
                let s = "successfully, new password:  "+json.pass;
                $('#message').html(s)
            }
            else{
                $('#message').html(json.message)
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
}