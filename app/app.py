import sqlite3

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
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            location TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_item(barcode, name, quantity, location):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO inventory (barcode, name, quantity, location)
        VALUES (?, ?, ?, ?)
    ''', (barcode, name, quantity, location))
    conn.commit()
    conn.close()

def update_item(id, barcode, name, quantity, location):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE inventory
        SET barcode = ?, name = ?, quantity = ?, location = ?
        WHERE id = ?
    ''', (barcode, name, quantity, location, id))
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

if __name__ == '__main__':
    create_table()
    # Example usage
    add_item('123456789012', 'Example Item', 10, 'Aisle 1')
    items = view_items()
    for item in items:
        print(item)