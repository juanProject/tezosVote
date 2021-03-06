from os.path import dirname, join
from unittest import TestCase
from pytezos import ContractInterface, MichelsonRuntimeError

admin      = "tz1ibMpWS6n6MJn73nQHtK5f4ogyYC1z9T9z"
alice      = "tz1L738ifd66ah69PrmKAZzckvvHnbcSeqjf"
bob        = "tz1LFuHW4Z9zsCwg1cgGTKU12WZAs27ZD14v"
frank      = "tz1Qd971cetwNr5f4oKp9xno6jBvghZHRsDr"
pascal     = "tz1TgK3oaBaqcCHankT97AUNMjcs87Tfj5vb"
jacob      = "tz1VphG4Lgp39MfQ9rTUnsm7BBWyXeXnJSMZ"
lucina     = "tz1ZAZo1xW4Veq5t7YqWy2SMbLdskmeBmzqs"
mark       = "tz1ccWCuJqMxG4hoa1g5SKhgdTwXoJBM8kpc"
jean       = "tz1hQzKQpprB5JhNxZZRowEDRBoieHRAL84b"
boby       = "tz1hTic2GpaNumpTtYwqyPSBd9KcWifRMuEN"
bartholome = "tz1hv9CrgtaxiCayc567KUvCyWDQRF9sVNuf"
lucas      = "tz1iWMsg4UNSSQNKYsiH5s2maUZ9xBwymXxR"

class voteContractTest(TestCase):

    @classmethod
    def setUpClass(cls):
        project_dir = dirname(dirname(__file__))
        print("projectdir", project_dir)
        cls.voteContract = ContractInterface.create_from(join(project_dir, 'bin/vote.tz'))

    def test_vote(self):
        result = self.voteContract.vote(
            True
        ).result(
            storage = {
            "votes": { },
            "paused": False,
            "admin": admin,
            "voteCount": 0,
            "result": ""
            },
            source = alice
        )
        self.assertEqual(True, result.storage['votes'][alice])
    
    def test_no_second_vote(self):
        with self.assertRaises(MichelsonRuntimeError):
            self.voteContract.vote( False ).result(
                storage = {
                "votes": { alice: True },
                "paused": False,
                "admin": admin,
                "voteCount": 1,
                "result": ""
                },
                source = alice
            )
    
    def test_admin_vote(self):
        with self.assertRaises(MichelsonRuntimeError):
            self.voteContract.vote( False ).result(
                storage = {
                "votes": { alice: True },
                "paused": False,
                "admin": admin,
                "voteCount": 1,
                "result": ""
                },
                source = admin
            )

    def test_contract_paused(self):
        with self.assertRaises(MichelsonRuntimeError):
            self.voteContract.vote( False ).result(
                storage = {
                "votes": { bob: True, frank: False, pascal: False, jacob: False, lucina: False, mark: False, jean: False, boby: False , bartholome: False, lucas: False},
                "paused": True,
                "admin": admin,
                "voteCount": 10,
                "result": "non"
                },
                source = alice
            )
    
    def test_auto_pause(self):
        result = self.voteContract.vote(
            True
        ).result(
            storage = {
            "votes": { bob: True, frank: False, pascal: False, jacob: False, lucina: False, mark: False, jean: False, boby: False , bartholome: False },
            "paused": False,
            "admin": admin,
            "voteCount": 9,
            "result": ""
            },
            source = alice
        )
        self.assertEqual(10, result.storage["voteCount"])
        self.assertEqual(True, result.storage['paused'])
    
    def test_reset(self):
        result = self.voteContract.reset(
            0
        ).result(
            storage = {
            "votes": { bob: True, frank: False, pascal: False, jacob: False, lucina: False, mark: False, jean: False, boby: False , bartholome: False, lucas: False },
            "paused": True,
            "admin": admin,
            "voteCount": 10,
            "result": "oui"
            },
            source = admin
        )
        self.assertEqual({}, result.storage["votes"])
        self.assertEqual(False, result.storage["paused"])
        self.assertEqual(0, result.storage["voteCount"])
        self.assertEqual("", result.storage["result"])

    def test_reset_not_amdin(self):
        with self.assertRaises(MichelsonRuntimeError):
            self.voteContract.reset(
                0
            ).result(
                storage = {
                "votes": { bob: True, frank: False, pascal: False, jacob: False, lucina: False, mark: False, jean: False, boby: False , bartholome: False, lucas: False },
                "paused": True,
                "admin": admin,
                "voteCount": 10,
                "result": "non"
                },
                source = alice
            )

    def test_get_result(self):
        result = self.voteContract.vote(
            True
        ).result(
            storage = {
            "votes": { bob: True, frank: True, pascal: True, jacob: True, lucina: True, mark: False, jean: False, boby: False , bartholome: False },
            "paused": False,
            "admin": admin,
            "voteCount": 9,
            "result": ""
            },
            source = alice
        )
        self.assertEqual("oui", result.storage["result"])

    def test_draw(self):
        result = self.voteContract.vote(
            True
        ).result(
            storage = {
            "votes": { bob: True, frank: True, pascal: True, jacob: True, lucina: False, mark: False, jean: False, boby: False , bartholome: False },
            "paused": False,
            "admin": admin,
            "voteCount": 9,
            "result": ""
            },
            source = alice
        )
        self.assertEqual("egalite", result.storage["result"])
