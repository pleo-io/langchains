from chat_gpt.anonymization_chain import AnonymizationChain
from chat_gpt.de_anonymization_chain import DeAnonymizationChain
from langchain.llms import BaseLLM
from langchain.memory import ConversationBufferMemory
from langchain.chains import SimpleSequentialChain, ConversationChain
from logging import Logger

from chat_gpt.prompt import generate_prompt


def setup_anonymization_chains(key: bytes):
    anonymization_chain = AnonymizationChain(key=key, verbose=True)
    de_anonymization_chain = DeAnonymizationChain(key=key, verbose=True)
    return anonymization_chain, de_anonymization_chain


def setup_conversational_chain(
    anonymization_chain: AnonymizationChain,
    de_anonymization_chain: DeAnonymizationChain,
    llm: BaseLLM,
    memory: ConversationBufferMemory,
    logger: Logger,
):
    logger.info("Setting up LangChain...")

    chain = SimpleSequentialChain(
        chains=[
            anonymization_chain,
            ConversationChain(
                llm=llm,
                prompt=generate_prompt(),
                verbose=True,
                memory=memory,
                input_key="anonymized",
            ),
            de_anonymization_chain,
        ]
    )

    logger.info("Set up LangChain")
    return chain
