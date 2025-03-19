from flask import Flask, render_template, request
from sqlalchemy import create_engine, text

app = Flask(__name__) 
#connection string is formatted: mysql://user:password@server/database
con_str = "mysql://root:cset155@localhost/boatdb"
engine = create_engine(con_str, echo=True)
conn = engine.connect()

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/boats')
def boats():
    boats = conn.execute(text('SELECT * FROM boats')).all()
    for boat in boats:
        print(boat)
    return render_template('boats.html', boats = boats[:10])


@app.route('/boatCreate', methods = ['GET'])
def getBoat():
    return render_template('boat_create.html')

@app.route('/boatCreate', methods = ['POST'])
def createBoat():
    conn.execute(text('INSERT INTO boats (id, name, type, owner_id, rental_price) VALUES (:id, :name, :type, :owner_id, :rental_price)'), {
        "id": request.form["id"],
        "name": request.form["name"],
        "type": request.form["type"],
        "owner_id": request.form["owner_id"],
        "rental_price": request.form["rental_price"]
    })
    conn.commit()
    return render_template('boat_create.html')

if __name__ == '__main__':
    app.run(debug=True)#last line