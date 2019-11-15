# kafka-heroku-idempotence
Test app to show problem with enabling idempotence setting when using Heroku's Kafka

__1) Clone the test code repo__ 
```
$ git clone git@github.com:larsar/kafka-heroku-idempotence.git
Cloning into 'kafka-heroku-idempotence'...
```

__2) Create a .env file with the Heroku Kafka environment variables__

__3) Create the test topic: heroku kafka:topics:create idempotence-test-topic -a APP_NAME__ 

__4) Create virtual enviroment with python 3__
```
$ make venv
virtualenv -p python3 venv
Running virtualenv with interpreter /usr/local/bin/python3
...
```

__5) Activate virtual environment__
```
$ source venv/bin/activate
```

__6) Install dependencies__
```
$ make install
pip install -r requirements.txt
...
```

__7) Run the test that works (the message is sent to the topic)__
```
$ python without_idempotence_setting.py 
Done
```

__8) Run the test that fails (the flush method hangs)__
```
$ python with_idempotence_setting.py 
^C^C^C^C


Traceback (most recent call last):
  File "with_idempotence_setting.py", line 11, in <module>
    p.flush()
KeyboardInterrupt
```