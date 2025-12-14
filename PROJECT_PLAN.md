---
name: FlowTex Factory Simulator
overview: Create a Flask web application that simulates a T-shirt factory production line using data structures (Queues, Stacks, Linked Lists) and algorithms (merge sort) to process CSV production data.
todos: []
---

# FlowTex Factory Simulator - Implementation Plan

## Project Structure

```
dsa_project/
├── app.py                 # Main Flask application
├── data_structures.py     # Custom DSA implementations (Queue, Stack, Linked List)
├── factory_simulator.py  # Factory simulation logic
├── requirements.txt       # Python dependencies
├── templates/
│   ├── base.html         # Base template
│   ├── index.html        # Main dashboard
│   ├── queues.html       # Product line queues view
│   ├── rejected.html     # Rejected products stack view
│   └── sorted.html       # Sorted products view
└── static/
    └── style.css         # Basic styling
```

## Core Components

### 1. Data Structures (`data_structures.py`)

**Queue Class** (FIFO):

- `enqueue(item)` - Add product to end
- `dequeue()` - Remove product from front
- `is_empty()` - Check if empty
- `size()` - Get queue length
- `display()` - Get all items

**Stack Class** (LIFO):

- `push(item)` - Add rejected product
- `pop()` - Remove top product
- `is_empty()` - Check if empty
- `peek()` - View top without removing
- `size()` - Get stack length

**Linked List Class**:

- `append(item)` - Add accepted product to end
- `display()` - Get all items
- `size()` - Get list length
- Node structure: `data` and `next` pointer

### 2. Factory Simulator (`factory_simulator.py`)

**FactorySimulator Class**:

- `load_from_csv(filepath)` - Parse CSV and populate queues
- `process_queues()` - Process products from queues
- `handle_rejection(product)` - Push to rejection stack
- `handle_acceptance(product, line)` - Add to linked list
- `sort_products(products, field, algorithm='merge')` - Sort by field
- Three Queue instances (Line A, B, C)
- One Stack instance (rejected products)
- Three Linked List instances (accepted per line)

**Sorting Algorithm**:

- Merge sort implementation
- Sortable fields: `product_id`, `weight_g`, `production_timestamp`, `raw_defect_score`

### 3. Flask Application (`app.py`)

**Routes**:

- `GET /` - Dashboard showing factory status
- `GET /queues` - View all product line queues
- `GET /process` - Process one item from each queue
- `GET /rejected` - View rejected products stack
- `GET /accepted` - View accepted products (linked lists)
- `GET /sort` - Sort products page
- `POST /sort` - Apply sorting with selected field
- `POST /upload` - Upload CSV file

**Features**:

- CSV file upload and parsing
- Real-time queue processing
- Visual representation of data structures
- Sorting with field selection

### 4. Web Interface (`templates/`)

**Base Template** (`base.html`):

- Navigation bar
- Bootstrap or simple CSS styling
- Flash message display

**Dashboard** (`index.html`):

- Factory statistics (total products, processed, rejected, accepted)
- Quick actions (process queues, view structures)
- CSV upload form

**Queues View** (`queues.html`):

- Display all three product line queues
- Show queue size and items
- Process button

**Rejected View** (`rejected.html`):

- Display rejection stack (LIFO order)
- Show rejection reasons
- Stack size indicator

**Sorted View** (`sorted.html`):

- Field selection dropdown
- Display sorted results table
- Sort algorithm info

## Implementation Details

### CSV Parsing

- Use `csv` module to read uploaded file
- Validate schema matches expected fields
- Handle missing/invalid data gracefully

### Data Flow

1. Upload CSV → Parse → Enqueue products to respective line queues
2. Process queues → Check inspection status
3. Rejected products → Push to stack
4. Accepted products → Append to linked list
5. Sorting → Apply merge sort on selected field

### Merge Sort Implementation

- Recursive divide-and-conquer
- Handle different data types (string, numeric, datetime)
- Return sorted list without modifying original

## Dependencies

- Flask 2.3+
- Python 3.8+

## Testing Considerations

- Test with sample CSV matching the schema
- Verify queue FIFO behavior
- Verify stack LIFO behavior
- Verify linked