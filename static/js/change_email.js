function change_email() {
    $.ajax({
        type: "POST",
        url: "/ce",
        data: $('form').serialize(),
        success: function (response) {
            let json = $.parseJSON(response);
            if (json.status === "OK")
                $(location).attr('href', "/userpage");
            else
                $('#message').html(json.message)
        },
        error: function (error) {
            console.log(error);
        }
    });
}

$('#form').submit(function (e){
    e.preventDefault();
    change_email()
});