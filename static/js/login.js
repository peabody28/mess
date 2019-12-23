$('#form').submit(function(e){
    e.preventDefault();
    $.ajax({
        type: "POST",
        url: "/check",
        data: $('#form').serialize(),
        success: function(response) {
            let json = $.parseJSON(response);
            if (json.status === "OK") {
                let url = "/messenger";
                $(location).attr('href', url);
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
