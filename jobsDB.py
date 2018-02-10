# "Jobs Database"

import sqlite3

class SQLFuncs:
    def __init__(self, sqlite_file):
        """
        Establish connection, creator cursor object, and create main SQL table if it
        does not already exist.
        """
        print('Opening connection...')
        self.db = sqlite3.connect(sqlite_file)
        self.c = self.db.cursor()
        self.c.execute(
            """
            CREATE TABLE IF NOT EXISTS jobs(
            id                INTEGER PRIMARY KEY,
            company           TEXT,
            position          TEXT,
            apply_date        TEXT,
            CL_bool           INTEGER DEFAULT 0,     # Cover letter yes/no     (0==False)
            TY_bool           INTEGER DEFAULT 0,     # Thank you letter yes/no (0==False)
            interivew_bool    INTEGER DEFAULT 0,     # In-person yes/no        (0==False)
            phonescrn_bool    INTEGER DEFAULT 0,     # Phone screen yes/no     (0==False)
            contact           TEXT    DEFAULT NULL,
            notes_post_phone  TEXT    DEFAULT NULL,
            notes_post_person TEXT    DEFAULT NULL,
            URL               TEXT    DEFAULT NULL,
            offer             TEXT    DEFAULT 'OPEN')
            """)

    def close(self):
        """
        Commit changes and close connection to database.
        """
        print('Saving changes...\nDisconnecting from database...')
        self.db.commit()
        self.db.close()


def shell():
    # Try to establish connection
    try:
        Database = SQLFuncs("jobDB.sqlite")

    except Exception as e:
        Database.db.rollback()
        print('Oops, something went wrong.')
        print(e)

    else:
        print('Connection successful!')

        while True:
            command = input('> ')
            
            # Raw SQL query
            if command == "newJob()":
                company = input('Company: ')
                position = input('Position: ')
                contact = input('Contact: ')
                date_application = input('Date of application (YYYY-MM-DD)\n')

                try:
                    Database.c.execute("""
                       INSERT INTO jobs
                       (company, position, contact, apply_date)
                       VALUES (?, ?, ?, ?)
                       """, (company, position,
                             contact, date_application))
                    Database.db.commit()
                    print('Success!')

                except Exception as e:
                    Database.db.rollback()
                    print(e)

            elif command == 'raw()':
                query = input('Enter your full query:\n')

                try:
                    Database.c.execute(query)
                    results = Database.c.fetchall()
                    print()
                    for result in results:
                        print(result, '\n\n')

                except Exception as e:
                    Database.db.rollback()
                    print(e)

            # View structure of comments table
            elif command == '--struct':
                print('jobs'.center(30, '-'))
                print("id         INTEGER PRIMARY KEY",
                      "company    TEXT",
                      "position   TEXT",
                      "contact    TEXT DEFAULT NULL",
                      "apply_date TEXT",
                      "------------------------------", sep='\n')

            # Disconnect
            elif command == '--dc':
                Database.close()
                break


if __name__ == '__main__':
    shell()
# JobsDB
