from database import *

create_table()

conn = get_connection()
cursor = conn.cursor()

cursor.execute("SELECT * FROM promo_codes")

for promo in cursor.fetchall():
    print(promo["code"], "-", promo["type"])

conn.close()