# Tezos vote school project

This smart contract should :
    
    - allow any user to vote "oui" or "non" (True or False)
    - allow user to vote once and only once
    - pause contract if 10 user voted
    - display result of the current vote in the storage (after 10 votes)
    - allow admin to reset votes (inlcuding state of the contract and result)
    - deny admin vote
    - define admin at contract deployment

# Compile and deployment

This smart contract is coded in ligo, you should install [ligo cli](https://ligolang.org/docs/next/intro/installation/)

### To compile source code :

```Shell
ligo compile-contract src/voteContract.ligo main > bin/vote.tz
```

### Compiling storage and parameters

This is an exemple of compiling storage :

```Shell
ligo compile-storage src/voteContract.ligo main 'record
 votes = (map[] : map(address, bool));
 paused = False;
 admin = ( "tz1ibMpWS6n6MJn73nQHtK5f4ogyYC1z9T9z": address);
 voteCount = 0n;
 result = "";
end'
```

it should print :

```Shell
(Pair (Pair (Pair "tz1ibMpWS6n6MJn73nQHtK5f4ogyYC1z9T9z" False) (Pair "" 0)) {})
```

### Endpoints

This contract has two end points : Vote and Reset

To compile parameters for Vote (you can vote True or False): 

```Shell
ligo compile-parameter src/voteContract.ligo main "Vote(record vote=True; end)"
```

it should print :
```Shell
(Right True)
```
And for Reset : 

```Shell
ligo compile-parameter src/voteContract.ligo main "Reset(0)"
```

it should print :
```Shell
(Left 0)
```

To deploy you should see [Tezos](https://tezos.gitlab.io/introduction/howtoget.html)

# Test code

code testing is done by pytest

```Shell
pytest tests/voteTest.py
```