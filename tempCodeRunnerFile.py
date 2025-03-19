@app.route('/boatCreate', method = ['POST'])
def createBoat():
    # conn.execute(text('INSERT INTO boats values(id, name, type, owner_id, rental_price)'), request.form).all()
    data=request.form
    print(data)
    return render_template('boat_create.html')