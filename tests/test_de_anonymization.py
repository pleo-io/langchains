import pytest
from langchains.anonymization.de_anonymization_chain import DeAnonymizationChain
from langchains.anonymization.anonymization_chain import AnonymizationChain
from Crypto import Random
from re import findall, match

key = Random.get_random_bytes(16)
anonymization_chain = AnonymizationChain(key=key)
chain = DeAnonymizationChain(key=key)


def test_does_deanonymize_with_personal_information_present():
    input = {
        "text": """Hello, my name is David Johnson and I live in Maine.
    My credit card number is 4095-2609-9393-4932
    """
    }
    result = anonymization_chain(input)["anonymized"]
    de_anonymized = chain(result)["text"]
    assert de_anonymized


def test_does_not_deanonymize_with_no_personal_information_present():
    input = {"text": """Hello, I'm a flying dog."""}
    result = anonymization_chain(input)["anonymized"]
    de_anonymized = chain(result)["text"]
    assert de_anonymized == input["text"]


def test_does_not_deanonymize_crypto():
    input = {"text": """This is a crypto address: 16Yeky6GMjeNkAiNcBY7ZhrLoMSgg1BoyZ"""}
    result = anonymization_chain(input)["anonymized"]
    de_anonymized = chain(result)["text"]
    assert de_anonymized == input["text"]
