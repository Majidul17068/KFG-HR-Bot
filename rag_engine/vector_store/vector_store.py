import os
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from config.config import Config
import logging
from typing import List, Dict, Any, Optional
import json
import hashlib
from pathlib import Path
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=Config.CHROMA_DB_PATH,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Load embedding model
        self.embedding_model = SentenceTransformer(Config.EMBEDDING_MODEL)
        
        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name="kfg_policies_v2",
            metadata={"description": "KFG Policy Documents - Enhanced Organization"}
        )
        
        logger.info("Vector store initialized successfully")
    
    def _flatten_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Flatten metadata to ensure all values are simple types for ChromaDB"""
        flattened = {}
        for key, value in metadata.items():
            if isinstance(value, dict):
                # Flatten nested dictionaries by converting to strings
                flattened[key] = json.dumps(value, ensure_ascii=False)
            elif isinstance(value, list):
                # Convert lists to comma-separated strings
                flattened[key] = ", ".join(str(item) for item in value) if value else ""
            elif isinstance(value, (str, int, float, bool)) or value is None:
                # Keep simple types as is
                flattened[key] = value
            else:
                # Convert any other type to string
                flattened[key] = str(value)
        return flattened

    def add_document(self, document_id: str, text: str, metadata: Dict[str, Any] = None):
        """Add a document to the vector store - each file as one chunk for better context"""
        try:
            if metadata is None:
                metadata = {}
            
            # Flatten metadata for ChromaDB compatibility
            flattened_metadata = self._flatten_metadata(metadata)
            
            # Add document ID and filename to metadata
            flattened_metadata['document_id'] = document_id
            flattened_metadata['filename'] = metadata.get('filename', document_id)
            
            # Treat each file as one chunk for complete policy context
            # No chunking - keep the entire document intact
            chunks = [text]  # Single chunk containing the entire file
            
            # Generate embeddings for the single chunk
            embeddings = self.embedding_model.encode(chunks)
            
            # Normalize embeddings
            normalized_embeddings = []
            for embedding in embeddings:
                norm = np.linalg.norm(embedding)
                if norm > 0:
                    normalized_embedding = embedding / norm
                else:
                    normalized_embedding = embedding
                normalized_embeddings.append(normalized_embedding.tolist())
            
            # Create unique IDs for the single chunk
            ids = [f"{document_id}_chunk_0"]
            
            # Add to collection
            self.collection.add(
                embeddings=normalized_embeddings,
                documents=chunks,
                metadatas=[flattened_metadata] * len(chunks),
                ids=ids
            )
            
            logger.info(f"Added document {document_id} as single chunk (file-based chunking)")
            return 1  # Return 1 since we're treating each file as one chunk
            
        except Exception as e:
            logger.error(f"Error adding document {document_id}: {e}")
            return 0
    
    def add_documents_from_organized_folder(self, organized_path: str = None):
        """Add all organized documents to the vector store - each file as one chunk"""
        if organized_path is None:
            organized_path = "./kfg_policy/organized"
        
        added_documents = []
        
        if not os.path.exists(organized_path):
            logger.error(f"Organized folder not found: {organized_path}")
            return added_documents
        
        # Process organized documents
        for filename in os.listdir(organized_path):
            if filename.endswith('_organized.txt'):
                file_path = os.path.join(organized_path, filename)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                    
                    if text.strip():
                        # Get corresponding metadata
                        metadata_file = filename.replace('_organized.txt', '_metadata.json')
                        metadata_path = os.path.join("./kfg_policy/metadata", metadata_file)
                        
                        metadata = {}
                        if os.path.exists(metadata_path):
                            with open(metadata_path, 'r', encoding='utf-8') as f:
                                metadata = json.load(f)
                        
                        # Add document ID
                        document_id = filename.replace('_organized.txt', '')
                        
                        # Add to vector store (each file as one chunk)
                        chunks_added = self.add_document(document_id, text, metadata)
                        
                        if chunks_added > 0:
                            added_documents.append({
                                'document_id': document_id,
                                'filename': filename,
                                'chunks_added': chunks_added,  # Will always be 1 now
                                'metadata': metadata,
                                'approach': 'file-based_chunking'
                            })
                
                except Exception as e:
                    logger.error(f"Error processing {filename}: {e}")
        
        logger.info(f"Added {len(added_documents)} documents to vector store (file-based chunking)")
        return added_documents
    
    def add_documents_from_folder(self, folder_path: str):
        """Legacy method - now redirects to organized folder"""
        return self.add_documents_from_organized_folder(folder_path)
    
    def search(self, query: str, n_results: int = None) -> List[Dict[str, Any]]:
        """Enhanced search optimized for file-based chunks with better relevance"""
        if n_results is None:
            n_results = Config.MAX_DOCUMENTS_PER_QUERY
        
        try:
            # Get query embedding and normalize it
            query_embedding = self.embedding_model.encode([query])[0]
            query_embedding = query_embedding / (np.linalg.norm(query_embedding) + 1e-8)  # Normalize using numpy
            query_embedding = query_embedding.tolist()
            
            # Search in collection - get more results for better filtering
            search_results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=min(n_results * 2, 15),  # Get more results for filtering
                include=['documents', 'metadatas', 'distances']
            )
            
            # Format and filter results by relevance
            formatted_results = []
            for i in range(len(search_results['documents'][0])):
                doc = search_results['documents'][0][i]
                metadata = search_results['metadatas'][0][i]
                distance = search_results['distances'][0][i]
                
                # Convert distance to similarity (cosine similarity)
                # ChromaDB uses L2 distance, convert to cosine similarity
                similarity = max(0, 1 - (distance ** 2) / 2)
                
                # Only include results above minimum similarity threshold
                if similarity >= Config.MIN_SIMILARITY_SCORE:
                    formatted_results.append({
                        'document': doc,
                        'metadata': metadata,
                        'similarity': similarity,
                        'distance': distance
                    })
            
            # Sort by similarity and take top results
            formatted_results.sort(key=lambda x: x['similarity'], reverse=True)
            return formatted_results[:n_results]
            
        except Exception as e:
            logger.error(f"Error in search: {e}")
            return []
    
    def search_by_category(self, query: str, category: str, n_results: int = None) -> List[Dict[str, Any]]:
        """Search documents within a specific category"""
        if n_results is None:
            n_results = Config.MAX_DOCUMENTS_PER_QUERY
        
        try:
            # Get query embedding
            query_embedding = self.embedding_model.encode([query])[0].tolist()
            
            # Search with category filter
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results * 2,  # Get more results to filter
                where={"category": category},
                include=['documents', 'metadatas', 'distances']
            )
            
            # Format and filter results
            formatted_results = []
            for i in range(len(results['documents'][0])):
                doc = results['documents'][0][i]
                metadata = results['metadatas'][0][i]
                distance = results['distances'][0][i]
                
                similarity = 1 - distance
                
                formatted_results.append({
                    'document': doc,
                    'metadata': metadata,
                    'similarity': similarity,
                    'distance': distance
                })
            
            # Sort by similarity and limit results
            formatted_results.sort(key=lambda x: x['similarity'], reverse=True)
            return formatted_results[:n_results]
            
        except Exception as e:
            logger.error(f"Category search error: {e}")
            return []
    
    def search_by_type(self, query: str, doc_type: str, n_results: int = None) -> List[Dict[str, Any]]:
        """Search documents of a specific type"""
        if n_results is None:
            n_results = Config.MAX_DOCUMENTS_PER_QUERY
        
        try:
            # Get query embedding
            query_embedding = self.embedding_model.encode([query])[0].tolist()
            
            # Search with document type filter
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results * 2,
                where={"document_type": doc_type},
                include=['documents', 'metadatas', 'distances']
            )
            
            # Format and filter results
            formatted_results = []
            for i in range(len(results['documents'][0])):
                doc = results['documents'][0][i]
                metadata = results['metadatas'][0][i]
                distance = results['distances'][0][i]
                
                similarity = 1 - distance
                
                formatted_results.append({
                    'document': doc,
                    'metadata': metadata,
                    'similarity': similarity,
                    'distance': distance
                })
            
            # Sort by similarity and limit results
            formatted_results.sort(key=lambda x: x['similarity'], reverse=True)
            return formatted_results[:n_results]
            
        except Exception as e:
            logger.error(f"Type search error: {e}")
            return []
    
    def get_document_by_id(self, document_id: str) -> List[Dict[str, Any]]:
        """Get all chunks of a specific document"""
        try:
            results = self.collection.get(
                where={"document_id": document_id},
                include=['documents', 'metadatas']
            )
            
            # Sort chunks by index
            chunks = []
            for i in range(len(results['documents'])):
                chunks.append({
                    'document': results['documents'][i],
                    'metadata': results['metadatas'][i]
                })
            
            chunks.sort(key=lambda x: x['metadata'].get('chunk_index', 0))
            return chunks
            
        except Exception as e:
            logger.error(f"Error getting document {document_id}: {e}")
            return []
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection"""
        try:
            if not self.collection:
                return {"error": "Collection not initialized"}
            
            count = self.collection.count()
            return {
                "total_documents": count,
                "collection_name": self.collection.name,
                "status": "active"
            }
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {"error": str(e)}
    
    def get_document_categories(self) -> List[str]:
        """Get all available document categories"""
        try:
            if not self.collection:
                return []
            
            # Get all documents and extract unique categories
            results = self.collection.get()
            categories = set()
            
            for metadata in results['metadatas']:
                if metadata and 'category' in metadata:
                    categories.add(metadata['category'])
            
            return sorted(list(categories))
        except Exception as e:
            logger.error(f"Error getting document categories: {e}")
            return []
    
    def get_document_types(self) -> List[str]:
        """Get all available document types"""
        try:
            if not self.collection:
                return []
            
            # Get all documents and extract unique types
            results = self.collection.get()
            types = set()
            
            for metadata in results['metadatas']:
                if metadata and 'document_type' in metadata:
                    types.add(metadata['document_type'])
            
            return sorted(list(types))
        except Exception as e:
            logger.error(f"Error getting document types: {e}")
            return []
    
    def delete_document(self, document_id: str):
        """Delete all chunks of a specific document"""
        try:
            self.collection.delete(where={"document_id": document_id})
            logger.info(f"Deleted document {document_id}")
        except Exception as e:
            logger.error(f"Error deleting document {document_id}: {e}")
    
    def clear_collection(self):
        """Clear all documents from the collection"""
        try:
            # Get all document IDs and delete them
            results = self.collection.get()
            if results['ids']:
                self.collection.delete(ids=results['ids'])
            logger.info("Collection cleared successfully")
        except Exception as e:
            logger.error(f"Error clearing collection: {e}")
            # Try alternative method
            try:
                self.collection.delete(where={})
                logger.info("Collection cleared using alternative method")
            except Exception as e2:
                logger.error(f"Alternative clear method also failed: {e2}")
    
    def rebuild_index(self):
        """Rebuild the entire index from organized documents"""
        try:
            logger.info("Rebuilding vector index...")
            
            # Clear existing collection
            self.clear_collection()
            
            # Recreate collection
            self.collection = self.client.get_or_create_collection(
                name="kfg_policies_v2",
                metadata={"description": "KFG Policy Documents - Rebuilt Index"}
            )
            
            # Add all organized documents
            added_docs = self.add_documents_from_organized_folder()
            
            logger.info(f"Index rebuilt with {len(added_docs)} documents")
            return added_docs
            
        except Exception as e:
            logger.error(f"Error rebuilding index: {e}")
            return []

if __name__ == "__main__":
    # Initialize vector store and add documents
    vector_store = VectorStore()
    
    # Add documents from the extracted folder
    results = vector_store.add_documents_from_organized_folder(Config.EXTRACTED_PATH)
    
    print(f"Added {len(results)} documents to vector store")
    print("Collection stats:", vector_store.get_collection_stats()) 