$('input').keydown(function(e) {
    if(e.keyCode === 13) {
        e.preventDefault();//убрал стандартную обработку enter-a
        get_data()
    }
});