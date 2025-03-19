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
    for boats in boats:
        print(boats)
    return render_template('boats.html', boats = boats[:10])


@app.route('/boatCreate', methods = ['GET'])
def getBoat():
    return render_template('boat_create.html')

@app.route('/boatCreate', methods = ['POST'])
def createBoat():
    conn.execute(text('INSERT INTO boats values(:id, :name, :type, :owner_id, :rental_price)'), request.form).all()
    conn.commit()
    return render_template('boat_create.html')

# @app.route('/<name>')
# def welcome(name): 
#     return render_template('user.html', name = name)

# @app.route('/hello')
# def hello():
#     return f'hello'

# @app.route('/hello/<int:name>')
# def serving_cofee(name):
#     return f'the next number is {name +1}'

# @app.route('/donut')
# def donuts():
#     return 'here is your donut'


if __name__ == '__main__':
    app.run(debug=True)#last line