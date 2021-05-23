import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################


@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate App!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )



@app.route("/api/v1.0/precipitation")
def precipitation():
    
    session = Session(engine)
    most_recent_date=session.query(func.max(Measurement.date)).all()
    max_date = np.ravel(most_recent_date)[0]

    max_date_2 = dt.datetime.strptime(max_date, '%Y-%m-%d')
    max_date_2_ly = max_date_2 - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= max_date_2_ly).\
    filter(Measurement.prcp != "None").\
    order_by(Measurement.date.asc()).all()

    session.close()
    
    print(results)

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)
    

@app.route("/api/v1.0/stations")
def stations():
   
    session = Session(engine)
    list_stations = session.query(Station.station).all()

    session.close()
    
    # Convert list of tuples into normal list
    all_names = list(np.ravel(list_stations))

    return jsonify(all_names)    
    
@app.route("/api/v1.0/tobs")
def tobs():
   
    session = Session(engine)
    most_active_station = session.query(Measurement.station,func.count(Measurement.station)).\
        group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()


    tobs = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station == most_active_station[0]).\
    filter(Measurement.date >= '2017-01-01').all()

    session.close()
    
    # Convert list of tuples into normal list
    all_names = list(np.ravel(tobs))

    return jsonify(all_names)    

@app.route("/api/v1.0/start/<start>")
def start(start):

    session = Session(engine)
    most_active_station = session.query(Measurement.station,func.count(Measurement.station)).\
        group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()


    lowest_temp = session.query(func.min(Measurement.tobs)).\
    filter(Measurement.station == most_active_station[0]).\
    filter(Measurement.date >= start).first()
    
    highest_temp = session.query(func.max(Measurement.tobs)).\
    filter(Measurement.station == most_active_station[0]).\
    filter(Measurement.date >= start).first()
    
    average_temp = session.query(func.avg(Measurement.tobs)).\
    filter(Measurement.station == most_active_station[0]).\
    filter(Measurement.date >= start).first()

    
    session.close()
    
    print(f"start= {start}")
    
    # Convert list of tuples into normal list
    all_names_1 = list(np.ravel(lowest_temp))
    all_names_2 = list(np.ravel(highest_temp))
    all_names_3 = list(np.ravel(average_temp))

        
    
    if all_names_1 != " ":
        return jsonify(f"lowest temp = {all_names_1}, highest temp = {all_names_2}, average temp = {all_names_3}")

    
    return jsonify({"error": f"Character with real_name {real_name} not found."}), 404


@app.route("/api/v1.0/start/end/<start>/<end>")
def start_end(start, end):

    session = Session(engine)
    most_active_station = session.query(Measurement.station,func.count(Measurement.station)).\
        group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()


    lowest_temp = session.query(func.min(Measurement.tobs)).\
    filter(Measurement.station == most_active_station[0]).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).first()
    
    highest_temp = session.query(func.max(Measurement.tobs)).\
    filter(Measurement.station == most_active_station[0]).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).first()
    
    average_temp = session.query(func.avg(Measurement.tobs)).\
    filter(Measurement.station == most_active_station[0]).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).first()

    
    session.close()
    
    print(f"start= {start}")
    print(f"end= {end}")
    
    # Convert list of tuples into normal list
    all_names_1 = list(np.ravel(lowest_temp))
    all_names_2 = list(np.ravel(highest_temp))
    all_names_3 = list(np.ravel(average_temp))

        
    
    if all_names_1 != " ":
        return jsonify(f"lowest temp = {all_names_1}, highest temp = {all_names_2}, average temp = {all_names_3}")

    
    return jsonify({"error": f"Character with real_name {real_name} not found."}), 404

 
    
if __name__ == "__main__":
    app.run(debug=True)


