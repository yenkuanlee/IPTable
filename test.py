import psycopg2

conn = psycopg2.connect(database="postgres",user="postgres",host="127.0.0.1", port="5432")
cur = conn.cursor()
cur.execute("CREATE FOREIGN TABLE IF NOT EXISTS testt(tsid bigint, name text, score int) server ipserver options(table_name 'testt')")
conn.commit()

for i in range(100):
    cur.execute("INSERT INTO testt values(1,'Kevin',"+str(i)+")")
    conn.commit()
