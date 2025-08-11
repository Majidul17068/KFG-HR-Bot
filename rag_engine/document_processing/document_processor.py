#!/usr/bin/env python3
"""
Enhanced Document Processor for KFG Policy Documents
Optimized for cost efficiency and better document organization
"""

import os
import re
import json
import logging
import shutil
import sys
import os
import json
import re
from datetime import datetime
from typing import Dict, List, Any, Tuple
from pathlib import Path

# Add the project root to Python path for imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from config.config import Config

class DocumentProcessor:
    def __init__(self):
        self.setup_logging()
        self.setup_directories()
        
        # Enhanced OCR text fixes for KFG documents
        self.ocr_fixes = {
            'DG!': 'DGM',
            'abed': 'abed',
            'Resend': 'Resend',
            'Lerner': 'Learner',
            'Se': 'Se',
            'minimumTk': 'minimum Tk',
            'Tk': 'Tk',
            'Tk.': 'Tk.',
            'Tk,': 'Tk.',
            'KFG': 'KFG',
            'KFIL': 'KFIL',
            'KML': 'KML',
            'AGM': 'AGM',
            'DGM': 'DGM',
            'GM': 'GM',
            'HRD': 'HRD',
            'TA': 'TA',
            'DA': 'DA',
            'FTDA': 'FTDA',
            'IOU': 'IOU',
            'APO': 'APO',
            'bKash': 'bKash',
            'Eidulfitur': 'Eidulfitur',
            'Gojaria': 'Gojaria',
            'Panchagarh': 'Panchagarh',
            'Sagarica': 'Sagarica',
            'Thakurgaon': 'Thakurgaon'
        }
        
        # Policy categories for better organization
        self.policy_categories = {
            'salary': ['salary', 'increment', 'structure', 'payment', 'wage'],
            'allowance': ['allowance', 'house', 'food', 'transport', 'location', 'guard', 'furniture'],
            'leave': ['leave', 'holiday', 'off day', 'replacement'],
            'bonus': ['bonus', 'incentive', 'performance', 'production'],
            'travel': ['TA', 'DA', 'tour', 'travel', 'fuel', 'car'],
            'recruitment': ['recruitment', 'worker', 'employee', 'hiring'],
            'medical': ['medical', 'health', 'insurance'],
            'transport': ['transport', 'car', 'motorcycle', 'driver'],
            'general': ['policy', 'procedure', 'notice', 'circular', 'order']
        }
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=getattr(logging, Config.LOG_LEVEL),
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(Config.LOG_FILE),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_directories(self):
        """Create necessary directories for document organization"""
        directories = [
            Config.PROCESSED_PATH,
            os.path.join(Config.PROCESSED_PATH, 'by_category'),
            os.path.join(Config.PROCESSED_PATH, 'by_date'),
            os.path.join(Config.PROCESSED_PATH, 'metadata')
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            self.logger.info(f"Created directory: {directory}")
    
    def clean_ocr_text(self, text: str) -> str:
        """
        Enhanced text cleaning for KFG policy documents
        """
        if not text:
            return ""
        
        # Apply OCR fixes
        for wrong, correct in self.ocr_fixes.items():
            text = text.replace(wrong, correct)
        
        # Fix common spacing issues
        text = re.sub(r'\s+', ' ', text)  # Multiple spaces to single
        text = re.sub(r'([a-zA-Z])([0-9])', r'\1 \2', text)  # Space between English and numbers
        text = re.sub(r'([0-9])([a-zA-Z])', r'\1 \2', text)  # Space between numbers and English
        
        # Fix broken words at line breaks
        text = re.sub(r'([a-zA-Z])\s*\n\s*([a-zA-Z])', r'\1\2', text)
        
        # Fix table formatting
        text = re.sub(r'(\|)\s*(\|)', r'\1\2', text)  # Fix broken table separators
        
        # Remove excessive newlines and whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r'[ \t]+', ' ', text)
        
        # Clean up special characters but preserve important ones
        text = re.sub(r'[^\w\s\.\,\-\|\:\;\(\)\[\]\{\}\@\#\$\%\&\*\+\=\<\>\?\/\~`!]', '', text)
        
        # Fix common policy document formatting issues
        text = re.sub(r'([A-Z])\s*\.\s*([A-Z])', r'\1.\2', text)  # Fix abbreviations
        text = re.sub(r'(\d+)\s*\.\s*(\d+)', r'\1.\2', text)  # Fix decimal numbers
        
        return text.strip()
    
    def categorize_policy(self, text: str, filename: str) -> str:
        """
        Categorize policy documents based on content and filename
        """
        text_lower = text.lower()
        filename_lower = filename.lower()
        
        # Check each category
        for category, keywords in self.policy_categories.items():
            for keyword in keywords:
                if keyword in text_lower or keyword in filename_lower:
                    return category
        
        return 'general'
    
    def extract_metadata(self, text: str, filename: str) -> Dict[str, Any]:
        """
        Enhanced metadata extraction for KFG policy documents
        """
        metadata = {
            'filename': filename,
            'original_filename': filename,
            'document_number': '',
            'date': '',
            'policy_name': '',
            'company_name': 'KFG',
            'document_type': '',
            'category': '',
            'processed_date': datetime.now().isoformat(),
            'file_size': 0,
            'word_count': len(text.split()),
            'language': 'en'
        }
        
        # Extract document type from filename
        filename_lower = filename.lower()
        if 'policy' in filename_lower:
            metadata['document_type'] = 'Policy'
        elif 'proposal' in filename_lower:
            metadata['document_type'] = 'Proposal'
        elif 'procedure' in filename_lower:
            metadata['document_type'] = 'Procedure'
        elif 'notice' in filename_lower:
            metadata['document_type'] = 'Notice'
        elif 'circular' in filename_lower:
            metadata['document_type'] = 'Circular'
        elif 'order' in filename_lower:
            metadata['document_type'] = 'Order'
        else:
            metadata['document_type'] = 'Document'
        
        # Extract date patterns
        date_patterns = [
            r'(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})',  # DD/MM/YYYY
            r'(\d{4}[\/\-\.]\d{1,2}[\/\-\.]\d{1,2})',  # YYYY/MM/DD
            r'(\w+\s+\d{1,2},\s*\d{4})',  # Month DD, YYYY
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                metadata['date'] = match.group(1)
                break
        
        # Extract policy name (first line or title)
        lines = text.split('\n')
        if lines:
            first_line = lines[0].strip()
            if len(first_line) > 10 and len(first_line) < 200:
                metadata['policy_name'] = first_line
        
        # Categorize the policy
        metadata['category'] = self.categorize_policy(text, filename)
        
        return metadata
    
    def structure_content(self, text: str) -> Dict[str, str]:
        """
        Structure policy content into sections for better retrieval
        """
        sections = {
            'title': '',
            'summary': '',
            'main_content': '',
            'key_points': [],
            'dates': [],
            'amounts': [],
            'contacts': []
        }
        
        lines = text.split('\n')
        
        # Extract title (first non-empty line)
        for line in lines:
            if line.strip() and len(line.strip()) > 5:
                sections['title'] = line.strip()
                break
        
        # Extract key points (lines with bullet points or numbers)
        key_points = []
        for line in lines:
            line = line.strip()
            if (line.startswith('•') or line.startswith('-') or 
                re.match(r'^\d+\.', line) or re.match(r'^[A-Z]\.', line)):
                key_points.append(line)
        sections['key_points'] = key_points[:10]  # Limit to 10 key points
        
        # Extract amounts (currency values)
        amounts = re.findall(r'Tk\.?\s*\d+[,\d]*', text)
        sections['amounts'] = amounts[:5]  # Limit to 5 amounts
        
        # Extract dates
        dates = re.findall(r'\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4}', text)
        sections['dates'] = dates[:5]  # Limit to 5 dates
        
        # Main content (everything else)
        sections['main_content'] = text
        
        return sections
    
    def process_document(self, file_path: str) -> Dict[str, Any]:
        """
        Process a single policy document with enhanced cleaning
        """
        try:
            filename = os.path.basename(file_path)
            self.logger.info(f"Processing document: {filename}")
            
            # Read the document
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
            
            if not text.strip():
                self.logger.warning(f"Empty document: {filename}")
                return None
            
            # Clean the text
            cleaned_text = self.clean_ocr_text(text)
            
            # Extract metadata
            metadata = self.extract_metadata(cleaned_text, filename)
            
            # Structure content
            structured_content = self.structure_content(cleaned_text)
            
            # Create processing result
            result = {
                'filename': filename,
                'file_path': file_path,
                'metadata': metadata,
                'content': {
                    'original': text,
                    'cleaned': cleaned_text,
                    'structured': structured_content
                },
                'processing_status': 'success',
                'processing_date': datetime.now().isoformat()
            }
            
            self.logger.info(f"Successfully processed: {filename}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error processing {file_path}: {e}")
            return {
                'filename': filename,
                'file_path': file_path,
                'error': str(e),
                'processing_status': 'error',
                'processing_date': datetime.now().isoformat()
            }
    
    def organize_documents(self, processed_docs: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Organize documents by category and date for better management
        """
        organized = {
            'by_category': {},
            'by_date': {},
            'by_type': {},
            'summary': {
                'total_documents': len(processed_docs),
                'categories': {},
                'types': {},
                'processing_errors': 0
            }
        }
        
        for doc in processed_docs:
            if doc.get('processing_status') == 'error':
                organized['summary']['processing_errors'] += 1
                continue
            
            metadata = doc.get('metadata', {})
            category = metadata.get('category', 'general')
            doc_type = metadata.get('document_type', 'Document')
            date = metadata.get('date', 'Unknown')
            
            # Organize by category
            if category not in organized['by_category']:
                organized['by_category'][category] = []
            organized['by_category'][category].append(doc)
            
            # Organize by type
            if doc_type not in organized['by_type']:
                organized['by_type'][doc_type] = []
            organized['by_type'][doc_type].append(doc)
            
            # Organize by date
            if date not in organized['by_date']:
                organized['by_date'][date] = []
            organized['by_date'][date].append(doc)
            
            # Update summary counts
            organized['summary']['categories'][category] = organized['summary']['categories'].get(category, 0) + 1
            organized['summary']['types'][doc_type] = organized['summary']['types'].get(doc_type, 0) + 1
        
        return organized
    
    def save_organized_documents(self, organized_docs: Dict, output_path: str):
        """
        Save organized documents to structured folders
        """
        try:
            # Save by category
            for category, docs in organized_docs['by_category'].items():
                category_path = os.path.join(output_path, 'by_category', category)
                os.makedirs(category_path, exist_ok=True)
                
                for doc in docs:
                    filename = doc['filename']
                    clean_filename = self.sanitize_filename(filename)
                    
                    # Save cleaned text
                    text_path = os.path.join(category_path, f"{clean_filename}_cleaned.txt")
                    with open(text_path, 'w', encoding='utf-8') as f:
                        f.write(doc['content']['cleaned'])
                    
                    # Save metadata
                    metadata_path = os.path.join(category_path, f"{clean_filename}_metadata.json")
                    with open(metadata_path, 'w', encoding='utf-8') as f:
                        json.dump(doc['metadata'], f, indent=2, ensure_ascii=False)
                    
                    # Save structured content
                    structured_path = os.path.join(category_path, f"{clean_filename}_structured.json")
                    with open(structured_path, 'w', encoding='utf-8') as f:
                        json.dump(doc['content']['structured'], f, indent=2, ensure_ascii=False)
            
            # Save summary
            summary_path = os.path.join(output_path, 'processing_summary.json')
            with open(summary_path, 'w', encoding='utf-8') as f:
                json.dump(organized_docs['summary'], f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Saved organized documents to: {output_path}")
            
        except Exception as e:
            self.logger.error(f"Error saving organized documents: {e}")
    
    def sanitize_filename(self, filename: str) -> str:
        """
        Sanitize filename for safe file system operations
        """
        # Remove or replace problematic characters
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
        sanitized = re.sub(r'\s+', '_', sanitized)
        sanitized = sanitized.strip('._')
        
        # Limit length
        if len(sanitized) > 100:
            name, ext = os.path.splitext(sanitized)
            sanitized = name[:95] + ext
        
        return sanitized
    
    def process_all_documents(self, folder_path: str = None) -> List[Dict[str, Any]]:
        """
        Process all documents in the specified folder
        """
        if folder_path is None:
            folder_path = Config.ORIGINAL_PATH
        
        self.logger.info(f"Starting batch document processing from: {folder_path}")
        
        if not os.path.exists(folder_path):
            self.logger.error(f"Folder not found: {folder_path}")
            return []
        
        # Get all text files
        text_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
        self.logger.info(f"Found {len(text_files)} text files to process")
        
        processed_docs = []
        
        for filename in text_files:
            file_path = os.path.join(folder_path, filename)
            result = self.process_document(file_path)
            if result:
                processed_docs.append(result)
        
        # Organize documents
        organized_docs = self.organize_documents(processed_docs)
        
        # Save organized documents
        self.save_organized_documents(organized_docs, Config.PROCESSED_PATH)
        
        # Save processing results
        self._save_processing_results(processed_docs, folder_path)
        
        self.logger.info(f"Completed processing {len(processed_docs)} documents")
        return processed_docs
    
    def _save_processing_results(self, processed_docs: List[Dict], folder_path: str):
        """
        Save processing results for reference
        """
        try:
            results_file = os.path.join(folder_path, 'processing_results.json')
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(processed_docs, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Saved processing results to: {results_file}")
            
        except Exception as e:
            self.logger.error(f"Error saving processing results: {e}")
    
    def get_processing_summary(self, processed_docs: List[Dict]) -> Dict[str, Any]:
        """
        Get summary statistics of processed documents
        """
        if not processed_docs:
            return {}
        
        total_docs = len(processed_docs)
        successful = len([d for d in processed_docs if d.get('processing_status') == 'success'])
        errors = total_docs - successful
        
        categories = {}
        types = {}
        
        for doc in processed_docs:
            if doc.get('processing_status') == 'success':
                metadata = doc.get('metadata', {})
                category = metadata.get('category', 'unknown')
                doc_type = metadata.get('document_type', 'unknown')
                
                categories[category] = categories.get(category, 0) + 1
                types[doc_type] = types.get(doc_type, 0) + 1
        
        return {
            'total_documents': total_docs,
            'successful_processing': successful,
            'processing_errors': errors,
            'success_rate': (successful / total_docs) * 100 if total_docs > 0 else 0,
            'categories': categories,
            'document_types': types
        }

 