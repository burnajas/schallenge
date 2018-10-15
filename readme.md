**Suade Interview Task - Report Exporting Service**

This service takes an abstract report and returns either a PDF document or an XML file determined by user request parameters.

The service provides a RESTful API with the following endpoint:

`/reports/<int:report_id>/<string:type>`

`report_id` is the unique report id.

`type` represents the report return type; PDF or XML

Therefore a request to return PDF version of report_id 1 would be:

`/resports/1/pdf`

The test database runs locally and can be created using `docker-compose`.

Assuming docker-compose is installed run the following command to activate this test service:

`docker-compose up -d`

This report exporting service runs on Python3.6. The `requirements.txt` file contains project dependencies.

To run the service (Windows):

`set FLASK_APP=suade_challenge`

`set FLASK_ENV=development`

`flask run`