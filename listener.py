import datetime
import os
from inspect import signature
import traceback
from string import ascii_letters, digits
from urllib.parse import unquote

def get_file(file):
    if os.path.exists("./"+file):
        with open("./"+file, 'rb') as f:
            f_data = f.read()

        return True, f_data
    return False, 0

def listen(self, clientdata, addr, debug):
    from .request_info import Request
    listening = True

    while listening:
        try:
            msg = clientdata.recv(4096).decode('utf-8')
        except ConnectionAbortedError:
            print("Connection broken with:", addr)
            break

        if msg == "":
            continue

        msg = msg.split("\n")
        request_headers = {}
        for i in msg:
            try:
                out = i.strip("\r").split(": ")
                request_headers[out[0]] = out[1]
            except:
                continue


        location = msg[0].split()[1]
        method = msg[0].split()[0]
        response_code = 500
        resp_headers = {}
        form = {}

        if method == "POST":
            msg_clone = msg[:]
            msg_clone.reverse()
            for i in msg_clone:
                if i == '\r':
                    break
                i_split = str(i).split('=')
                form_out = ""
                for i in list(i_split[1]):
                    if i == "+":
                        form_out += " "
                        continue
                    form_out += i

                form[i_split[0]] = unquote(form_out)

        self.before_req()
        if self.routes.get(location) is not None:
            if method not in self.routes[location]['methods']:
                response_code = 405
                if self.handled_errors.get(response_code) is not None:
                    clientdata.send(
                        f'HTTP/1.0 {response_code} Method not allowed'
                        '\n\n'
                        f'{self.handled_errors[response_code]()}'.encode()
                    )
                else:
                    clientdata.send(
                        f'HTTP/1.0 {response_code} Method not allowed'
                        '\n\n'
                        'Method not allowed'.encode()
                    )

            try:
                response_code = 200

                newline = "\n"

                if len(signature(self.routes[location]["func"]).parameters) >= 1:
                    cookies = {}
                    if request_headers.get('Cookie') is not None:
                        for i in request_headers['Cookie'].split("; "):
                            if i == "":
                                continue
                            cookie = i.split("=")
                            cookies[cookie[0]] = cookie[1]

                    req_data = Request(addr, request_headers, resp_headers=resp_headers, status_code=response_code, method=method, form=form, cookies=cookies)
                    func_out = self.routes[location]["func"](req_data)
                    resp_headers = req_data.respone_headers
                    response_code = req_data.status_code
                else:
                    func_out = self.routes[location]["func"]()

                clientdata.send(
                    f'HTTP/1.0 {response_code} OK\n'
                    f'{"".join(f"%s: %s{newline}" % (val1, val2) for val1, val2 in resp_headers.items())}'
                    '\n\n'
                    '<h1></h1>'
                    f'{func_out}'.encode()
                )
            except Exception:
                response_code = 500
                if self.handled_errors.get(response_code) is not None:
                    clientdata.send(
                        f'HTTP/1.0 {response_code} Server error'
                        '\n\n'
                        f'{self.handled_errors[response_code]()}'.encode()
                    )
                else:
                    clientdata.send(
                        f'HTTP/1.0 {response_code} Server Error'
                        '\n\n'
                        f'<h1>Something went wrong.</h1>\n'.encode()
                    )
                if debug:
                    clientdata.send(
                        f'<h1>Exception information: </h1>\n'
                        f'{traceback.format_exc()}'.encode()
                    )
                print(f"{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - HTTP '{location}' {response_code} - {addr[0]}")
                clientdata.close()
                return

        else:
            is_file = get_file(location)
            if is_file[0]:
                response_code = 200
                clientdata.send(
                    f'HTTP/1.1 {response_code} OK\n'
                    f"Content-Type: image/jpeg\n"
                    "Accept-Ranges: bytes\n\n".encode()
                )
                clientdata.send(is_file[1])
                print(
                    f"{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - HTTP '{location}' {response_code} - {addr[0]}")
                clientdata.close()
                return


            found = False
            kwargs = {}
            out = {}
            for idx, i in enumerate(self.routes):
                out = i
                temp_loc = location
                if self.routes[i]['has_special']:
                    out_s = out.replace('<>', "")

                    no_ascii = out_s
                    for b in list(ascii_letters+digits):
                        no_ascii = no_ascii.replace(b, "")

                    no_ascii_loc = temp_loc
                    for b in list(ascii_letters+digits):
                        no_ascii_loc = no_ascii_loc.replace(b, "")


                    if no_ascii_loc != no_ascii:
                        continue

                    no_etc = temp_loc[1:]
                    for b in list(no_ascii):
                        no_etc = no_etc.replace(b, ' ')

                    no_etc_out = out
                    for b in list(no_ascii):
                        no_etc_out = no_etc_out.replace(b, ' ')


                    no_etc = no_etc.split()
                    no_etc_out = no_etc_out.split()


                    kwargs = {}
                    true_idx = -1
                    for b in zip(no_etc, no_etc_out):
                        true_idx += 1
                        if b[1] == '<>':
                            kwargs[self.routes[i]['special_list'][true_idx]] = b[0]
                            continue

                        true_idx -= 1
                        if b[0] != b[1]:
                            break

                    else:
                        found = True
                        break




            if found:
                if method not in self.routes[out]['methods']:
                    response_code = 405
                    if self.handled_errors.get(response_code) is not None:
                        clientdata.send(
                            f'HTTP/1.0 {response_code} Method not allowed'
                            '\n\n'
                            f'{self.routes.get(location)}'.encode()
                        )

                    clientdata.send(
                        f'HTTP/1.0 {response_code} Method not allowed'
                        '\n\n'
                        'Method not allowed'.encode()
                    )

                try:
                    response_code = 200

                    newline = "\n"

                    if len(signature(self.routes[out]["func"]).parameters)-len(kwargs) >= 1:
                        req_data = Request(addr, request_headers, resp_headers=resp_headers, status_code=response_code, method=method, form=form)
                        func_out = self.routes[out]["func"](req_data, **kwargs)
                        resp_headers = req_data.respone_headers
                        response_code = req_data.status_code
                    else:
                        func_out = self.routes[out]["func"](**kwargs)

                    clientdata.send(
                        f'HTTP/1.0 {response_code} OK\n'
                        f'{"".join(f"%s: %s{newline}" % (val1, val2) for val1, val2 in resp_headers.items())}'
                        '\n\n'
                        '<h1></h1>'
                        f'{func_out}'.encode()
                    )
                except Exception:
                    response_code = 500
                    if self.handled_errors.get(response_code) is not None:
                        clientdata.send(
                            f'HTTP/1.0 {response_code} Server error'
                            '\n\n'
                            f'{self.handled_errors[response_code]()}'.encode()
                        )

                    clientdata.send(
                        f'HTTP/1.0 {response_code} Server Error'
                        '\n\n'
                        f'<h1>Something went wrong.</h1>\n'.encode()
                    )
                    if debug:
                        clientdata.send(
                            f'<h1>Exception information: </h1>\n'
                            f'{traceback.format_exc()}'.encode()
                        )
                    print(
                        f"{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - HTTP '{location}' {response_code} - {addr[0]}")
                    clientdata.close()
                    return



            else:
                response_code = 404
                if self.handled_errors.get(response_code) is not None:
                    clientdata.send(
                        f'HTTP/1.0 {response_code} Not found'
                        '\n\n'
                        f'{self.handled_errors[response_code]()}'.encode()
                    )
                else:
                    clientdata.send(
                        f'HTTP/1.0 {response_code} Not Found'
                        '\n\n'
                        '<h1>404 not found</h1>'.encode()
                    )



        if len(signature(self.after_req).parameters) >= 1:
            self.after_req(Request(addr, request_headers, resp_headers=resp_headers, status_code=response_code, method=method, form=form, after_req=True))
        else:
            self.after_req()

        print(f"{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - HTTP '{location}' {response_code} - {addr[0]}")
        clientdata.close()
        listening = False