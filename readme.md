**Suade Interview Task - Report Exporting Service**

This service takes an abstract report and returns either a PDF document or an XML file determined by user request parameters.

The service provides a RESTful API with the following endpoint:

`/report/<int:report_id>/<string:type>`

`report_id` is the unique report id.

`type` represents the report return type; PDF or XML

The service is available as a Docker container. Assuming Docker is installed run the following command to activate the service:

@todo

 