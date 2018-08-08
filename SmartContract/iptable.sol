pragma solidity ^0.4.21;

contract IPTable {

    string schema;

    struct TableShard {
        uint256 tsid;
        address owner;
        uint rowCount;
	string description;
        string fhash;
    }

    function IPTable(string _schema) public{
        schema = _schema;
    }

    mapping(address => string) public shard;    // the newest fhash
    mapping(address => TableShard) public Tshard;    // sale info
    mapping(address => TableShard[]) public pocket;    // buy data and put info into pocket
    address[] public saleList;

    function Time_call() returns (uint256){
        return now;
    }

    function stringsEqual(string storage _a, string memory _b) internal constant returns (bool) {
        bytes storage a = bytes(_a);
        bytes memory b = bytes(_b);
        if (a.length != b.length)
            return false;
        for (uint i = 0; i < a.length; i ++)
            if (a[i] != b[i])
                return false;
        return true;
    }

    function commitFhash(string Fhash){
	shard[msg.sender] = Fhash;
    }

    function pushShard(uint rcnt, string dct){
        Tshard[msg.sender].tsid= Time_call();
        Tshard[msg.sender].owner = msg.sender;
        Tshard[msg.sender].rowCount = rcnt;
        Tshard[msg.sender].description = dct;
        Tshard[msg.sender].fhash = shard[msg.sender];
        bool flag = true;
        for(uint i=0;i<saleList.length;i++){
            if(saleList[i]==msg.sender){
                flag = false;
                break;
            }
            if(saleList[i]==0x00){
                saleList[i] = msg.sender;
                flag = false;
                break;
            }
        }
        if(flag){
            saleList.length ++;
            saleList[saleList.length-1] = msg.sender;
        }
    }

    function GetSchema() public returns (string){
        return schema;
    }

    function GetSaleList() constant returns (address[]) {
        return saleList;
    }

    function GetInfo() public returns (string) {
	return (shard[msg.sender]);
    }

    function GetShardInfo(address Sman)public returns(uint,string){
        return (Tshard[Sman].rowCount,Tshard[Sman].description);
    }

    function Buy(address Sman) {
        string Fhash = Tshard[Sman].fhash;
        bool flag = true;
        for(uint i=0;i<pocket[msg.sender].length;i++){
            if(stringsEqual(pocket[msg.sender][i].fhash,Fhash)){    // duplicate
                flag = false;
                break;
            }
        }
        if(flag){
            pocket[msg.sender].length ++;
            pocket[msg.sender][pocket[msg.sender].length-1] = Tshard[Sman];
        }
    }

    function ShowPocket() constant returns(uint[]){
        uint[] memory output = new uint[](pocket[msg.sender].length);
        for(uint i=0;i<pocket[msg.sender].length;i++){
            output[i] = pocket[msg.sender][i].tsid;
        }
        return output;
    }

    function GetPocketShardInfo(uint256 TSID)public returns(uint256,address,uint,string,string){
        for(uint i=0;i<pocket[msg.sender].length;i++){
            if(pocket[msg.sender][i].tsid==TSID){
                return(TSID,pocket[msg.sender][i].owner,pocket[msg.sender][i].rowCount,pocket[msg.sender][i].description,pocket[msg.sender][i].fhash);
            }
        }
    }

}
