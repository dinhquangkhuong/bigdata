import psycopg2
import os
from dotenv import load_dotenv

load_dotenv(".env")
database_url = os.getenv("DATABASE_URL")
conn = psycopg2.connect(database_url)
cur = conn.cursor()

cur.execute("""
  create table student_score(
    student_id int,
    year int,
    literature float,
    physics float,
    chemistry float,
    biology float,
    math float,
    foregn_language float,
    foreign_language_type varchar(8),
    english float,
    history float,
    geography float,
    civic_education float,
    primary key(student_id, year)
  )
""")

    # student_id
    # math 
    # year
    # literature
    # physics 
    # chemistry 
    # biology 
    # foriegn_language
    # foreign_language_type
    # english 
    # history 
    # geography
    # civic_education

cur.execute("""
  create table exam_subjects(
    code varchar(8) primary key,
    first varchar(32),
    second varchar(32),
    thrid varchar(32)
  )
""")

cur.execute("""
  create table entry_point_university(
    subject_uni_id uuid primary key,
    uni_id int not null,
    code varchar(32) not null,
    year int not null,
    name varchar(255),
    entry_point float,
    fee bigint,
    note text
  )
""")

cur.execute("""
  create table exam_subjects_uni(
    subject_uni_id uuid primary key,
    uni_id int,
    code varchar(32),
    year int,
    code_subjects varchar(8) references exam_subjects(code)
  )
""")


# chinese float,
# japanese float,
# french float,
# german float,
# russian float



# cur.execute("""
#   CREATE INDEX idx_thread_id ON thread(thread_id)
# """)
# cur.execute("""
#   CREATE INDEX idx_comment_id ON comment(comment_id)
# """)

conn.commit()
