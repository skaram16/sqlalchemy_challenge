import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlachemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine('sqlite:///Resources/hawaii.sqlite', connect_args= {'check_same_thread':False})


Base=automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#weather app
app = Flask(__name__)


recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

recent_date = list(np.ravel(recent_Date))[0]
recent_date = dt.datetime.strptime(recent_date, '%Y-%m-%d')
recent_year = int(dt.datetime.strftime(recent_date, '%Y')
recent_month = int(dt.datetime.strftime(recent_date, '%m')
recent_day = int(dt.datetime.strftime(recent_date, '%d')

year_before = dt.date(recent_year, recent_month, recent_day) - dt.timedelta(days=365)
year_before = dt.datetime(strftime(year_before, '%Y-%m-%d')




@app.route("/")
def home():
    return(f'"Welcome to Surf's Up!: Hawai'i Climate API<br/>"
            f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<br/>"
            f"Available Routes:<br/>"
            f"/api/v1.0/stations ~~~~~ a list of all weather observation stations<br/>"
            f"/api/v1.0/precipitaton ~~ the latest year of preceipitation data<br/>"
            f"/api/v1.0/temperature ~~ the latest year of temperature data<br/>"
            f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<br/>"
            f"~~~ datesearch (yyyy-mm-dd)<br/>"
            f"/api/v1.0/datesearch/2015-05-30  ~~~~~~~~~~~ low, high, and average temp for date given and each date after<br/>"
            f"/api/v1.0/datesearch/2015-05-30/2016-01-30 ~~ low, high, and average temp for date given and each date up to and including end date<br/>"
            f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<br/>"
            f"~ data available from 2010-01-01 to 2017-08-23 ~<br/>"
            f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

@app.route("/api/v1.0/stations")
def stations():
     results = session.query(Station.name).all()
     all_stations = list(np.ravel(results))
     return jsonify(all_stations)

@app.route("/api/v1.0/precipitation")
def precipitation():

    results = (session.query(Measurement.date, Measurement.prcp, Measurement.station).filter(Measurement.date > year_before).order_by(Measurement.date).all())

    precipData = []
    for result in results:
        precipDict = {result.date: result.prcp, "Station": result.station}
        precipData.append(precipDict)

    return jsonify(precipData)

@app.route("/api/v1.0/temperature")
def temperature():

    results = (session.query(Measurement.date, Measurement.tobs, Measurement.station).filter(Measurement.date > year_before).order_by(Measurement.date).all())

    tempData = []
    for result in results:
        tempDict = {result.date: result.tobs, "Station": result.station}
        tempData.append(tempDict)

    return jsonify(tempData)

@app.route('/api/v1.0/datesearch/<start_date>')
def start(start_date):
    sel = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    results = (session.query(*sel).filter(func.strftime('%Y-%m-%d', Measurement.date) >=start_date).group_by(Measurement.date).all())

    dates = []
    for result in results:
        date_dict = {}
        date_dict["Date"] = result[0]
        date_dict["Low Temperature"] = result[1]
        date_dict["Average Temperature"]  = result[2]
        date_dict["High Temperature"] = result[3]
        dates.append(date_dict)
    return jsonify(dates)

@app.route('/api/v1.0/datesearch/<start_date>/<end_date>')
def start_end(start_date, end_date):
    sel = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    results = (session.query(*sel).filter(func.strftime("%Y-%m-%d", Measurement.date) >= start_date).filter(func.strftime("%Y-%m-%d", Measurement.date) <= end_date).group_by(Measurement.date).all())

    dates = []
    for result in results:
        date_dict = {}
        date_dict["Date"] = result[0]
        date_dict["Low Temperature"] = result[1]
        date_dict["Average Temperature"]  = result[2]
        date_dict["High Temperature"] = result[3]
        dates.append(date_dict)
    return jsonify(dates)

if __name__ == "__main__":
    app.run(debug=True)
    
