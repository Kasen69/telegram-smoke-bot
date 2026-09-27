import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database import create_table, add_promo


create_table()

code = input("Промокод: ").strip().upper()
promo_type = input("Тип (reset_cd): ").strip()

add_promo(code, promo_type)

print(f"Промокод {code} успішно створено!")