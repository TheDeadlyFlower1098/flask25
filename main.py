from flask import Flask, render_template, request
from sqlalchemy import create_engine, text

app = Flask(__name__) #Initialize the Flask app

# Database connection string (update credentials as needed)
# Formating: mysql://user:password@server/database
con_str = "mysql://root:cset155@localhost/boatdb"
engine = create_engine(con_str, echo=True)
conn = engine.connect() #creates the database engine

# Home route - displays the home page
@app.route('/')
def hello():
    return render_template('index.html')

# Route to display a list of boats (limited to 10)
@app.route('/boats')
def boats():

     # Fetch all boats from the database
    boats = conn.execute(text('SELECT * FROM boats')).all()

    for boat in boats:
        print(boat)

    # Pass boat data to the template
    return render_template('boats.html', boats = boats[:10]) 


@app.route('/boatCreate', methods = ['GET'])
def getBoat():
    return render_template('boat_create.html')

@app.route('/boatCreate', methods = ['POST'])
def createBoat():
    try:
        conn.execute(text('insert into boats values(:id, :name, :type, :owner_id, :rental_price)'), request.form)
    # conn.commit()
        return render_template('boat_create.html', error = None, success = 'successful')
    except:
        return render_template('boat_create.html', error = "fail", success = None)

# Run the Flask application in debug mode
if __name__ == '__main__':
    app.run(debug=True)