Adding asset parser and enrichment configurations:

Go to quick-dev directory in metron installation
Run: vagrant up  Then run: vagrant ssh  Then: sudo -i
1) hbase shell
2) alter 'enrichment', 'assets'
3) exit()
4) cp /<threatdetection dir>/metron/parsers/asset.json /usr/metron/0.2.1BETA/config/zookeeper/parsers
5) cp /<threatdetection dir>/metron/enrichments/bro.json /usr/metron/0.2.1BETA/config/zookeeper/enrichments
6) /usr/hdp/current/kafka-broker/bin/kafka-topics.sh --zookeeper node1:2181 --create --topic assets --partitions 1 --replication-factor 1
7) /usr/metron/0.2.1BETA/bin/zk_load_configs.sh -z node1:2181 -m PUSH -i /usr/metron/0.2.1BETA/config/zookeeper
8) tail /<threatdetection dir>/metron/sample_data/asset_data_ref.csv | /usr/hdp/current/kafka-broker/bin/kafka-console-producer.sh --broker-list node1:6667 --topic assets
