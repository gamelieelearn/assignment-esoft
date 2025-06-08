from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.metrics import get_meter_provider, set_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

# Only set MeterProvider if not already set
if not isinstance(get_meter_provider(), MeterProvider):
    exporter = OTLPMetricExporter()
    reader = PeriodicExportingMetricReader(exporter)
    meter_provider = MeterProvider(metric_readers=[reader])
    set_meter_provider(meter_provider)
    meter = meter_provider.get_meter('assignment-esoft.inference_service')
else:
    meter = get_meter_provider().get_meter('assignment-esoft.inference_service')


def get_meter():
    return meter
