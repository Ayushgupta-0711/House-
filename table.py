import mysql.connector as mc

conn = mc.connect(user='root', password='ayush@#11', host='localhost', database='house_p')

if conn.is_connected():
    print("You are connected.")
else:
    print('Unable to connect.')

mycursor = conn.cursor()


query = """CREATE TABLE pdata(
    size VARCHAR(80),
    total_sqft VARCHAR(80),
    bath VARCHAR(80),
    balcony VARCHAR(80),
    predicted INT
)
"""

mycursor.execute(query)
print('Your table is created.')

mycursor.close()
conn.close()

