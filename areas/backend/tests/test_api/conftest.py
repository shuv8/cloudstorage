import os
import subprocess
import sys
import time
import pytest
import requests
from requests import ConnectionError

from tests.test_api.api_client.client import APIClient

repo_root = os.path.abspath(os.path.join(__file__, os.path.pardir))
app_path = os.path.dirname(__file__).replace('tests\\test_api', 'web_server.py')
app_host = '127.0.0.1'
app_port = '5000'


@pytest.fixture(scope='session')
def api_log_client():
    logs_path = os.path.join(repo_root, 'tmp', 'logs')
    return APIClient(base_url=f'http://{app_host}:{app_port}', log_file=logs_path)


def wait_ready(host, port):
    started = False
    st = time.time()
    while time.time() - st <= 5:
        try:
            requests.get(f'http://{host}:{port}')
            started = True
            break
        except ConnectionError:
            pass
    if not started:
        raise RuntimeError('App didn\'t started in 5s!')


def pytest_configure(config):
    if not hasattr(config, 'workerinput'):
        app_stderr_path = os.path.join(repo_root, 'tmp', 'app_stderr')
        app_stdout_path = os.path.join(repo_root, 'tmp', 'app_stdout')
        app_stderr = open(app_stderr_path, 'w')
        app_stdout = open(app_stdout_path, 'w')
        env = os.environ.copy()
        # env.update({'COVERAGE_PROCESS_START': 'setup.cfg'})
        proc = subprocess.Popen([sys.executable, app_path], env=env,
                                stderr=app_stderr, stdout=app_stdout)
        config.proc = proc
        config.app_stderr = app_stderr
        config.app_stdout = app_stdout
        wait_ready(app_host, app_port)


def pytest_unconfigure(config):
    config.proc.terminate()
    exit_code = config.proc.wait()
    assert exit_code == 1
    config.app_stderr.close()
    config.app_stdout.close()