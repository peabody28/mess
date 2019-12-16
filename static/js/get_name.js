function get_name() {
    $.ajax({
        type: "POST",
        url: "/cn",
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