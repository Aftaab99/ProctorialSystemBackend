CREATE TABLE IF NOT EXISTS Department(department_id VARCHAR(15) PRIMARY KEY, department_name VARCHAR(50));

CREATE TABLE IF NOT EXISTS Student(student_usn VARCHAR(10) CHECK (student_usn ~ '^[0-9][A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{3}') PRIMARY KEY,first_name VARCHAR(20), middle_name VARCHAR(20), last_name VARCHAR(20), joining_year NUMERIC(4), expected_graduation_year NUMERIC(4), quota VARCHAR(15) CHECK(quota in ('CET', 'COMED-K', 'MANAGEMENT')), email_id VARCHAR(320), phone NUMERIC(10), department_id VARCHAR(15) REFERENCES Department(department_id) ON DELETE CASCADE, dob DATE);

CREATE TABLE IF NOT EXISTS Parent(student_usn VARCHAR(15) REFERENCES Student(student_usn) ON DELETE CASCADE, name VARCHAR(50), contact NUMERIC(10), email_id VARCHAR(320));

CREATE TABLE IF NOT EXISTS Faculty(faculty_id VARCHAR(320) PRIMARY KEY, name VARCHAR(50), department_id VARCHAR(15) REFERENCES Department(department_id) ON DELETE CASCADE);

CREATE TABLE IF NOT EXISTS Proctor(proctor_id VARCHAR(320), student_usn VARCHAR(15), PRIMARY KEY(proctor_id,student_usn), FOREIGN KEY(proctor_id) REFERENCES Faculty(faculty_id) ON DELETE CASCADE, FOREIGN KEY(student_usn) REFERENCES Student(student_usn) ON DELETE CASCADE);

CREATE TABLE IF NOT EXISTS Reports(meet_date VARCHAR(10),proctor_id VARCHAR(320) REFERENCES Proctor(proctor_id) ON DELETE CASCADE, PRIMARY KEY(meet_date,proctor_id));
CREATE TABLE IF NOT EXISTS Remarks(meet_date VARCHAR(10) REFERENCES Reports(meet_date) ON DELETE CASCADE,proctor_id VARCHAR(320) REFERENCES Proctor(proctor_id) ON DELETE CASCADE, student_usn VARCHAR(10) REFERENCES Student(student_usn) ON DELETE CASCADE, remark VARCHAR(250), PRIMARY KEY(meet_date,proctor_id,student_usn));

CREATE TABLE IF NOT EXISTS Admin(admin_password varchar(50));
INSERT INTO Admin VALUES('ef5c965c33d32e9939d9f31670d3aa82') ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS ProctorCredentials(proctor_id VARCHAR(320) UNIQUE REFERENCES Faculty(faculty_id) ON DELETE CASCADE, password VARCHAR(512));
