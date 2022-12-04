# Dependencies

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
Base.prepare(autoload_with=engine)

# Save references to the tables
Station = Base.classes.station
Measure = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """return json with the date as the key and the value as the precipitation for the last year in the DB"""
    precip = session.query(Measure.date, Measure.prcp).\
        filter(Measure.date>=(dt.date(2017,8,23) - dt.timedelta(days = 365))).all()
    session.close()

    precip_ls = list(np.ravel(precip))
    return jsonify(precip_ls)
    
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """return jsonified data of all the stations in the DB"""
    stations = session.query(Station.station).distinct().count()
    session.close()

    stations_ls = list(np.ravel(stations))
    return jsonify(stations)
    
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """return jsonified data of all the stations in the DB"""
    stationbusyyear = session.query(Measure.station, Measure.date, Measure.tobs).\
        filter(Measure.station == 'USC00519281',Measure.date>=(dt.date(2017,8,18) - dt.timedelta(days = 365))).all()
    session.close()

    stationbusyyear_ls = list(np.ravel(stationbusyyear))
    return jsonify(stationbusyyear_ls)

