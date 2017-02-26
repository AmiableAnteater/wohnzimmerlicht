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
    to_send_col: null,
    to_send_val: null
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
    if (this.state.to_send_col !== null && this.state.to_send_val !== null) {
      console.log("Sending missed message")
      this.doSend(this.state.to_send_col, this.state.to_send_val)
    }
  };

  onClose = (evt) => { console.log("onClose" + evt) };

  onMessage = (evt) => { 
    console.log("response: " + evt.data);
    let col = evt.data.substring(0,1);
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
  
  doSend = (col, val) =>
  {
    this.setColState(col, val);
    let message = col + val;
    console.log("websocket: " + this.state.websocket + " sent: " + message);
    if (this.state.websocket == null || this.state.websocket.readyState !== this.state.websocket.OPEN) {
      this.setState({to_send_col: col, to_send_val: val})
      this.openWebsocket()
    } else {
      this.state.websocket.send(message);
      this.setState({to_send_col: null, to_send_val: null})
    }
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
      </section>
    );
  }
}

export default App;
