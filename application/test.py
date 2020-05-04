# python -m application.test

import unittest
from flask_testing import TestCase

try:
    from application import create_app, db
    import unittest
except Exception as e:
    print("Some Modules are missing {} ".format(e))


class BubbleTest(unittest.TestCase):
    # Check for response 200
    def test_index(self):
        app = create_app()
        tester = app.test_client(self)
        response = tester.get("/db/bubbles")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    # Check if content return is application/json
    def test_index_content(self):
        app = create_app()
        tester = app.test_client(self)
        response = tester.get("/db/bubbles")
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')


class HeatmapTest(unittest.TestCase):
    # Check if content return is application/json
    def test_index_content(self):
        app = create_app()
        tester = app.test_client(self)
        response = tester.get("/db/heatmap")
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')


class RacechartTest(unittest.TestCase):
    # Check if content return is application/json
    def test_index_content(self):
        app = create_app()
        tester = app.test_client(self)
        response = tester.get("/db/racechart")
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')


if __name__ == '__main__':
    unittest.main()
