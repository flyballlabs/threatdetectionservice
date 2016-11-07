import kafka
from kafka import KafkaProducer
from kafka import BrokerConnection
from sys import api_version
#dt = datetime.now()
#date = datetime.strftime(dt, '%Y-%m-%d')

#connector = kafka.BrokerConnection(host='10.10.10.154', port='6667', afi=ip_)
#connector.connect()
#if connector.connected() == True:
#    print("connected")
#else:
#    print("not connected")

#producer = KafkaProducer(bootstrap_servers=['10.10.10.154:6667'],api_version=(0,9))
#producer = KafkaProducer(bootstrap_servers='50.253.243.17:6667')
producer = KafkaProducer(bootstrap_servers='50.253.243.17:6667', value_serializer=lambda m: json.dumps(m).encode('ascii'), api_version=(0, 9))

for _ in range(100):
    producer.send('pcap', {'key': 'value'})
    producer.flush()
    producer.send('asset', b'some_message_bytes')
#while True:
#t = time.time()
#while t <= 100:   
#producer.send('kafka-topic', key=b'foo', value=b'bar')
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
