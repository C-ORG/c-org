import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import App from "./App";
// import { Web3Provider } from 'react-web3';
import * as serviceWorker from "./serviceWorker";

// ReactDOM.render(
//   <Web3Provider><App />
// </Web3Provider>, document.getElementById("root"));

ReactDOM.render(<App />, document.getElementById("root"));



// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: http://bit.ly/CRA-PWA
serviceWorker.unregister();
