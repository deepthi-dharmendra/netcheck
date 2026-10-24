
import re
import unittest


def parse_windows_times(output):
    pattern = r"time([=<])\s*(\d+(?:\.\d+)?)\s*ms"
    matches = re.findall(pattern, output)

    times = []
    for operator, value in matches:
        measured_time = float(value)

        if operator == "=":
            times.append(measured_time)
        elif operator == "<" and measured_time == 1:
            # Estimate only; the exact time is below 1 ms.
            times.append(0.5)

    return times


class TestWindowsPingParser(unittest.TestCase):
    def test_whole_number(self):
        self.assertEqual(
            parse_windows_times("Reply from 8.8.8.8: time=12ms"),
            [12.0],
        )

    def test_fractional_time(self):
        self.assertEqual(
            parse_windows_times("Reply from 8.8.8.8: time=12.7ms"),
            [12.7],
        )

    def test_under_one_millisecond(self):
        self.assertEqual(
            parse_windows_times("Reply from 8.8.8.8: time<1ms"),
            [0.5],
        )


if __name__ == "__main__":
    unittest.main()
