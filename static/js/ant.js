// open socket using standard syntax
var ws = $.gracefulWebSocket("ws://192.168.2.6:2005");

// send message to server using standard syntax
ws.send("R\r\n");

// listen for messages from server using standard syntax
ws.onmessage = function (event) {
   var msg = event.data;
   alert(msg);   
};
