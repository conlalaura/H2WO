# Documentation

> Authors: Alex Leccadito, Laura Conti

## Context

This is the semester project for the PM3 module at ZHAW.
The task was to implement a webserver.

## Goal

The goal of this project is to enable people to discover enjoyable, free places around them with essential amenities
like water fountains, benches, and public restrooms. Leveraging OpenStreetMaps, it highlights locations ideal for
relaxing, socializing, or spending a day outdoors—all without any cost.

## Project Organisation

### Project Roles

| Role          | Name           |
|---------------|----------------|
| Product Owner | Alex Leccadito |
| Scrum Master  | Laura Conti    |
| Team Member   | Alex Leccadito |
| Team Member   | Laura Conti    |

### Project Tasks

| Task                 | Responsible    |
|----------------------|----------------|
| mongoDB Setup        | Laura Conti    | 
| mongoDB Queries      | Laura Conti    |
| Webserver Routes     | Laura Conti    | 
| UI/UX Design         | Alex Leccadito | 
| UI/UX Implementation | Alex Leccadito | 
| Map Service          | Alex Leccadito | 
| Amenity Clustering   | Alex Leccadito |
| Chart/Statistic      | Laura Conti    | 
| Clean Code           | Everyone       | 
| Code Testing         | Laura Conti    | 
| Inline Documentation | Everyone       | 
| Documentation        | Laura Conti    | 
| Project Presentation | Everyone       | 

## System Overview

```
├── data/
│   ├── __init__.py
│   ├── dummy_document.json   # For pytest
│   ├── mongodb_loader.py     # Loads data from OSM DB, creates smaller project DB, and inserts dummy reviews
│   └── osm-output.json       # OSM data provided by lecturer
├── lib/
│   └── Review.py             # Dataclass for reviews
├── static/
│   ├── css/                  # Styling sheets for pages
│   │   ├── global.css
│   │   ├── home.css
│   │   ├── map.css
│   │   └── statistics.css
│   ├── fonts/
│   │   └── *.tff
│   ├── img/
│   │   ├── *.png
│   │   ├── *.svg
│   │   └── *.jpg
│   └── js/
│       ├── map.js
│       └── statistics.js
├── templates/
│   ├── home.html
│   ├── map.html
│   └── statistics.html
├── tests/
│   ├── test_models.py
│   ├── test_pymongo_loader.py
│   └── test_Review.py
├── Documentation.md
├── main.py
├── README.py
├── requirements.txt
└── routes.py
```



| Code Block             | Functionality                                                                                                                                                                                                                                                                                      |
|------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| data/mongodb_loader.py | This script sets up the mongoDB collections used for this project. It queries the given json and selects project relevant amenities, providing a smaller and faster collection for the project. Further, it adds dummy reviews to the project collection to be used for the project demonstration. |
| lib/Review.py          | The Review dataclass serves as the foundational blueprint for reviews, making it easier in the process to adhere to datatypes.                                                                                                                                                                     |
| static/css/*.css       | The css styling for all html pages. `global.css` is used in all html pages additionally to page-specific styling sheets.                                                                                                                                                                           |
| static/js/*.js         | JavaScript functionalities for map and statistics pages.                                                                                                                                                                                                                                           |
| templates/*.html       | The html layouts for all pages.                                                                                                                                                                                                                                                                    |
| models.py              | mongoDB query functions used in routes.                                                                                                                                                                                                                                                            |
| routes.py              | Flask server with all the webserver routes including three API's.                                                                                                                                                                                                                                  |

## API

### /api/amenities/<amenity_type>

This endpoint retrieves amenities from the database based on the specified amenity type. It supports querying all
project-relevant amenities or filtering by a specific type.

#### HTTP Methods

`GET`: Retrieves all documents for the specified amenity.

#### Example Response

```
[
    {
        "amenity": "fountain",
        "drinking_water": "no",
        "id": "60018172",
        "lat": 46.2073807,
        "lon": 6.1558891,
        "name": "Jet d'eau"
    },
    {
        "amenity": "fountain",
        "id": "60474582",
        "lat": 47.4253117,
        "lon": 9.3782856,
        "name": "Zofinger-Brunnen"
    }
]
```

### API Endpoint: /api/review/<amenity_id>

This endpoint enables users to interact with reviews for a specific amenity.

#### HTTP Methods

`GET`: Retrieves all reviews for the specified amenity.

`POST`: Submits a new review for the specified amenity.

#### Example Response

```
[
    {
        "username": "john_doe",
        "rating": 5,
        "comment": "Clean and well-maintained."
    },
    {
        "username": "jane_smith",
        "rating": 4,
        "comment": "Good location but can be crowded."
    }
]

```

### API Endpoint: /api/toilet_statistics_data

This endpoint retrieves statistical data about toilet amenities from the database. The data includes aggregated
information for toilet properties such as gender accessibility etc. in percentages.

#### HTTP Methods

`GET`: Retrieves statistical values needed for plotting.

#### Example Response

```
[
    {
        "_id": null,
        "fields": {
            "key": "wheelchair",
            "no": 12,
            "yes": 26
        }
    },
    {
        "_id": null,
        "fields": {
            "key": "unisex",
            "no": 3,
            "yes": 30
        }
    }
]
```

### API Endpoint: /api/sparsity_statistics_data

This endpoint provides statistical insights into the key sparsity of amenities. For each amenity type with specific
keys, it returns a single percentage value indicating the average presence of the expected keys.

#### HTTP Methods

`GET`: Retrieves statistical values needed for plotting.

#### Example Response

```
[
    {
        "fountain": 50
    },
    {
        "drinking_water": 13
    }
]
```

## Retrospective

### Task Allocation

One of the highlights of this project was the ease with which tasks were divided among team members. The division of
responsibilities felt natural and synergistic, allowing everyone to focus on tasks they genuinely enjoyed. This approach
not only boosted individual motivation but also contributed to a highly collaborative and productive team dynamic.

### Meetings and Communication

While the team was consistently active and engaged in the project, we only began holding designated meetings later in
the process. At the start, the independent nature of the work allowed us to operate without regular check-ins, and we
managed to navigate this phase successfully. However, this ad-hoc approach could have led to issues if circumstances had
been less favorable. Moving forward, scheduling regular meetings from the beginning will be a priority to ensure
structured communication and coordination.

### Kanban Board

A Kanban board was introduced in the later stages of the project, and it proved to be a valuable tool for tracking tasks
and assigning responsibilities. In hindsight, implementing the board earlier would have provided greater clarity and
organization throughout the project’s lifecycle. This is a key learning for future projects, as an early introduction of
a task management system can help streamline workflow and improve accountability.

## Outlook

The statistics revealed that restroom as well as other amenities' tags are often sparse. To address this, a valuable
feature would allow users to
request updates or additions to amenity tags (e.g., marking a restroom as "gender-neutral" or "wheelchair accessible").
This functionality would enrich the information available for amenities, making the service more useful, enhancing
accuracy, and fostering inclusivity for all users.
Enhancements to the frontend would introduce a **Tag Update Form** for users to propose changes and a **Request Status
Viewer** to track submitted requests.

On the backend, the Flask server would require additional endpoints:

- **POST /request-tag-update**: To accept user requests with the amenity ID and suggested tags.
- **GET /tag-requests**: To fetch pending requests (accessible only to admins).
- **PATCH /tag-update/:id**: To approve or reject tag update requests.

The database would also need to support logging user requests and their statuses. This functionality could be integrated
as an additional parameter within the `Review` dataclass, ensuring a streamlined workflow for tracking and managing
requests.

