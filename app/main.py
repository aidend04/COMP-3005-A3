import psycopg2
from psycopg2 import errors


def main():
    conn = sqlConnection()
    if conn is None:
        print(
            "db connection failed please check the connection parameters and try again"
        )
        return

    # get all students example
    getAllStudents(conn)

    # add student example
    addStudent(conn, "Aiden", "Dsouza", "aidendsouza@cmail.carleton.ca", "2026-11-14")
    getAllStudents(conn)

    # attempt to add student with same email as before to show unique error holds
    addStudent(conn, "Bob", "Duncan", "aidendsouza@cmail.carleton.ca", "2026-11-14")
    getAllStudents(conn)

    # # update student email example
    updateStudentEmail(conn, 4, "aiden@example.com")
    getAllStudents(conn)

    # update student email of student 3 with the example email from above to show error for unique email
    updateStudentEmail(conn, 3, "aiden@example.com")
    getAllStudents(conn)

    # delete student example
    deleteStudent(conn, 4)
    getAllStudents(conn)

    # delete a student who doesnt exist to show error for wrong student id
    deleteStudent(conn, 400)
    getAllStudents(conn)


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
        print(f"Failed to connect to the database: {e}")
        return


def getAllStudents(conn):
    try:
        with conn.cursor() as cur:
            sql = "SELECT * FROM students ORDER BY student_id;"
            cur.execute(sql)
            rows = cur.fetchall()
            for row in rows:
                print(row)
    except psycopg2.Error as e:
        conn.rollback()
        print(f"get students failed with error: {e}")


def addStudent(conn, first_name, last_name, email, enrollment_date):
    try:
        with conn.cursor() as cur:
            sql = "INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s, %s, %s, %s);"
            cur.execute(sql, (first_name, last_name, email, enrollment_date))
            conn.commit()
            print(f"successfully added student {first_name} {last_name}")
    except errors.UniqueViolation:
        conn.rollback()
        print(f"{email} is already in database, all emails must be unique")
        return
    except psycopg2.Error as e:
        conn.rollback()
        print(f"add student failed with error: {e}")
        return


def updateStudentEmail(conn, student_id, new_email):
    try:
        with conn.cursor() as cur:
            sql = "UPDATE students SET email = %s WHERE student_id = %s"
            cur.execute(sql, (new_email, student_id))
            conn.commit()
            if cur.rowcount == 0:
                print(f"no student with student id {student_id} update did not occur")
            else:
                print(f"successfully updated student: {student_id} to use {new_email}")
    except errors.UniqueViolation:
        conn.rollback()
        print(f"{new_email} is already in database, all emails must be unique")
        return
    except psycopg2.Error as e:
        conn.rollback()
        print(f"update student failed with error: {e}")
        return


def deleteStudent(conn, student_id):
    try:
        with conn.cursor() as cur:
            sql = "DELETE FROM students WHERE student_id = %s"
            cur.execute(sql, (student_id,))
            conn.commit()
            if cur.rowcount == 0:
                print(f"no student with student id {student_id} delete did not occur")
            else:
                print(f"successfully deleted student: {student_id}")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"update student failed with error: {e}")
        return


if __name__ == "__main__":
    main()
