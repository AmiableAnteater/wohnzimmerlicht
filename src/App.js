import React, { Component } from 'react';
import Slider from 'rc-slider';
import './App.css';
import 'rc-slider/assets/index.css';


class App extends Component {
  state = {
    r: 0,
    g: 0,
    b: 0,
    websocket: null,
    to_send_msg: null,
  };
  
  isOpening = false;

  componentDidMount() { 
    console.log("didMount - start this==" + this);
    this.openWebsocket();
    console.log("didMount - end");
  }

  openWebsocket = () => {
    if (this.isOpening) {
      console.log("Already opening...");
      return;
    }
    this.isOpening = true;
    let ws = new WebSocket("ws://ras.pi:5000/");
    ws.onopen = (evt) => { this.onOpen(evt) };
    ws.onclose = (evt) => { this.onClose(evt) };
    ws.onmessage = (evt) => { this.onMessage(evt) };
    ws.onerror = (evt) => { this.onError(evt) };
    this.setState({ websocket: ws });
  }  

  onOpen = (evt) => {
    console.log("onOpen");
    this.isOpening = false;
    if (this.state.to_send_msg !== null) {
      console.log("Sending missed message");
      this.sendMessage(this.state.to_send_msg);
    }
  };

  onClose = (evt) => { 
    console.log("onClose" + evt);
  };

  onMessage = (evt) => { 
    console.log("response: " + evt.data);
    let col = evt.data.substring(0,1);
    if (col === 'X') {
      this.setState({ r:0, g:0, b:0 });
      return;
    }

    let val = parseInt(evt.data.substring(1), 10); 
    console.log("setting " + col + " to " + val);
    if ("rgb".indexOf(col) !== -1 && val >= 0 && val <= 255) {
      this.setState({ [col]: val });
    }
  };

  onError = (evt) => { 
    console.log('error: ' + evt.data + '\n');
    this.isOpening = false;
    if (this.state.websocket !== null) {
      this.state.websocket.close();
    }
    this.setState({ websocket: null });
  }

  setColState = (col, val) =>
  {
    console.log("setting " + col + " to " + val);
    if ("rgb".indexOf(col) !== -1 && val >= 0 && val <= 255) {
      this.setState({ [col]: val });
    }
  }
 
  sendMessage = (message) =>
  {
    if (this.state.websocket == null || this.state.websocket.readyState !== this.state.websocket.OPEN) {
      console.log("websocket: " + this.state.websocket + ' not ready. Storing message: ' + message);
      this.setState({to_send_msg: message});
      this.openWebsocket();
    } else {
      console.log("Sending message: " + message);
      this.state.websocket.send(message);
      console.log("Sent message: " + message);
      this.setState({to_send_msg: null});
      console.log("State changed.");
    }
  }
 
  doSend = (col, val) =>
  {
    this.setColState(col, val);
    let message = col + val;
    this.sendMessage(message);
  }

  onSliderChangeColR = (value) =>
  {
    this.doSend("r", value);  
  }

  onSliderChangeColG = (value) =>
  {
    this.doSend("g", value);  
  }

  onSliderChangeColB = (value) =>
  {
    this.doSend("b", value);  
  }

  onPressOff = () =>
  {
    this.setState({r:0, g:0, b:0});
    this.sendMessage('X');
  }

  render() {
    return (
      <section className="container">
        <div className="item">
          <Slider value={this.state.r} onChange={this.onSliderChangeColR} max={255}/>
        </div>
        <div className="item">
          <Slider value={this.state.g} onChange={this.onSliderChangeColG} max={255}/>
        </div>
        <div className="item">
          <Slider value={this.state.b} onChange={this.onSliderChangeColB} max={255}/>
        </div>
        <button onClick={this.onPressOff}>Licht aus</button>
      </section>
    );
  }
}

export default App;
