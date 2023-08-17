import pytest
from langchains.anonymization.anonymization_chain import AnonymizationChain
from Crypto import Random
from re import findall, match

base_64_regex = r"<([A-Z_]+)-([A-Za-z0-9+\/=]*)>"

key = Random.get_random_bytes(16)
chain = AnonymizationChain(key=key)


def find_anonymized(input: str):
    return findall(base_64_regex, input)


def test_does_anonymize_with_personal_information_present():
    input = {
        "text": """Hello, my name is David Johnson and I live in Maine.
    My credit card number is 4095-2609-9393-4932
    """
    }
    result = chain(input)["anonymized"]
    anonymized = find_anonymized(result)
    present = list(
        map(
            lambda kv: kv[0] in ["PERSON", "LOCATION", "CREDIT_CARD"],
            anonymized,
        )
    )
    assert all(present)
    assert len(anonymized) == 3


def test_does_not_anonymize_with_no_personal_information_present():
    input = {"text": """Hello, I'm a flying dog."""}
    result = chain(input)["anonymized"]
    anonymized = find_anonymized(result)
    assert len(anonymized) == 0


def test_does_not_anonymize_crypto():
    input = {"text": """This is a crypto address: 16Yeky6GMjeNkAiNcBY7ZhrLoMSgg1BoyZ"""}
    result = chain(input)["anonymized"]
    anonymized = find_anonymized(result)
    assert len(anonymized) == 0
