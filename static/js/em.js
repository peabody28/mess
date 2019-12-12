function em(){
    var socket = io.connect('http://127.0.0.1:5000');

    $('#in_but').on("click", function(event) {
        socket.emit('Slider value changed', {data: $('form').serialize() });
        $('#form')[0].reset();//обнулил input
        $('#form').focus();
    });
    socket.on('update value', function(msg) {
        let mes = msg["name"]+":  "+msg["mes"]+"     "+msg["time"]+"\n";
        $('#messages').append(mes);
    });
}