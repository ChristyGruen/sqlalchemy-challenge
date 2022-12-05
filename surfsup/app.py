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
        f"Available Static API Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        "<br/>"
        "<br/>"
        f"Available Dynamic API Routes:<br/>"
        f"/api/v1.0/temp/<start_date><br/>"
        f"/api/v1.0/temp/<start_date>/<end_date>"     
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """return json with the date as the key and the value as the precipitation for the last year in the DB"""
    final_date = session.query(Measure.date,func.strftime('%Y',Measure.date),\
        func.strftime('%m',Measure.date),func.strftime('%d',Measure.date)).\
        order_by(Measure.date.desc()).first()
    
    year_ago_date = dt.date(int(final_date[1]),int(final_date[2]),int(final_date[3])) - dt.timedelta(days = 365)

    precip = session.query(Measure.date, Measure.prcp).\
        filter(Measure.date>=(dt.date(int(final_date[1]),\
        int(final_date[2]),int(final_date[3])) - dt.timedelta(days = 365))).all()

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

# @app.route("/api/v1.0/temp") #@app.route("/api/v1.0/temp/<query_date>")
# def temp():  #def temp(start_date):
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     """return the min,max and average temps calculated from the given start date to the end of the dataset"""
#     # query the data
#     query_date = dt.date(2013,8,14)

#     temp_query = session.query(func.min(Measure.tobs), func.max(Measure.tobs), func.avg(Measure.tobs)).\
#     filter(Measure.date>=query_date).all()

#     session.close()

#     temp_query_ls = list(np.ravel(temp_query))

#     return jsonify(temp_query_ls)

# @app.route("/api/v1.0/temp3/<query_year><query_month><query_day>")
# def temp3(query_year,query_month,query_day):  #def temp(start_date):
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     """return the min,max and average temps calculated from the given start date to the end of the dataset"""
#     # query the data
#     # static date to test query query_date = dt.date(2013,8,14)
#     query_date2 = dt.date(int(query_year),int(query_month),int(query_day))

#     temp_query = session.query(func.min(Measure.tobs), func.max(Measure.tobs), func.avg(Measure.tobs)).\
#     filter(Measure.date>=query_date2).all()

#     session.close()

#     temp_query_ls = list(np.ravel(temp_query))

#     return jsonify(temp_query_ls)


@app.route("/api/v1.0/temp4/<query_date>")
def temp4(query_date):  #def temp(start_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """return the min,max and average temps calculated from the given start date to the end of the dataset"""
    # query the data
    # static date to test query query_date = dt.date(2013,8,14)
    #query_date2 = dt.date(int(query_year),int(query_month),int(query_day))

    temp_query = session.query(func.min(Measure.tobs), func.max(Measure.tobs), func.avg(Measure.tobs)).\
    filter(Measure.date>=query_date).all()

    session.close()

    temp_query_ls = list(np.ravel(temp_query))

    return jsonify(temp_query_ls)







@app.route("/api/v1.0/temp2/<start_date>/<end_date>")
def temp2(start_date,end_date):  # def temp(start_date,end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # query the data
    # start_date = dt.date(2016,8,14)
    # end_date = dt.date(2017,8,14)

    temp_query2 = session.query(func.min(Measure.tobs), func.max(Measure.tobs), func.avg(Measure.tobs)).\
        filter(Measure.date >= start_date).filter(Measure.date <=end_date).all()

    session.close()

    temp_query2_ls = list(np.ravel(temp_query2))

    return jsonify(temp_query2_ls)
    

    # if __name__ == "__main__":
    #     app.run(debug=True)

# @app.route("/api/v1.0/christry")
# def christry():
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     """return jsonified data of all the stations in the DB"""

#     station_busiest = session.query(Measure.station, func.count(Measure.station)).\
#         group_by(Measure.station).order_by(func.count(Measure.station).desc()).first()

#     sbld = session.query(Measure.station,Measure.date,func.strftime('%Y',Measure.date),\
#         func.strftime('%m',Measure.date),func.strftime('%d',Measure.date)).\
#         filter(Measure.station == station_busiest[0]).order_by(Measure.date.desc()).first()

#     st_year_ago = dt.date(int(sbld[2]),int(sbld[3]),int(sbld[4])) - dt.timedelta(days = 365)

#     st_year_data = session.query(Measure.station, Measure.date, Measure.tobs).\
#         filter(Measure.station == sbld[0],\
#         Measure.date>=(dt.date(int(sbld[2]),int(sbld[3]),int(sbld[4])) - dt.timedelta(days = 365))).all()

#     session.close()

#     # #put data into pd dataframe
    # st_year_data_df = pd.DataFrame(st_year_data,columns = ['station','date','tobs'])
    # #describe df
    # describe_df = st_year_data_df.describe()
    # return jsonify(describe_df)


    # st_year_data_ls = list(np.ravel(st_year_data))

    # return jsonify(st_year_data_ls)