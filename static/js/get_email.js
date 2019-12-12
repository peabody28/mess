
function get_email() {
    $.ajax({
        type: "POST",
        url: "/ce",
        data: $('form').serialize(),
        success: function(response) {
            let json = $.parseJSON(response);
            if (json.status === "OK"){
                let s = "successfully, new email:  "+json.eml;
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