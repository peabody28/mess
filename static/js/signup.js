$('#form').submit(function(e){
    e.preventDefault();
    $.ajax({
        type: "POST",
        url: "/search_pair",
        data: $('#form').serialize(),

        success: function(response) {
            let json = $.parseJSON(response);
            if (json.status === "OK"){
                $.ajax({
                    type: "POST",
                    url: "/add_user",
                    data: $('#form').serialize(),
                    success: function () {
                        let url = "/messenger";
                        $(location).attr('href',url);
                    }
                });
            }
            else{
                $('#message').html(json.message)
            }
        },
        error: function () {
            console.log("error")
        }
    });
});

