// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract TaskStorage {
    struct Task {
        address user;
        string taskId;
        string ipfsHash; // or data hash
        uint256 timestamp;
    }

    Task[] public tasks;

    mapping(string => bytes32) public taskHashProof;
    
    event TaskStored(address indexed user, string taskId, string ipfsHash, uint256 timestamp);

    function storeTask(string memory taskId, string memory ipfsHash) public {
        tasks.push(Task(msg.sender, taskId, ipfsHash, block.timestamp));
        emit TaskStored(msg.sender, taskId, ipfsHash, block.timestamp);
        taskHashProof[taskId] = keccak256(abi.encodePacked(ipfsHash));
    }

    function getTask(uint index) public view returns (Task memory) {
        require(index < tasks.length, "Invalid index");
        return tasks[index];
    }

    function getTaskCount() public view returns (uint) {
        return tasks.length;
    }
}
