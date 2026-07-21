import sys
import os
import xml.etree.ElementTree as ET

from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
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

header_value = os.environ["OTEL_EXPORTER_OTLP_HEADERS"]

exporter = OTLPMetricExporter(
    endpoint=os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"],
    headers={
        "Authorization": os.environ["OTEL_EXPORTER_OTLP_HEADERS"].strip()
    },
)

reader = PeriodicExportingMetricReader(
    exporter
)

provider = MeterProvider(
    metric_readers=[reader]
)

metrics.set_meter_provider(provider)
meter = metrics.get_meter("pytest")

test_counter = meter.create_counter("pytest.tests", description="Number of tests by result")
test_counter.add(
    passed,
    {
        "status": "passed"
    }
)

test_counter.add(
    failures,
    {
        "status": "failed"
    }
)

test_counter.add(
    errors,
    {
        "status": "errors"
    }
)

test_counter.add(
    skipped,
    {
        "status": "skipped"
    }
)

attributes = {
    "repository": os.getenv("GITHUB_REPOSITORY"),
    "branch": os.getenv("GITHUB_REF_NAME"),
    "commit": os.getenv("GITHUB_SHA", "")[:7],
    "workflow": os.getenv("GITHUB_WORKFLOW"),
}


test_counter.add(
    passed,
    {
        **attributes,
        "status": "passed"
    }
)

provider.force_flush()
provider.shutdown()