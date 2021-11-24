from flask import Flask, jsonify
import numpy as np
import pandas as pd
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect = True)
session = Session(engine) 

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def Home_page():
    return(
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")   
def precipitation():
    last_year = dt.datetime(2017,8, 23) - dt.timedelta(days = 365)
    scores_precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > last_year).\
    order_by(Measurement.date).all()

    precipitation_yearly = []
    for i in precipitation:
        info = {}
        info['date'] = precipitation[0]
        info['prcp'] = precipitation[1]
        precipitation_yearly.append(info)
    
    session.close()

    return jsonify(precipitation_yearly)

@app.route("/api/v1.0/stations")
def stations():
   session = Session(engine)
   station = session.query(Station.station, Station.name).all()

   Dict_station = {} 

   for station, name in station:
       Dict_station = name 

   session.close 

   return jsonify(stations) 

@app.route('/api/v1.0/tobs<br/>')
def tobs():
    session=Session(engine)
    results = session.query(Measurement.station, Measurement.tobs).\
    filter(Measurement.date.between('2016-08-23', '2017-08-23')).all()
    tobs_list = []
    for i in results:
       dict = {}
       dict["station"] = tobs[0]
       dict["tobs"] = float(tobs[1])
       list.append(dict)  

    session.close 

    return jsonify(tobs_list) 


@app.route("/api/v1.0/<start><br/>")
def temp_start(start):
    session = Session(engine)

    temp_start = []

    all_temps = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start and Measurement.date <= end).order_by(Measurement.date).all()

    for date, min, max, avg in all_temps:
        dict = {}
        dict['date'] = date
        dict['TMIN'] = min
        dict['TMAX'] = max
        dict['TAVG'] = avg
        temp_start.append(dict)
    

    return jsonify(temp_start) 

@app.route("/api/v1.0/<start>/<end>")
def temp_end(start,end):
    session = Session(engine)
    temp_end = []

    all_temps = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start and Measurement.date <= end).order_by(Measurement.date).all()

    for date, min, max, avg in all_temps:
        temp_dict = {}
        temp_dict['date'] = date
        temp_dict['TMIN'] = min
        temp_dict['TMAX'] = max
        temp_dict['TAVG'] = avg
        all_temps.append(temp_end)
    
    session.close()

    return jsonify(all_temps)

if __name__ == '__main__':
    app.run(debug=True)



