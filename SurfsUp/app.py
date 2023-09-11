# Import dependencies and reflect database
import numpy as np


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


from flask import Flask, jsonify

# Create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect Database into ORM classes
Base = automap_base()
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def welcome():
    """List all available API routes."""
    return (
        "Available Routes:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query the precipitation data for the last 12 months
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= 'YOUR_START_DATE_HERE').all()

    session.close()

    # Convert list of tuples into normal list
    precip_data = {date: prcp for date, prcp in results}

    # Return the JSON representation of the dictionary
    return jsonify(precip_data)

@app.route("/api/v1.0/stations")
def station_list():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query the list of distinct stations
    results = session.query(Measurement.station).distinct().all()

    session.close()

    # Convert list of tuples into normal list
    station_list = [station for station, in results]

    # Return the JSON representation of the list
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def temperature_observations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query the dates and temperature observations of the most active station for the previous year of data
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'YOUR_STATION_ID_HERE').filter(Measurement.date >= 'YOUR_START_DATE_HERE').all()

    session.close()

    # Convert list of tuples into normal list
    temperature_data = [{"Date": date, "Temperature": tobs} for date, tobs in results]

    # Return the JSON representation of the list
    return jsonify(temperature_data)

if __name__ == '__main__':
    app.run(debug=True)
