import os
import sys
from flask import Flask
from flask import request, jsonify, render_template, json
import psycopg2
import json
from psycopg2.extras import RealDictCursor


# Create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)

# if test_config is None:
#     # Load the instance config, if it exists, when not testing
#     app.config.from_pyfile('config.py', silent=True)
# else:
#     # Load the test config if passed in
#     app.fonfig.from_mapping(test_config)


# Ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass


# this is the line where wer update our user data user = 
conn = psycopg2.connect("dbname=pet_hotel user='acefox' ")
conn.autocommit = True
cur = conn.cursor()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/pet', methods=['GET'])
def getpets():
    cur = conn.cursor(cursor_factory=RealDictCursor)
    print("in pet get")
    cur.execute("""
    SELECT 
    "pet"."ID" as "id",
    "pet"."name" as "pets_name" ,
    "owner"."name" as "owners_name",
    "breed",
    "color",
    "checked-in"
    FROM "pet"
    JOIN "owner" 
    on "owner"."ID" = "pet"."owner_id";""")
    result = cur.fetchall()
    cur.close()
    # indent just makes it look pretty
    return json.dumps(result, indent =2)
   


## OWNER
@app.route('/api/owner', methods = ['GET'])
def getUser():
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
     SELECT owner.name, owner."ID" as "id", COUNT(pet.name) as pet_count 
     FROM owner JOIN "pet"
     ON "owner"."ID" = "pet"."owner_id" 
     GROUP BY owner."ID";""")
    result = cur.fetchall()
    cur.close()
    return json.dumps(result, indent =2)
# SELECT COUNT(column_name)
# FROM table_name
# WHERE condition; 

@app.route('/api/pet/', methods=['POST'])
def addowner():
    petName = request.form.get('name')
    ownerId = request.form.get('owner_id')
    petBreed = request.form.get('breed')
    petColor = request.form.get('color')

    cur.execute("INSERT INTO pet (name, owner_id, breed, color) VALUES (%s, %s, %s, %s);",
                (str(petName),str(ownerId),str(petBreed),str(petColor)))
    print("in /pet POST, req.body is :", req.body)
    #beatles.append(beatle)

    def refreshdata():
        cur.execute("SELECT * FROM pet;")
        result = cur.fetchall()
        # (1, 100, "abc'def")
        return result
    currentdbstate = refreshdata()
    return "pet is now {}".format(currentdbstate)


@app.route('/api/pet/checkin/<id>', methods=['PUT'])
def checkIn(id):
    cur.execute('UPDATE pet SET "checked-in" = CURRENT_TIMESTAMP WHERE "ID" = %s;',
                (id,))
    print("in /pet POST, pet name is :", id)
    #beatles.append(beatle)

    def refreshdata():
        cur.execute("SELECT * FROM pet;")
        result = cur.fetchall()
        # (1, 100, "abc'def")
        return result
    currentdbstate = refreshdata()
    return "pet is now {}".format(currentdbstate)

# UPDATE table_name
# SET column1 = value1, column2 = value2, ...
# WHERE condition; 



# @app.route('/pet/<id>', methods=['DELETE'])
# def deletepet(id):
#     index = id
#     print("In /pet DELETE, index is", index)
#     cur.execute("DELETE FROM pet WHERE 'id' = (%s);", (index))
#     #beatles.pop(int(index))
#     return "Deleted {} from pets.".format(index)


@app.route('/api/pet/<id>', methods = ['DELETE'])
def deletePet( id ):
    query = 'DELETE FROM pet WHERE "ID" = (%s)'
    id = int(id)
    print (id)
    cur.execute(query, (id,))
    return 'ok'



# CREATE TABLE "pet" ("ID" SERIAL PRIMARY KEY, 
# "name" VARCHAR(100), 
# "owner_id" INT REFERENCES "owner",
# "breed" VARCHAR(100),
# "color" VARCHAR(100), 
# "checked-in" TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
# "checked-out" TIMESTAMP );

# cur.close()
# conn.close()

    # return "data from owner table is {}".format(result)

@app.route('/api/owner/<ownerName>', methods = ['POST'])
def addOwner( ownerName ):  
    query = 'INSERT INTO owner (name) VALUES (%s)'
    name = str(ownerName)
    print (name)
    cur.execute(query, (name,))
    return "ok"

@app.route('/api/owner/<id>', methods = ['DELETE'])
def deleteOwner( id ):
    query = 'DELETE FROM owner WHERE "ID" = (%s)'
    id = int(id)
    print (id)
    cur.execute(query, (id,))
    return 'ok'

@app.route('/api/pet/checkout/<id>', methods = ['PUT'])
def checkout ( id ):
    query = 'UPDATE pet SET "checked-in" = null WHERE "ID" = (%s)'
    id = int(id)
    print (id)
    cur.execute(query, (id,))
    return 'ok'

app.run()



