type actionVote is record [
  vote : bool;
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
  result: string;
]

function is_admin(const store: storageType): bool is
    block { skip } with (sender = store.admin)

function is_paused(const store: storageType): bool is
    block { skip } with (store.paused)

function get_result(const store: storageType): string is
    block { 
        const count : int = 0;
        const result : string = "none";
        for elem in map store.votes block {
            case store.votes[elem] of
                Some (bool) -> if bool = True then count := count + 1 else count := count - 1 
                | None -> block {
                    skip
                }
            end
        };
        if count > 0 then
            result := "oui"
        else if count < 0 then
            result := "non"
        else result := "egalite"

     } with (result)

function subVote(const vote: bool; const store: storageType): (list(operation) * storageType) is
    begin
        if is_paused(store) = False then
            if is_admin(store) = False then
                case store.votes[sender] of
                    Some (bool) -> failwith("you have already voted !")
                    | None -> block {
                        store.votes[sender] := vote;
                        store.voteCount := store.voteCount + 1n;
                        if store.voteCount = 10n then block{
                          store.paused := True; 
                          store.result := get_result(store)
                        } else skip
                    }
                end
            else failwith("Admin can't vote");
        else failwith("Contract is paused");
    end with ((nil: list(operation)) , store)

function reset(const store: storageType): (list(operation) * storageType) is
    begin
        if is_admin(store) = True then block {
            for elem in map store.votes block {
                remove elem from map store.votes;
            };
            store.paused := False;
            store.voteCount := 0n;
            store.result := "";
        } else failwith("Access denied: you are not admin")
    end with ((nil: list(operation)) , store)

function main(const action : actionContract; const store: storageType) : (list(operation) * storageType) is
  block {skip} with
    case action of
        | Vote(v) -> subVote(v.vote, store)
        | Reset (a) -> reset(store)
    end