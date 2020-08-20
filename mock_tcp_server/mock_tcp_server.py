"""
    An example of usage::

        def test_timeout(self):
            answer = 'HTTP/1.1 200 OK\n\nHello World!'
            with MockTcpServer(response_delay=2, response_data=answer) as srv:
                mock_url = 'http://{}:{}/'.format(srv.host, srv.port)
                request_ts = time.time()
                self.assertRaises(
                    TimeoutError,
                    make_request,  # some function that makes HTTP request
                    url=mock_url,
                    timeout=1
                )
                self.assertAlmostEqual(time.time()-request_ts, 1, delta=0.1)
"""

import socketserver
import threading
from time import sleep
import time

# from gevent.tests.test__refcount import make_request


class HTTPHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server,
                 response_delay=0, response_data='HTTP/1.1 200 OK\n\n'):
        self.response_delay = response_delay
        self.response_data = response_data

        socketserver.BaseRequestHandler.__init__(
            self, request, client_address, server
        )

    def handle(self):
        self.data = self.request.recv(8192).strip()
        sleep(self.response_delay)
        self.request.sendall(self.response_data)


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


class MockTcpServer(object):
    def __init__(self, handler_class=HTTPHandler,
                 host='localhost', port=8080,
                 response_delay=None, response_data=None):
        self.host = host
        self.port = port
        self.handler_class = handler_class
        self.response_delay = response_delay
        self.response_data = response_data
        self.server = None

    def start(self):
        if self.server:
            self.stop()

        self.server = ReusableTCPServer(
            (self.host, self.port),
            _handler_factory(self.handler_class,
                             response_delay=self.response_delay,
                             response_data=self.response_data))
        httpd_thread = threading.Thread(target=self.server.serve_forever)
        httpd_thread.setDaemon(True)
        httpd_thread.start()

    def stop(self):
        if not self.server:
            return
        self.server.shutdown()
        self.server.server_close()
        self.server = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()


def _handler_factory(handler_class, *args, **kwargs):
    # skip overwriting uninitialized named arguments
    kwargs = {k:v for k, v in kwargs.iteritems() if v is not None}
    def handler(request, client_address, server):
        handler_class(request, client_address, server, *args, **kwargs)
    return handler

class mock_test:
    def test_timeout(self):
        answer = 'HTTP/1.1 200 OK\n\nHello World!'
        print(answer)
        with MockTcpServer(response_delay=2, response_data=answer) as srv:
            mock_url = 'http://{}:{}/'.format(srv.host, srv.port)
            request_ts = time.time()
            self.assertRaises(
                TimeoutError,
                HTTPHandler,  # some function that makes HTTP request
                url=mock_url,
                timeout=1
                )
            print(self.assertAlmostEqual(time.time()-request_ts, 1, delta=0.1))

if __name__ == '__main__':
    mock_test().test_timeout()


