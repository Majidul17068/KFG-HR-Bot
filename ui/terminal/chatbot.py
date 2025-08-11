import os
import logging
import sys
from typing import List, Dict, Any, Optional
from pathlib import Path

# Add the project root to Python path for imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from rag_engine.vector_store.vector_store import VectorStore
from models.llm.deepseek_client import DeepSeekClient
from rag_engine.document_processing.document_processor import DocumentProcessor
from config.config import Config

logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL))
logger = logging.getLogger(__name__)

class KFGChatbot:
    def __init__(self):
        """Initialize the KFG Policy Chatbot with cost optimization"""
        try:
            self.vector_store = VectorStore()
            self.deepseek_client = DeepSeekClient()
            self.document_processor = DocumentProcessor()
            
            logger.info("KFG Chatbot initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize chatbot: {e}")
            raise
    
    def process_and_index_documents(self, force_reprocess: bool = False) -> Dict[str, Any]:
        """Process documents and add them to vector store with improved organization"""
        try:
            results = {
                "processed_files": [],
                "indexed_documents": [],
                "errors": [],
                "organization_summary": {}
            }
            
            # Check if organized documents exist
            if os.path.exists(Config.ORGANIZED_PATH):
                logger.info("Using existing organized documents")
                # Get organization summary
                organized_files = [f for f in os.listdir(Config.ORGANIZED_PATH) if f.endswith('_organized.txt')]
                results["processed_files"] = organized_files
                
                # Create summary from organized structure
                summary = self._get_organized_summary()
                results["organization_summary"] = summary
            else:
                logger.info("Organized documents not found, processing from scratch...")
                # Run document organization
                try:
                    from fix_kfg_documents import KFGDocumentFixer
                    fixer = KFGDocumentFixer()
                    fixer_results = fixer.process_all_documents()
                    results["processed_files"] = [doc['filename'] for doc in fixer_results['processed']]
                    results["organization_summary"] = fixer_results['summary']
                except Exception as e:
                    logger.error(f"Document organization failed: {e}")
                    results["errors"].append(f"Document organization failed: {e}")
                    return results
            
            # Index documents in vector store
            logger.info("Indexing documents in vector store...")
            indexed_docs = self.vector_store.add_documents_from_organized_folder()
            results["indexed_documents"] = indexed_docs
            
            # Get collection stats
            stats = self.vector_store.get_collection_stats()
            results["stats"] = stats
            
            logger.info(f"Successfully processed and indexed {len(indexed_docs)} documents")
            return results
            
        except Exception as e:
            logger.error(f"Error in process_and_index_documents: {e}")
            results["errors"].append(str(e))
            return results
    
    def _get_organized_summary(self) -> Dict[str, Any]:
        """Get summary from organized document structure"""
        try:
            summary = {
                'total_files': 0,
                'categories': {},
                'types': {},
                'organized_path': Config.ORGANIZED_PATH
            }
            
            # Count organized files
            organized_path = Path(Config.ORGANIZED_PATH)
            if organized_path.exists():
                organized_files = list(organized_path.glob("*.txt"))
                summary['total_files'] = len(organized_files)
                
                # Count by category
                category_path = organized_path / "by_category"
                if category_path.exists():
                    for category_folder in category_path.iterdir():
                        if category_folder.is_dir():
                            category_files = list(category_folder.glob("*.txt"))
                            summary['categories'][category_folder.name] = len(category_files)
                
                # Count by type
                type_path = organized_path / "by_type"
                if type_path.exists():
                    for type_folder in type_path.iterdir():
                        if type_folder.is_dir():
                            type_files = list(type_folder.glob("*.txt"))
                            summary['types'][type_folder.name] = len(type_files)
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting organized summary: {e}")
            return {'error': str(e)}
    
    def chat(self, query: str, chat_history: List[Dict[str, str]] = None, 
             category_filter: str = None, doc_type_filter: str = None) -> Dict[str, Any]:
        """Enhanced chat function with filtering and cost optimization"""
        try:
            if not query.strip():
                return {
                    "response": "Please provide a question about KFG policies.",
                    "sources": [],
                    "error": None,
                    "cost_estimate": {}
                }
            
            # Search for relevant documents with filtering
            logger.info(f"Searching for documents related to: {query}")
            
            if category_filter:
                relevant_docs = self.vector_store.search_by_category(query, category_filter, Config.MAX_DOCUMENTS_PER_QUERY)
            elif doc_type_filter:
                relevant_docs = self.vector_store.search_by_type(query, doc_type_filter, Config.MAX_DOCUMENTS_PER_QUERY)
            else:
                relevant_docs = self.vector_store.search(query, Config.MAX_DOCUMENTS_PER_QUERY)
            
            logger.info(f"Vector store returned {len(relevant_docs)} documents")
            for i, doc in enumerate(relevant_docs):
                logger.info(f"Doc {i}: similarity={doc.get('similarity', 0):.3f}, length={len(doc.get('document', ''))}, filename={doc['metadata'].get('filename', 'Unknown')}")
            
            # Filter documents by similarity threshold (vector store already filters by MIN_SIMILARITY_SCORE)
            # So we can use a lower threshold here for better coverage
            filtered_docs = [
                doc for doc in relevant_docs 
                if doc.get('similarity', 0) >= 0.2  # Lower threshold for better coverage
            ]
            
            logger.info(f"After filtering: {len(filtered_docs)} documents")
            for i, doc in enumerate(filtered_docs):
                logger.info(f"Filtered Doc {i}: similarity={doc.get('similarity', 0):.3f}, length={len(doc.get('document', ''))}")
            
            if not filtered_docs:
                logger.info("No relevant documents found")
                return {
                    "response": "I couldn't find any relevant policy information for your question. Please try rephrasing your question or ask about a different policy topic.",
                    "sources": [],
                    "error": None,
                    "cost_estimate": {}
                }
            
            # Get cost estimate before generating response
            cost_estimate = self.deepseek_client.get_cost_estimate(query, filtered_docs)
            
            # Generate response using RAG
            logger.info("Generating response using DeepSeek...")
            response = self.deepseek_client.chat_with_rag(
                query=query,
                context_documents=filtered_docs,
                chat_history=chat_history
            )
            
            # Prepare sources information
            sources = []
            for doc in filtered_docs:
                sources.append({
                    "filename": doc['metadata'].get('filename', 'Unknown'),
                    "similarity": doc.get('similarity', 0),
                    "category": doc['metadata'].get('category', 'Unknown'),
                    "document_type": doc['metadata'].get('document_type', 'Unknown'),
                    "date": doc['metadata'].get('date', 'Unknown')
                })
            
            return {
                "response": response,
                "sources": sources,
                "error": None,
                "cost_estimate": cost_estimate,
                "documents_used": len(filtered_docs)
            }
            
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return {
                "response": f"An error occurred while processing your question: {str(e)}",
                "sources": [],
                "error": str(e),
                "cost_estimate": {}
            }
    
    def get_policy_categories(self) -> List[str]:
        """Get available policy categories"""
        try:
            return self.vector_store.get_document_categories()
        except Exception as e:
            logger.error(f"Error getting policy categories: {e}")
            return []
    
    def get_document_types(self) -> List[str]:
        """Get available document types"""
        try:
            return self.vector_store.get_document_types()
        except Exception as e:
            logger.error(f"Error getting document types: {e}")
            return []
    
    def search_policies(self, query: str, category: str = None, doc_type: str = None, 
                       limit: int = 5) -> List[Dict[str, Any]]:
        """Search policies with optional filtering and better context"""
        try:
            if category:
                results = self.vector_store.search_by_category(query, category, limit)
            elif doc_type:
                results = self.vector_store.search_by_type(query, doc_type, limit)
            else:
                results = self.vector_store.search(query, limit)
            
            # Format results for display with more context
            formatted_results = []
            for doc in results:
                # Get more content for better context
                content = doc['document']
                if len(content) > 500:
                    # Show first 300 and last 200 characters for long documents
                    content_preview = content[:300] + "..." + content[-200:]
                else:
                    content_preview = content
                
                formatted_results.append({
                    "content": content_preview,
                    "full_content": content,  # Keep full content for detailed analysis
                    "filename": doc['metadata'].get('filename', 'Unknown'),
                    "similarity": doc.get('similarity', 0),
                    "category": doc['metadata'].get('category', 'Unknown'),
                    "document_type": doc['metadata'].get('document_type', 'Unknown'),
                    "date": doc['metadata'].get('date', 'Unknown'),
                    "entities": doc['metadata'].get('entities', {})
                })
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error in search_policies: {e}")
            return []
    
    def get_policy_summary(self, policy_name: str = None) -> Dict[str, Any]:
        """Get summary of policies or specific policy details"""
        try:
            if policy_name:
                # Get specific policy details
                policy_docs = self.vector_store.get_document_by_id(policy_name)
                if policy_docs:
                    metadata = policy_docs[0]['metadata']
                    return {
                        "name": policy_name,
                        "category": metadata.get('category', 'Unknown'),
                        "document_type": metadata.get('document_type', 'Unknown'),
                        "date": metadata.get('date', 'Unknown'),
                        "chunks": len(policy_docs),
                        "content_preview": policy_docs[0]['document'][:300] + "..." if len(policy_docs[0]['document']) > 300 else policy_docs[0]['document']
                    }
                else:
                    return {"error": "Policy not found"}
            else:
                # Get overall policy summary
                stats = self.vector_store.get_collection_stats()
                return {
                    "total_policies": stats.get('total_documents', 0),
                    "categories": stats.get('categories', {}),
                    "document_types": stats.get('document_types', {}),
                    "embedding_model": stats.get('embedding_model', 'Unknown')
                }
                
        except Exception as e:
            logger.error(f"Error in get_policy_summary: {e}")
            return {"error": str(e)}
    
    def upload_and_process_document(self, file_path: str, filename: str) -> Dict[str, Any]:
        """Upload and process a new policy document"""
        try:
            logger.info(f"Processing uploaded document: {filename}")
            
            # Process the document
            result = self.document_processor.process_document(file_path)
            
            if result and result.get('processing_status') == 'success':
                # Add to vector store
                chunks_added = self.vector_store.add_document(
                    document_id=os.path.splitext(filename)[0],
                    text=result['content']['cleaned'],
                    metadata=result['metadata']
                )
                
                return {
                    "success": True,
                    "filename": filename,
                    "chunks_added": chunks_added,
                    "metadata": result['metadata'],
                    "message": f"Document processed and indexed successfully with {chunks_added} chunks"
                }
            else:
                return {
                    "success": False,
                    "filename": filename,
                    "error": result.get('error', 'Unknown processing error'),
                    "message": "Failed to process document"
                }
                
        except Exception as e:
            logger.error(f"Error in upload_and_process_document: {e}")
            return {
                "success": False,
                "filename": filename,
                "error": str(e),
                "message": "An error occurred during document processing"
            }
    
    def get_document_list(self) -> List[Dict[str, Any]]:
        """Get list of all indexed documents"""
        try:
            stats = self.vector_store.get_collection_stats()
            return [
                {
                    "total_documents": stats.get('total_documents', 0),
                    "categories": stats.get('categories', {}),
                    "document_types": stats.get('document_types', {}),
                    "embedding_model": stats.get('embedding_model', 'Unknown')
                }
            ]
        except Exception as e:
            logger.error(f"Error in get_document_list: {e}")
            return []
    
    def delete_document(self, document_id: str) -> Dict[str, Any]:
        """Delete a document from the vector store"""
        try:
            self.vector_store.delete_document(document_id)
            return {
                "success": True,
                "message": f"Document {document_id} deleted successfully"
            }
        except Exception as e:
            logger.error(f"Error deleting document {document_id}: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to delete document {document_id}"
            }
    
    def test_system(self) -> Dict[str, Any]:
        """Test all system components"""
        results = {
            "vector_store": False,
            "deepseek_api": False,
            "document_processor": False,
            "overall": False
        }
        
        try:
            # Test vector store
            stats = self.vector_store.get_collection_stats()
            results["vector_store"] = bool(stats.get('total_documents', 0) >= 0)
            
            # Test DeepSeek API
            results["deepseek_api"] = self.deepseek_client.test_connection()
            
            # Test document processor
            results["document_processor"] = os.path.exists(Config.PROCESSED_PATH)
            
            # Overall status
            results["overall"] = all([results["vector_store"], results["deepseek_api"], results["document_processor"]])
            
        except Exception as e:
            logger.error(f"Error in system test: {e}")
            results["overall"] = False
        
        return results
    
    def get_cost_analysis(self) -> Dict[str, Any]:
        """Get cost analysis and optimization suggestions"""
        try:
            cost_stats = cost_monitor.get_usage_summary()
            
            # Get collection stats for context
            collection_stats = self.vector_store.get_collection_stats()
            
            analysis = {
                "total_requests": cost_stats.get('total', {}).get('requests', 0),
                "total_tokens": cost_stats.get('total', {}).get('tokens', 0),
                "average_tokens_per_request": cost_stats.get('total', {}).get('tokens', 0) / max(cost_stats.get('total', {}).get('requests', 1), 1),
                "estimated_cost": cost_stats.get('total', {}).get('cost_usd', 0),
                "optimization_suggestions": []
            }
            
            # Generate optimization suggestions
            if cost_stats.get('average_tokens_per_request', 0) > 1000:
                analysis["optimization_suggestions"].append("Consider reducing MAX_TOKENS in config")
            
            if collection_stats.get('total_chunks', 0) > 1000:
                analysis["optimization_suggestions"].append("Consider reducing CHUNK_SIZE for more precise retrieval")
            
            if not analysis["optimization_suggestions"]:
                analysis["optimization_suggestions"].append("System is well-optimized for cost efficiency")
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in cost analysis: {e}")
            return {"error": str(e)}
    
    def get_custom_prompts(self) -> Dict[str, Any]:
        """Get available custom prompts and their details"""
        try:
            from config.custom_prompts import CustomPrompts
            prompts = CustomPrompts.get_all_prompts()
            
            return {
                "success": True,
                "custom_prompts": prompts,
                "total_prompts": len(prompts),
                "message": "Custom prompts retrieved successfully"
            }
        except Exception as e:
            logger.error(f"Error getting custom prompts: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to retrieve custom prompts"
            }
    
    def add_custom_prompt(self, prompt_key: str, keywords: List[str], response: str, confidence_boost: float = 0.9) -> Dict[str, Any]:
        """Add a new custom prompt dynamically"""
        try:
            from config.custom_prompts import CustomPrompts
            
            # Add new prompt to the custom prompts
            CustomPrompts.CUSTOM_PROMPTS[prompt_key] = {
                "keywords": keywords,
                "response": response,
                "confidence_boost": confidence_boost,
                "source": "Dynamically Added Custom Policy"
            }
            
            return {
                "success": True,
                "message": f"Custom prompt '{prompt_key}' added successfully",
                "prompt_key": prompt_key,
                "keywords": keywords
            }
        except Exception as e:
            logger.error(f"Error adding custom prompt: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to add custom prompt '{prompt_key}'"
            }
    
    def optimize_for_cost(self) -> Dict[str, Any]:
        """Apply cost optimization strategies"""
        try:
            optimizations = {
                "chunk_size_reduced": False,
                "similarity_threshold_increased": False,
                "max_documents_reduced": False,
                "max_tokens_reduced": False
            }
            
            # Get current stats
            stats = self.vector_store.get_collection_stats()
            current_chunks = stats.get('total_chunks', 0)
            
            # Suggest optimizations based on current state
            if current_chunks > 500:
                optimizations["chunk_size_reduced"] = True
                logger.info("Suggesting chunk size reduction for cost optimization")
            
            # Check if we can increase similarity threshold
            if current_chunks > 200:
                optimizations["similarity_threshold_increased"] = True
                logger.info("Suggesting similarity threshold increase for better relevance")
            
            return {
                "success": True,
                "optimizations": optimizations,
                "message": "Cost optimization analysis completed",
                "suggestions": [
                    "Consider reducing CHUNK_SIZE from 512 to 400",
                    "Increase SIMILARITY_THRESHOLD to 0.8",
                    "Reduce MAX_DOCUMENTS_PER_QUERY to 1 for very specific queries"
                ]
            }
            
        except Exception as e:
            logger.error(f"Error in cost optimization: {e}")
            return {"success": False, "error": str(e)} 