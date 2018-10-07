var Migrations = artifacts.require("./Migrations.sol");

/*
const checkBalance = account => new Promise((resolve, reject) => {
  web3.eth.getBalance(account, (err, result) => {
    
    if (err) {
      return reject(err);
    }

    resolve(result.toNumber());
  });
});
*/
module.exports = function(deployer, network, accounts) {
  deployer.deploy(Migrations);
/*
  return checkBalance(accounts[0])
    .then(accountBalance => {

      console.log('Current account balance', accountBalance);

      return Promise.resolve();
    })
    .then(_ => deployer.deploy(Migrations))
    .catch(err => throw err);
*/
};
