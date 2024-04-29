import psycopg2

conn = psycopg2.connect("postgres://khuong:12@127.0.0.1:5432/bigdata")

cur = conn.cursor()

cur.execute("""
  CREATE TABLE thread (
    thread_id UUID PRIMARY KEY,
    userName VARCHAR(255),
    subject VARCHAR(255),
    postDate DATE,
    postContent TEXT
  )
""")

cur.execute("""
  CREATE TABLE comment (
    comment_id UUID PRIMARY KEY,
    thread_id UUID REFERENCES thread(thread_id),
    userName VARCHAR(255),
    postDate DATE,
    postContent TEXT
  )
""");

cur.execute("""
  CREATE TABLE comment_reply (
    comment_id UUID REFERENCES comment(comment_id),
    comment_id_reply_to UUID REFERENCES comment(comment_id)
  )
""")

cur.execute("""
  CREATE INDEX idx_thread_id ON thread(thread_id)
""")

cur.execute("""
  CREATE INDEX idx_comment_id ON comment(comment_id)
""")

conn.commit()
