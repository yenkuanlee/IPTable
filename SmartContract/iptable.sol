pragma solidity ^0.4.0;

contract IPTable {

    struct Person {
	string Ehash;
	string StudentID;
        string tag;
	string role;
    }

    function IPTable() public{
    }

    mapping(bytes24 => Person) public user;
    
    function setNode(bytes24 Email, string e, string s, string t, string r){
	user[Email].Ehash = e;
	user[Email].StudentID = s;
	user[Email].tag = t;
	user[Email].role = r;
    }

    function setTag(bytes24 Email, string t){
        user[Email].tag = t;
    }

    function GetEhash(bytes24 person) constant returns (string) {
        return user[person].Ehash;
    }

    function GetInfo(bytes24 email) public returns (string,string,string,string) {
	return (user[email].Ehash,user[email].StudentID,user[email].tag,user[email].role);
    }

}
