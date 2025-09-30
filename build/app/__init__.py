#!/usr/bin/env python3

import os
import sqlite3
import hashlib

def init_database():
    """Initialize the SQLite database with tables and seed data"""
    
    db_path = '/app/data/inventory.db'
    
    # Create data directory if it doesn't exist
    import os
    os.makedirs('/app/data', exist_ok=True)
    
    # Remove existing database
    if os.path.exists(db_path):
        os.remove(db_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'employee',
            first_name TEXT,
            last_name TEXT,
            phone TEXT,
            address TEXT,
            city TEXT,
            postal_code TEXT,
            country TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create inventory items table
    cursor.execute('''
        CREATE TABLE inventory_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            supplier TEXT NOT NULL,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create password reset tokens table
    cursor.execute('''
        CREATE TABLE password_reset_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            token TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            used BOOLEAN DEFAULT FALSE
        )
    ''')
    
    # Insert users (avec des mots de passe très complexes - impossible à deviner)
    users_data = [
        ('admin', 'admin@techcorp.local', hashlib.sha256('K9$mX#vB2pQ7@nL4R!eH3zF8wC6uI5yT'.encode()).hexdigest(), 'admin', 'Robert', 'Anderson', '+33 6 85 42 91 73', '42 Avenue des Champs-Élysées', 'Paris', '75008', 'France'),
        ('jennifer.morgan', 'j.morgan@techcorp.local', hashlib.sha256('P3$kM9@nV5zL7!qR2hB4xF8tE1wQ6uY'.encode()).hexdigest(), 'manager', 'Jennifer', 'Morgan', '+33 6 74 58 32 19', '15 Rue de la République', 'Lyon', '69002', 'France'),
        ('david.chen', 'd.chen@techcorp.local', hashlib.sha256('Z8#lN4@vR9zP5!mK7qX2hB6tF3wL1uE'.encode()).hexdigest(), 'employee', 'David', 'Chen', '+33 6 92 67 15 84', '8 Boulevard Saint-Germain', 'Paris', '75005', 'France'),
        ('sarah.wilson', 's.wilson@techcorp.local', hashlib.sha256('Q5@mX8#pL3zN7!vR4hK9tB2wF6uE1qY'.encode()).hexdigest(), 'hr', 'Sarah', 'Wilson', '+33 6 31 78 45 92', '23 Rue Victor Hugo', 'Marseille', '13001', 'France'),
        ('michael.torres', 'm.torres@techcorp.local', hashlib.sha256('R7!pK4@nL9zX2#mV6hQ5tB8wF3uE1yL'.encode()).hexdigest(), 'employee', 'Michael', 'Torres', '+33 6 56 89 23 47', '67 Avenue de la Liberté', 'Toulouse', '31000', 'France'),
        ('lisa.parker', 'l.parker@techcorp.local', hashlib.sha256('L6#vB3@pK8zN4!mR7hX2tQ9wF5uE1yP'.encode()).hexdigest(), 'supervisor', 'Lisa', 'Parker', '+33 6 49 82 36 15', '11 Place de la Bastille', 'Paris', '75011', 'France')
    ]
    
    cursor.executemany(
        'INSERT INTO users (username, email, password, role, first_name, last_name, phone, address, city, postal_code, country) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        users_data
    )
    
    # Insert inventory items (enlever le flag)
    inventory_data = [
        ('Laptops HP EliteBook 840', 'Electronics', 25, 899.99, 'HP Enterprise'),
        ('Office Chairs Ergonomic', 'Furniture', 15, 299.99, 'Steelcase Inc'),
        ('Network Switches Cisco', 'Electronics', 8, 1299.99, 'Cisco Systems'),
        ('Wireless Mice Logitech', 'Electronics', 50, 29.99, 'Logitech Corp'),
        ('Conference Tables Oak', 'Furniture', 5, 799.99, 'Herman Miller'),
        ('Security Cameras 4K', 'Security', 12, 199.99, 'Hikvision'),
        ('Monitors Dell UltraSharp', 'Electronics', 30, 449.99, 'Dell Technologies'),
        ('Standing Desks Electric', 'Furniture', 10, 699.99, 'Flexispot'),
        ('Keyboards Mechanical', 'Electronics', 40, 129.99, 'Corsair Gaming'),
        ('Webcams Logitech 4K', 'Electronics', 20, 159.99, 'Logitech Corp')
    ]
    
    cursor.executemany(
        'INSERT INTO inventory_items (name, category, quantity, price, supplier) VALUES (?, ?, ?, ?, ?)',
        inventory_data
    )
    
    conn.commit()
    conn.close()
    
    print("✅ Database initialized successfully")
    print(f"📊 Created {len(users_data)} users")
    print(f"📦 Created {len(inventory_data)} inventory items")

if __name__ == "__main__":
    init_database()
