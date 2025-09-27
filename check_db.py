import sqlite3

def check_reservations():
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    
    c.execute('SELECT * FROM reservations')
    reservations = c.fetchall()
    
    print("Reservations in database:")
    print("-" * 50)
    for reservation in reservations:
        print(f"ID: {reservation[0]}")
        print(f"Name: {reservation[1]}")
        print(f"Email: {reservation[2]}")
        print(f"Phone: {reservation[3]}")
        print(f"Guests: {reservation[4]}")
        print(f"Date: {reservation[5]}")
        print(f"Time: {reservation[6]}")
        print(f"Special Requests: {reservation[7]}")
        print(f"Status: {reservation[8]}")
        print(f"Created At: {reservation[9]}")
        print("-" * 50)
    
    conn.close()

if __name__ == '__main__':
    check_reservations()

    