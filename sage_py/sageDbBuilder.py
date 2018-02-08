import csv
import os
import peewee


DATABASE = peewee.SqliteDatabase('sagehen.db')


class HourData(peewee.Model):
    """An instance of the HourData class is a row in sqlite3 database
    file. Each static class variable represents a row value for a
    particular column.
    """
    date_time = peewee.DateTimeField()
    solar_rad = peewee.FloatField(
        null=True,
    )
    wind_ave = peewee.FloatField(
        null=True,
    )
    wind_dir = peewee.IntegerField(
        null=True,
    )
    wind_max = peewee.FloatField(
        null=True,
    )
    temp_ave = peewee.FloatField(
        null=True,
    )
    temp_max = peewee.FloatField(
        null=True,
    )
    temp_min = peewee.FloatField(
        null=True,
    )
    soil_tave = peewee.FloatField(
        null=True,
    )
    soil_tmax = peewee.FloatField(
        null=True,
    )
    soil_tmin = peewee.FloatField(
        null=True,
    )
    rh_ave = peewee.IntegerField(
        null=True,
    )
    rh_max = peewee.IntegerField(
        null=True,
    )
    rh_min = peewee.IntegerField(
        null=True,
    )
    dew_pt = peewee.FloatField(
        null=True,
    )
    wet_bulb = peewee.FloatField(
        null=True,
    )
    pressure = peewee.IntegerField(
        null=True,
    )
    snow = peewee.FloatField(
        null=True,
    )
    precip = peewee.FloatField(
        null=True,
    )

    class Meta:
        database = DATABASE

    def __str__(self):
        return self.date_time.strftime("%Y-%m-%d %H:%M")


def connect_and_create_tables():
    """Uses Peewee's builtin methods to connect to a sqlite3 database
    defined by the DATABASE Object (a Peewee database Object), add the
    appropriate tables, and close the connection.
    """
    DATABASE.connect()
    DATABASE.create_tables([HourData], safe=True)
    DATABASE.close()


def build_db():
    """Uses a context manager to read each line of a CSV file,
    creates a HourData object for the line which in turn adds the data to
    the database.
    """
    with open('../SAGEHEN_1APR1997-14DEC2017.csv') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            Alpha = HourData()
            date_str = row['DATE'] + " " + row['HOUR OF DAY ENDING AT L.S.T'] + ":00"
            Alpha.date_time = date_str
            if row["TOTAL SOLAR RAD (K W-hr/m^2)"] != "":
                Alpha.solar_rad = float(row["TOTAL SOLAR RAD (K W-hr/m^2)"])
            if row["AVE WIND SPEED (m/s)"] != "":
                Alpha.wind_ave = float(row["AVE WIND SPEED (m/s)"])
            if row["V. WIND DIR (Deg)"] != "":
                Alpha.wind_dir = int(row["V. WIND DIR (Deg)"])
            if row["MAX WIND SPEED (m/s)"] != "":
                Alpha.wind_max = float(row["MAX WIND SPEED (m/s)"])
            if row["AIR TEMP AVE (Deg C)"] != "":
                Alpha.temp_ave = float(row["AIR TEMP AVE (Deg C)"])
            if row["AIR TEMP MAX (Deg C)"] != "":
                Alpha.temp_max = float(row["AIR TEMP MAX (Deg C)"])
            if row["AIR TEMP MIN (Deg C)"] != "":
                Alpha.temp_min = float(row["AIR TEMP MIN (Deg C)"])
            if row["SOIL TEMP AVE (Deg C)"] != "":
                Alpha.soil_tave = float(row["SOIL TEMP AVE (Deg C)"])
            if row["SOIL TEMP MAX (Deg C)"] != "":
                Alpha.soil_tmax = float(row["SOIL TEMP MAX (Deg C)"])
            if row["SOIL TEMP MIN (Deg C)"] != "":
                Alpha.soil_tmin = float(row["SOIL TEMP MIN (Deg C)"])
            if row["RELATIVE HUMIDITY AVE (%)"] != "":
                Alpha.rh_ave = int(row["RELATIVE HUMIDITY AVE (%)"])
            if row["RELATIVE HUMIDITY MAX (%)"] != "":
                Alpha.rh_max = int(row["RELATIVE HUMIDITY MAX (%)"])
            if row["RELATIVE HUMIDITY MIN (%)"] != "":
                Alpha.rh_min = int(row["RELATIVE HUMIDITY MIN (%)"])
            if row["DEW PT. (Deg C)"] != "":
                Alpha.dew_pt = float(row["DEW PT. (Deg C)"])
            if row["WET BULB (Deg C)"] != "":
                Alpha.wet_bulb = float(row["WET BULB (Deg C)"])
            if row["BARO. PRESS. (mb)"] != "":
                Alpha.pressure = int(row["BARO. PRESS. (mb)"])
            if row["SNOW DEPTH (mm)"] != "":
                Alpha.snow = float(row["SNOW DEPTH (mm)"])
            if row["TOTAL PRECIP (mm)"] != "":
                Alpha.precip = float(row["TOTAL PRECIP (mm)"])
            Alpha.save()


if __name__ == "__main__":
    connect_and_create_tables()
    build_db()
    os.system("say 'Built Database'")
