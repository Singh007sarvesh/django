# API

## Creating company profile

## REQUEST:

### HTTP POST api/companies

````
INPUT
{
    "Details":[
    {
        "id": 1,
        "name": "abc",
        "location": "xyz",
        "url": "http://abc.com",
        "description" : "abc",
        "logo":[
        {
            "id": 3
            "name": "abc"
            "type": "jpj"
            "path": "xyz"
        }
        ],

    }
    ]

}
````
## RESPONSE

````
OUTPUT
{
    "response":201
}
````

## List of job for all users

## REQUEST:

### HTTP GET api/job-postings

````
RESPONSE
{
    "jobs":[
    {
        "job_id" : 1,
        "name" : "Software Developer":,
        "description" : "python/java/c++",
        "vacancy" : 2,
        "company" : [
        {
            "id": 1,
            "name": "xyz",
            "location": "abc",
            "url": "http://xyz.com"
        }
        ],
        "status" : "initial/waiting_for_approval/hold/expired/posted",
    },
    "has many" : True
    ]
}

````

### List of job pending for approval

## REQUEST:

### HTTP GET api/job-postings

````
RESPONSE
{
    "jobs":[
    {
        "job_id" : 1,
        "name" : "Software Developer":,
        "description" : "python/java/c++/REST API",
        "vacancy" : 3,
        "company" : [
        {
            "id": 2,
            "name": "pqr",
            "location": "Bangalore",
            "url": "http://pqr.com"
        }
        ]
        "status" : "initial"
    },
    "has many" : True
    ]
}

````

## REQUEST

### HTTP PUT/PATCH

````
INPUT
{
    "jobs":[
    {
        "job_id" : 1,
        "name" : "Software Developer":,
        "description" : "python/java/c++/REST API",
        "vacancy" : 3,
        "company" : [
        {
            "id": 2,
            "name": "pqr",
            "location": "Bangalore",
            "url": "http://pqr.com"
        }
        ]
        "status" : "approved"
    }
    ]
}

````