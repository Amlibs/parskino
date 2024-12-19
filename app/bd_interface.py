import sqlite3


def creareDB():
    with sqlite3.connect('films.db') as connection:
        cursor = connection.cursor()
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS Films(
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        allseats INTEGER NOT NULL,
                        notfreeseats INTEGER NOT NULL
                        )
                    '''
                )
        
        connection.commit()


def writeToDB(name, allSeats, notFreeSeats):
    with sqlite3.connect('films.db') as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Films where name = ?', (name,))
        res = cursor.fetchall()
        if len(res) == 0:
            cursor.execute('INSERT INTO Films (name, allseats, notfreeseats) VALUES (?, ?, ?)', (name, allSeats, notFreeSeats))
        else:
            cursor.execute('UPDATE Films SET allseats = ?, notfreeseats = ? WHERE name = ?', (allSeats, notFreeSeats, name))
        
        connection.commit()


def readFromDB():
    with sqlite3.connect('films.db') as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT name, allseats, notfreeseats FROM Films')
        res = cursor.fetchall()
        return res

def deleteDB():
    with sqlite3.connect('films.db') as connection:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM Films')
