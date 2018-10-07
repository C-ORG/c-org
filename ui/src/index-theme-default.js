//const address = "0x7D1Ea59E14f8739DEDeA58Cb9d11c90cbBe5Be27";
const address = "0xC1099087B8413BC575DB00517Ef98264eea9786c";
const abi = [{'constant': false, 'inputs': [{'name': 'paramAlpha', 'type': 'uint256'}], 'name': 'setAlpha', 'outputs': [], 'payable': false, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': true, 'inputs': [], 'name': 'getBalance', 'outputs': [{'name': 'y', 'type': 'uint256'}], 'payable': false, 'stateMutability': 'view', 'type': 'function'}, {'constant': true, 'inputs': [{'name': '', 'type': 'address'}], 'name': 'balances', 'outputs': [{'name': '', 'type': 'uint256'}], 'payable': false, 'stateMutability': 'view', 'type': 'function'}, {'constant': true, 'inputs': [], 'name': 'sellReserve', 'outputs': [{'name': '', 'type': 'uint256'}], 'payable': false, 'stateMutability': 'view', 'type': 'function'}, {'constant': false, 'inputs': [], 'name': 'revenue', 'outputs': [], 'payable': true, 'stateMutability': 'payable', 'type': 'function'}, {'constant': false, 'inputs': [{'name': 'paramSlope', 'type': 'uint256'}], 'name': 'setSlope', 'outputs': [], 'payable': false, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': false, 'inputs': [{'name': 'amount', 'type': 'uint256'}], 'name': 'freeTokens', 'outputs': [], 'payable': false, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': true, 'inputs': [], 'name': 'getSellReserve', 'outputs': [{'name': 'y', 'type': 'uint256'}], 'payable': false, 'stateMutability': 'view', 'type': 'function'}, {'constant': true, 'inputs': [{'name': 'x', 'type': 'uint256'}], 'name': 'sqrt', 'outputs': [{'name': 'y', 'type': 'uint256'}], 'payable': false, 'stateMutability': 'pure', 'type': 'function'}, {'constant': true, 'inputs': [], 'name': 'owner', 'outputs': [{'name': '', 'type': 'address'}], 'payable': false, 'stateMutability': 'view', 'type': 'function'}, {'constant': false, 'inputs': [], 'name': 'buy', 'outputs': [], 'payable': true, 'stateMutability': 'payable', 'type': 'function'}, {'constant': true, 'inputs': [], 'name': 'getNumTokens', 'outputs': [{'name': 'y', 'type': 'uint256'}], 'payable': false, 'stateMutability': 'view', 'type': 'function'}, {'constant': false, 'inputs': [{'name': 'paramBeta', 'type': 'uint256'}], 'name': 'setBeta', 'outputs': [], 'payable': false, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': false, 'inputs': [{'name': 'tokens', 'type': 'uint256'}], 'name': 'sell', 'outputs': [], 'payable': false, 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'name': 'paramA', 'type': 'uint256'}, {'name': 'paramAlpha', 'type': 'uint256'}, {'name': 'paramBeta', 'type': 'uint256'}], 'payable': false, 'stateMutability': 'nonpayable', 'type': 'constructor'}, {'anonymous': false, 'inputs': [{'indexed': false, 'name': 'tokens', 'type': 'uint256'}, {'indexed': false, 'name': 'sellReserve', 'type': 'uint256'}], 'name': 'UpdateTokens', 'type': 'event'}];

let contractInstance = null;
let userAddress = null;


window.addEventListener('load', function() {
  console.log("loading");
  // Check if Web3 has been injected by the browser:
  if (typeof web3 !== 'undefined') {
    // You have a web3 browser! Continue below!
  console.log("starting");
userAddress = web3.eth.defaultAccount;
web3js = new Web3(web3.currentProvider);
// const web3 = new Web3(web3.currentProvider);
//const web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));
contractInstance = new web3js.eth.Contract(abi, address);



   updateBalance(userAddress);
   updateSellReserve();
   updateNumTokens();




  } else {
     // Warn the user that they need to get a web3 browser
     // Or install MetaMask, maybe with a nice graphic.
  console.warn("need metamask");
  }

})


function buy() {
   console.log('buy', userAddress);
  const value = $("#buy-value").val();
  contractInstance.methods.buy().send({from: userAddress,
                                           value: value,
                                           gas:100000})
  .then(function() {
    updateBalance(userAddress);
    updateSellReserve();
    updateNumTokens();
  });
}


function sell() {
  const value = $("#sell-value").val();
  contractInstance.methods.sell(value).send({from: userAddress,gas:100000})
  .then(function() {
    updateBalance(userAddress);
    updateSellReserve();
    updateNumTokens();
  });
}

function updateBalance(address) {
  contractInstance.methods.getBalance().call({from:address})
  .then((balance) => {
    $("#balance").html(balance);
  });
}

function updateSellReserve() {
  contractInstance.methods.getSellReserve().call()
  .then((res) => {
    $("#sell-reserve").html(parseInt(res)/1000);
  });
}

function updateNumTokens() {
  contractInstance.methods.getNumTokens().call()
  .then((res) => {
    $("#n-tokens").html(res);
  });
}



// $(document).ready(function() {
//     updateBalance(userAddress);
//     updateSellReserve();
//     updateNumTokens();
// });
