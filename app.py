import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Check table names
print(Base.classes.keys())

# Save reference to the tables
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
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"To get average, maximum, and minimum temperatures over a time period,<br/>"
        f"use the below routes with date format 'YYYY-MM-DD'<br/>"
        f"e.g. /api/v1.0/2016-10-10/2016-12-31<br/>"
        f"<br/>"
        f"/api/v1.0/start-date<br/>"
        f"/api/v1.0/start-date/end-date"
    )

# Returns all dates and all precipitation amounts
@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    """Return a list of all date and precipitation records"""
    # Query all measurements
    results = session.query(Measurement.date,Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list
    prcp_by_date = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_by_date.append(prcp_dict)

    return jsonify(prcp_by_date)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all stations"""
    session = Session(engine)

    # Query all station names
    results = session.query(Station.name).all()

    session.close()

    # Store all station names in a list
    stations_all = list(np.ravel(results))

    return jsonify(stations_all)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of all stations"""
    session = Session(engine)

    # Query temperatures recorded from most active station in the last year with available data
    results = session.query(Measurement.tobs).\
    filter(Measurement.date >= '2016-08-18').\
    filter(Measurement.station == 'USC00519281').all()

    session.close()

    # Store temperature data in a list
    tobs_all = list(np.ravel(results))

    return jsonify(tobs_all)

@app.route("/api/v1.0/<start>/<end>")
def dynamic_temps(start,end):
    """Fetch the Justice League character whose real_name matches
       the path variable supplied by the user, or a 404 if not."""

    session = Session(engine)

    # Create start_date and end_date variables in YYYY-MM-DD format
    start_date = datetime.strptime(start, "%Y-%m-%d").date()
    end_date = datetime.strptime(end,"%Y-%m-%d").date()

    # Calculate and store average temperature
    avg_temp = session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).all()

    # Calculate and store minimum temperature
    min_temp = session.query(func.min(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).all()

    # Calculate and store maximum temperature
    max_temp = session.query(func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).all()
    
    session.close()

    # Generate empty list and dictionary for temperature data 
    temps_list = []
    temps_dict={}
    temps_dict["avg_temp"] = list(np.ravel(avg_temp))
    temps_dict["min_temp"] = list(np.ravel(min_temp))
    temps_dict["max_temp"] = list(np.ravel(max_temp))

    temps_list.append(temps_dict)

    return jsonify(temps_list)

@app.route("/api/v1.0/<start>")
def start_temps(start):

    session = Session(engine)

    # Create start_date variable in YYYY-MM-DD format
    start_date = datetime.strptime(start, "%Y-%m-%d").date()

    # Calculate and store average temperature
    avg_temp = session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

    # Calculate and store minimum temperature
    min_temp = session.query(func.min(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

     # Calculate and store maximum temperature
    max_temp = session.query(func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    
    session.close()

    # Create empty list and dictionary to store avg, min, and max temperature 
    temps_list = []
    temps_dict={}
    temps_dict["avg_temp"] = list(np.ravel(avg_temp))
    temps_dict["min_temp"] = list(np.ravel(min_temp))
    temps_dict["max_temp"] = list(np.ravel(max_temp))

    temps_list.append(temps_dict)

    return jsonify(temps_list)


if __name__ == '__main__':
    app.run(debug=True)
