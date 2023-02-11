

document.addEventListener('DOMContentLoaded', () => {

    //var socket = io.connect('http://' + location.hostname + ':' + location.port);

    var socket = io('https://pics.proyectocoder.com');
   

    let room = 'Pics';
    joinRoom("Pics");

    // Display incoming messages
    socket.on('message', data => {
        const p = document.createElement('p');
        const span_username = document.createElement('span');
        const span_time = document.createElement('span');
        const br = document.createElement('br');

        // Sanitiza el mensaje del usuario

        if (data.username == username) {
            p.setAttribute("class", "my-msg")
            // my user
            span_username.setAttribute("class", "my-user")
            span_username.innerHTML = data.username;
            // my time
            span_time.setAttribute("class", "my-time")
            span_time.innerHTML = data.time;
            p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_time.outerHTML;
            document.querySelector('#display-message-section').append(p);
            
        } else if( typeof data.username !== 'undefined') {
            p.setAttribute("class", "other-msg");
            // other username
            span_username.setAttribute("class","other-user");
            span_username.innerHTML = data.username;
            // other time
            span_time.setAttribute("class", "other-time")
            span_time.innerHTML = data.time;
            // append
            p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_time.outerHTML;
            document.querySelector('#display-message-section').append(p);

        } else {
            printSysMsg(data.msg);
        }
    scrollDownChat();

    });

    // Send message
    document.querySelector('#send_message').onclick = () => {

        
        socket.send({'msg':document.querySelector('#user_message').value,
        'username': username, 'room': room});
        // Clear message area
        document.querySelector('#user_message').value = '';
    }

    // Room selection
    document.querySelectorAll('.select-room').forEach(p => {
        p.onclick = () => {
            let newRoom = p.innerHTML;
            if (newRoom == room) {
                msg = `Ya se encuentra en el chat ${room}.`
                printSysMsg(msg);
            } else {
                leaveRoom(room);
                joinRoom(newRoom);
                room = newRoom;
            }
        }
    });

    //Leave room 
    function leaveRoom(room) {
        socket.emit('leave', {'username': username, 'room': room});
    }

    //Join room 
    function joinRoom(room) {
        socket.emit('join', {'username': username, 'room': room});
        // Clear message area
        document.querySelector('#display-message-section').innerHTML = ''
        // Autofocus on text box
        document.querySelector('#user_message').focus();
    }


    //Scroll down chat
    function scrollDownChat() {
        const chatWindow = document.querySelector('#display-message-section');
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    //Print message
    function printSysMsg(msg) {
        const p = document.createElement('p');
        p.innerHTML = msg;
        document.querySelector('#display-message-section').append(p);
        scrollDownChat()
    }

    
    
})