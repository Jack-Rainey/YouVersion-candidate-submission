# Project A API Implementation
## Introduction
I decided to complete the API project over the front end project because front-end design is not a strong suit of mine. The API development process was straightforward and fun!

## Requirements and How to Run
### Run Server
To start the server, run the following commands from the root directory:
```
python -m pip install -r requirements.txt
python -m flask --app src/server.py run --debug
```

Once the server is running, you will get a message containing a active server, such as
```
http://127.0.0.1:5000
```
Once aquired nativate to a page, such as
```
http://127.0.0.1:5000/votd?day=195&version=206
```

### Run Tests
You can also run the test file for this project by running
```
python -m pip install -r requirements.txt
python tests/test_server.py
```


## Decisions and Assumptions
### Definition of Today
Since the IP address is not a reliable way to verify the user's time zone, the code defaults to UTC time to calculate the current day for the verse of the day request.

### Default Version
- There is no default Bible version.
- Since the project writeup specifies a default for day, but not for version, I thought that no default would be the safest and most straightforward viable option given the unclear specifications.

### Programming Language and Framework
I chose to use the Flask environment in the Python programming language because Python is my strongest language and Flask made for simple implementation of the given task.

### Caching
For caching the verse of the days and versions, a basic Python dictionary was used. For the verse of the days, this consisted of a key of type `(day, version)` with a value of the JSON response as defined in the [writeup](docs/project-a-api.md). For the versions, this consisted of a key of `en*` followed by a list of the JSON responses for each available English Bible version.

### Testing
The test file, unlike the real server, this page does not use the real YouVersion API as specified by project parameters. It tests using mocked data whether the URL specified resulted in a happy path, if the date specified by the URL was invalid, and if data recieved proper data from YouVersion.

## What I Would Do Next
1. Add a cache test to `docs/test_server.py`.
2. Make the cache persist even when the server shuts down to avoid unnecessary calls after restarts.