
class Request:
    def __init__(self, ip=None, request_headers:dict=dict, form:dict=dict, resp_headers:dict=dict, status_code=200, method="GET", cookies:dict=dict, after_req=False):
        self.client_ip = ip
        self.request_headers = request_headers
        self.respone_headers = resp_headers
        self.form = form
        self.status_code = status_code
        self.after_req = after_req
        self.method = method
        self.cookies = cookies

        if after_req:
            self.set_cookie = None
            self.delete_cookie = None

    def set_cookie(self, name, value, expires=None):
        if expires is None:
            self.respone_headers['Set-Cookie'] = f"{name}={value}; HttpOnly;"
        else:
            self.respone_headers['Set-Cookie'] = f"{name}={value}; HttpOnly; Max-Age={expires}"

    def delete_cookie(self, name):
        self.respone_headers['Set-Cookie'] = f"{name}=delete; HttpOnly; Max-Age=0"
