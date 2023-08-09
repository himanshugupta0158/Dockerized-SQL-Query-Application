import shapefile # pip install pyshp
import json

def shp_shx_data_extraction(shp_file_path, shx_file_path):

    sf = shapefile.Reader(shp_file_path, shx=shx_file_path)

    print(sf)

    # Get the shapes (geometry) and records (attributes)
    shapes = sf.shapes()
    records = sf.records()

    # Get the field names from the shapefile
    field_names = [field[0] for field in sf.fields[1:]]

    # Create a list to store the features (geometry + attributes)
    features = []

    # Loop through shapes and records
    for i in range(len(shapes)):
        shape = shapes[i]
        record = records[i]
        
        # Convert shape and record to dictionary
        feature = {
            "type": "Feature",
            "geometry": shape.__geo_interface__,
            "properties": {}
        }
        
        # Populate properties
        for field, value in zip(field_names, record):
            feature["properties"][field] = value
        
        features.append(feature)

    # Create the GeoJSON structure
    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }

    # Close the .shp file
    sf.close()

    return geojson_data

