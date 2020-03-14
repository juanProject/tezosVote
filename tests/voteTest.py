from os.path import dirname, join
from unittest import TestCase
from pytezos import ContractInterface, MichelsonRuntimeError

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
            self.voteContract.vote( False ).result(
                storage = {
                "votes": { alice: True },
                "paused": False,
                "admin": "tz1VphG4Lgp39MfQ9rTUnsm7BBWyXeXnJSMZ",
                "voteCount": 1
                },
                source = alice
            )
    
    def test_admin_vote(self):
        alice = "tz1ibMpWS6n6MJn73nQHtK5f4ogyYC1z9T9z"

        with self.assertRaises(MichelsonRuntimeError):
            self.voteContract.vote( False ).result(
                storage = {
                "votes": { alice: True },
                "paused": False,
                "admin": "tz1ibMpWS6n6MJn73nQHtK5f4ogyYC1z9T9z",
                "voteCount": 0
                },
                source = alice
            )

    def test_contract_paused(self):
        alice = "tz1ibMpWS6n6MJn73nQHtK5f4ogyYC1z9T9z"

        with self.assertRaises(MichelsonRuntimeError):
            self.voteContract.vote( False ).result(
                storage = {
                "votes": { alice: True },
                "paused": True,
                "admin": "tz1VphG4Lgp39MfQ9rTUnsm7BBWyXeXnJSMZ",
                "voteCount": 0
                },
                source = alice
            )
    
    def test_auto_pause(self):
        alice = "tz1ibMpWS6n6MJn73nQHtK5f4ogyYC1z9T9z"

        result = self.voteContract.vote(
            True
        ).result(
            storage = {
            "votes": { },
            "paused": False,
            "admin": "tz1VphG4Lgp39MfQ9rTUnsm7BBWyXeXnJSMZ",
            "voteCount": 9
            },
            source = alice
        )
        self.assertEqual(10, result.storage["voteCount"])
        self.assertEqual(True, result.storage['paused'])
    
    def test_reset(self):
        admin = "tz1ibMpWS6n6MJn73nQHtK5f4ogyYC1z9T9z"
        result = self.voteContract.reset(
            0
        ).result(
            storage = {
            "votes": { alice: True, bob: True },
            "paused": True,
            "admin": "tz1ibMpWS6n6MJn73nQHtK5f4ogyYC1z9T9z",
            "voteCount": 10
            },
            source = alice
        )
        self.assertEqual({}, result.storage["votes"])
        self.assertEqual(False, result.storage["paused"])
        self.assertEqual(0, result.storage["voteCount"])