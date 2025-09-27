from flask import Flask, render_template, request, jsonify
import sqlite3
import json
from datetime import datetime

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    
    # Create delivery_orders table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS delivery_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            customer_email TEXT NOT NULL,
            customer_phone TEXT NOT NULL,
            delivery_address TEXT NOT NULL,
            delivery_city TEXT NOT NULL,
            delivery_zip TEXT NOT NULL,
            delivery_instructions TEXT,
            order_items TEXT NOT NULL,
            total_amount REAL NOT NULL,
            order_date TEXT NOT NULL,
            status TEXT DEFAULT 'pending'
        )
    ''')
    
    # Create reservations table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            customer_email TEXT NOT NULL,
            customer_phone TEXT NOT NULL,
            number_of_guests INTEGER NOT NULL,
            reservation_date TEXT NOT NULL,
            reservation_time TEXT NOT NULL,
            special_requests TEXT,
            status TEXT DEFAULT 'pending',
            created_at TEXT NOT NULL
        )
    ''')
    
    # Create contact_messages table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            status TEXT DEFAULT 'new',
            created_at TEXT NOT NULL,
            responded_at TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database when app starts
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/delivery')
def delivery():
    return render_template('delivery.html')

@app.route('/booking')
def booking():
    return render_template('booking.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/reservations')
def reservations():
    return render_template('reservation.html')

@app.route('/submit_delivery_order', methods=['POST'])
def submit_delivery_order():
    try:
        data = request.get_json()
        
        # Extract customer information
        customer_info = data['customer_info']
        items = data['items']
        total = data['total']
        
        # Connect to database
        conn = sqlite3.connect('restaurant.db')
        c = conn.cursor()
        
        # Insert order into database
        c.execute('''
            INSERT INTO delivery_orders 
            (customer_name, customer_email, customer_phone, delivery_address, delivery_city, delivery_zip, delivery_instructions, order_items, total_amount, order_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            customer_info['name'],
            customer_info['email'],
            customer_info['phone'],
            customer_info['address'],
            customer_info['city'],
            customer_info['zip'],
            customer_info.get('instructions', ''),
            json.dumps(items),
            total,
            datetime.now().isoformat()
        ))
        
        conn.commit()
        order_id = c.lastrowid
        conn.close()
        
        return jsonify({'success': True, 'order_id': order_id})
    
    except Exception as e:
        print(f"Error processing order: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/submit_reservation', methods=['POST'])
def submit_reservation():
    try:
        # Get form data
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'phone', 'guests', 'date', 'time']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
        
        # Connect to database
        conn = sqlite3.connect('restaurant.db')
        c = conn.cursor()
        
        # Insert reservation into database
        c.execute('''
            INSERT INTO reservations 
            (customer_name, customer_email, customer_phone, number_of_guests, reservation_date, reservation_time, special_requests, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['name'],
            data['email'],
            data['phone'],
            int(data['guests']),
            data['date'],
            data['time'],
            data.get('special-requests', ''),
            datetime.now().isoformat()
        ))
        
        conn.commit()
        reservation_id = c.lastrowid
        conn.close()
        
        return jsonify({
            'success': True, 
            'reservation_id': reservation_id,
            'message': 'Reservation submitted successfully!'
        })
    
    except Exception as e:
        print(f"Error processing reservation: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    try:
        # Get form data
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'subject', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
        
        # Connect to database
        conn = sqlite3.connect('restaurant.db')
        c = conn.cursor()
        
        # Insert contact message into database
        c.execute('''
            INSERT INTO contact_messages 
            (name, email, subject, message, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            data['name'],
            data['email'],
            data['subject'],
            data['message'],
            datetime.now().isoformat()
        ))
        
        conn.commit()
        message_id = c.lastrowid
        conn.close()
        
        return jsonify({
            'success': True, 
            'message_id': message_id,
            'message': 'Your message has been sent successfully! We will get back to you soon.'
        })
    
    except Exception as e:
        print(f"Error processing contact message: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/reservations')
def get_reservations():
    try:
        conn = sqlite3.connect('restaurant.db')
        c = conn.cursor()
        
        c.execute('''
            SELECT * FROM reservations ORDER BY created_at DESC
        ''')
        
        reservations = []
        for row in c.fetchall():
            reservations.append({
                'id': row[0],
                'customer_name': row[1],
                'customer_email': row[2],
                'customer_phone': row[3],
                'number_of_guests': row[4],
                'reservation_date': row[5],
                'reservation_time': row[6],
                'special_requests': row[7],
                'status': row[8],
                'created_at': row[9]
            })
        
        conn.close()
        return jsonify({'success': True, 'reservations': reservations})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/contact_messages')
def get_contact_messages():
    try:
        conn = sqlite3.connect('restaurant.db')
        c = conn.cursor()
        
        c.execute('''
            SELECT * FROM contact_messages ORDER BY created_at DESC
        ''')
        
        messages = []
        for row in c.fetchall():
            messages.append({
                'id': row[0],
                'name': row[1],
                'email': row[2],
                'subject': row[3],
                'message': row[4],
                'status': row[5],
                'created_at': row[6],
                'responded_at': row[7]
            })
        
        conn.close()
        return jsonify({'success': True, 'messages': messages})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/admin/contact_messages')
def admin_contact_messages():
    return render_template('admin_contact.html')

if __name__ == '__main__':
    app.run(debug=True)