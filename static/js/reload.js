function reload() {
    $.ajax({
        type: "GET",
        url: "/cast",
        success: function(response) {
            let json = $.parseJSON(response);
            if (json.status === "OK") {
                let s = "";
                let tags = [];
                let messages = [];
                let time = [];
                $.each(json.data, function (index, data) {
                    $.each(data, function (key, value) {
                        if (key==="tag")
                            tags.push(value);
                        else if (key==="mess")
                            messages.push(value);
                        else
                            time.push(value);
                    });
                });
                $.each(tags, function (index) {
                let message = "";
                let big = false;
                if(messages[index].length > 40){
                    big = true;
                    let x = 0;
                    let len = messages[index].length;
                    while(len>40){
                        message+=messages[index].substr(x, 40)+"\n";
                        x+=40;
                        len-=40;
                    }
                    message+=messages[index].slice(x, messages[index].length-1);
                }
                else
                    message=messages[index];
                if (big===true)
                    s+="\n"+tags[index]+":    "+message.bold()+"             "+time[index]+"\n\n";
                else
                    s+=tags[index]+":    "+message.bold()+"             "+time[index]+"\n";

                });
                $('#messages').html(s)
            }
            else{
                console.log("error in function 'reload'")
            }
        },
        error: function(error) {
            console.log(error);
        }
    });

}
let timerId;
