#!/usr/local/bin/python3

import psycopg2

connection = psycopg2.connect(database="distal",
                              user="distal_user",
                              password="...")
cursor = connection.cursor()

print('Content-Type: text/html; charset=UTF-8')
print()
print()
print('<html>')
print('<head><title>Select Country</title></head>')
print('<body>')
print('<form method="POST" action="selectArea.py">')
print('<select name="countryID" size="10">')

cursor.execute("SELECT id,name FROM countries " +
               "ORDER BY name")
for id,name in cursor:
    print('<option value="'+str(id)+'">'+name+'</option>')

print('</select>')
print('<p>')
print('<input type="submit" value="OK">')
print('</form>')
print('</body>')
print('</html>')

