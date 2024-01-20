var ws = null;
function connectToWS(){
  //https://stackoverflow.com/a/10418013 
  var loc = window.location, new_uri;
  if (loc.protocol === "https:") {
      new_uri = "wss:";
  } else {
      new_uri = "ws:";
  }
  new_uri += "//" + loc.host;
  new_uri += loc.pathname + "blinkrate_ws";

  ws = new WebSocket(new_uri);
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
