import sqlite3

# Initialize DB connection and create table if it doesn't exist
conn = sqlite3.connect('stephen_king_adaptations.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table
             (movieID TEXT, movieName TEXT, movieYear INTEGER, imdbRating REAL)''')

# Load file content to DB
with open('stephen_king_adaptations.txt', 'r') as f:
    lines = [tuple(line.strip().split(',')) for line in f.readlines()]
    c.executemany("INSERT INTO stephen_king_adaptations_table VALUES (?, ?, ?, ?)", lines)
conn.commit()

def search_db(query, param):
    c.execute(query, param)
    rows = c.fetchall()
    return rows or ["No matching record found"]

# Search options
search_options = {
    '1': {
        'message': "Enter the movie name: ",
        'query': "SELECT * FROM stephen_king_adaptations_table WHERE movieName LIKE ?",
        'param': lambda x: ('%' + x + '%', )
    },
    '2': {
        'message': "Enter the movie year: ",
        'query': "SELECT * FROM stephen_king_adaptations_table WHERE movieYear=?",
        'param': lambda x: (x, )
    },
    '3': {
        'message': "Enter the movie rating: ",
        'query': "SELECT * FROM stephen_king_adaptations_table WHERE imdbRating >= ?",
        'param': lambda x: (x, )
    }
}

while True:
    choice = input("\nOptions:\n1. Search by movie name\n2. Search by movie year\n3. Search by movie rating\n4. STOP\nEnter your choice: ")
    if choice == '4':
        break
    elif choice in search_options:
        param = input(search_options[choice]['message'])
        results = search_db(search_options[choice]['query'], search_options[choice]['param'](param))
        for result in results:
            print(result)
    else:
        print("Invalid choice. Please enter again.")
