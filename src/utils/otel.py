import os

ENABLE_OTEL = os.getenv('ENABLE_OTEL', '0') == '1'

if ENABLE_OTEL:
    try:
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
    except Exception:
        ENABLE_OTEL = False
        meter = None
else:
    meter = None


# No-op metric classes
class NoOpCounter:
    def add(self, amount, *args, **kwargs):
        pass


class NoOpHistogram:
    def record(self, value, *args, **kwargs):
        pass


class NoOpMeter:
    def create_counter(self, *args, **kwargs):
        return NoOpCounter()

    def create_histogram(self, *args, **kwargs):
        return NoOpHistogram()


def get_meter():
    if meter is not None:
        return meter
    return NoOpMeter()
