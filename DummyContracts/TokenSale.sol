pragma solidity ^0.4.21;

contract TokenSaleChallengeTest {

    uint256 constant PRICE_PER_TOKEN = 1 ether;

    function getPrice(uint256 numTokens) public pure returns (uint256 result) {
        result = numTokens * PRICE_PER_TOKEN;
    }
}