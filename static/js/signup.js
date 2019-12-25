$('#form').submit(function(e){
    e.preventDefault();
    let data = $('#form').serialize();
    $.ajax({
        type: "POST",
        url: "/search_pair",
        data: data,
        success: function(response) {
            let json = $.parseJSON(response);
            if (json.status === "OK")
                $.ajax({
                    type: "POST",
                    url: "/add_user",
                    data: data,
                    success: function (r) {
                        let json = $.parseJSON(r);
                        if (json.status==="OK")
                            $(location).attr('href',"/messenger");
                        else
                            console.log("error in func add_user")
                    }
                });
            else
                $('#message').html(json.message)
        },
        error: function (error) {
            console.log(error, "error in signup.js")
        }
    });
});

