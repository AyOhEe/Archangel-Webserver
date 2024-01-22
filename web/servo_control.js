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
  new_uri += loc.pathname + "servo_state";

  ws = new WebSocket(new_uri);
}

function sendToWS(data){
  ws.send(data);
}

function prepareSlider(index){
  var sliderIndex = (index + 1).toString();
  var slider = document.getElementById("servo_" + sliderIndex + "_slider");
  var label = document.getElementById("servo_" + sliderIndex + "_label");
  slider.oninput = function() {
    label.innerHTML = "Servo " + sliderIndex + " angle: " + slider.value;
  }

  slider.onchange = function() {
    sendToWS(index.toString() + slider.value);
  }
}


connectToWS();
prepareSlider(0);
prepareSlider(1);
prepareSlider(2);
