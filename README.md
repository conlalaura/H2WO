# H2WO Webservice

This project helps people find nice, free places to hang out in their city that have useful amenities like water fountains, benches, and public restrooms. By using open data and maps, it shows spots that are great for relaxing, meeting friends, or enjoying a day outside without spending money.

## Setup

### Install Dependencies

From the project root directory run:

```bash
pip install -r requirements.txt
```

### Load Database in MongoDB
This project requires the osm-output.json file to be imported into MongoDB under the database name osm and the collection name osm. If this has not been done yet, follow the steps below:

1. Install MongoDB:
   - Follow the installation [instructions](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-windows/).
2. Ensure the JSON file is in the correct location:
    - Copy the osm-output.json file into the data folder. Note that this file is ignored by .gitignore due to its size.
3. Run the import script:
    - Use the following script to import the data into MongoDB:

```
python data/mongodb_loader.py
```

This script loads the osm-output.json file into MongoDB, filters the relevant amenities and keys, and stores the results in a new, more compact collection for efficient caching.

## Development

### Run Code Formatter

From the project root directory run:

```
python -m black .
```
