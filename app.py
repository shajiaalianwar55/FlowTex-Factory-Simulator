"""
FlowTex Factory Simulator - Flask Application
Main web application for factory simulation
"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from factory_simulator import FactorySimulator

app = Flask(__name__)
app.secret_key = 'flowtex_factory_simulator_secret_key_2024'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'csv'}

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Global factory simulator instance
factory = FactorySimulator()


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    """Dashboard - Main page"""
    stats = factory.get_statistics()
    return render_template('index.html', stats=stats)


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle CSV file upload"""
    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Load CSV into factory
        success, message = factory.load_from_csv(filepath)
        
        if success:
            flash(message, 'success')
        else:
            flash(message, 'error')
        
        # Clean up uploaded file
        try:
            os.remove(filepath)
        except:
            pass
        
        return redirect(url_for('index'))
    else:
        flash('Invalid file type. Please upload a CSV file.', 'error')
        return redirect(url_for('index'))


@app.route('/queues')
def queues():
    """View all product line queues"""
    line_a_items = factory.line_a_queue.display()
    line_b_items = factory.line_b_queue.display()
    line_c_items = factory.line_c_queue.display()
    
    return render_template('queues.html',
                         line_a=line_a_items,
                         line_b=line_b_items,
                         line_c=line_c_items,
                         line_a_size=factory.line_a_queue.size(),
                         line_b_size=factory.line_b_queue.size(),
                         line_c_size=factory.line_c_queue.size())


@app.route('/process')
def process():
    """Process one item from each queue"""
    processed = factory.process_queues()
    
    if processed:
        messages = []
        for line, product in processed:
            status = "rejected" if product.get('inspected') and not product.get('passed_inspection') else "accepted"
            messages.append(f"{line}: {product.get('product_id')} - {status}")
        flash(f"Processed {len(processed)} products: " + "; ".join(messages), 'success')
    else:
        flash('No products to process. Queues are empty.', 'info')
    
    return redirect(url_for('queues'))


@app.route('/rejected')
def rejected():
    """View rejected products stack"""
    rejected_items = factory.rejection_stack.display()  # Already reversed to show top first
    stack_size = factory.rejection_stack.size()
    
    return render_template('rejected.html',
                         rejected=rejected_items,
                         stack_size=stack_size)


@app.route('/accepted')
def accepted():
    """View accepted products (linked lists)"""
    line_a_accepted = factory.line_a_accepted.display()
    line_b_accepted = factory.line_b_accepted.display()
    line_c_accepted = factory.line_c_accepted.display()
    
    return render_template('accepted.html',
                         line_a=line_a_accepted,
                         line_b=line_b_accepted,
                         line_c=line_c_accepted,
                         line_a_size=factory.line_a_accepted.size(),
                         line_b_size=factory.line_b_accepted.size(),
                         line_c_size=factory.line_c_accepted.size())


@app.route('/sort', methods=['GET', 'POST'])
def sort():
    """Sort products page"""
    sortable_fields = [
        ('product_id', 'Product ID'),
        ('weight_g', 'Weight (grams)'),
        ('production_timestamp', 'Production Timestamp'),
        ('raw_defect_score', 'Raw Defect Score')
    ]
    
    sorted_products = None
    selected_field = None
    
    if request.method == 'POST':
        field = request.form.get('field')
        if field:
            selected_field = field
            # Get all products from queues, accepted lists, and rejected stack
            all_products = []
            
            # Add products from queues
            all_products.extend(factory.line_a_queue.display())
            all_products.extend(factory.line_b_queue.display())
            all_products.extend(factory.line_c_queue.display())
            
            # Add accepted products
            all_products.extend(factory.line_a_accepted.display())
            all_products.extend(factory.line_b_accepted.display())
            all_products.extend(factory.line_c_accepted.display())
            
            # Add rejected products
            all_products.extend(factory.rejection_stack.display())
            
            if all_products:
                sorted_products = factory.sort_products(all_products, field, algorithm='merge')
            else:
                flash('No products available to sort. Please upload a CSV file first.', 'info')
    
    return render_template('sorted.html',
                         sortable_fields=sortable_fields,
                         sorted_products=sorted_products,
                         selected_field=selected_field)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

