# Web Framework
## What it is
Web Framework is a flask like web framework that can do basic things like see cookies, set cookies, render_templates, and much more.  

## What it can do
* Set cookies
* View cookies
* Render templates
* Load blueprints
* Have http routes
* Handle post and get requests
* Redirect
* Flash
* Etc.

## Docuentation
### Getting started
To start with the module you need to initialise the WebApp class with a name of your choice mine is called app.  
After that you can create a round by writing: @app.route("/") and then your function. The function should return html.  
This html is the html that the website will load. And finally you say app.start(ip='0.0.0.0', port=port, debug=bebug)

The following code is an example of how your code could look like.   
```python
from WebApp import WebApp

app = WebApp()

@app.route("/") # '/' is the page that show's when you load up the page
def index():
  return "<h1>Hello, world</h1>"
  
app.start("0.0.0.0", 80, True) # 0.0.0.0 is your ip on the local network.
```

### Creating routes
There are currently 3 options for routes. These are: GET, POST, and route (Which is the same as GET but can also be GET and POST)  
These indicate the method(s) that are allowed.  

For all 3 you need to specify the route. And for route you can optionally specify the allowed methods. But you can leave it empty on GET.  
Implamentation:  

Route: 
```python
from WebApp import WebApp

app = WebApp()

@app.route("/" ["GET", "POST"]) # The second arg is optional. If left empty it will be GET
def index():
  return "<h1>Hello, world</h1>"
  
app.start("0.0.0.0", 80, True)
```

get:
```python
from WebApp import WebApp

app = WebApp()

@app.get("/")
def index():
  return "<h1>Hello, world</h1>"
  
app.start("0.0.0.0", 80, True)
```

post: 
```python
from WebApp import WebApp

app = WebApp()

@app.post("/")
def index():
  return "<h1>Hello, world</h1>"
  
app.start("0.0.0.0", 80, True)
```

### Rendering templates
Rendering templates is done using the jinja2 library. For more information on it please see this: (jinja2 docs)[https://jinja.palletsprojects.com/en/3.1.x/]
Template rendering only needs the location of the .html file passing kwargs is optional.

PLEASE NOTICE THAT FOR THE MOMENT YOU CAN ONLY SPECIFY .HTML FILES THAT ARE LOCATED IN THE SAME DIRECTORY AS YOUR PYTHON FILE!

Example code: 
Python code: 
```python
from WebApp import WebApp, render_template

app = WebApp()

@app.get("/")
def index():
  return render_template("index.html", greet="Hola!")
  
app.start("0.0.0.0", 80, True)
```
Html: 
```html
<h1>{{ greet }} Welcome to my homepage!</h1>
```
### Getting request data
You can get request data by adding a parameter to your function. After that if you have an IDE you can add the request class to your parameter.  
The Request class has: 
* The ip of the client
* Request headers
* Setable response headers
* Setable response code's
* Setting cookies
* Getting cookies
* Getting the request form
* And way more

Example code: 
```python
from WebApp import WebApp, Request

app = WebApp()

@app.get("/")
def index(request:Request): # The :Request makes it easy for IDE's to read
  request.cookies # Returns a dict of all the cookies
  request.set_cookie(name="my_name", value="A value") 
  request.response_headers # returns a dict. You can also add or remove headers if you want that.
  request.request_headers # The headers recieved with the request.
  request.client_ip # The ip of the user visiting the site
  request.method # The method of the request
  request.status_code # The response code of the http form. Also can be modified
  request.form # Returns a dict of the http form
  
  return "<h1>Hello, world</h1>"
  
app.start("0.0.0.0", 80, True)
```

### Flashing
Flashing is pretty much the same as in flask. It allows you to send messages when rendering a template. These can be shown by hand or using things like bootstrap
Flashing can be done with the **'flash'** functions and takes 2 parameter those are: message, category.

Example jinja code:
```html
{% for category, message in get_flashed_messages() %}
    Message: {{message}}
    Category of the message: {{category}}
    
    
    <!--
    Uncomment if you have bootstrap
    {% if category == 'error' %}
    <div class="alert alert-danger alter-dismissable fade show" role="alert">
      {{ message }}
      <button type="button" class="close" data-dismiss="alert">
        <span aria-hidden="true">&times;</span>
      </button>
    </div>
    {% else %}
    <div class="alert alert-success alter-dismissable fade show" role="alert">
      {{ message }}
      <button type="button" class="close" data-dismiss="alert">
        <span aria-hidden="true">&times;</span>
      </button>
    </div>-->
    {% endif %} {% endfor %} 
```

### Redirect
Redirect is what is says, it redirects the user to another page. You can also show html and wait before the redirect. 

Example code: 
```python
from WebApp import WebApp, redirect

app = WebApp()

@app.get("/")
def index():
  wait_time = 2
  html = "<h1>I will be redirected</h1>"
  
  return redirect("/another-page", wait_time, html)
  
app.start("0.0.0.0", 80, True)
```

### Do something before and after request
WIP

### Blueprints
A blueprint can be used for external files that need to be loaded in to the main file. Blueprints only have the route function in the at the moment. But more will come.  

Example:
```python
from WebApp import Blueprint

api = Blueprint()

@api.route("/api/name")
def api_name():
  return "{'name': 'J3ldo'}"
```

### Loading blueprints
You can load blueprints in to your main file using the load_blueprint function in the WebApp class. This function will port all the routes in the blueprint on to the WebApp class.  

Example:
```python
from WebApp import WebApp
from api import api

app = WebApp()
app.load_blueprint(api)
  
app.start("0.0.0.0", 80, True)
```

### Handling errors
The error_handler decorator can handle functions such as: 404, 500, 405  
This can be handy if you want custom ui on the 404 page. Or return a custom json type response on 405.

Example:
```python
from WebApp import WebApp

app = WebApp()

@app.error_handler(404) #Now this function will activate on a status code of 404.
def not_found():
  return "<h1>Oops, seems we couldn't find this page.</h1>"

@app.get("/")
def index():
  return "<h1>Hello, world</h1>"
  
app.start("0.0.0.0", 80, True)
```

### Adding dynamic parts to url
Dynamic parts in your url can be handy if you want to get data from it. This data can be a message or a hash type for online hashing.  
Dynamic parts are implemented by putting it between these two characters '<', '>'.  

Example: 
```python
from WebApp import WebApp

app = WebApp()

@app.get("/<name>")
def index(name): #The name arg is for dynamic part of the url and it must match names.
  return f"<h1>Hello, {name}</h1>"
  
app.start("0.0.0.0", 80, True)
```

### Doing things before and after requests.
WIP
