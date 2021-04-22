from flask import Flask, jsonify
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
db_path = "Resources/hawaii.sqlite"
engine = create_engine(f"sqlite:///{db_path}")
conn = engine.connect()
base = automap_base()
base.prepare(engine, reflect = True)
base.classes.keys()
Measurement = base.classes.measurement
Station = base.classes.station
station_data = pd.read_sql('select * from Station ;', conn)
measurement_data = pd.read_sql('select * from Measurement ;', conn)
# reflect the tables
session = Session(engine)






app = Flask(__name__)

@app.route("/")
def home():
    return(f"Welcome to the home page, please copy and paste the following link after the base URL. <br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0<start><br/>"
    f"/api/v1.0/start/end<br/>")

    return("Welcome to the home page")

@app.route("/api/v1.0/precipitation")
def precipitation():
    latest_date = session.query(func.max(Measurement.date)).first()
    # Design a query to retrieve the last 12 months of precipitation data and plot the results. 
    # Starting from the most recent data point in the database. 

    # Calculate the date one year from the last date in data set.
    previos_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    last_12 = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > previos_year).all()

    # Save the query results as a Pandas DataFrame and set the index to the date column
    df = pd.DataFrame(last_12).set_index('date')

    # Sort the dataframe by date
    df = df.dropna()
    df = df.sort_values(["date"], ascending = True)
    # date = df['date']
    # prcp = df['prcp']
    


    # Use Pandas Plotting with Matplotlib to plot the data
    # plt.scatter(date,prcp)
    # plt.figsize()
    # df.plot(rot=90, color='red', figsize = (20,20))
    # plt.title("Precipitation last 12 months")
    # plt.ylabel("Precipitation")
    # plt.xlabel("Date")
    # plt.grid(which='both', axis="x")
    # plt.savefig('Precipitation_between_08_16_to_08_17.jpg')
    # plt.show()

    return (f"{df}")

@app.route("/api/v1.0/stations")
def stations():
    station_data = session.query(Station.station).all()
    station_list = list(np.ravel(station_data))
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    previos_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    all_temp = session.query(Measurement.date, Measurement.tobs).filter\
        (Measurement.date > previos_year).all()
    sta = list(np.ravel(all_temp))
    return jsonify(sta)

@app.route("/api/v1.0/<start>")
def start():
    lowest_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.station == 'USC00519281').first()
    print(f"The lowest temperature is {lowest_temp}")

    highest_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.station == 'USC00519281').first()
    print(f"The highest temperature is {highest_temp}")

    average_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.station == 'USC00519281').first()
    print(f"The average temperature is {average_temp}")


if __name__ == "__main__":
    app.run(debug=True)