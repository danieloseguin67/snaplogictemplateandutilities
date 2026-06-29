"content"
"# WeatherDataPostalcode Pipeline Description

## Overview
This pipeline retrieves location information based on a given postal code and uses it to fetch hourly weather forecast data. It first calls a postal code API to obtain geographic coordinates and place details, then queries a weather API for hourly temperature forecasts at that location. The resulting data is processed and exported in two formats: an Excel file and a CSV file, both named after the input postal code.

---

## Pipeline Flow Diagram

HTTP Client (Zippopotam API)
  +---> JSON Splitter
          +---> Mapper (MapFromJsonToVar)
                  +---> HTTP Client (Open-Meteo Weather API)
                          +---> Mapper (Hour and Temperature)
                                  +---> JSON Splitter (Flatten Rows)
                                          +---> Copy
                                                  +---> Excel Formatter ---> Excel File Writer
                                                  +---> CSV Formatter   ---> CSV File Writer

---

## Snaps

### 1. HTTP Client (Postal Code API)
Sends a GET request to the Zippopotam API using the pipeline parameter postcode to retrieve location data. The endpoint is constructed dynamically from the postcode value. Extracts the JSON response entity for downstream processing.

### 2. JSON Splitter (Places Array)
Splits the Zippopotam API response by iterating over the places array in the response body, producing one document per place entry so each location can be processed individually.

### 3. Mapper (MapFromJsonToVar)
Maps fields from the place entry to simplified variable names. Extracts latitude, longitude, city name, state name, and state abbreviation from the place document and maps them to flat output fields for use in the next API call.

### 4. HTTP Client (Open-Meteo Weather API)
Sends a GET request to the Open-Meteo forecast API using the latitude and longitude values extracted in the previous step. Requests hourly temperature data in Fahrenheit. The query parameters for latitude, longitude, hourly field, and temperature unit are set dynamically from the mapped document fields.

### 5. Mapper (Hour and Temperature)
Transforms the hourly forecast response by zipping the time array and the temperature array into an array of objects. Each object contains an Hour field and a Temperature field. The resulting array is stored under the rows key in the output document.

### 6. JSON Splitter (Flatten Rows)
Splits the rows array into individual documents, producing one document per hourly weather record. Each output document contains a single Hour and Temperature pair.

### 7. Copy
Duplicates the stream of hourly weather records, routing data to both Segment 1 and Segment 2 simultaneously. This allows the same data to be written to both Excel and CSV formats without duplicating upstream processing.

### 8. Excel Formatter
Formats the incoming hourly weather data into an Excel workbook. The worksheet is named Weather Data. Receives data from Segment 1 of the Copy snap.

### 9. Excel File Writer
Writes the formatted Excel workbook to a file. The file name is constructed dynamically using the postcode pipeline parameter, resulting in a file named weather_output_postcode.xlsx. Overwrite mode is enabled, so re-running the pipeline replaces any existing file.

### 10. CSV Formatter
Formats the incoming hourly weather data as a CSV file. Uses comma as the delimiter, double-quote as the quote character, minimal quoting mode, UTF-8 encoding, and LF newline characters. Receives data from Segment 2 of the Copy snap.

### 11. CSV File Writer
Writes the formatted CSV data to a file. The file name is constructed dynamically using the postcode pipeline parameter, resulting in a file named weather_output_postcode.csv. Overwrite mode is enabled, so re-running the pipeline replaces any existing file.

---

## Notes

- The pipeline uses the postcode pipeline parameter to dynamically construct API request URLs and output file names.
- The Zippopotam API is a free postal code lookup service that returns geographic and place information for a given postal code.
- The Open-Meteo API is a free weather forecast service that provides hourly temperature data based on latitude and longitude coordinates.
- The Copy snap enables parallel output to both Excel and CSV formats without duplicating any upstream processing steps.
- Both output files are written with overwrite mode enabled, so re-running the pipeline will replace any existing output files.
- Temperature values are returned in Fahrenheit as specified in the Weather API query parameters.
- The pipeline has no authentication requirements; both the Zippopotam and Open-Meteo APIs are publicly accessible without API keys.
"
