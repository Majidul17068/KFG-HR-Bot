#!/usr/bin/env python3
"""
Enhanced Document Fixer for KFG Policy Documents
This script will reorganize, clean, and properly index all policy documents
"""

import os
import json
import shutil
import logging
from pathlib import Path
from typing import Dict, List, Any
import re
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class KFGDocumentFixer:
    def __init__(self):
        self.base_path = Path("./kfg_policy")
        self.cleaned_path = self.base_path / "cleaned_documents"
        self.organized_path = self.base_path / "organized"
        self.metadata_path = self.base_path / "metadata"
        
        # Create organized directory structure
        self.setup_directories()
        
        # Enhanced policy categories with better mapping
        self.policy_categories = {
            'salary_compensation': [
                'salary', 'increment', 'structure', 'payment', 'wage', 'bonus', 
                'incentive', 'performance', 'production', 'minimum salary'
            ],
            'allowances': [
                'allowance', 'house', 'food', 'transport', 'location', 'guard', 
                'furniture', 'mess', 'hair cutting', 'night', 'overtime'
            ],
            'travel_expenses': [
                'TA', 'DA', 'tour', 'travel', 'fuel', 'car', 'motorcycle', 
                'driver', 'helper', 'mechanic', 'FTDA'
            ],
            'leave_holidays': [
                'leave', 'holiday', 'off day', 'replacement', 'notice pay'
            ],
            'recruitment_hr': [
                'recruitment', 'worker', 'employee', 'hiring', 'job group', 
                'designation', 'transfer', 'retirement'
            ],
            'medical_benefits': [
                'medical', 'health', 'insurance', 'financial aid'
            ],
            'transport_facilities': [
                'transport', 'car', 'motorcycle', 'driver', 'pick and drop'
            ],
            'general_policies': [
                'policy', 'procedure', 'notice', 'circular', 'order', 'office'
            ]
        }
        
        # Document type mapping
        self.document_types = {
            'policy': ['policy', 'procedure', 'guideline'],
            'notice': ['notice', 'circular', 'order', 'memo'],
            'proposal': ['proposal', 'request', 'recommendation'],
            'approval': ['approval', 'approved', 'authorization']
        }
    
    def setup_directories(self):
        """Create organized directory structure"""
        directories = [
            self.organized_path,
            self.metadata_path,
            self.organized_path / "by_category",
            self.organized_path / "by_type",
            self.organized_path / "by_date"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {directory}")
    
    def clean_filename(self, filename: str) -> str:
        """Clean and standardize filename"""
        # Remove special characters and standardize
        cleaned = re.sub(r'[^\w\s\-_\.]', '', filename)
        cleaned = re.sub(r'\s+', '_', cleaned)
        cleaned = cleaned.replace('__', '_').strip('_')
        return cleaned
    
    def categorize_document(self, text: str, filename: str) -> str:
        """Enhanced document categorization"""
        text_lower = text.lower()
        filename_lower = filename.lower()
        
        # Check each category
        for category, keywords in self.policy_categories.items():
            for keyword in keywords:
                if keyword.lower() in text_lower or keyword.lower() in filename_lower:
                    return category
        
        return 'general_policies'
    
    def determine_document_type(self, text: str, filename: str) -> str:
        """Determine document type based on content and filename"""
        text_lower = text.lower()
        filename_lower = filename.lower()
        
        for doc_type, keywords in self.document_types.items():
            for keyword in keywords:
                if keyword.lower() in text_lower or keyword.lower() in filename_lower:
                    return doc_type
        
        return 'notice'
    
    def extract_date(self, text: str, filename: str) -> str:
        """Extract date from text or filename"""
        # Look for date patterns
        date_patterns = [
            r'(\d{1,2})[/\-](\d{1,2})[/\-](\d{4})',  # DD/MM/YYYY
            r'(\d{4})[/\-](\d{1,2})[/\-](\d{1,2})',  # YYYY/MM/DD
            r'(\w+)\s+(\d{1,2}),?\s*(\d{4})',        # Month DD, YYYY
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text + " " + filename)
            if match:
                try:
                    if len(match.groups()) == 3:
                        if len(match.group(1)) == 4:  # YYYY format
                            return f"{match.group(1)}-{match.group(2).zfill(2)}-{match.group(3).zfill(2)}"
                        else:  # DD format
                            return f"{match.group(3)}-{match.group(2).zfill(2)}-{match.group(1).zfill(2)}"
                except:
                    continue
        
        return "unknown_date"
    
    def create_metadata(self, text: str, filename: str, file_path: str) -> Dict[str, Any]:
        """Create comprehensive metadata for document"""
        # Get file stats
        stat = os.stat(file_path)
        
        # Determine category and type
        category = self.categorize_document(text, filename)
        doc_type = self.determine_document_type(text, filename)
        date = self.extract_date(text, filename)
        
        # Extract key information
        word_count = len(text.split())
        char_count = len(text)
        
        # Look for key entities
        entities = {
            'organizations': [],
            'positions': [],
            'amounts': [],
            'locations': []
        }
        
        # Extract organizations
        org_patterns = [r'\bKFG\b', r'\bKFIL\b', r'\bKML\b', r'\bSysnova\b']
        for pattern in org_patterns:
            if re.search(pattern, text):
                entities['organizations'].append(re.search(pattern, text).group())
        
        # Extract positions
        pos_patterns = [r'\bAGM\b', r'\bDGM\b', r'\bGM\b', r'\bHRD\b', r'\bAPO\b']
        for pattern in pos_patterns:
            if re.search(pattern, text):
                entities['positions'].append(re.search(pattern, text).group())
        
        # Extract amounts
        amount_patterns = [r'Tk\.?\s*(\d+(?:,\d+)*(?:\.\d+)?)', r'(\d+(?:,\d+)*(?:\.\d+)?)\s*Tk']
        for pattern in amount_patterns:
            matches = re.findall(pattern, text)
            entities['amounts'].extend(matches)
        
        metadata = {
            'filename': filename,
            'original_filename': filename,
            'category': category,
            'document_type': doc_type,
            'date': date,
            'file_size': stat.st_size,
            'word_count': word_count,
            'char_count': char_count,
            'entities': entities,
            'processing_date': datetime.now().isoformat(),
            'version': '2.0',
            'status': 'processed'
        }
        
        return metadata
    
    def process_document(self, file_path: str) -> Dict[str, Any]:
        """Process a single document"""
        try:
            filename = os.path.basename(file_path)
            logger.info(f"Processing: {filename}")
            
            # Read file content
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            if not content.strip():
                logger.warning(f"Empty file: {filename}")
                return None
            
            # Clean filename
            cleaned_filename = self.clean_filename(filename)
            
            # Create metadata
            metadata = self.create_metadata(content, filename, file_path)
            
            # Create organized file
            organized_filename = f"{cleaned_filename}_organized.txt"
            organized_path = self.organized_path / organized_filename
            
            with open(organized_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Save metadata
            metadata_filename = f"{cleaned_filename}_metadata.json"
            metadata_path = self.metadata_path / metadata_filename
            
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            # Copy to category folder
            category_folder = self.organized_path / "by_category" / metadata['category']
            category_folder.mkdir(exist_ok=True)
            
            category_file = category_folder / organized_filename
            shutil.copy2(organized_path, category_file)
            
            # Copy to type folder
            type_folder = self.organized_path / "by_type" / metadata['document_type']
            type_folder.mkdir(exist_ok=True)
            
            type_file = type_folder / organized_filename
            shutil.copy2(organized_path, type_file)
            
            logger.info(f"Successfully processed: {filename}")
            return {
                'filename': filename,
                'organized_filename': organized_filename,
                'metadata': metadata,
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Error processing {filename}: {e}")
            return {
                'filename': filename,
                'error': str(e),
                'status': 'error'
            }
    
    def process_all_documents(self):
        """Process all documents in the kfg_policy folder"""
        logger.info("Starting document processing...")
        
        results = {
            'processed': [],
            'errors': [],
            'summary': {}
        }
        
        # Process all .txt files
        txt_files = list(self.base_path.glob("*.txt"))
        logger.info(f"Found {len(txt_files)} text files to process")
        
        for file_path in txt_files:
            result = self.process_document(str(file_path))
            if result:
                if result['status'] == 'success':
                    results['processed'].append(result)
                else:
                    results['errors'].append(result)
        
        # Generate summary
        results['summary'] = {
            'total_files': len(txt_files),
            'successfully_processed': len(results['processed']),
            'errors': len(results['errors']),
            'categories': {},
            'types': {}
        }
        
        # Count by category and type
        for result in results['processed']:
            category = result['metadata']['category']
            doc_type = result['metadata']['document_type']
            
            results['summary']['categories'][category] = results['summary']['categories'].get(category, 0) + 1
            results['summary']['types'][doc_type] = results['summary']['types'].get(doc_type, 0) + 1
        
        # Save results
        results_file = self.base_path / "processing_results_v2.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Processing complete. Results saved to {results_file}")
        return results
    
    def create_index_file(self):
        """Create a comprehensive index file for all documents"""
        logger.info("Creating document index...")
        
        index = {
            'total_documents': 0,
            'categories': {},
            'types': {},
            'documents': []
        }
        
        # Read all metadata files
        metadata_files = list(self.metadata_path.glob("*_metadata.json"))
        
        for metadata_file in metadata_files:
            try:
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                
                index['documents'].append(metadata)
                index['total_documents'] += 1
                
                # Count by category
                category = metadata['category']
                if category not in index['categories']:
                    index['categories'][category] = []
                index['categories'][category].append(metadata['filename'])
                
                # Count by type
                doc_type = metadata['document_type']
                if doc_type not in index['types']:
                    index['types'][doc_type] = []
                index['types'][doc_type].append(metadata['filename'])
                
            except Exception as e:
                logger.error(f"Error reading metadata file {metadata_file}: {e}")
        
        # Save index
        index_file = self.base_path / "document_index_v2.json"
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Index created with {index['total_documents']} documents")
        return index

def main():
    """Main function to run the document fixer"""
    fixer = KFGDocumentFixer()
    
    # Process all documents
    results = fixer.process_all_documents()
    
    # Create index
    index = fixer.create_index_file()
    
    # Print summary
    print("\n" + "="*50)
    print("DOCUMENT PROCESSING COMPLETE")
    print("="*50)
    print(f"Total files processed: {results['summary']['total_files']}")
    print(f"Successfully processed: {results['summary']['successfully_processed']}")
    print(f"Errors: {results['summary']['errors']}")
    
    print("\nCategories:")
    for category, count in results['summary']['categories'].items():
        print(f"  {category}: {count}")
    
    print("\nDocument Types:")
    for doc_type, count in results['summary']['types'].items():
        print(f"  {doc_type}: {count}")
    
    print("\nFiles are now organized in:")
    print(f"  Organized: {fixer.organized_path}")
    print(f"  Metadata: {fixer.metadata_path}")
    print(f"  Index: {fixer.base_path}/document_index_v2.json")

if __name__ == "__main__":
    main() 