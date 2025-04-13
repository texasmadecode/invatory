import sqlite3
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Database connection
def create_connection():
    conn = sqlite3.connect('inventory.db')
    return conn

# Create the database table
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

# CRUD operations
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

def get_item(id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM inventory WHERE id = ?', (id,))
    item = cursor.fetchone()
    conn.close()
    return item

# Routes
@app.get("/")
async def index(request: Request):
    items = view_items()
    return templates.TemplateResponse("index.html", {"request": request, "items": items})

@app.post("/add")
async def add(
    barcode: str = Form(...),
    device_type: str = Form(...),
    in_use: str = Form(...),
    working: str = Form(...),
    notes: str = Form(None)
):
    try:
        add_item(barcode, device_type, in_use, working, notes)
        return RedirectResponse("/", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding device: {e}")

@app.get("/edit/{id}")
async def edit_form(request: Request, id: int):
    item = get_item(id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return templates.TemplateResponse("edit.html", {"request": request, "item": item})

@app.post("/edit/{id}")
async def edit(
    id: int,
    barcode: str = Form(...),
    device_type: str = Form(...),
    in_use: str = Form(...),
    working: str = Form(...),
    notes: str = Form(None)
):
    try:
        update_item(id, barcode, device_type, in_use, working, notes)
        return RedirectResponse("/", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating device: {e}")

@app.post("/delete/{id}")
async def delete(id: int):
    try:
        delete_item(id)
        return RedirectResponse("/", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting device: {e}")

# Initialize the database
create_table()

# HTML template for index.html
index_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Inventory</title>
</head>
<body>
    <h1>Inventory</h1>
    <form action="/add" method="POST">
        <input type="text" name="barcode" placeholder="Barcode" required>
        <input type="text" name="deviceType" placeholder="Device Type" required>
        <input type="text" name="inUse" placeholder="In Use" required>
        <input type="text" name="working" placeholder="Working" required>
        <textarea name="notes" placeholder="Notes"></textarea>
        <button type="submit">Add Device</button>
    </form>
    <table>
        <tr>
            <th>ID</th>
            <th>Barcode</th>
            <th>Device Type</th>
            <th>In Use</th>
            <th>Working</th>
            <th>Notes</th>
            <th>Actions</th>
        </tr>
        {% for item in items %}
        <tr>
            <td>{{ item[0] }}</td>
            <td>{{ item[1] }}</td>
            <td>{{ item[2] }}</td>
            <td>{{ item[3] }}</td>
            <td>{{ item[4] }}</td>
            <td>{{ item[5] }}</td>
            <td>
                <form action="/delete/{{ item[0] }}" method="POST">
                    <button type="submit">Delete</button>
                </form>
                <a href="/edit/{{ item[0] }}">Edit</a>
            </td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

# Save the HTML template to the templates directory
with open("templates/index.html", "w") as f:
    f.write(index_html)