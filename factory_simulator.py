"""
Factory Simulator for FlowTex Factory
Handles product processing, queues, stacks, and sorting
"""

import csv
from datetime import datetime
from data_structures import Queue, Stack, LinkedList


class FactorySimulator:
    """Simulates factory production line operations"""
    
    def __init__(self):
        # Three queues for three product lines
        self.line_a_queue = Queue()
        self.line_b_queue = Queue()
        self.line_c_queue = Queue()
        
        # Stack for rejected products
        self.rejection_stack = Stack()
        
        # Linked lists for accepted products per line
        self.line_a_accepted = LinkedList()
        self.line_b_accepted = LinkedList()
        self.line_c_accepted = LinkedList()
        
        # Track all products for sorting
        self.all_products = []
    
    def load_from_csv(self, filepath):
        """Load products from CSV file and populate queues"""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    # Convert data types
                    product = {
                        'product_id': row.get('product_id', ''),
                        'product_line': row.get('product_line', ''),
                        'batch_id': row.get('batch_id', ''),
                        'line_sequence': int(row.get('line_sequence', 0)) if row.get('line_sequence') else 0,
                        'size': row.get('size', ''),
                        'color': row.get('color', ''),
                        'weight_g': float(row.get('weight_g', 0)) if row.get('weight_g') else 0.0,
                        'production_timestamp': row.get('production_timestamp', ''),
                        'raw_defect_score': float(row.get('raw_defect_score', 0)) if row.get('raw_defect_score') else 0.0,
                        'inspected': row.get('inspected', '').lower() == 'true',
                        'passed_inspection': row.get('passed_inspection', '').lower() == 'true',
                        'rejection_reason': row.get('rejection_reason', '')
                    }
                    
                    # Add to appropriate queue based on product line
                    if product['product_line'] == 'Line A':
                        self.line_a_queue.enqueue(product)
                    elif product['product_line'] == 'Line B':
                        self.line_b_queue.enqueue(product)
                    elif product['product_line'] == 'Line C':
                        self.line_c_queue.enqueue(product)
                    
                    # Store in all products for sorting
                    self.all_products.append(product)
            
            return True, f"Loaded {len(self.all_products)} products"
        except FileNotFoundError:
            return False, "CSV file not found"
        except Exception as e:
            return False, f"Error loading CSV: {str(e)}"
    
    def get_queue(self, line_name):
        """Get queue for a specific line"""
        if line_name == 'Line A':
            return self.line_a_queue
        elif line_name == 'Line B':
            return self.line_b_queue
        elif line_name == 'Line C':
            return self.line_c_queue
        return None
    
    def get_accepted_list(self, line_name):
        """Get accepted linked list for a specific line"""
        if line_name == 'Line A':
            return self.line_a_accepted
        elif line_name == 'Line B':
            return self.line_b_accepted
        elif line_name == 'Line C':
            return self.line_c_accepted
        return None
    
    def process_queues(self):
        """Process one item from each queue"""
        processed = []
        
        # Process Line A
        if not self.line_a_queue.is_empty():
            product = self.line_a_queue.dequeue()
            if product:
                if product.get('inspected') and not product.get('passed_inspection'):
                    self.handle_rejection(product)
                else:
                    self.handle_acceptance(product, 'Line A')
                processed.append(('Line A', product))
        
        # Process Line B
        if not self.line_b_queue.is_empty():
            product = self.line_b_queue.dequeue()
            if product:
                if product.get('inspected') and not product.get('passed_inspection'):
                    self.handle_rejection(product)
                else:
                    self.handle_acceptance(product, 'Line B')
                processed.append(('Line B', product))
        
        # Process Line C
        if not self.line_c_queue.is_empty():
            product = self.line_c_queue.dequeue()
            if product:
                if product.get('inspected') and not product.get('passed_inspection'):
                    self.handle_rejection(product)
                else:
                    self.handle_acceptance(product, 'Line C')
                processed.append(('Line C', product))
        
        return processed
    
    def handle_rejection(self, product):
        """Push rejected product to rejection stack"""
        self.rejection_stack.push(product)
    
    def handle_acceptance(self, product, line):
        """Add accepted product to linked list"""
        accepted_list = self.get_accepted_list(line)
        if accepted_list:
            accepted_list.append(product)
    
    def merge_sort(self, arr, field):
        """Merge sort implementation for sorting products by field"""
        if len(arr) <= 1:
            return arr
        
        # Divide
        mid = len(arr) // 2
        left = self.merge_sort(arr[:mid], field)
        right = self.merge_sort(arr[mid:], field)
        
        # Conquer and merge
        return self._merge(left, right, field)
    
    def _merge(self, left, right, field):
        """Merge two sorted arrays"""
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            left_val = self._get_field_value(left[i], field)
            right_val = self._get_field_value(right[j], field)
            
            # Compare based on data type
            if self._compare_values(left_val, right_val):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        # Add remaining elements
        result.extend(left[i:])
        result.extend(right[j:])
        
        return result
    
    def _get_field_value(self, product, field):
        """Extract field value from product"""
        value = product.get(field, '')
        
        # Handle datetime strings
        if field == 'production_timestamp' and isinstance(value, str):
            try:
                return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            except:
                try:
                    return datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f')
                except:
                    return value
        
        return value
    
    def _compare_values(self, left, right):
        """Compare two values (handles different types)"""
        # Handle None values
        if left is None:
            return False
        if right is None:
            return True
        
        # Handle datetime objects
        if isinstance(left, datetime) and isinstance(right, datetime):
            return left <= right
        
        # Handle numeric types
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left <= right
        
        # Handle strings
        if isinstance(left, str) and isinstance(right, str):
            return left <= right
        
        # Fallback to string comparison
        return str(left) <= str(right)
    
    def sort_products(self, products, field, algorithm='merge'):
        """Sort products by specified field using merge sort"""
        if algorithm == 'merge':
            return self.merge_sort(products.copy(), field)
        else:
            return products.copy()
    
    def get_statistics(self):
        """Get factory statistics"""
        total_in_queues = (
            self.line_a_queue.size() + 
            self.line_b_queue.size() + 
            self.line_c_queue.size()
        )
        total_rejected = self.rejection_stack.size()
        total_accepted = (
            self.line_a_accepted.size() + 
            self.line_b_accepted.size() + 
            self.line_c_accepted.size()
        )
        total_processed = total_rejected + total_accepted
        
        return {
            'total_products': len(self.all_products),
            'in_queues': total_in_queues,
            'processed': total_processed,
            'rejected': total_rejected,
            'accepted': total_accepted,
            'line_a_queue': self.line_a_queue.size(),
            'line_b_queue': self.line_b_queue.size(),
            'line_c_queue': self.line_c_queue.size(),
            'line_a_accepted': self.line_a_accepted.size(),
            'line_b_accepted': self.line_b_accepted.size(),
            'line_c_accepted': self.line_c_accepted.size()
        }

