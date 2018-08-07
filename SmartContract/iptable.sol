pragma solidity ^0.4.21;

contract IPTable {

    string schema;

    struct TableShard {
        uint rowCount;
	string description;
    }

    function IPTable(string _schema) public{
        schema = _schema;
    }

    mapping(address => string) public shard;
    mapping(address => TableShard) public Tshard;
    address[10] saleList;
    
    function commitShard(string Fhash){
	shard[msg.sender] = Fhash;
    }

    function pushShard(uint rcnt, string dct){
        Tshard[msg.sender].rowCount = rcnt;
        Tshard[msg.sender].description = dct;
        for(uint i=0;i<saleList.length;i++){
            if(saleList[i]==msg.sender)
                break;
            if(saleList[i]==0x00){
                saleList[i] = msg.sender;
                break;
            }
        }
    }

    function GetSchema() public returns (string){
        return schema;
    }

    /* Please see FoodResume/Resume/Resume.sol
    function GetSaleList() public returns (string){
        string X ;
        for(uint i=0;i<saleList.length;i++){
            if(saleList[i]==0x00)
                continue;
            X = X+(saleList[i])+"#";
        }
        return X;
    }
    */

    function GetInfo() public returns (string) {
	return (shard[msg.sender]);
    }

    function GetShardInfo(address Sman)public returns(uint,string){
        return (Tshard[Sman].rowCount,Tshard[Sman].description);
    }

}
