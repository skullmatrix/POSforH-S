from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Serve the main HTML file
@app.route('/')
def home():
    return render_template('index.html')

# Database setup - connects to SQLite
def get_db_connection():
    conn = sqlite3.connect('pos_database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/add_item', methods=['POST'])
def add_item():
    data = request.json
    name = data['name']
    price = data['price']
    conn = get_db_connection()
    conn.execute('INSERT INTO items (name, price) VALUES (?, ?)', (name, price))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/view_items', methods=['POST'])
def view_items():
    conn = get_db_connection()
    items = conn.execute('SELECT id, name, price FROM items').fetchall()
    conn.close()
    return jsonify([{'id': item['id'], 'name': item['name'], 'price': item['price']} for item in items])

@app.route('/add_inventory', methods=['POST'])
def add_inventory():
    data = request.json
    item_id = data['item_id']
    quantity = data['quantity']
    conn = get_db_connection()
    conn.execute('INSERT INTO inventory (item_id, quantity) VALUES (?, ?)', (item_id, quantity))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/create_transaction', methods=['POST'])
def create_transaction():
    data = request.json
    items = data['items']
    total = 0
    conn = get_db_connection()
    for item in items:
        item_id = item['item_id']
        quantity = item['quantity']
        price = conn.execute('SELECT price FROM items WHERE id = ?', (item_id,)).fetchone()['price']
        total += price * int(quantity)
    conn.execute('INSERT INTO transactions (total) VALUES (?)', (total,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success', 'total': total})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)