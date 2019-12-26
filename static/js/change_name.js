let socket = io.connect('http://127.0.0.1:5000');//запуск прослушки порта

function change_name() {
    $.ajax({
        type: "POST",
        url: "/cn",
        data: $('form').serialize(),
        success: function (response) {
            let json = $.parseJSON(response);
            if (json.status === "OK") {
                let mess = json.past_name + " CHANGE NAME TO " + json.new_name;
                socket.emit('add_message', {data: mess, code: 1});
                $(location).attr('href', "/userpage");
            }
            else
                $('#message').html(json.message)
        },
        error: function (error) {
            console.log(error);
        }
    });
}

socket.on('update', function(msg) {
    let message = msg["name"]+":&nbsp;&nbsp;&nbsp;&nbsp;"+msg["message"]+"&nbsp;&nbsp;&nbsp;&nbsp;"+"<span>"+msg["time"]+"</span>"+"<br>";
    $('.messages').append(message);
});

$('#form').submit(function (e){
    e.preventDefault();
    change_name()
});

