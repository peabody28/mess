$('#form').submit( function(e) {
    e.preventDefault();
    $.ajax({
        type: "POST",
        url: "/cn",
        data: $('#form').serialize(),
        success: function (response) {
            let json = $.parseJSON(response);
            if (json.status === "OK") {
                let url = "/userpage";
                $(location).attr('href', url);
            }
            else{
                $('#message').html(json.message)
            }
        }
    });
});