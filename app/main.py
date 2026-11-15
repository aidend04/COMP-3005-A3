import psycopg2
from psycopg2 import errors


def main():
    # open a connection to the database, stop if it fails
    conn = sqlConnection()
    if conn is None:
        print(
            "db connection failed please check the connection parameters and try again"
        )
        return

    # get all students example
    getAllStudents(conn)
    print()

    # add student example
    addStudent(conn, "Aiden", "Dsouza", "aidendsouza@cmail.carleton.ca", "2026-11-14")
    print()
    getAllStudents(conn)
    print()

    # attempt to add student with same email as before to show unique error holds
    addStudent(conn, "Bob", "Duncan", "aidendsouza@cmail.carleton.ca", "2026-11-14")
    print()
    getAllStudents(conn)
    print()

    # update student email example
    updateStudentEmail(conn, 4, "aiden@example.com")
    print()
    getAllStudents(conn)
    print()

    # update student email of student 3 with the example email from above to show error for unique email
    updateStudentEmail(conn, 3, "aiden@example.com")
    print()
    getAllStudents(conn)
    print()

    # delete student example
    deleteStudent(conn, 4)
    print()
    getAllStudents(conn)
    print()

    # delete a student who doesnt exist to show error for wrong student id
    deleteStudent(conn, 400)
    print()
    getAllStudents(conn)
    print()


# connects to the postgres db and returns the connection, or None if it fails
def sqlConnection():
    try:
        # Connect to postgres DB
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            dbname="a3_db",
            user="postgres",
            password="comp3005!",
        )
        return conn
    except psycopg2.OperationalError as e:
        # db is not running or connection details are wrong
        print(f"Failed to connect to the database: {e}")
        return


# prints every student in the table ordered by id
def getAllStudents(conn):
    try:
        with conn.cursor() as cur:
            sql = "SELECT * FROM students ORDER BY student_id;"
            cur.execute(sql)
            # get all result rows and print them one per line
            rows = cur.fetchall()
            for row in rows:
                print(row)
    except psycopg2.Error as e:
        # undo the failed transaction so the connection can still be used
        conn.rollback()
        print(f"get students failed with error: {e}")


# inserts a new student into the table
def addStudent(conn, first_name, last_name, email, enrollment_date):
    try:
        with conn.cursor() as cur:
            # %s placeholders let psycopg2 safely fill in the values
            sql = "INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s, %s, %s, %s);"
            cur.execute(sql, (first_name, last_name, email, enrollment_date))
            # save the change to the db
            conn.commit()
            print(f"successfully added student {first_name} {last_name}")
    except errors.UniqueViolation:
        # email column is UNIQUE so a duplicate email fails here
        conn.rollback()
        print(f"{email} is already in database, all emails must be unique")
        return
    except psycopg2.Error as e:
        # any other db error
        conn.rollback()
        print(f"add student failed with error: {e}")
        return


# changes the email of the student with the given id
def updateStudentEmail(conn, student_id, new_email):
    try:
        with conn.cursor() as cur:
            sql = "UPDATE students SET email = %s WHERE student_id = %s"
            cur.execute(sql, (new_email, student_id))
            conn.commit()
            # rowcount is 0 when no student has that id
            if cur.rowcount == 0:
                print(f"no student with student id {student_id} update did not occur")
            else:
                print(f"successfully updated student: {student_id} to use {new_email}")
    except errors.UniqueViolation:
        # new email is already used by another student
        conn.rollback()
        print(f"{new_email} is already in database, all emails must be unique")
        return
    except psycopg2.Error as e:
        # any other db error
        conn.rollback()
        print(f"update student failed with error: {e}")
        return


# removes the student with the given id
def deleteStudent(conn, student_id):
    try:
        with conn.cursor() as cur:
            # trailing comma makes (student_id,) a tuple, which execute expects
            sql = "DELETE FROM students WHERE student_id = %s"
            cur.execute(sql, (student_id,))
            conn.commit()
            # rowcount is 0 when no student has that id
            if cur.rowcount == 0:
                print(f"no student with student id {student_id} delete did not occur")
            else:
                print(f"successfully deleted student: {student_id}")
    except psycopg2.Error as e:
        # any other db error
        conn.rollback()
        print(f"update student failed with error: {e}")
        return


if __name__ == "__main__":
    main()
