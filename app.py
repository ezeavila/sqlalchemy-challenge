import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


import datetime as dt

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Welcome to our page. Available routes: <br/>"
        f"Precipitation: /api/v1.0/precipitation <br/>"
        f"Stations: /api/v1.0/stations <br/>"
        f"Temperature: /api/v1.0/stations <br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    session = Session(engine)

    precp_day = [Measurement.date,func.sum(Measurement.prcp)]

    daily_total_precp = session.query(*precp_day).\
    filter(func.strftime("%Y,%m,%d", Measurement.date) >= "2016,08,23").\
    group_by(Measurement.date).\
    order_by(Measurement.date).all()


    session.close()

    precipitation = []
    for date, prcp in daily_total_precp:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation.append(precipitation_dict)

    return jsonify(precipitation)



if __name__ == "__main__":
    app.run(debug=True)