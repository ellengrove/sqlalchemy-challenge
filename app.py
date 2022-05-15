import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Check table names
print(Base.classes.keys())

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
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
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
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all measurements
    results = session.query(Station.name).all()

    session.close()

    # Create a dictionary from the row data and append to a list
    stations_all = list(np.ravel(results))

    return jsonify(stations_all)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all measurements
    results = session.query(Measurement.tobs).\
    filter(Measurement.date >= '2016-08-18').\
    filter(Measurement.station == 'USC00519281').all()

    session.close()

    # Create a dictionary from the row data and append to a list
    tobs_all = list(np.ravel(results))

    return jsonify(tobs_all)

@app.route("/api/v1.0/<start>")
def start_temps(start):
    """Fetch the Justice League character whose real_name matches
       the path variable supplied by the user, or a 404 if not."""

    session = Session(engine)

    print(start)
    start_date = dt.date(start)
    print(start_date)

    avg_temp = session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.station == 'USC00519281').all()

    min_temp = session.query(func.min(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.station == 'USC00519281').all()

    max_temp = session.query(func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.station == 'USC00519281').all()
    
    session.close()
    
    temp_dict = {'avg_temp' : avg_temp,
                'min_temp' : min_temp,
                'max_temp' : max_temp}

    return jsonify(temp_dict)


if __name__ == '__main__':
    app.run(debug=True)
