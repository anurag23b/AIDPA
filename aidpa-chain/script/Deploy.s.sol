// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.24;

import "forge-std/Script.sol";
import "../src/TaskStorage.sol";

contract DeployTaskStorage is Script {
    function run() external {
        vm.startBroadcast();
        new TaskStorage();
        vm.stopBroadcast();
    }
}
