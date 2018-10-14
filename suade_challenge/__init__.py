from flask import Flask, render_template, make_response
from datetime import datetime
import pdfkit
from xml.etree.ElementTree import Element, SubElement, tostring
from sqlalchemy import create_engine


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # When using separate test servers, use settings files or environment variables to hold these details.
    if test_config['TESTING']:
        engine = create_engine('postgresql://postgres:password@localhost:5432/suade')
    else:
        # postgres://interview:uo4uu3AeF3@candidate.suade.org:5432/suade  # @todo Can't connect for some reason
        engine = create_engine('postgresql://postgres:password@localhost:5432/suade')

    @app.route('/')
    def information():
        return render_template('index.html')

    @app.route('/reports/<int:report_id>/<string:report_type>', methods=['GET'])
    def reports(report_id, report_type):
        """Controller for getting the report
        The data for report_id  is retrieved from the database and a Report instance created.
        The rendered document is created using the `render` method within a specialised Generator class.
        """
        # Load the report from the database.
        conn = engine.connect()
        # First report record. List of Tuples returned
        lst_report_names = [rec[0] for rec in conn.execute("SELECT organization FROM reports WHERE id={}".format(report_id)) if rec is not None]
        conn.close()
        if not lst_report_names:
            return render_template('404.html'), 404  # return a 404
        # We have a list therefore report exists, now get items
        conn = engine.connect()
        # First report record
        lst_items = []
        gen_item_tuples = (rec for rec in conn.execute("SELECT name, price FROM items WHERE report_id={}".format(report_id)) if rec is not None)
        conn.close()
        for item_tuple in gen_item_tuples:
            lst_items.append({'name': item_tuple[0], 'price': str(item_tuple[1])})
        obj_report = Report(lst_report_names[0], datetime.now(), lst_items)
        # Create the appropriate report and return to user.
        try:
            obj_generator = Generator().factory(report_type, obj_report)
        except Exception as e:
            # @todo Error logging here
            if e.args[1] == 404:
                return page_not_found(e)
            else:
                raise e
        return obj_generator.render()

    @app.errorhandler(404)
    def page_not_found(e):
        """Handle page not found"""
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        """Handle server error"""
        return render_template('500.html'), 500

    return app


class Report(object):
    """
    Report class to validate and hold all report content.
    """
    def __init__(self, org_name, report_date, items):
        """Initialise with all report contents."""
        # Do some type checking
        if not isinstance(org_name, str):
            raise Exception("Invalid Type for Organization")
        self._org_name = org_name
        if not isinstance(report_date, datetime):
            raise Exception("Invalid Type for Report Date")
        self._report_date = report_date
        if not isinstance(items, list):
            raise Exception("Invalid Type for Items")
        self._items = items

    @property
    def org_name(self):
        """Getter for organization name
        :rtype: str
        """
        return self._org_name

    @property
    def report_date(self):
        """Getter for report name
        :rtype: datetime
        """
        return self._report_date

    @property
    def items(self):
        """Gettter for items
        :rtype: list
        """
        return self._items


class Generator(object):
    """
    Class that handles the rendering of the reports.
    """
    def factory(self, gen_type, report):
        """Factory that returns a specialised generator. For instance PDF generator that renders the report content
        in PDF.
        :type: gen_type str
        :type: report Report
        """
        if gen_type == "pdf":
            return PDFReport(report)
        if gen_type == "xml":
            return XMLReport(report)
        if gen_type == "html":
            return HTMLReport(report)
        raise Exception('Report type not found', 404)

    def render(self):
        """This function produces the document output."""
        pass


class PDFReport(Generator):
    """
    PDF specialised version of the report.
    """
    def __init__(self, report):
        """Add report at instantiation
        :type report: Report
        """
        self._report = report

    def render(self):
        """Generate PDF report"""
        # Define template dictionary.
        report_detail = {
            'org_name': self._report.org_name,
            'report_date': self._report.report_date.strftime("%Y/%m/%d"),
            'render_timestamp': datetime.now().strftime("%Y/%m/%d %X"),
            'inventory': self._report.items
        }
        # Render HTML template to be converted to PDF
        rendered = render_template('report.html', **report_detail)
        # Define PDF options
        options = {
            '--encoding': "utf-8",
        }
        # Generate PDF
        pdf = pdfkit.from_string(
            rendered,
            False,
            # css=lst_css,
            options=options
        )
        # Create response
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=risk_assessment.pdf'
        # Return generated PDF
        return response


class XMLReport(Generator):
    """
    XML specialised version of the report.
    """
    def __init__(self, report):
        """Add report at instantiation
        :type report: Report
        """
        self._report = report

    def render(self):
        """Generate XML report"""
        xml = Element('report')
        org = SubElement(xml, 'organization')
        org.text = self._report.org_name
        reported = SubElement(xml, 'reported')
        reported.text = self._report.report_date.strftime("%Y/%m/%d")
        created = SubElement(xml, 'created')
        created.text = self._report.report_date.now().strftime("%Y/%m/%d %X")
        items = SubElement(xml, 'items')
        for this_item in self._report.items:
            item = SubElement(items, 'item')
            item_name = SubElement(item, 'name')
            item_name.text = this_item['name']
            item_price = SubElement(item, 'price')
            item_price.text = this_item['price']
        # Create response
        response = make_response(tostring(xml))
        response.headers['Content-Type'] = 'text/xml'
        # Return generated XML
        return response


class HTMLReport(Generator):
    """
    HTML specialised version of the report.
    """
    def __init__(self, report):
        """Add report at instantiation
        :type report: Report
        """
        self._report = report

    def render(self):
        """Generate HTML report"""
        # Define template dictionary.
        report_detail = {
            'org_name': self._report.org_name,
            'report_date': self._report.report_date.strftime("%Y/%m/%d"),
            'render_timestamp': datetime.now().strftime("%Y/%m/%d %X"),
            'inventory': self._report.items
        }
        # Render the template and return
        return render_template('report.html', **report_detail)
