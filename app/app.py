import sqlite3
from flask import Flask, request, render_template, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

def create_connection():
    conn = sqlite3.connect('inventory.db')
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY,
            barcode TEXT NOT NULL,
            device_type TEXT NOT NULL,
            in_use TEXT NOT NULL,
            working TEXT NOT NULL,
            notes TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_item(barcode, device_type, in_use, working, notes):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO inventory (barcode, device_type, in_use, working, notes)
        VALUES (?, ?, ?, ?, ?)
    ''', (barcode, device_type, in_use, working, notes))
    conn.commit()
    conn.close()

def update_item(id, barcode, device_type, in_use, working, notes):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE inventory
        SET barcode = ?, device_type = ?, in_use = ?, working = ?, notes = ?
        WHERE id = ?
    ''', (barcode, device_type, in_use, working, notes, id))
    conn.commit()
    conn.close()

def delete_item(id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM inventory
        WHERE id = ?
    ''', (id,))
    conn.commit()
    conn.close()

def view_items():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM inventory')
    rows = cursor.fetchall()
    conn.close()
    return rows

@app.route('/')
def index():
    items = view_items()
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add():
    barcode = request.form['barcode']
    device_type = request.form['deviceType']
    in_use = request.form['inUse']
    working = request.form['working']
    notes = request.form['notes']
    add_item(barcode, device_type, in_use, working, notes)
    flash('Device added successfully!')
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        barcode = request.form['barcode']
        device_type = request.form['deviceType']
        in_use = request.form['inUse']
        working = request.form['working']
        notes = request.form['notes']
        update_item(id, barcode, device_type, in_use, working, notes)
        flash('Device updated successfully!')
        return redirect(url_for('index'))
    else:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM inventory WHERE id = ?', (id,))
        item = cursor.fetchone()
        conn.close()
        return render_template('edit.html', item=item)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    delete_item(id)
    flash('Device deleted successfully!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    create_table()
    app.run(host='0.0.0.0', port=5000, debug=True)