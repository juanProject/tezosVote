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

function mainVote(const action : actionContract; const store: storageType) : (list(operation) * storageType) is
  block {skip} with
    case action of
        | Vote(v) -> submitVote(v.choice, store)
        | Reset (a) -> reset(store)
    end