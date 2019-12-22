function update(){
    let socket = io.connect('http://127.0.0.1:5000');//запуск прослушки порта

    $('#in_but').on("click", function(event) {
        if ($('#inp').val() !== ""){
            socket.emit('add_mess', {data: $('form').serialize() });
            $('#form')[0].reset();//обнулил input
            $('#inp').focus();
            $('#err_message').html("")
        }
        else
             $('#err_message').html("Введи сообщение!")

    });
    $('form').keydown(function(e) {
        if(e.keyCode === 13) {
            e.preventDefault();//убрал стандартную обработку enter-a
            if ($('#inp').val() !== ""){
                socket.emit('add_mess', {data: $('form').serialize() });
                $('#form')[0].reset();//обнулил input
                $('#inp').focus();
                $('#err_message').html("")
            }
            else
                 $('#err_message').html("Введи сообщение!")
        }
    });
    socket.on('update', function(msg) {
        let mes = msg["name"]+":&nbsp;&nbsp;&nbsp;&nbsp;"+msg["mes"]+"&nbsp;&nbsp;&nbsp;&nbsp;"+"<span>"+msg["time"]+"</span>"+"<br>";
        $('.messages').append(mes);
    });
}