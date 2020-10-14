CREATE TABLE IF NOT EXISTS Department (
    department_id varchar(15) PRIMARY KEY,
    department_name varchar(50)
);

CREATE TABLE IF NOT EXISTS Student (
    student_usn varchar(10) CHECK (student_usn ~ '^[0-9][A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{3}') PRIMARY KEY,
    first_name varchar(20),
    middle_name varchar(20),
    last_name varchar(20),
    joining_year numeric(4),
    expected_graduation_year numeric(4),
    quota varchar(15) CHECK (quota IN ('CET', 'COMED-K', 'MANAGEMENT')),
    email_id varchar(320),
    phone numeric(10),
    department_id varchar(15) REFERENCES Department (department_id) ON DELETE CASCADE,
    dob date
);

CREATE TABLE IF NOT EXISTS Parent (
    student_usn varchar(15) REFERENCES Student (student_usn) ON DELETE CASCADE,
    name varchar(50),
    contact numeric(10),
    email_id varchar(320)
);

CREATE TABLE IF NOT EXISTS Faculty (
    faculty_id varchar(320) PRIMARY KEY,
    name varchar(50),
    department_id varchar(15) REFERENCES Department (department_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Proctor (
    proctor_id varchar(320),
    student_usn varchar(15) UNIQUE,
    PRIMARY KEY (proctor_id, student_usn),
    FOREIGN KEY (proctor_id) REFERENCES Faculty (faculty_id) ON DELETE CASCADE,
    FOREIGN KEY (student_usn) REFERENCES Student (student_usn) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Reports (
    meet_date varchar(10),
    proctor_id varchar(320) REFERENCES Faculty (faculty_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Remarks (
    meet_date varchar(10),
    proctor_id varchar(320) REFERENCES Faculty (faculty_id) ON DELETE CASCADE,
    student_usn varchar(10) REFERENCES Student (student_usn) ON DELETE CASCADE,
    remark varchar(250)
);

CREATE TABLE IF NOT EXISTS ProctorCredentials (
    proctor_id varchar(320) UNIQUE REFERENCES Faculty (faculty_id) ON DELETE CASCADE,
    password VARCHAR(512)
);

