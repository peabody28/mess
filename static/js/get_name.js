function get_name() {
    $.ajax({
        type: "POST",
        url: "/cn",
        data: $('form').serialize(),
        success: function(response) {
            let json = $.parseJSON(response);
            if (json.status === "OK"){
                let s = "successfully, new name:  "+json.name;
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