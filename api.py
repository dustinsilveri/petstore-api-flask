import pymysql
import os
import datetime
import logging
from flask import Flask, jsonify, request, send_file
from flaskext.mysql import MySQL
from flask_jwt_extended import JWTManager, jwt_required, create_access_token


###############################################################
## Config
app = Flask(__name__)

# MySQL Stuff
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1' 

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'flask_api'
mysql.init_app(app)

# JWT Stuff
app.config['JWT_SECRET_KEY'] = 'veracode'
app.config['JWT_ACCESS_TOKEN_EXPIRES '] = datetime.timedelta(days=365) 
jwt = JWTManager(app)

# Logging
logging.basicConfig(filename='log_1.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
###############################################################

###############################################################
### User Endpoints
### CREATE A USER ###
@app.route('/user', methods=['POST'])
def addUser():
    try:
        _json = request.json
        _username = _json['username']
        _firstname = _json['firstname']
        _lastname = _json['lastname']
        _email = _json['email']
        _password = _json['password']
        _phone = _json['phone']
        conn = mysql.connect()
        cursor = conn.cursor()
        if _username and _firstname and _lastname and _email and _password and _phone and request.method == 'POST':
            cursor.execute("select username FROM users WHERE username='%s'" % (_username))
            testUser = cursor.fetchone()
            if testUser:
                return jsonify(message="User Already Exist"), 409
            else:
                insertQuery = f"INSERT INTO users (username, firstname, lastname, email, password, phone ) VALUES (%s, %s, %s, %s, %s, %s )"
                insertValues = ( _username, _firstname, _lastname, _email, _password, _phone )
                cursor.execute(insertQuery, insertValues)
                conn.commit()
                return jsonify({'message':'User added successfully!', 'id':cursor.lastrowid}), 201
        else:
            return jsonify(message="Server Error"), 500
    except Exception as e:
        print(e)

### Login Route ###
@app.route('/user/login', methods=['POST'])
def login():
    try:
        _username = request.json['username']
        _password = request.json['password']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select username, password FROM users WHERE username='%s' AND password='%s'" % (_username, _password))
        userRow = cursor.fetchone()
        if userRow:
            access_token = create_access_token(identity=_username, fresh=True, expires_delta=False )
            return jsonify(message="Login Succeeded!", access_token=access_token), 201
        else:
            return jsonify(message="Bad Username or Password"), 401
    except Exception as e:
        print(e)

### Logout Route ###
@app.route('/user/logout', methods=['POST'])
def logout():
    try:
        _username = request.json['username']
        #TODO
        return jsonify(message='Logout Succeeded!'), 200
        
    except Exception as e:
        print(e)

### UPDATE A USER ###
# SQL Injections
@app.route('/user/<username>', methods=['PUT'])
def updateUser(username):
    try:
        _json = request.json
        _firstname = _json['firstname']
        _lastname = _json['lastname']
        _email = _json['email']
        _password = _json['password']
        _phone = _json['phone']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select username FROM users WHERE username='%s'" % (username))
        testUpdate = cursor.fetchone()
        if testUpdate:
            cursor.execute("UPDATE users SET firstname='%s', lastname='%s', email='%s', password='%s', phone='%s' WHERE username='%s'" % (_firstname, _lastname, _email, _password, _phone, username))
            conn.commit()
            response = jsonify(message="User updated successfully!"), 200
            return response
        else:
            return jsonify(message="User does not exist"), 404
    except Exception as e:
        print(e)

### GET ALL USERS ###
@app.route('/user')
def allUsers():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM users")
        userRows = cursor.fetchall()
        return jsonify(userRows), 200
    except Exception as e:
        print(e)

### GET A USER BY USERNAME
@app.route('/user/<username>', methods=['GET', 'TRACE', 'OPTIONS'])
def oneUser(username):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        #cursor.execute("SELECT * FROM users WHERE username =%s", username)
        cursor.execute("SELECT * FROM users WHERE username='%s'" %  (username))

        userRow = cursor.fetchone()
        if userRow:
            return jsonify(userRow), 200
        else:
            return jsonify(message='User does not exist'), 404
    except Exception as e:
        print(e)

### DELETE A USER BY USERNAME
# PAYLOAD http://localhost:5000/user/weld_pond'=(select(0)from(select(sleep(15)))as0x41)='
@app.route('/user/<username>', methods=['DELETE'])
def deleteUser(username):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("select username FROM users WHERE username='%s'" % (username))
        testDelete = cursor.fetchone()
        if testDelete:
            cursor.execute("DELETE FROM users WHERE username =%s", (username))
            conn.commit()
            res = jsonify({'message':'User deleted successfully'})
            res.status_code = 200
            return res
        else:
            return jsonify(message="User does not exist"), 404
    except Exception as e:
        print(e)
###############################################################

###############################################################
# Pet Endpoints
### CREATE A PET ###
@app.route('/pet', methods=['POST'])
def addPet():
    try:
        _json = request.json
        _category = _json['category']
        _name = _json['name']
        _photoUrls = _json['photoUrls']
        _tags = _json['tags']
        _status = _json['status']
        conn = mysql.connect()
        cursor = conn.cursor()
        if _category and _name and _photoUrls and _tags and _status and request.method == 'POST':
            insertQuery = f"INSERT INTO pets (category, name, photoUrls, tags, status ) VALUES (%s, %s, %s, %s, %s )"
            insertValues = ( _category, _name, _photoUrls, _tags, _status )
            cursor.execute(insertQuery, insertValues)
            conn.commit()
            return jsonify({'message':'Pet added successfully!', 'id':cursor.lastrowid}), 201
        else:
            return jsonify("Server Error"), 500
    except Exception as e:
        print(e)

### GET A PET BY ID
@app.route('/pet/<id>', methods=['GET', 'TRACE', 'OPTIONS'])
def onePet(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM pets WHERE id='%s'" %  (id))

        petRow = cursor.fetchone()
        if petRow:
            return jsonify(petRow), 200
        else:
            return jsonify(message="Pet does not exist"), 404
    except Exception as e:
        print(e)

### DELETE A PET BY ID
@app.route('/pet/<id>', methods=['DELETE'])
def deletePet(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("select id FROM pets WHERE id='%s'" % (id))
        testDelete = cursor.fetchone()
        if testDelete:
            cursor.execute("DELETE FROM pets WHERE id =%s", (id))
            conn.commit()
            res = jsonify({'message':'Pet deleted successfully'})
            res.status_code = 200
            return res
        else:
            return jsonify(message="Pet does not exist"), 404
    except Exception as e:
        print(e)

### FIND PET BY STATUS
@app.route('/pet/findByStatus')
def findByStatus():
    status = request.args.get('status')
    if not status:
        return 404
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM pets WHERE status='%s'" %  (status))

        statusRow = cursor.fetchone()
        if statusRow:
            return jsonify(statusRow), 200
        else:
            return jsonify(message="Something went wrong, status isn't correct"), 404
    except Exception as e:
        print(e)

    return send_file(os.path.join(os.getcwd(), logFile))

### UPDATE A PET ###
@app.route('/pet/<id>', methods=['PUT'])
def updatePet(id):
    try:
        _json = request.json
        _category = _json['category']
        _name = _json['name']
        _photoUrls = _json['photoUrls']
        _tags = _json['tags']
        _status = _json['status']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select id FROM pets WHERE id='%s'" % (id))
        testUpdate = cursor.fetchone()
        if testUpdate:
            cursor.execute("UPDATE pets SET category='%s', name='%s', photoUrls='%s', tags='%s', status='%s' WHERE id='%s'" % (_category, _name, _photoUrls, _tags, _status, id))
            conn.commit()
            response = jsonify(message="Pet updated successfully!"), 200
            return response
        else:
            return jsonify(message="Pet does not exist"), 404
    except Exception as e:
        print(e)
###############################################################

###############################################################
# Store Endpoints
### CREATE AN ORDER ###
@app.route('/store/order', methods=['POST'])
def addOrder():
    try:
        _json = request.json
        _petId = _json['petId']
        _qty = _json['qty']
        _shipDate = _json['shipDate']
        _status = _json['status']
        _complete = _json['complete']
        conn = mysql.connect()
        cursor = conn.cursor()
        if _petId and _qty and _shipDate and _status and _complete and request.method == 'POST':
            insertQuery = f"INSERT INTO orders (petId, qty, shipDate, status, complete ) VALUES (%s, %s, %s, %s, %s )"
            insertValues = ( _petId, _qty, _shipDate, _status, _complete )
            cursor.execute(insertQuery, insertValues)
            conn.commit()
            return jsonify({'message':'Order added successfully!', 'id':cursor.lastrowid}), 201
        else:
            return jsonify("Server Error"), 500
    except Exception as e:
        print(e)

### GET AN ORDER BY ID
@app.route('/store/order/<id>', methods=['GET', 'TRACE', 'OPTIONS'])
def oneOrder(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        #cursor.execute("SELECT * FROM users WHERE username =%s", username)
        cursor.execute("SELECT * FROM orders WHERE id='%s'" %  (id))

        orderRow = cursor.fetchone()
        if orderRow:
            return jsonify(orderRow), 200
        else:
            return jsonify(message="Order does not exist"), 404
    except Exception as e:
        print(e)

### DELETE AN ORDER BY ID
@app.route('/store/order/<id>', methods=['DELETE'])
def deleteOrder(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("select id FROM orders WHERE id='%s'" % (id))
        testDelete = cursor.fetchone()
        if testDelete:
            cursor.execute("DELETE FROM orders WHERE id =%s", (id))
            conn.commit()
            res = jsonify({'message':'Order deleted successfully'})
            res.status_code = 200
            return res
        else:
            return jsonify(message="Order does not exist"), 404
    except Exception as e:
        print(e)

### DISPLAY ORDER INVENTORY
@app.route('/store/inventory')
def orderInventory():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        placedQuery = cursor.execute("SELECT * FROM orders WHERE status='%s'" %  ('placed'))
        invPlaced=cursor.rowcount
        approvedQuery = cursor.execute("SELECT * FROM orders WHERE status='%s'" %  ('approved'))
        invApproved=cursor.rowcount
        deliveredQuery = cursor.execute("SELECT * FROM orders WHERE status='%s'" %  ('delivered'))
        invDelivered=cursor.rowcount
        inventory = {"placed": invPlaced, "approved": invApproved, "delivered": invDelivered}
        return (inventory), 200
    except Exception as e:
        print(e)
###############################################################

###############################################################
# Command Injection
# example of request: curl 'http://127.0.0.1:5000/admin/sleep%2010'
@app.route('/admin/run/<command>')
@jwt_required()
def run(command):
    out = os.popen(command).read()
    return jsonify(out)

# Directory Traversal
# example of request: curl 'http://127.0.0.1:5000/admin/log/?logFile=../../../../../etc/passwd'
@app.route('/admin/log')
@jwt_required()
def readLog():
    logFile = request.args.get('logFile')
    if not logFile:
        return 404
    return send_file(os.path.join(os.getcwd(), logFile))
###############################################################

###############################################################
## Creation of dummy data
def createUserTable():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute( 
            """CREATE TABLE IF NOT EXISTS users (
            id INT NOT NULL AUTO_INCREMENT,
            username VARCHAR(45) NOT NULL,
            firstname VARCHAR(45) NULL,
            lastname VARCHAR(45) NULL,
            email VARCHAR(45) NULL,
            password VARCHAR(255) NULL,
            phone VARCHAR(45) NULL,
            userStatus INT(11) NULL,
            PRIMARY KEY ( id )
            ) ENGINE=INNODB;"""
        )
        conn.commit()
        cursor.execute("select id FROM users WHERE id=1")
        testWeld = cursor.fetchone()
        if testWeld:
                pass
        else:
            cursor.execute(
                """INSERT INTO users (
                id, username, firstname, lastname, email, password, phone, userStatus) 
                VALUES (
                1, "weld_pond", "Chris", "Wysopal", "weld_pond@veracode.com", "V3RAC0d3", "555.111.2222", 1 );"""
            )
            conn.commit()
    except Exception as e:
        print(e)

def createPetTable():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute( 
            """CREATE TABLE IF NOT EXISTS pets (
            id INT NOT NULL AUTO_INCREMENT,
            category VARCHAR(45) NOT NULL,
            name VARCHAR(45) NULL,
            photoUrls VARCHAR(45) NULL,
            tags VARCHAR(45) NULL,
            status ENUM('available', 'pending', 'sold') NULL,
            PRIMARY KEY ( id )
            ) ENGINE=INNODB;"""
        )
        conn.commit()
        cursor.execute("select id FROM pets WHERE id=1")
        testPet = cursor.fetchone()
        if testPet:
                pass
        else:
            cursor.execute(
                """INSERT INTO pets (
                id, category, name, photoUrls, tags, status) 
                VALUES (
                1, "dog", "Max", "http://example.com/111.jpg", "cute", "available" );"""
            )
            conn.commit()
    except Exception as e:
        print(e)

def createOrderTable():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute( 
            """CREATE TABLE IF NOT EXISTS orders (
            id INT NOT NULL AUTO_INCREMENT,
            petId INT NOT NULL,
            qty INT NULL,
            shipDate DATE NULL,
            status ENUM('placed','approved','delivered') NULL,
            complete BOOLEAN NULL default 0,
            PRIMARY KEY ( id ),
            FOREIGN KEY (petId) REFERENCES pets(id)
            ) ENGINE=INNODB;"""
        )
        conn.commit()
        cursor.execute("select id FROM orders WHERE id=1")
        testPet = cursor.fetchone()
        if testPet:
                pass
        else:
            cursor.execute(
                """INSERT INTO orders (
                id, petId, qty, shipDate, status, complete) 
                VALUES (
                1, 1, 1, "2021-12-01", "placed", 0 );"""
            )
            conn.commit()
    except Exception as e:
        print(e)
###############################################################

###############################################################
## Engergize!
if __name__ == "__main__":
    createUserTable()
    createPetTable()
    createOrderTable()
    app.run(host='0.0.0.0', port=5000, debug=True)
###############################################################