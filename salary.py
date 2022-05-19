import redis
from os import remove
from flask import Flask,request
import time
from rq import Queue
from salary_worker import empty
from salary_worker import main
import logging



app = Flask(__name__)


r = redis.Redis()
q = Queue(connection=r)

#  ----------------------- store the logger history -------------------------------
# logging.basicConfig(filename='Salary_Log_Book.log', level=logging.DEBUG)
logging.basicConfig(filename='Salary_Log_Book.log', level=logging.INFO)


@app.route('/trigger',methods=['POST'])
def trigger():
    empty()
    data = request.get_json()
    global position
    position =data.get('position').lower()
    global name
    name = data.get('name')
    print(name)
    print('-'+position+'-') 
    job = q.enqueue(main,name,position)
    time.sleep(5)
    
    def waitUntil(condition): #defines function
        wU = True
        while wU == True:
            if (job.result != None):
                wU = False
            time.sleep(5)
    waitUntil(job.result)
    return job.result



if __name__ == '__main__':
    app.run() 