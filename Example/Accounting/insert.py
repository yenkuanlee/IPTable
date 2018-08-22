import psycopg2

conn = psycopg2.connect(database="postgres",user="postgres",host="127.0.0.1", port="5432")
cur = conn.cursor()

f = open('accounting.csv','r')
while True:
    line = f.readline()
    if not line:
        break
    line = line.replace("\n","")
    tmp = line.split(",")
    tmp[0] = tmp[0].replace("/","")
    cmd = "INSERT INTO accounting values(0,'"+tmp[0]+"','"+tmp[2]+"','"+tmp[3]+"',"+tmp[4]+");"
    cur.execute(cmd)
    conn.commit()
