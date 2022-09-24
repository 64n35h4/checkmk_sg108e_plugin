from .agent_based_api.v1 import *

def check_tp_link(item, section):
    for port, status, link, TxGoodPkt, TxBadPkt, RxGoodPkt, RxBadPkt in section:
        if item == port:
            yield Metric("TxGoodPkt", int(TxGoodPkt))
            yield Metric("TxBadPkt", int(TxBadPkt))
            yield Metric("RxGoodPkt", int(RxGoodPkt))
            yield Metric("RxBadPkt", int(RxBadPkt))
            yield Result(state=State.OK, summary=f"Status: {status}, Link: {link}, Stats: [{TxGoodPkt}, {TxBadPkt}, {RxGoodPkt}, {RxBadPkt}]")
            return

def discover_tp_link(section):
    for port, status, link, TxGoodPkt, TxBadPkt, RxGoodPkt, RxBadPkt in section:
        yield Service(item=port)

register.check_plugin(
    name="tp_link",
    service_name="Port %s",
    discovery_function=discover_tp_link,
    check_function=check_tp_link,
)
