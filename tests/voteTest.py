from os.path import dirname, join
from unittest import TestCase
from pytezos import ContractInterface

class voteContractTest(TestCase):

    @classmethod
    def setUpClass(cls):
        project_dir = dirname(dirname(__file__))
        print("projectdir", project_dir)
        cls.voteContract = ContractInterface.create_from(join(project_dir, 'bin/vote.tz'))

    def test_vote(self):
        alice = "tz1ibMpWS6n6MJn73nQHtK5f4ogyYC1z9T9z"

        result = self.voteContract.vote(
            True
        ).result(
            storage = {
            "votes": { },
            "paused": False,
            "admin": "tz1VphG4Lgp39MfQ9rTUnsm7BBWyXeXnJSMZ",
            "voteCount": 0
            },
            source = alice
        )
        self.assertEqual(True, result.storage['votes'][alice])
    
    def test_no_second_vote(self):
        alice = "tz1ibMpWS6n6MJn73nQHtK5f4ogyYC1z9T9z"

        with self.assertRaises(MichelsonRuntimeError):
            self.voteContract
                .vote( False )
                .result(
                    storage = {
                        "votes": { alice: True },
                        "paused": False,
                        "admin": "tz1VphG4Lgp39MfQ9rTUnsm7BBWyXeXnJSMZ",
                        "voteCount": 0
                    },
                    source = alice
                )

"""     def test_burn(self):
        alice = "tz1ibMpWS6n6MJn73nQHtK5f4ogyYC1z9T9z"
        valInit = 10
        valBurn = 2

        result = self.token_v3.burn(
            owner=alice,
            burnValue=valBurn
        ).result(
            storage={
            "admin": alice,
            "balances": { alice: valInit },
            "paused": False,
            "shareType": "APPLE",
            "totalSupply": 0
            },
            source=alice
        )
        self.assertEqual(valInit - valBurn, result.big_map_diff['balances'][alice])

    def test_set_admin(self):
        root = "tz1VphG4Lgp39MfQ9rTUnsm7BBWyXeXnJSMZ"
        alice = "tz1ibMpWS6n6MJn73nQHtK5f4ogyYC1z9T9z"
        result = self.token_v3.setAdmin(
            root
        ).result(
            storage={
            "admin": alice,
            "balances": {  },
            "paused": False,
            "shareType": "APPLE",
            "totalSupply": 0
            },
            source=alice
        )
        self.assertEqual(root, result.storage['admin'])

    def test_pause(self):
        root = "tz1VphG4Lgp39MfQ9rTUnsm7BBWyXeXnJSMZ"
        status = True
        result = self.token_v3.pause(
            status
        ).result(
            storage={
            "admin": root,
            "balances": {  },
            "paused": False,
            "shareType": "APPLE",
            "totalSupply": 0
            },
            source=root
        )
        self.assertEqual(status, result.storage['paused'])

    def test_transfer(self):
        bob = "tz1VphG4Lgp39MfQ9rTUnsm7BBWyXeXnJSMZ"
        alice = "tz1ibMpWS6n6MJn73nQHtK5f4ogyYC1z9T9z"
        valInit = 10
        valTransfer = 2

        result = self.token_v3.transfer(
            fromOwner=alice,
            toOwner=bob,
            value=valTransfer
        ).result(
            storage={
            "admin": alice,
            "balances": { alice: valInit },
            "paused": False,
            "shareType": "APPLE",
            "totalSupply": 0
            },
            source=alice
        )
        self.assertEqual(valInit - valTransfer, result.big_map_diff['balances'][alice])
        self.assertEqual(valTransfer, result.big_map_diff['balances'][bob]) """
