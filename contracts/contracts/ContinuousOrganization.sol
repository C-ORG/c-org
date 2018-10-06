pragma solidity ^0.4.24;

import "openzeppelin-solidity/contracts/ownership/Ownable.sol";

contract ContinuousOrganization is Ownable {

    /* The parameters of the Continuous Organisation. All are multiplied by 1000 */
    uint slope = 1000; // parametrize the buying linear curve
    uint alpha = 100; // fraction put into selling reserves when investors buy
    uint beta = 300; // fraction put into selling reserves when the CO has revenues

    /* The tokens of the Continuous Organisation */
    uint nTokens = 0;
    mapping(address => uint) public balances;
    uint public sellReserve = 0;

    /* Events */
    event UpdateTokens(uint tokens, uint sellReserve);

    /* This is the constructor. Solidity does not implement float number so we have to multiply constants by 1000 and rounding them before creating the smart contract.
    */
    constructor(uint paramA, uint paramAlpha, uint paramBeta) public {
        require(paramAlpha < 1001 && paramBeta < 1001);
        slope = paramA;
        alpha = paramAlpha;
        beta = paramBeta;
    }

    /* Getters and setters */
    function setSlope(uint paramSlope) public onlyOwner {
        slope = paramSlope;
    }
    function setAlpha(uint paramAlpha) public onlyOwner {
        alpha = paramAlpha;
    }
    function setBeta(uint paramBeta) public onlyOwner {
        beta = paramBeta;
    }
    function getBalance()
        public
        view
        returns (uint y) {
        y = balances[msg.sender];
    }
    function getSellReserve()
        public
        view
        returns (uint y) {
        y = sellReserve;
    }
    function getNumTokens()
        public
        view
        returns (uint y) {
        y = nTokens;
    }


    /* Babylonian method for square root. See: https://ethereum.stackexchange.com/a/2913 */
    function _sqrt(uint x)
        internal
        pure
        returns (uint y) {
        uint z = (x + 1) / 2;
        y = x;
        while (z < y) {
            y = z;
            z = (x / z + z) / 2;
        }
    }

    /* Minting and burning tokens */
    // #TODO protection against overflows
    function buy() public payable {
        require(msg.value > 0);

        // create tokens
        uint invest = msg.value;
        uint tokens = _sqrt(2*invest*1000/slope + nTokens*nTokens) - nTokens;
        balances[msg.sender] += tokens;
        nTokens += tokens;

        // redistribute tokens
        sellReserve += alpha*invest;
        owner.transfer((1000-alpha)/1000*invest);

        emit UpdateTokens(nTokens, sellReserve);
    }

    function sell(uint tokens) public {
        // check funds
        require(tokens > 0);
        require(balances[msg.sender] >= tokens);

        balances[msg.sender] -= tokens;
        uint withdraw = sellReserve*tokens/nTokens/nTokens*(2*nTokens - tokens);
        sellReserve -= withdraw;
        withdraw /= 1000;
        msg.sender.transfer(withdraw);

        emit UpdateTokens(nTokens, sellReserve);
    }

    function revenue()
        public
        onlyOwner
        payable {

        require(msg.value > 0);
        uint rev = msg.value;
        // create tokens
        uint tokens = _sqrt(2*rev*1000/slope + nTokens*nTokens) - nTokens;
        balances[owner] += tokens;
        nTokens += tokens;

        // redistribute tokens
        sellReserve += beta*rev;
        owner.transfer((1-beta)*rev/1000);

        emit UpdateTokens(nTokens, sellReserve);
    }

    function freeTokens(uint amount)
        public
        onlyOwner {

        require(amount > 0);
        nTokens += amount;
    }
}
