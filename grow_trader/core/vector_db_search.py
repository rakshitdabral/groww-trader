import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI

from grow_trader.logging.logger import logging
from grow_trader.exception.exception import CustomException
from grow_trader.config.pinecone_config import PINECONE_INDEX_NAME_EQ , PINECONE_API_KEY
from grow_trader.config.openai_config import OPENAI_API_KEY , OPENAI_EMBEDDING_MODEL , OPENAI_EMBEDDING_DIMENSION

load_dotenv()

class VectorDBSearch:
    def __init__(self, index_name: str = PINECONE_INDEX_NAME_EQ, api_key: str = PINECONE_API_KEY):
        try:
            self.index_name = index_name
            self.api_key = api_key
            self.pc = Pinecone(api_key=self.api_key)
            self.index = self.pc.Index(self.index_name)
            self.openai_client = OpenAI(api_key=OPENAI_API_KEY)
        except Exception as e:
            raise CustomException(e,sys)
    
    def search(self, query: str, top_k: int = 2):
        try:
            embedding_response = self.openai_client.embeddings.create(
                input=query,
                model=OPENAI_EMBEDDING_MODEL,
                dimensions=OPENAI_EMBEDDING_DIMENSION
            )
            if embedding_response is None:
                logging.error(f"Embedding response is None for query: {query}")
                raise ValueError(f"Embedding response is None for query: {query}")
            query_vector = embedding_response.data[0].embedding
            if query_vector is None:
                logging.error(f"Query vector is None for query: {query}")
                raise ValueError(f"Query vector is None for query: {query}")
            response = self.index.query(
                vector=query_vector,
                top_k=top_k,
                include_metadata=True
            )
            if response is None:
                logging.error(f"Response is None for query: {query}")
                raise ValueError(f"Response is None for query: {query}")
            
            # Convert QueryResponse to a JSON-serializable format
            results = []
            for match in response.matches:
                result = {
                    'id': match.id,
                    'score': match.score,
                    'metadata': match.metadata if match.metadata else {}
                }
                results.append(result)
            
            # Handle usage information safely
            usage_info = None
            if hasattr(response, 'usage') and response.usage:
                try:
                    if hasattr(response.usage, 'to_dict'):
                        usage_info = response.usage.to_dict()
                    else:
                        usage_info = {
                            'read_units': getattr(response.usage, 'read_units', None)
                        }
                except Exception:
                    usage_info = None
            
            return {
                'query': query,
                'matches': results,
                'namespace': response.namespace if hasattr(response, 'namespace') else None,
                'usage': usage_info
            }
        except Exception as e:
            raise CustomException(e,sys) from e