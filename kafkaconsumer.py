import json
from kafka import KafkaConsumer
from json import loads

Topicname='TestTopic'

consumer = KafkaConsumer(Topicname)


from influxdb import InfluxDBClient
import pandas as pd

client = InfluxDBClient('localhost', 8086, 'admin', 'Password1', 'reeshikafkadb')

client.create_database('reeshikafkadb')

#json_body = []

for message in consumer:
      print(message.value.decode("utf-8"))
      #print(json.loads(message.value))
      
    

      json_body = [
    {
        "measurement": "reeshidata",
        "tags": {
        },
        "fields": {'status':message.value.decode("utf-8")}
    }
]


      client.write_points(json_body)