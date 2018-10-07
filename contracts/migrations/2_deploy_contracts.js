let ContinuousOrganization = artifacts.require("./ContinuousOrganization.sol");

module.exports = function(deployer) {
  const name = "test token";
  const symbol = "TST";
  const slope = 1000; // parametrize the buying linear curve
  const alpha = 100; // fraction put into selling reserves when investors buy
  const beta = 50; // fraction put into selling reserves when the CO has revenues

  deployer.deploy(ContinuousOrganization, name, symbol, slope, alpha, beta);
};
