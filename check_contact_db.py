import sqlite3

def check_contact_messages():
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    
    c.execute('SELECT * FROM contact_messages')
    messages = c.fetchall()
    
    print("Contact Messages in database:")
    print("-" * 70)
    for message in messages:
        print(f"ID: {message[0]}")
        print(f"Name: {message[1]}")
        print(f"Email: {message[2]}")
        print(f"Subject: {message[3]}")
        print(f"Message: {message[4]}")
        print(f"Status: {message[5]}")
        print(f"Created At: {message[6]}")
        print(f"Responded At: {message[7]}")
        print("-" * 70)
    
    conn.close()

if __name__ == '__main__':
    check_contact_messages()