import sys
import xml.etree.ElementTree as ET

report_path = sys.argv[1]

tree = ET.parse(report_path)
root = tree.getroot()

if root.tag == "testsuites":
    suite = root.find("testsuite")
else:
    suite = root

name = suite.attrib.get("name")
errors = int(suite.attrib.get("errors"))
failures = int(suite.attrib.get("failures"))
skipped = int(suite.attrib.get("skipped"))
tests = int(suite.attrib.get("tests"))
time = float(suite.attrib.get("time"))
passed = tests - errors - failures- skipped

"""
print(f"Tests: {tests}")
print(f"Skipped: {skipped}")
print(f"Error: {errors}")
print(f"Failed: {failures}")
print(f"Passed: {passed}")
print(f"Time (s): {time}")
"""