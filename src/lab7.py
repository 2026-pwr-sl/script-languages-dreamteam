class HTTPRequest:
    def __init__(self, method, path, version):
        self.method = method
        self.path = path
        self.version = version

    def __str__(self):
        return f"{self.method} {self.path} {self.version}"


class BadRequestTypeError(Exception):
    """Raised when an HTTP request type is not recognized"""
    pass


class BadHTTPVersion(Exception):
    """Raised when an HTTP request version is not recognized"""
    pass


def reqstr2obj(request_string: str) -> HTTPRequest:
    """Converts a HTTP request string to an HTTPRequest object."""
    if type(request_string) is not str:
        raise TypeError("Input must be a string")

    lines = request_string.strip().splitlines()

    request_line = lines[0]

    parts = request_line.split(" ")

    if len(parts) != 3:
        return None

    method, path, version = parts

    allowed_methods = [
        "GET", "POST", "PUT", "DELETE", "PATCH",
        "OPTIONS", "HEAD", "TRACE", "CONNECT"
    ]

    if method not in allowed_methods:
        raise BadRequestTypeError(f"Illegal request type: {method}")

    allowed_versions = ["HTTP1.0", "HTTP1.1", "HTTP2.0"]

    if version not in allowed_versions:
        raise BadHTTPVersion(f"Unknown version: {version}")

    if path[0] != "/":
        raise ValueError

    return HTTPRequest(method=method, path=path, version=version)
