import unittest

from audit_drawio_edges import cross, segments


class CrossingTests(unittest.TestCase):
    def test_budget_forecast_old_routes_cross(self):
        budget = segments([(440, 505), (440, 1400), (570, 1400), (570, 1625)])
        forecast = segments([(460, 525), (460, 1420), (550, 1420), (550, 1905)])
        self.assertIn((460, 1400), [cross(a, b) for a in budget for b in forecast])

    def test_swapped_trunks_do_not_cross(self):
        budget = segments([(460, 505), (460, 1400), (570, 1400), (570, 1625)])
        forecast = segments([(440, 525), (440, 1420), (550, 1420), (550, 1905)])
        self.assertFalse(any(cross(a, b) for a in budget for b in forecast))

    def test_shared_endpoint_is_not_crossing(self):
        self.assertIsNone(cross(((0, 10), (20, 10)), ((20, 0), (20, 20))))


if __name__ == "__main__":
    unittest.main()
