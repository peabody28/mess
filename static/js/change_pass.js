function change_pass() {
    $.ajax({
        type: "POST",
        url: "/cp",
        data: $('form').serialize(),
        success: function(response) {
            let json = $.parseJSON(response);
            if (json.status === "OK")
                $(location).attr('href', "/userpage");
            else
                $('#message').html(json.message)
        },
        error: function(error) {
            console.log(error);
        }
    });
}

$('#form').submit(function (e) {
    e.preventDefault();
    change_pass()
});
