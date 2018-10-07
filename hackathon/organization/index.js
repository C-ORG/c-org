

let contractInstance = null;
let userAddress = null;
let balance = null;

window.addEventListener('load', function() {
  console.log("loading");

  if (typeof web3 !== 'undefined') {
  console.log("starting");
  userAddress = web3.eth.defaultAccount;
  web1 = new Web3(web3.currentProvider);
  web0 = web3;
  contractInstance = new web1.eth.Contract(abi, address);

   updateBalance(userAddress);
   updateSellReserve();
   updateNumTokens();

  } else {
     // Warn the user that they need to get a web0 browser
     // Or install MetaMask, maybe with a nice graphic.
  console.warn("need metamask");
  }
})


function buy() {
  const value = $("#buy-value").val();
  wei = web0.toWei(value, 'ether');
  transaction = contractInstance.methods.buy().send({
                    'from': userAddress,
                    'gas': 4712388,
                    'gasPrice': 100000,
                    'value': wei
    })
    .then(function() {
      updateBalance(userAddress);
      updateSellReserve();
      updateNumTokens();
    });
}


function sell() {
  const value = $("#sell-value").val();
  wei = web0.toWei(value, 'ether');
  contractInstance.methods.sell(wei).send({
    from: userAddress,
    gas: 4712388,
    gasPrice: 100000
  })
  .then(function() {
    updateBalance(userAddress);
    updateSellReserve();
    updateNumTokens();
  });
}

function transfer() {
  const value = $("#transfer-amount").val();
  wei = web0.toWei(value, 'ether');
  const address = $("#transfer-address").val();
  contractInstance.methods.transfer(address, wei).send({
    from: userAddress,
    gas: 4712388,
    gasPrice: 100000
  })
  .then(function() {
    updateBalance(userAddress);
    updateSellReserve();
    updateNumTokens();
  });
}

function transfer() {
  const value = $("#transfer-amount").val();
  wei = web0.toWei(value, 'ether');
  const address = $("#transfer-address").val();
  contractInstance.methods.transfer(address, wei).send({
    from: userAddress,
    gas: 4712388,
    gasPrice: 100000
  })
  .then(function() {
    updateBalance(userAddress);
    updateSellReserve();
    updateNumTokens();
  });
}


function revenue() {
  const value = $("#revenue-value").val();
  wei = web0.toWei(value, 'ether');
  contractInstance.methods.revenue().send({
    from: userAddress,
    gas: 4712388,
    gasPrice: 100000,
    value: wei
  })
  .then(function() {
    updateBalance(userAddress);
    updateSellReserve();
    updateNumTokens();
  });
}

function grant() {
  const value = $("#grant-value").val();
  wei = web0.toWei(value, 'ether');
  contractInstance.methods.storeDividend().send({
    from: userAddress,
    gas: 4712388,
    gasPrice: 100000,
    value: wei
  })
  .then(
    web0.eth.accounts.forEach(
      contractInstance.methods.askDividend().send({
        from: userAddress,
        gas: 4712388,
        gasPrice: 100000
      })
    )
  ).then(function() {
    updateBalance(userAddress);
    updateSellReserve();
    updateNumTokens();
  });
}


function updateBalance(address) {
  contractInstance.methods.balanceOf(address).call()
  .then((res) => {
    balance = parseFloat(web0.fromWei(res,"ether"));
    $("#balance-tok").html(balance.toFixed(3));
  });

  web1.eth.getBalance(address)
  .then((res) => {
    balance = parseFloat(web0.fromWei(res,"ether"));
    $("#balance-eth").html(balance.toFixed(3));
  });
}

function updateSellReserve() {
  contractInstance.methods.sellReserve().call()
  .then((res) => {
    $("#sell-reserve").html(parseFloat(web0.fromWei(res)).toFixed(3));
  });
}

function updateNumTokens() {
  contractInstance.methods.totalSupply().call()
  .then((res) => {
    $("#n-tokens").html(parseFloat(web0.fromWei(res)).toFixed(3));
  });
}

function sumUp() {
  const tbody = $("#sumup").find('tbody');
  $('#sumup tr').each(function (i, row) {
    row.remove();
  });

  let balancesTOK = [];
  web0.eth.accounts.forEach(function (i, address) {
    contractInstance.methods.balanceOf(address).call()
    .then((res) => {
      balancesTOK.append(parseFloat(web0.fromWei(res)).toFixed(3));
    });
  });

  let balancesETH = [];
  web0.eth.accounts.forEach(function (i, address) {
    web1.eth.getBalance(address)
    .then((res) => {
      balancesETH.append(parseFloat(web0.fromWei(res,"ether")));
    });
  });


  console.log(balancesETH);
  console.log(balancesTOK);

  web0.eth.accounts.forEach(function (i, address) {
    tbody.append("<tr><th scope='row'>" + i + "</th><td></td><td>" + balancesETH[i] + "</td><td>" + balancesTOK[i] + "</td></tr>");
  });

}


// $(document).ready(function() {
//     updateBalance(userAddress);
//     updateSellReserve();
//     updateNumTokens();
// });
