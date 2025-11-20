import cdsapi

# namelists
yr   = "2024"
mm   = "04"
dt   = ["25","26","27","28","29","30"]
path = "/scr1/alejandro/shared/era5/"

dataset = "reanalysis-era5-pressure-levels"
request = {
    "product_type": ["reanalysis"],
    "variable": [
        "geopotential",
        "relative_humidity",
        "specific_humidity",
        "temperature",
        "u_component_of_wind",
        "v_component_of_wind"
    ],
    "year": yr,
    "month": mm,
    "day": dt,
    "time": [
        "00:00",
        "03:00",
        "06:00",
        "09:00",
        "12:00",
        "15:00",
        "18:00",
        "21:00",
    ],
    "pressure_level": [
        "1", "2", "3",
        "5", "7", "10",
        "20", "30", "50",
        "70", "100", "125",
        "150", "175", "200",
        "225", "250", "300",
        "350", "400", "450",
        "500", "550", "600",
        "650", "700", "750",
        "775", "800", "825",
        "850", "875", "900",
        "925", "950", "975",
        "1000"
    ],
    "data_format": "grib",
    "download_format": "unarchived",
    "area": [-10, -60, -30, -30] # North, West, South, East
}

client = cdsapi.Client()
client.retrieve(dataset, request).download(path + f"era5_{yr}{mm}{dt[0]}_{yr}{mm}{dt[-1]}_3h_pl.grib")
