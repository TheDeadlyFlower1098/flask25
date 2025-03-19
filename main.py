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
    
#Route for searching bots
@app.route('/search', methods=['GET', 'POST'])
def searchBoat():
    results = []  # Initialize an empty results list
    if request.method == 'POST':  # Check if the form was submitted
        search_query = request.form['search']  # Get the search term from the form
        with engine.connect() as conn:
            # Query the database for boats matching the search term (partial match using LIKE)
            results = conn.execute(text('SELECT * FROM boats WHERE name LIKE :search'), {'search': f'%{search_query}%'}).fetchall()
    return render_template('search.html', results=results)  # Render the search results page

# Route for searching boats by ID and deleting
@app.route('/search_delete', methods=['GET', 'POST'])
def search_delete_boat():
    result = None  # Initialize result to None
    if request.method == 'POST':  # When the form is submitted
        search_query = request.form['search']  # Get the search term (boat ID)
        
        with engine.connect() as conn:
            # Query to check if the boat exists by ID
            result = conn.execute(text('SELECT * FROM boats WHERE id = :search'), {'search': search_query}).fetchone()
            
            if result:
                # If the boat is found, proceed with the deletion
                conn.execute(text('DELETE FROM boats WHERE id = :search'), {'search': search_query})
                return render_template('search_delete.html', result=result, success='Boat deleted successfully!')
            else:
                return render_template('search_delete.html', result=None, error="Boat not found!")
    
    return render_template('search_delete.html', result=result)  # Render the search results page


# Run the Flask application in debug mode
if __name__ == '__main__':
    app.run(debug=True)