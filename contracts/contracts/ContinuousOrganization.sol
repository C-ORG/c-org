pragma solidity ^0.4.24;

//import "./openzeppelin-solidity/contracts/math/SafeMath.sol";
//import "./openzeppelin-solidity/contracts/ownership/Ownable.sol";
//import "./openzeppelin-solidity/contracts/token/ERC20/StandardToken.sol";
import "contracts/contracts/openzeppelin-solidity/contracts/math/SafeMath.sol";
import "contracts/contracts/openzeppelin-solidity/contracts/ownership/Ownable.sol";
import "contracts/contracts/openzeppelin-solidity/contracts/token/ERC20/StandardToken.sol";

contract ContinuousOrganization is Ownable, StandardToken {
    using SafeMath for uint256;

    // ERC20 Token Definition.
    // Name and Symbol are not constants since we're going to set them at construction time.
    string public name;
    string public symbol;
    uint8 public constant decimals = 18;

    /* The parameters of the Continuous Organisation. All are multiplied by 1000 */
    uint public slope; // parametrize the buying linear curve
    uint public alpha; // fraction put into selling reserves when investors buy
    uint public beta; // fraction put into selling reserves when the CO has revenues
    uint256 public dividendBank_ = 0;

    /* The tokens of the Continuous Organisation */
    uint256 private sellReserve_ = 0;


    /* Events */
    event TokensPurchased(
        address indexed purchaser,
        uint256 value,
        uint256 amount
    );
    event TokensSold(
        address indexed seller,
        uint256 value,
        uint256 amount
    );
    event DividendsPurchased(
        address indexed purchaser,
        uint256 value,
        uint256 amount
    );

    /* This is the constructor. Solidity does not implement float number so we have to multiply constants by 1000 and rounding them before creating the smart contract.
    */
    constructor(string _name, string _symbol, uint _slope, uint _alpha, uint _beta) public {
        require(_alpha <= 1000 && _beta <= 1000);

        name = _name;
        symbol = _symbol;
        slope = _slope;
        alpha = _alpha;
        beta = _beta;
    }

    /* Getters and setters */
    function sellReserve()
        public
        view
        returns (uint256) {
        return sellReserve_;
    }

    // From: https://github.com/OpenZeppelin/openzeppelin-solidity/blob/v1.12.0/contracts/token/ERC20/MintableToken.sol
    function _mint(
        address _to,
        uint256 _amount
    )
        internal
        returns (bool)
    {
        totalSupply_ = totalSupply_.add(_amount);
        balances[_to] = balances[_to].add(_amount);
        emit Transfer(address(0), _to, _amount);
        return true;
    }

    // From: https://github.com/OpenZeppelin/openzeppelin-solidity/blob/v1.12.0/contracts/token/ERC20/BurnableToken.sol
    function _burn(address _who, uint256 _value) internal {
        require(_value <= balances[_who]);
        // no need to require value <= totalSupply, since that would imply the
        // sender's balance is greater than the totalSupply, which *should* be an assertion failure

        balances[_who] = balances[_who].sub(_value);
        totalSupply_ = totalSupply_.sub(_value);
        emit Transfer(_who, address(0), _value);
    }

    /* Babylonian method for square root. See: https://ethereum.stackexchange.com/a/2913 */
    function _sqrt(uint256 x)
        internal
        pure
        returns (uint256 y) {
        uint256 z = (x + 1) / 2;
        y = x;
        while (z < y) {
            y = z;
            z = (x / z + z) / 2;
        }
    }

    // Fallback function.
    function () external payable {
        buy();
    }

    function _tokenToEther(uint256 tokens)
        internal
        returns (uint256 y) {

        uint256 ratio = tokens*sellReserve_/totalSupply_/totalSupply_;
        y = ratio * (2 * totalSupply_ - tokens);
    }

    function _etherToToken(uint256 invest)
        internal
        returns (uint256 token) {

        uint256 ratio = 2*invest*10**uint256(decimals)*1000/slope;
        token = _sqrt(ratio + totalSupply_**2) - totalSupply_;
    }


    /* Minting and burning tokens */
    // #TODO protection against overflows
    function buy() public payable {
        require(msg.value > 0);

        // create tokens
        uint256 invest = msg.value;
        uint256 tokens = _etherToToken(invest);
        _mint(msg.sender, tokens);

        // redistribute tokens: keep a fraction in reserve and transfer the rest.
        uint256 reserve = (alpha*invest) / 1000;
        sellReserve_ += reserve;
        owner.transfer(invest - reserve);

        emit TokensPurchased(
            msg.sender,
            invest,
            tokens
        );
    }

    function sell(uint256 tokens) public {
        // check funds
        require(tokens > 0);

        // Burn the deposit. This will check the seller has enough.
        _burn(msg.sender, tokens);

        // Pay out from the reserve.
        uint256 withdraw = _tokenToEther(tokens);
        sellReserve_ -= withdraw;
        msg.sender.transfer(withdraw);

        emit TokensSold(
            msg.sender,
            withdraw,
            tokens
        );
    }


    function storeDividend() public payable {

        require(msg.value > 0);

        // create tokens
        uint256 invest = msg.value;
        uint256 tokens = _etherToToken(invest);
        _mint(address(this), tokens);

        emit DividendsPurchased(
            msg.sender,
            invest,
            tokens
        );
    }

    // redistribute tokens to hodlers
    function askDividend(address claimer) public {

        uint256 dividend = balanceOf(claimer)*balanceOf(address(this))/totalSupply_;
        _burn(address(this), dividend);
        _mint(claimer, dividend);
    }


    function revenue()
        public
        payable {

        require(msg.value > 0);
        uint256 rev = msg.value;

        // transfer a part of the revenue to the owner
        uint256 revForOwner = beta*rev/1000;


        // and the rest as dividends (in tokens)
        uint256 revForDividends = rev - revForOwner;
        uint256 tokens = _etherToToken(rev)/1000;
        _mint(address(this), tokens);

        emit DividendsPurchased(
            address(this),
            revForDividends,
            tokens
        );
    }
}
