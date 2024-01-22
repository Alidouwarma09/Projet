// static/js/chat.js
const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/');

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    alert(data.message);
};

document.querySelector('#chat-input').addEventListener('keyup', function (e) {
    if (e.keyCode === 13) {  // Touche "Enter"
        const messageInputDom = document.querySelector('#chat-input');
        const message = messageInputDom.value;
        chatSocket.send(JSON.stringify({
            'message': message
        }));
        messageInputDom.value = '';
    }
});
