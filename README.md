# COMP-3005-A3

A Python application that connects to a PostgreSQL database and runs CRUD operations on a `students` table.

## Youtube Video Link

- https://www.youtube.com/watch?v=dVi02GWzjkc


## Project Structure

```
COMP-3005-A3/
├── app/
│   └── main.py            # Python application (CRUD functions + demo in main())
├── db/
│   ├── ddl.sql            # Creates the students table
│   └── a3_q1_insert.sql   # Inserts the initial sample data
└── README.md
```

## Prerequisites

- [Python 3](https://www.python.org/downloads/) (3.8 or newer)
- [PostgreSQL](https://www.postgresql.org/download/) (running locally on port `5432`)
- `pgadmin4` pgAdmin to run the SQL scripts

## Setup

### 1. Create the database

Create a database named `a3_db`:

- In pgAdmin: right-click **Databases** → **Create** → **Database...** and name it `a3_db`.

### 2. Create the table and insert the sample data

From the project root, use the two SQL scripts in order:

- In pgAdmin: open the Query Tool on `a3_db`, then copy the contents of `db/ddl.sql` into the query tool and click `F5` to run. Then copy the contents of `db/a3_q1_insert.sql` into the query tool and click `f5` to run.)

This creates the `students` table and inserts three students (IDs 1–3).

### 3. Install the Python dependency

The app uses `psycopg2` to talk to PostgreSQL:

```bash
pip install psycopg2-binary
```

### 4. Check the connection settings

The connection details are set in `sqlConnection()` in [app/main.py](app/main.py):

```python
host="localhost",
port=5432,
dbname="a3_db",
user="postgres",
password="comp3005!",
```

Change these to match your PostgreSQL install if needed (most likely the `password`).

## Running the Application

Python is interpreted, so there is no compile step. From the project root, run:

```bash
python app/main.py
```

(On macOS/Linux you may need `python3` instead of `python`.)

The program connects to the database and runs the example calls in `main()`, printing the result of each operation and the contents of the `students` table to the console. If the connection fails, it prints an error message and exits.

## Application Functions

| Function | Description |
| --- | --- |
| `getAllStudents(conn)` | Prints every row in the `students` table, ordered by `student_id`. |
| `addStudent(conn, first_name, last_name, email, enrollment_date)` | Inserts a new student. Prints an error if the email is already in use. |
| `updateStudentEmail(conn, student_id, new_email)` | Updates a student's email. Prints an error if the email is already in use or the student ID does not exist. |
| `deleteStudent(conn, student_id)` | Deletes a student by ID. Prints a message if the student ID does not exist. |

To try a different operation, comment or uncomment the example calls in `main()` in [app/main.py](app/main.py) and run the program again.

## Resetting the Database

The examples in `main()` expect a newly added student to get ID `4`. To start from a clean state, drop the table and re-run the SQL scripts.
