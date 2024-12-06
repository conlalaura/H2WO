# Documentation

> Authors: Alex Leccadito, Laura Conti

## Context

This is the semester project for the PM3 module at ZHAW.
The task was to implement a webserver.

## Goal

TODO

## Project Organisation

### Project Roles

| Role          | Name           |
|---------------|----------------|
| Product Owner | Alex Leccadito |
| Scrum Master  | Laura Conti    |
| Team Member   | Alex Leccadito |
| Team Member   | Laura Conti    |

### Project Tasks

TODO: add more granularity to alex's tasks

| Task                 | Responsible    |
|----------------------|----------------|
| mongoDB Setup        | Laura Conti    | 
| mongoDB Queries      | Laura Conti    |
| Webserver Routes     | Laura Conti    | 
| GUI                  | Alex Leccadito | 
| Map Service          | Alex Leccadito | 
| Chart/Statistic      | Laura Conti    | 
| Clean Code           | Everyone       | 
| Code Testing         | Laura Conti    | 
| Inline Documentation | Everyone       | 
| Documentation        | Laura Conti    | 
| Project Presentation | Everyone       | 

## System Overview

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

## Testing

TODO

## Retrospective

TODO

## Outlook
The statistics revealed that restroom tags are often sparse. To address this, a valuable feature would allow users to request updates or additions to amenity tags (e.g., marking a restroom as "gender-neutral" or "wheelchair accessible"). This functionality would enrich the information available for amenities, making the service more useful, enhancing accuracy, and fostering inclusivity for all users.
Enhancements to the frontend would introduce a **Tag Update Form** for users to propose changes and a **Request Status
Viewer** to track submitted requests.

On the backend, the Flask server would require additional endpoints:

- **POST /request-tag-update**: To accept user requests with the amenity ID and suggested tags.
- **GET /tag-requests**: To fetch pending requests (accessible only to admins).
- **PATCH /tag-update/:id**: To approve or reject tag update requests.

The database would also need to support logging user requests and their statuses. This functionality could be integrated
as an additional parameter within the `Review` dataclass, ensuring a streamlined workflow for tracking and managing
requests.

## Attachment

TODO
