from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_bcrypt import Bcrypt
from utils.config import Config as cfg
from sqlalchemy import text
from models.models import InmateModel,CellModel, CrimeModel, UserModel, db 

config = cfg.read_config('./config/config.yaml') #Read the config file using the config class
app = Flask(__name__) #Create the flask app

database_url = config['db']['uri'] #Get the database url from the config file
app.config['SQLALCHEMY_DATABASE_URI'] = database_url #Set the database url
db.init_app(app)
bcrypt = Bcrypt(app)
@app.before_request
def create_tables():
    db.create_all()

@app.route('/', methods=['GET']) 
def index():
    return render_template('index.html') #Render the index html

#Crud operations

#Create
@app.route('/AddInmate', methods=['GET','POST'])
def add_inmate():
    cells = CellModel.query.all()
    crimes = CrimeModel.query.all()
    if request.method == 'POST':
        fullname = request.form.get('name')
        inmatenum = request.form.get('number')
        if InmateModel.query.filter_by(inmatenum=inmatenum).first():
            return str("Inmate already exists")
        arrivaldate = request.form.get('arrival_date')
        sentencetime = request.form.get('sentence_time')
        penalty = request.form.get('penalty')
        cell_num = request.form.get('cellnum')
        cell = CellModel.query.filter_by(cellnum=cell_num).first().cellid
        if CellModel.count_inmates(cell) >= CellModel.query.filter_by(cellid=cell).first().numberofbeds:
            return str("Cell is full")
        crime_description = request.form.get('crime')
        crime = db.session.query(CrimeModel).filter_by(description=crime_description).first().crimeid
        inmate = InmateModel(fullname, inmatenum, arrivaldate, sentencetime, penalty, cell, crime)
        db.session.add(inmate)
        db.session.commit()
        db.session.close()
        return str("Inmate succesfully added <button><a href='/'>Click here to go back</a></button>")
    #if the method is get then render the addform html file
    return render_template('addform.html', cells=cells, crimes=crimes)

#Get all inmates
@app.route('/Inmates', methods=['GET'])
def get_inmates():
    inmates = InmateModel.query.all()
    inmates_dict = []
    for inmate in inmates:
        inmates_dict.append({
            'id': inmate.inmateid,
            'fullname': inmate.fullname,
            'inmatenum': inmate.inmatenum,
            'arrivaldate': inmate.arrivaldate,
            'sentencetime': inmate.sentencetime,
            'penalty': inmate.penalty,
            'cellid': inmate.cellid,
            'crimeid': inmate.crimeid
        })
    return jsonify(inmates_dict)


#Get an inmate based on id
@app.route('/Inmate/<int:id>', methods=['GET'])
def get_inmate(id):
    inmate = InmateModel.query.filter_by(inmateid=id).first()
    if inmate:
        inmate_dict = {
            'id': inmate.inmateid,
            'fullname': inmate.fullname,
            'inmatenum': inmate.inmatenum,
            'arrivaldate': inmate.arrivaldate,
            'sentencetime': inmate.sentencetime,
            'penalty': inmate.penalty,
            'cellid': inmate.cellid,
            'crimeid': inmate.crimeid
        }
        return jsonify(inmate_dict)
    return str("Inmate not found")


#Delete an inmate
@app.route('/DeleteInmate', methods=['GET','POST'])
def delete_inmate():
    if request.method == 'POST':
        inmateid = request.form.get('id')
        inmate = InmateModel.query.filter_by(inmateid=inmateid).first()
        if inmate:
            db.session.delete(inmate)
            db.session.commit()
            db.session.close()
            return str("Inmate succesfully deleted <button><a href='/'>Click here to go back</a></button>")
        return str("Inmate not found")
    return render_template('deleteform.html')

#Upate an inmate's cell
@app.route('/UpdateInmate', methods=['GET','POST'])
def update_inmate():
    cells = CellModel.query.all()
    inmates = InmateModel.query.all()
    if request.method == 'POST':
        inmate_name = request.form.get('inmatename')
        inmate = InmateModel.query.filter_by(fullname=inmate_name).first()
        cell_num = request.form.get('cellnum')
        cell = CellModel.query.filter_by(cellnum=cell_num).first().cellid
        if CellModel.count_inmates(cell) >= CellModel.query.filter_by(cellid=cell).first().numberofbeds:
            return str("Cell is full")
        inmate.cellid = cell
        db.session.commit()
        db.session.close()
        return str("Sucesfully update cell <button><a href='/'>Click here to go back</a></button>")
    return render_template('updateform.html', cells=cells, inmates=inmates)


#Join crimes and inmates table for statistical view
@app.route('/CrimeStatistics', methods=['GET', 'POST'])
def get_crime_statistics():
    if request.method == 'POST':
        crime = request.form.get('crimename')
        #description = db.session.query(CrimeModel).filter_by(description=crime).first().crimeid
        description = CrimeModel.query.filter_by(description=crime).first()
        inmate = InmateModel.query.filter_by(crimeid=description).first()
        if inmate :
            response = db.session.execute(text(f"select * FROM inmate INNER JOIN crime ON crime.crimeid = inmate.crimeid WHERE inmate.crimeid = {inmate.crimeid}")).tuples()
            response_dict = [
                {
                    'id': row.inmateid,
                    'fullname': row.fullname,
                    'inmatenum': row.inmatenum,
                    'arrivaldate': row.arrivaldate,
                    'sentencetime': row.sentencetime,
                    'penalty': row.penalty,
                    'cellid': row.cellid,
                    'crimeid': row.crimeid,
                    'description': row.description
                } for row in response
            ]
            return jsonify(response_dict)
        return str("No data for that crime")
    return render_template('statistics.html', crimes=CrimeModel.query.all())

#Login with hashed passwords check
@app.route('/Login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        user = UserModel.query.filter_by(username=username).first()
        if user:
            user_password = user.password
            password = request.form.get('password')
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            hashed_db_password = bcrypt.generate_password_hash(user_password).decode('utf-8')
        if hashed_password == hashed_db_password:
            return render_template('index.html')
    return render_template('login.html')

@app.route('/Logout', methods=['GET'])
def logout():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) #Run the app
