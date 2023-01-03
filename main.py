from flask import Flask, render_template, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Teoriadecuerdas16'
app.config['MYSQL_DB'] = 'api'
mysql = MySQL(app)


@app.route('/api/customers')
@cross_origin()
def getAllCustomers():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, nombre, apellido, email, telefono, adress  FROM customers')
    data = cur.fetchall()
    result = []
    for row in data:
        content = {
            'id': row[0],
            'nombre': row[1],
            'apellido': row[2],
            'email': row[3],
            'telefono': row[4],
            'adress': row[5]
        }
        result.append(content)
    return jsonify(result)  # Convierte el result en json


# Por defecto cuando llamamos una url se esta utilizando el tipo de dato GET
@app.route('/api/customers/<int:id>')
@cross_origin()
def getCustomer(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, nombre, apellido, email, telefono, adress  FROM customers WHERE id =' + str(id))
    if cur.rowcount == 0:
        return jsonify('No encontradó')
    row = cur.fetchone()
    return jsonify({
        'id': row[0],
        'nombre': row[1],
        'apellido': row[2],
        'email': row[3],
        'telefono': row[4],
        'adress': row[5]
    })


@app.route('/api/customers', methods=['POST'])
@cross_origin()
def createCustomer():
    if 'id' in request.json:
        UpdateCustomer()
    else:
        createCustomer()
    return "ok"


def createCustomer():
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO `customers` (`id`, `nombre`, `apellido`, `email`, `telefono`, `adress`) VALUES (NULL, %s, %s, %s, %s, %s);",
        (request.json['nombre'], request.json['apellido'], request.json['email'], request.json['telefono'],
         request.json['adress']))
    mysql.connection.commit()
    return "Cliente guardado"


def UpdateCustomer():
    cur = mysql.connection.cursor()
    cur.execute(
        "UPDATE `customers` SET `nombre` = %s, `apellido` = %s, `email` = %s, `telefono` = %s, `adress` = %s WHERE `customers`.`id` = %s;",
        (request.json['nombre'], request.json['apellido'], request.json['email'], request.json['telefono'],
         request.json['adress'],
         request.json['id']))
    mysql.connection.commit()
    return "Cliente actualizado"


@app.route('/api/customers/<int:id>', methods=['DELETE'])
@cross_origin()
def removeCustomer(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM `customers` WHERE `customers`.`id` = " + str(id) + ";")
    mysql.connection.commit()
    return "Cliente eliminado"


@app.route('/')
@cross_origin()
def index():
    return render_template('index.html')


@app.route('/<path:path>')
@cross_origin()
def publicFiles(path):
    return render_template(path)

if __name__ == '__main__':
    app.run(None, 3000, True)
