# Prometheus 客户端
# 作者 charis
# 时间 2023-1-10

from prometheus_client import Counter,Gauge,push_to_gateway
from prometheus_client.core import CollectorRegistry

class Prometheus():

    # put 一个任务
    def putPrometheus(self, ipPort, jobs, path):
        registry = CollectorRegistry()
        data1 = Gauge('gauge_test_metric', 'This is a gauge-test-metric', ['method', 'path', 'instance'],
                      registry=registry)
        data1.labels(method='get', path=path, instance='instance1').inc(3)
        push_to_gateway(ipPort, job=jobs, registry=registry)


if __name__ == '__main__':
    p = Prometheus()
    p.putPrometheus("漏洞地址", "test01", "/test01")