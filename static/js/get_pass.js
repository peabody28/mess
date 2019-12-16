function get_pass() {
    $.ajax({
        type: "POST",
        url: "/cp",
        data: $('form').serialize(),
        success: function(response) {
            let json = $.parseJSON(response);
            if (json.status === "OK"){
                var url = "/userpage";
                $(location).attr('href',url);
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