## kafka python ##
import kafka
from kafka import KafkaProducer
from kafka import BrokerConnection
from sys import api_version
import time
#dt = datetime.now()
#date = datetime.strftime(dt, '%Y-%m-%d')

#connector = kafka.BrokerConnection(host='10.10.10.154', port='6667', afi=ip_)
#connector.connect()
#if connector.connected() == True:
#    print("connected")
#else:
#    print("not connected")

producer = KafkaProducer(bootstrap_servers='10.10.10.154:6667', retries=5, client_id='kafka-python',
                         value_serializer=lambda m: json.dumps(m).encode('ascii'), api_version=(0, 9))
# produce asynchronously
#while True:
#    producer.send('pcap', {'key': 'value'})

#i = 0
#while i <= 10:
#    producer.get()
#    i += 1

t = time.time()
while t <= 10:
    #producer.send('pcap', {'key': 'value'})
    producer.send('pcap', b'test')
    
# block until all async messages are sent
producer.flush()
#producer.close()

'''
## kafka python usage ##
from kafka import KafkaProducer
from kafka.errors import KafkaError

producer = KafkaProducer(bootstrap_servers=['broker1:1234'])

# Block for 'synchronous' sends
try:
    record_metadata = future.get(timeout=10)
except KafkaError:
    # Decide what to do if produce request failed...
    log.exception()
    pass

# Successful result returns assigned partition and offset
print (record_metadata.topic)
print (record_metadata.partition)
print (record_metadata.offset)

# produce keyed messages to enable hashed partitioning
producer.send('my-topic', key=b'foo', value=b'bar')

# encode objects via msgpack
producer = KafkaProducer(value_serializer=msgpack.dumps)
producer.send('msgpack-topic', {'key': 'value'})

# produce json messages
producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('ascii'))
producer.send('json-topic', {'key': 'value'})
'''
