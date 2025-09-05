// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.24;

import "forge-std/Test.sol";
import "../src/TaskStorage.sol";

contract TaskStorageTest is Test {
    TaskStorage taskStorage;

    function setUp() public {
        taskStorage = new TaskStorage();
    }

    function testStoreAndGetTask() public {
        taskStorage.storeTask("123", "QmHashHere");
        TaskStorage.Task memory t = taskStorage.getTask(0);

        assertEq(t.taskId, "123");
        assertEq(t.ipfsHash, "QmHashHere");
        assertEq(t.user, address(this));
    }

    function testGetTaskCount() public {
        taskStorage.storeTask("id1", "hash1");
        taskStorage.storeTask("id2", "hash2");

        assertEq(taskStorage.getTaskCount(), 2);
    }
}
