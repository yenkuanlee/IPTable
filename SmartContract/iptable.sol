pragma solidity ^0.4.0;

contract IPTable {

    string schema;

    function IPTable(string _schema) public{
        schema = _schema;
    }

    mapping(address => string) public shard;
    
    function setShard(string Ehash){
	shard[msg.sender] = Ehash;
    }

    function GetSchema() public returns (string){
        return schema;
    }

    function GetInfo() public returns (string) {
	return (shard[msg.sender]);
    }

}
