from langchains.anonymization.de_anonymization_chain import DeAnonymizationChain
from langchains.anonymization.anonymization_chain import AnonymizationChain
from base64 import b64decode

key = b64decode("r6fXjPXeemR0szANNILHjA==".encode("utf-8"))
chain = DeAnonymizationChain(key=key)


def test_does_deanonymize_with_personal_information_present():
    input = {
        "text": """Hello, my name is <PERSON-xjQH0vx1qHqjdItB8EVYWA==> and I live in <LOCATION-uTsyxpF5ZyS2ngrOr0vbQg==>. My credit card number is <CREDIT_CARD-bo7Zt/uxdB3Hv9QFxxmRy/dwIVLr1P97uj5bnO5qFFE=>
    """
    }
    expected = """Hello, my name is David Johnson and I live in Maine. My credit card number is 4095-2609-9393-4932
    """
    de_anonymized = chain(input)["text"]
    assert de_anonymized == expected


def test_does_not_deanonymize_with_no_personal_information_present():
    input = {"text": """Hello, I'm a flying dog."""}
    de_anonymized = chain(input)["text"]
    assert de_anonymized == input["text"]


def test_does_deanonymize_crypto():
    input = {"text": """<CREDIT_CARD-bo7Zt/uxdB3Hv9QFxxmRy/dwIVLr1P97uj5bnO5qFFE=>"""}
    de_anonymized = chain(input)["text"]
    assert de_anonymized == """4095-2609-9393-4932"""
