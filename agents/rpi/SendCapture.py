from kafka import KafkaProducer

#producer = KafkaProducer(bootstrap_servers=['10.10.10.154:6667'],api_version=(0,9))
producer = KafkaProducer(bootstrap_servers='10.10.10.154:6667')
#for _ in range(100):
#    producer.send('pcap', b'some_message_bytes')

    # Block until all pending messages are sent
#    producer.flush()
    # Block until a single message is sent (or timeout)


