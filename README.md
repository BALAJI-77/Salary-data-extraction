# salary-scarping-
salary scraping using selenium 



Step  1:
        - Install all the package requirement for python env and linux python env
        - The python env used for running flask server 
        - The linux env used for running rq worker (redis)
        - create virtal env in linux 
                - virtualenv -p python3.9 worker
                - source worker/bin/activate
                - pip3 install rq==1.2.2
    
Step - 2:
        - run the flask server 
        - run the redis-server.exe file
        - run the rq worker 

Step - 3:
        - send the param in json format
                ```
                {
                  "name": "james",
                  "position": "python Developer"
                }
                ```
