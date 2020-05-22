# run tests: python -m application.test
# Hoping to implement pytest stuff soon 5/20/20
from flask_testing import TestCase

try:
    from application import create_app, db
    import unittest
except Exception as e:
    print("Some Modules are missing {} ".format(e))


class BubbleTest(unittest.TestCase):
    '''Testing the summary table used for the bubbles visualization'''

    def test_index(self):
        # Check for response 200
        app = create_app()
        tester = app.test_client(self)
        response = tester.get("/db/bubbles")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_index_content(self):
        # Check if content return is application/json
        app = create_app()
        tester = app.test_client(self)
        response = tester.get("/db/bubbles")
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')


class HeatmapTest(unittest.TestCase):
    '''Testing the uscounties table used for the heatmap visualization'''

    def test_index_content(self):
        # Check if content return is application/json
        app = create_app()
        tester = app.test_client(self)
        response = tester.get("/db/heatmap")
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')


class RacechartTest(unittest.TestCase):
    '''Testing the covidall table used for the racechart visualization'''

    def test_index_content(self):
        # Check if content return is application/json
        app = create_app()
        tester = app.test_client(self)
        response = tester.get("/db/racechart")
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')


if __name__ == '__main__':
    unittest.main()
