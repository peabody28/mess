let socket = io.connect('http://127.0.0.1:5000');//запуск прослушки порта

function send() {
    if ($('#inp').val() !== ""){
        socket.emit('add_message', {data: $('#inp').val(), code: 0 });
        $('#form')[0].reset();//обнулил input
        $('#inp').focus();
        $('#err_message').html("")//убираю сообщение если оно есть
    }
    else
         $('#err_message').html("Введи сообщение!")
}

socket.on('update', function(msg) {
    let message = msg["name"]+":&nbsp;&nbsp;&nbsp;&nbsp;"+msg["message"]+"&nbsp;&nbsp;&nbsp;&nbsp;"+"<span>"+msg["time"]+"</span>"+"<br>";
    $('.messages').append(message);
});

$('#form').submit(function(e){
    e.preventDefault();
    send()
});