import sys
import os
import xml.etree.ElementTree as ET

from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.metrics.export import (
    PeriodicExportingMetricReader
)
from opentelemetry.exporter.otlp.proto.http.metric_exporter import (
    OTLPMetricExporter
)

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

exporter = OTLPMetricExporter(
    endpoint=os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"],
    headers={
        "Authorization": os.environ["OTEL_EXPORTER_OTLP_HEADERS"].strip()
    },
)

reader = PeriodicExportingMetricReader(
    exporter
)

resource = Resource.create(
    {
        "service.name": "ros2-validation-ci",
        "service.instance.id": "ros2-validation-ci",
    }
)

provider = MeterProvider(
    resource=resource,
    metric_readers=[reader]
)

metrics.set_meter_provider(provider)
meter = metrics.get_meter("pytest")

pass_gauge = meter.create_gauge(name="pytest_pass_counter", unit="1", description="Number of passed tests")
fail_gauge = meter.create_gauge(name="pytest_fail_counter", unit="1", description="Number of failed tests")
skipped_gauge = meter.create_gauge(name="pytest_skipped_counter", unit="1", description="Number of skipped tests")
time_gauge = meter.create_gauge(name="pytest_time_gague", unit="seconds", description="Time of the test suite")

pass_gauge.set(passed)
fail_gauge.set(failed)
skipped_gauge.set(skipped)
time_gauge.set(time)
provider.force_flush()
provider.shutdown()