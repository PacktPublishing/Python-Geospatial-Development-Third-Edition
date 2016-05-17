# create_db.py

import psycopg2

connection = psycopg2.connect(database="distal",
                              user="distal_user",
                              password="...")
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS countries")
cursor.execute("""
    CREATE TABLE countries (
        id      SERIAL,
        name    VARCHAR(255),
        outline GEOMETRY(GEOMETRY, 4326),

        PRIMARY KEY (id))
""")
cursor.execute("""
    CREATE INDEX countryIndex ON countries
        USING GIST(outline)
""")

cursor.execute("DROP TABLE IF EXISTS shorelines")
cursor.execute("""
    CREATE TABLE shorelines (
        id   SERIAL,
        level INTEGER,
        outline GEOMETRY(GEOMETRY, 4326),

        PRIMARY KEY (id))
""")
cursor.execute("""
    CREATE INDEX shorelineIndex ON shorelines
        USING GIST(outline)
""")

cursor.execute("DROP TABLE IF EXISTS places")
cursor.execute("""
    CREATE TABLE places (
        id       SERIAL,
        name     VARCHAR(255),
        position GEOGRAPHY(POINT, 4326),

        PRIMARY KEY (id))
""")
cursor.execute("""
    CREATE INDEX placeIndex ON places
        USING GIST(position)
""")

connection.commit()

