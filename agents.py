import re
from datetime import date, datetime, timedelta
from transformers import BitsAndBytesConfig, pipeline
import torch
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.core.prompts.prompts import SimpleInputPrompt
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.embeddings.langchain import LangchainEmbedding
from llama_index.core import download_loader
from llama_index.core.vector_stores.types import MetadataFilters, ExactMatchFilter

class FactsGenerator:
    def __init__(self):
        self.model = HuggingFaceLLM(
                context_window=4096,
                max_new_tokens=256,
                generate_kwargs={"temperature": 0.0, "do_sample": False},
                tokenizer_name="models/tokenizer",
                model_name="models/model",
                device_map="auto",
                # Uncomment the following line if leveraging CUDA for reduced memory usage
                model_kwargs={"torch_dtype":torch.float16, "load_in_4bit":True}
        )
        self.embed_model = LangchainEmbedding(HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2"))
        self.service_context=ServiceContext.from_defaults(chunk_size=1024, llm=self.model, embed_model=self.embed_model)

        self.fact_prompt = """
                [INST] System: Your specialization lies in the following task:
                            Extract important facts from call logs discussed by teams during meetings in a clear and straightforward manner.
                            Respond to user queries using the extracted facts.
                            Provide answers solely from the team's perspective without adding extra explanations.
                            Response should always be in JSON format:
                            Example output: {{"date": "<<answer>>", "facts": [<<answer>>]}}
                [/INST]
                [INST] Query: {question}?[/INST]
        
        """

        self.contradiction_prompt = """        
            [INST]System: You're tasked with building a system specialized in fact contradiction detection for call logs. The system should accomplish the following:
            
                1.Given two sets of facts - one from previous meetings and one from today's meeting - classify today's meeting facts into two categories:
                    ADD: If there are new facts introduced in today's meeting that were not present in previous meetings.
                    Modify: If any fact(s) present in both today's and previous meetings have been modified, include the modified facts in the "Modify" category.
            
                2. Classify previous meeting facts into the "Delete" category:
                    Delete: If any fact that was present in previous meetings is now absent in today's meeting facts.
                Your task is to create a JSON output structured as follows:
                {{
              "today's_date": "2024-04-01",
              "discrepancies": [
                {{
                  "type": "ADD",
                  "fact": [{{facts}}]
                }},
                {{
                  "type": "REMOVE",
                  "fact": [{{facts}}]
                }},
                {{
                  "type": "UPDATE",
                  "fact": [{{facts}}]
                }}
              ]
            }}
            
            [/INST]
            
            [INST]
            previous meeting: {previous_facts}
            [/INST]
            
            [INST]
            today meeting : {current_facts}
            [/INST]
        """

    def prepare_data(self, URL):
        BeautifulSoupWebReader = download_loader("BeautifulSoupWebReader")
        loader = BeautifulSoupWebReader()
        documents = loader.load_data(urls=URL)
        pattern = r"(\d{4})(\d{2})(\d{2})"
        for doc in documents:
            url = doc.metadata['URL']
            match = re.search(pattern, url)
            if match:
                year, month, day = match.groups()
                doc.metadata['date'] = f"{year}-{month}-{day}"
            else:
                print("Invalid filename format. Could not extract date.")

        documents = sorted(documents, key=lambda x: x.metadata['date'])
        return documents

    def process_data(self, urls, query):
        documents = self.prepare_data(urls)
        index = VectorStoreIndex.from_documents(documents, service_context=self.service_context)

        facts = {}
        for doc in documents:
            date = doc.metadata['date']
            filters = MetadataFilters(filters=[ExactMatchFilter(key="date", value=date)])
            query_engine = index.as_query_engine(filters=filters)
            response = query_engine.query(self.fact_prompt.format(question=query))
            facts[date] = response.response

        contradiction_facts = {}
        for id, key in enumerate(facts):
            # Create a separate index for each document
            if id == 0:
                continue
            filters = MetadataFilters(filters=[ExactMatchFilter(key="date", value=key)])
            query_engine = index.as_query_engine(filters=filters)
            previous_facts = []
            for k in facts:
                if k < key:
                    previous_facts += facts[k]
            response = query_engine.query(self.contradiction_prompt.format(previous_facts=previous_facts,
                                                                           current_facts=facts[key]))
            contradiction_facts[key] = response.response

        return contradiction_facts


