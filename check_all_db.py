import sqlite3

def check_all_tables():
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    
    # Check reservations
    print("RESERVATIONS:")
    print("=" * 50)
    c.execute('SELECT * FROM reservations')
    reservations = c.fetchall()
    for reservation in reservations:
        print(f"ID: {reservation[0]}, Name: {reservation[1]}, Date: {reservation[5]}")
    print(f"Total reservations: {len(reservations)}")
    print()
    
    # Check contact messages
    print("CONTACT MESSAGES:")
    print("=" * 50)
    c.execute('SELECT * FROM contact_messages')
    messages = c.fetchall()
    for message in messages:
        print(f"ID: {message[0]}, Name: {message[1]}, Subject: {message[3]}")
    print(f"Total messages: {len(messages)}")
    print()
    
    # Check delivery orders
    print("DELIVERY ORDERS:")
    print("=" * 50)
    c.execute('SELECT * FROM delivery_orders')
    orders = c.fetchall()
    for order in orders:
        print(f"ID: {order[0]}, Name: {order[1]}, Total: ${order[9]}")
    print(f"Total orders: {len(orders)}")
    
    conn.close()

if __name__ == '__main__':
    check_all_tables()