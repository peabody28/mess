function change_name() {
    $.ajax({
        type: "POST",
        url: "/cn",
        data: $('form').serialize(),//передаю данные формы в функцию cn
        success: function(response) {
            let json = $.parseJSON(response);
            if (json.status === "OK"){
                let url = "/userpage";
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