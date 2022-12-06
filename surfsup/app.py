#notes to run flask app:  change terminal directory to directory containing app.py, then type python -m flask run 
# to quit, type clt-C
# https://code.visualstudio.com/docs/python/tutorial-flask

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
    """Available api routes."""
    return (
        f"SQLalchemy Challenge Module 10:  Chris Gruenhagen 6Dec2022<br/>"
         "<br/>"
        f"Available Static API Routes:<br/>"
         "<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        "<br/>"
        "<br/>"
        f"Available Dynamic API Routes:<br/>"
        f"Update the api route with the query start date or start and end dates in the format provided.<br/>"
        f"minimum start date = 2010-01-01, maximum end date = 2017-08-23<br/>"
        "<br/>"
        f"/api/v1.0/start/YYYY-MM-DD <br/>"
        f"for example: /api/v1.0/start/2014-02-04<br/>"
         "<br/>"
        f"/api/v1.0/start_end/YYYY-MM-DD/YYYY-MM-DD <br/>"
        f"for example: /api/v1.0/start_end/2014-04-05/2016-12-31" 
    )

#static api route for json of all stations precip data for the last year recorded in the DB
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """return jsonified data of precipitation data for the last year in the DB"""
    #determine the last measurement date
    final_date = session.query(Measure.date,func.strftime('%Y',Measure.date),\
        func.strftime('%m',Measure.date),func.strftime('%d',Measure.date)).\
        order_by(Measure.date.desc()).first()
    
    #calculate the year ago date for query start
    year_ago_date = dt.date(int(final_date[1]),int(final_date[2]),int(final_date[3])) - dt.timedelta(days = 365)

    #query the data from query start date and return a jsonified result
    precip = session.query(Measure.date, Measure.prcp).\
        filter(Measure.date>=(dt.date(int(final_date[1]),\
        int(final_date[2]),int(final_date[3])) - dt.timedelta(days = 365))).all()
    
    session.close()

    precip_ls = list(np.ravel(precip))
    return jsonify(precip_ls)

 #static api for a list of all stations   
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """return jsonified data of all the stations in the DB"""
    #query db for unique station ids and return a list of the stations
    stations = session.query(Station.station).distinct().all()
    session.close()

    stations_ls = list(np.ravel(stations))
    return jsonify(stations_ls)
    
#static api route for the busiest station temp data for the last year recorded in the DB
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """return jsonified data of the busiest station temp data for the last year recorded in the DB"""

    station_busiest = session.query(Measure.station, func.count(Measure.station)).\
        group_by(Measure.station).order_by(func.count(Measure.station).desc()).first()

    sbld = session.query(Measure.station,Measure.date,func.strftime('%Y',Measure.date),\
        func.strftime('%m',Measure.date),func.strftime('%d',Measure.date)).\
        filter(Measure.station == station_busiest[0]).order_by(Measure.date.desc()).first()

    st_year_ago = dt.date(int(sbld[2]),int(sbld[3]),int(sbld[4])) - dt.timedelta(days = 365)

    st_year_data = session.query(Measure.station, Measure.date, Measure.tobs).\
        filter(Measure.station == sbld[0],\
        Measure.date>=(dt.date(int(sbld[2]),int(sbld[3]),int(sbld[4])) - dt.timedelta(days = 365))).all()

    session.close()

    st_year_data_ls = list(np.ravel(st_year_data))
    return jsonify(st_year_data_ls)

#dynamic api route with query start date
@app.route("/api/v1.0/start/<query_date>")
def start(query_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """return the min,max and average temps calculated from the given start date to the end of the dataset"""
    # query and return the data from the given start date to the end of the dataset
    start_query = session.query(func.min(Measure.tobs), func.max(Measure.tobs), func.avg(Measure.tobs)).\
    filter(Measure.date>=query_date).all()

    session.close()

    start_query_ls = list(np.ravel(start_query))

    return jsonify(start_query_ls)

#dynamic api route with query start and end date
@app.route("/api/v1.0/start_end/<start_date>/<end_date>")
def start_end(start_date,end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # query and return the data from the given start date to the given end date

    start_end = session.query(func.min(Measure.tobs), func.max(Measure.tobs), func.avg(Measure.tobs)).\
        filter(Measure.date >= start_date).filter(Measure.date <=end_date).all()

    session.close()

    start_end_ls = list(np.ravel(start_end))

    return jsonify(start_end_ls)
    
