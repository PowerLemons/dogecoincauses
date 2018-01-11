# dogecoincauses

Backend service for the Dogecoin causes project. It enables a series of REST endpoints that process and return data related to the causes previously loaded in the database. These endpoints will be used as the only way of connecting and querying the data layer.

### Technology

The following technologies have been used to implement the service:

* [Python 3.4](https://www.python.org/) - programming language
* [MongoDB 3.4](https://www.mongodb.com/) - NoSQL database

### Installation

The application is at the moment conceived to run in a single node along with a MongoDB instance. This instance is intended to allow local connections and should have a collection called "dogecoin-causes" created.

The dependencies are stored into the file called "requirements.txt". To install from it with PIP:

```
pip install -r requirements.txt
```

### Running

To load the "dummy" causes data in the database run the script "create_causes.py" and to run a Flask instance execute the script called "application.py".

To request the resource open the URL "http://127.0.0.1:5000/causes" in a web browser or run the command:

```
curl -X GET "http://127.0.0.1:5000/causes"
```

This command will return a JSON object with a key containing the array of causes stored in the database.

### Developing

For development is recommended the creation of a Python virtual environment. The project would be then installed inside this virtual environment.

### Structure

No modules created for the time being. The folder "settings" contains a file that stores the MongoDB configuration variables. In Production these variables will be loaded by means of environment variables.

### Endpoints

** Causes **

----

Returns a list of causes stored in MongoDB.

* **URL**

  /causes

* **Method**
  
  `GET`

* **URL parameters**

  **Required**
 
  `filter = String [ all | money (from = Numeric, to = Numeric) | cause_id (id = [String]) | country_id (code = [String]) ]`

  **Optional**
 
  `None`

* **Success response**
  
  * **Code:** 200<br />
    **Content:** `{causes : [{}]}`
 
* **Error response:**

  * **Code:** 200<br />
    **Content:** `{error: [ wrong_money_filter_params | no_country_codes | no_cause_ids | wrong_filter | no_filter ]}`

* **Sample Call**

  /causes?filter=country&code=es&code=nl

### Database

The service connects to a MongoDB instance.

### Deployment

Reserved for Production instructions.

### Notes

None
