from database import *

create_table()

code = input("Промокод: ").strip().upper()

conn = get_connection()
cursor = conn.cursor()

cursor.execute(
    "DELETE FROM promo_codes WHERE code = ?",
    (code,)
)

conn.commit()
conn.close()

print("Промокод видалено.")