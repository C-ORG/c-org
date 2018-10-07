var HDWalletProvider = require("truffle-hdwallet-provider");

module.exports = {
  // See <http://truffleframework.com/docs/advanced/configuration>
  // to customize your Truffle configuration!
  networks: {
    ropsten: {
      provider: function() {
        return new HDWalletProvider("man sleep dance broom creek invite fragile wisdom divorce loan three split", "https://ropsten.infura.io/b26c78e15a68424294d4ebb9614261c5b26c78e15a68424294d4ebb9614261c5");
      },
      network_id: '3',
    },
    development: {
      host: "127.0.0.1",
      port: 8545,
      network_id: "*"
    }
  }
};
