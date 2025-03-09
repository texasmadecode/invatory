import unittest
import sqlite3
from app import app, create_table, add_item, view_items

class InventoryTestCase(unittest.TestCase):

    def setUp(self):
        # Set up a temporary database for testing
        self.app = app.test_client()
        self.app.testing = True
        self.db = 'test_inventory.db'
        app.config['DATABASE'] = self.db

        # Create the table in the temporary database
        self.conn = sqlite3.connect(self.db)
        create_table()

    def tearDown(self):
        # Close the database connection and remove the temporary database
        self.conn.close()
        import os
        os.remove(self.db)

    def test_add_item(self):
        # Test adding an item to the inventory
        response = self.app.post('/add', data=dict(
            barcode='123456789012',
            deviceType='student',
            inUse='yes',
            working='yes',
            notes='Test device'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Device added successfully!', response.data)

        # Verify the item was added to the database
        items = view_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0][1], '123456789012')
        self.assertEqual(items[0][2], 'student')
        self.assertEqual(items[0][3], 'yes')
        self.assertEqual(items[0][4], 'yes')
        self.assertEqual(items[0][5], 'Test device')

    def test_index(self):
        # Test the index page
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Device Inventory', response.data)

if __name__ == '__main__':
    unittest.main()