import pytest
import os

def log_hook(name, config=None):
    worker = os.environ.get("PYTEST_XDIST_WORKER")
    who = worker if worker else "MASTER"
    msg = f"[{who}] HOOK: {name}"
    if config:
        config._metadata = getattr(config, "_metadata", [])
        config._metadata.append(msg)
    print(msg)

def pytest_addoption(parser):
    log_hook("pytest_addoption")

def pytest_configure(config):
    log_hook("pytest_configure", config)
    if hasattr(config, "workerinput"):
        log_hook("worker detected", config)
    else:
        log_hook("controller config", config)

def pytest_sessionstart(session):
    log_hook("pytest_sessionstart", session.config)

def pytest_collect_file(path, parent):
    log_hook(f"pytest_collect_file -> {path}")
    return None  # Let pytest continue default collection

def pytest_pycollect_makeitem(collector, name, obj):
    log_hook(f"pytest_pycollect_makeitem -> {name}")
    return None  # Let pytest collect normally

def pytest_collection_modifyitems(session, config, items):
    log_hook(f"pytest_collection_modifyitems (total items: {len(items)})", config)

def pytest_runtest_setup(item):
    log_hook(f"pytest_runtest_setup -> {item.name}")

def pytest_runtest_call(item):
    log_hook(f"pytest_runtest_call -> {item.name}")

def pytest_runtest_teardown(item):
    log_hook(f"pytest_runtest_teardown -> {item.name}")

def pytest_runtest_logreport(report):
    log_hook(f"pytest_runtest_logreport -> {report.nodeid} ({report.when})")

def pytest_sessionfinish(session, exitstatus):
    log_hook("pytest_sessionfinish", session.config)

def pytest_unconfigure(config):
    log_hook("pytest_unconfigure", config)

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    log_hook("pytest_terminal_summary", config)
    if hasattr(config, "_metadata"):
        terminalreporter.write_sep("=", "PYTEST HOOK TRACE")
        for msg in config._metadata:
            terminalreporter.write_line(msg)

