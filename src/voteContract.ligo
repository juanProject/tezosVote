type actionVote is record [
  choice: bool;
]

type actionContract is
| Vote of actionVote
| Reset of int

type voteList is map(address, bool)

type storageType is record [
  votes: voteList;
  paused: bool;
  admin: address;
  voteCount: nat;
]

function is_admin(const store: storageType): bool is
    block { skip } with (sender = store.admin)

function is_paused(const store: storageType): bool is
    block { skip } with (store.paused)

function submitvote(const vote: bool; const store: storageType): (list(operation) * storageType) is
    begin
        if is_paused(store) then
            if is_admin(store) then
                failwith("Admin can't vote");
            else {
                case store.votes[sender] of
                    Some (bool) -> failwith("you have already voted !")
                    | None -> block {
                        store.votes[sender] := vote;
                        store.voteCount := store.voteCount + 1n;
                        if store.voteCount = 10 then 
                            store.paused := True 
                        else skip
                    }
                end
            }
        else failwith("Contract is paused");
    end with ((nil: list(operation)) , store)

function mainVote(const action : actionContract; const store: storageType) : (list(operation) * storageType) is
  block {skip} with
    case action of
        | Vote(v) -> submitVote(v.choice, store)
        | Reset (a) -> reset(store)
    end