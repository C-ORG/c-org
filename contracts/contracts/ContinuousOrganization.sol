pragma solidity ^0.4.24;

import "openzeppelin-solidity/contracts/math/SafeMath.sol";
import "openzeppelin-solidity/contracts/ownership/Ownable.sol";
import "openzeppelin-solidity/contracts/token/ERC20/StandardToken.sol";

contract ContinuousOrganization is Ownable, StandardToken {
    using SafeMath for uint256;

    // ERC20 Token Definition.
    // Name and Symbol are not constants since we're going to set them at construction time.
    string public name;
    string public symbol;
    uint8 public constant decimals = 18;

    /* The parameters of the Continuous Organisation. All are multiplied by 1000 */
    uint slope = 1000; // parametrize the buying linear curve
    uint alpha = 100; // fraction put into selling reserves when investors buy
    uint beta = 300; // fraction put into selling reserves when the CO has revenues

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
    function setSlope(uint paramSlope) public onlyOwner {
        slope = paramSlope;
    }
    function setAlpha(uint paramAlpha) public onlyOwner {
        alpha = paramAlpha;
    }
    function setBeta(uint paramBeta) public onlyOwner {
        beta = paramBeta;
    }
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
        uint tokens = _sqrt(2*invest*1000/slope + totalSupply_*totalSupply_) - totalSupply_;
        _mint(msg.sender, tokens);

        // redistribute tokens: keep a fraction in reserve and transfer the rest.
        uint reserve = alpha*invest;
        sellReserve_ += reserve;
        owner.transfer(invest - reserve);

        emit TokensPurchased(
            msg.sender,
            invest,
            tokens
        );
    }

    function sell(uint tokens) public {
        // check funds
        require(tokens > 0);

        // Burn the deposit. This will check the seller has enough.
        _burn(msg.sender, tokens);

        // Pay out from the reserve.
        uint withdraw = sellReserve_*tokens/totalSupply_/totalSupply_*(2*totalSupply_ - tokens);
        sellReserve_ -= withdraw;
        withdraw /= 1000;
        msg.sender.transfer(withdraw);

        emit TokensSold(
            msg.sender,
            withdraw,
            tokens
        );
    }

    function revenue()
        public
        onlyOwner
        payable {

        require(msg.value > 0);
        uint rev = msg.value;
        // create tokens
        uint tokens = _sqrt(2*rev*1000/slope + totalSupply_*totalSupply_) - totalSupply_;
        _mint(owner, tokens);

        // redistribute tokens
        sellReserve_ += beta*rev;
        owner.transfer((1-beta)*rev/1000);
    }
}
