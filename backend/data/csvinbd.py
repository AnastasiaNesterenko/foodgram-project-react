# import csv
# import psycopg2
#
# connection = psycopg2.connect("host='db' port='5432' name='postgres' user='postgres' password='postgres'")
# cursor = connection.cursor()
#
# with open(
#         'ingredients.csv', 'r', newline='', encoding='utf-8'
# ) as csvfile:
#     reader_ingredients = csv.DictReader(csvfile, delimiter=',')
#     to_db_ingredients = [
#         (str(row), row['name'], row['measurement_unit'])
#         for row in reader_ingredients
#     ]
#
# cursor.executemany(
#     'INSERT INTO recipes_ingredient '
#     '(id, name, measurement_unit) VALUES (?, ?, ?)',
#     to_db_category
# )
# connection.commit()
# connection.close()
