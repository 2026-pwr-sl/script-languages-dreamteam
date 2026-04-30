import pytest

from lab7 import *

def test_typeerror():
    with pytest.raises(TypeError):
        reqstr2obj(12345)

    with pytest.raises(TypeError):
        reqstr2obj(["GET","/","HTTP/1.1"])

    with pytest.raises(TypeError):
            reqstr2obj(None)        


def test_returns():
    result = reqstr2obj("GET / HTTP1.1")

    assert isinstance(result, HTTPRequest)



def test_specreturn():
    result = reqstr2obj("GET / HTTP1.1")

    assert result.method == "GET"
    assert result.path == "/"
    assert result.version == "HTTP1.1"


def test_checkreturns():
    result = reqstr2obj("GET /index.html HTTP1.1")

    assert result.method == "GET"
    assert result.path == "/index.html"
    assert result.version == "HTTP1.1"

    result2 = reqstr2obj("POST /api/login HTTP1.0")
     
    assert result2.method == "POST"
    assert result2.path == "/api/login"
    assert result2.version == "HTTP1.0"

    result3 = reqstr2obj("DELETE /users/123 HTTP2.0")
    
    assert result3.method == "DELETE"
    assert result3.path == "/users/123"
    assert result3.version == "HTTP2.0"

def test_returnnone():
    result = reqstr2obj("GET /")
    assert result is None

    result2 = reqstr2obj("GET  /  HTTP2.0")
    assert result2 is None

    result3 = reqstr2obj("GET  / HTTP1.0")
    assert result3 is None

def test_illegal():
     
    with pytest.raises(BadRequestTypeError):
        reqstr2obj("DOWNLOAD /movie.mp4 HTTP1.1")

def test_versions():
    with pytest.raises(BadHTTPVersion):
        reqstr2obj("GET /asdasd HTTP6")

def test_path():
    with pytest.raises(ValueError):
        reqstr2obj("GET asdasd HTTP1.1")