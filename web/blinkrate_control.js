var ws = null;
function connectToWS(){
  ws = new WebSocket("ws://10.42.0.1:8080/blinkrate_ws");
}

function sendToWS(data){
  ws.send(data);
}

function prepareSlider(){
  var slider = document.getElementById("blinkrate_slider");
  var label = document.getElementById("blinkrate_label");
  slider.oninput = function() {
    label.innerHTML = "Blink rate (ms): " + slider.value;
  }
  slider.onchange = function() {
    sendToWS(slider.value);
  }
}


connectToWS();
prepareSlider();
