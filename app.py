from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_mysqldb import MySQL, MySQLdb

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'prodw3'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

app.secret_key = 'mysecretkey'




@app.route('/')
def home():
    return render_template("home.html")


@app.route('/Login', methods=["GET", "POST"])
def Login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('select * from usuario where email=%s', (email,))
        usuario = cur.fetchone()
        cur.close()
        if len(usuario) > 0:
            if password == usuario['password']:
                session['nickname'] = usuario['nickname']
                session['email'] = usuario['email']
                session_active = True
                return redirect(url_for('master'))


@app.route('/Logout')
def Logout():
    session.clear()
    return render_template('home.html')


@app.route('/Register')
def Register():
    return render_template("Register.html")


@app.route('/Agregar_usuario', methods=['POST'])
def Agregar_usuario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        nickname = request.form['nickname']
        password = request.form['password']
        conf_password = request.form['conf-password']
        cellphone = request.form['cellphone']
        email = request.form['email']

        cur = mysql.connection.cursor()

        if password == conf_password:

            cur.execute("insert into usuario(nombre, nickname, password, cellphone, email) values(%s,%s,%s,%s,%s)",
                        (nombre, nickname, password, cellphone, email))
            mysql.connection.commit()
            flash('usuario agregado')
            session['nickname'] = nickname
            session['email'] = email
            return redirect(url_for('home'))


@app.route('/gestorProductos')
def gestorProductos():
    cur = mysql.connection.cursor()
    cur.execute('select * from producto')
    data = cur.fetchall()
    return render_template('gestorProductos.html', productos=data)


@app.route('/agregarProducto', methods=['POST'])
def agregar_producto():
    if request.method == 'POST':
        url_img = request.form['url_img']
        nombre = request.form['nombre']
        precio_unitario = request.form['precio_unitario']
        cantidad = request.form['cantidad']
        descripcion = request.form['descripcion']

        cur = mysql.connection.cursor()
        cur.execute('insert into producto(url_img, nombre, precio_unitario, cantidad, descripcion) values(%s ,%s ,%s ,%s ,%s)',
                    (url_img, nombre, precio_unitario, cantidad, descripcion))
        mysql.connection.commit()
        return redirect(url_for('gestorProductos'))


@app.route('/eliminar_producto/<string:id>')
def eliminar_producto(id):
    cur = mysql.connection.cursor()
    cur.execute('delete from producto where id = {0}'.format(id))
    mysql.connection.commit()
    flash('eliminado correctamente')
    return redirect(url_for('gestorProductos'))


@app.route('/actualizar_producto', methods=['POST'])
def actualizar_producto():
    if request.method == 'POST':

        id = request.form['id']
        url_img = request.form['url_img']
        nombre = request.form['nombre']
        precio_unitario = request.form['precio_unitario']
        cantidad = request.form['cantidad']
        descripcion = request.form['descripcion']

        cur = mysql.connection.cursor()

        cur.execute('update producto set url_img=%s ,nombre=%s ,precio_unitario=%s ,cantidad=%s ,descripcion=%s where id = %s',
                    (url_img, nombre, precio_unitario, cantidad, descripcion, id))

        print(descripcion)

        mysql.connection.commit()
        return redirect(url_for('gestorProductos'))
    else:
        return 'no entro ni mierda'


@app.route('/shoppingList')
def shoppingList():

    cur = mysql.connection.cursor()

    cur.execute('select id, nro_pedido, nombre, precio_unitario, cantidad_requerida, precio_unitario*cantidad_requerida "sub_total" from shoppinglist')
    data = cur.fetchall()
    return render_template('shoppingList.html', lista=data)


@app.route('/shopListAct', methods=['POST'])
def shopListAct():
    if request.method == 'POST':
        id = request.form['id']
        nro_pedido = request.form['nro_pedido']
        nombre = request.form['nombre']
        precio_unitario = request.form['precio_unitario']
        cantidad_requerida = request.form['cantidad_requerida']

        cur = mysql.connection.cursor()
        cur.execute('update shoppinglist set nro_pedido=%s, nombre=%s, precio_unitario=%s, cantidad_requerida=%s where id = %s',
                    (nro_pedido, nombre, precio_unitario, cantidad_requerida, id))
        mysql.connection.commit()
        return redirect(url_for('shoppingList'))


@app.route('/editar', methods = ['POST'])
def editar():
    if request.method == 'POST':
        id = request.form['id']
        cur = mysql.connection.cursor()
        cur.execute('select * from shoppinglist where id = %s', (id))
        data = cur.fetchone()
        return render_template('cantidadProducto.html', lista=data)


@app.route('/eliminar/<string:id>')
def eliminar_pedido(id):
    cur = mysql.connection.cursor()
    cur.execute('delete from shoppinglist where id = {0}'.format(id))
    mysql.connection.commit()
    flash('eliminado correctamente')
    return redirect(url_for('shoppingList'))


@app.route('/master')
def master():
    cur = mysql.connection.cursor()
    cur.execute('select * from producto')
    data = cur.fetchall()
    return render_template('master.html', productos=data)


@app.route('/pushProducto', methods=['POST'])
def pushProducto():
    if request.method == 'POST':
        id = request.form['id']

        miLista = list(range(999, 9999))

        random.shuffle(miLista)
       
        nro_pedido = miLista[:1]

        nombre = request.form['nombre']
        precio_unitario = request.form['precio_unitario']
        cantidad_requerida = request.form['cantidad_requerida']

        print(id, nombre, nro_pedido)
        cur = mysql.connection.cursor()
        cur.execute('insert into shoppinglist( id, nro_pedido, nombre, precio_unitario, cantidad_requerida) values(%s, %s, %s, %s, %s)',
                    (id, nro_pedido, nombre, precio_unitario, cantidad_requerida))

        mysql.connection.commit()
        return redirect(url_for('master'))
    
@app.route('/apiProductos')
def get():   
        cur = mysql.connection.cursor()
        cur.execute('select * from producto')
        data = cur.fetchall()
        productos = []
        producto = {}
        for fila in data:
            producto = {'id' : fila['id'],
                        'nombre' : fila['nombre']
                        ,'precio_unitario' : fila['precio_unitario']
                        ,'cantidad' : fila['cantidad']
                        ,'descripcion' : fila['descripcion']
                        ,'url_img' : fila['url_img']
                        }
            
            productos.append(producto)
            producto = {}
        return jsonify('productos: ',productos)
        
      
    



if __name__ == '__main__':

    app.run(port=3000, debug=True)
