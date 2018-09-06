from flask import Flask, jsonify
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np


app = Flask(__name__)
    
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)


@app.route("/")
def welcome():
   
    return (
        f"Welcome to this Climate Analysis<br/>"

        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start_end<br/"

    )
  
@app.route("/api/v1.0/precipitation")
def precipitation():
    #Calculate the date 1 year ago from today
    one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

    #Perform a query to retrieve the data and precipitation scores
    precip_analysis = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23").filter(Measurement.date <="2017-08-23").all()

    #Create a dictionary from returned list
    results = dict(precip_analysis)
    return jsonify(results)

#Return a list of all stations
@app.route("/api/v1.0/stations")
def stations():
    
    station = session.query(Station.id, Station.station).all()

    station_dict = dict(station)

    return jsonify(station_dict)

#Return a list of all precipitation levels in the last year
@app.route("/api/v1.0/tobs")
def tobs():
    
    last_year = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    print(last_year)

    #Calculate the date 1 year ago from today
    one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    print(one_year_ago)

    #Perform a query to retrieve the data and precipitation scores
    tobs = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date > one_year_ago).order_by(Measurement.date).all()

    # Create a dictionary from returned list
    tobs_dict = dict(tobs)
    return jsonify(tobs_dict)

#Fetch a JSON list of minimum temperatures, average temperatures, and max temperatures for a given start
@app.route("/api/v1.0/<start>")
def start_date(start):
    
    #start = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    start_date = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    return jsonify(start_date)

#Fetch a JSON list of minimum temperatures, average temperatures, and max temperatures for a given start
@app.route("/api/v1.0/<start_end>")
def start_end(start, end):
    
    start_end_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(start_end_results)



if __name__ == '__main__':
    app.run(debug=True)
