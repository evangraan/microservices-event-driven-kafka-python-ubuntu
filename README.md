# Introduction

This repository contains a simple event-driven hospital scheduling system using kafka, postgresql and python on Ubuntu

The state machines are simple:
* The hospital has 2 floors with 3 rooms each, designated A1-3 and B1-3
* The hospital employs 2 nurses, one doctor, 2 porters and 2 cleaners
* A generator creates a patient every 5 seconds
* The hospital admissions tries to book a room for the patient. If no rooms are available, the patient is referred to another hostpital
* Once a patient has a room booked, if a porter is available, the porter is scheduled to escort the patient to their room.
* If a porter is not available, the patient waits in a waiting room until a porter is available
* The porter receives the scheduling request and escorts the patient to the room
* Once a patient is in a room, a medical staff member is scheduled to see them
* If no medical staff are available, the patient is put on a waiting list
* Medical staff once scheduled moves to the required rooms and sees patients
* Once a patient has been seen, a porter is scheduled to take the patient to the hospital exit
* If a porter is not available, the patient is placed on a waiting list
* A scheduled porter escorts the patient to the hospital exit. On arrival there, a cleaner is scheduled to clean the room
* Once a room has been cleaned, the room becomes available for a new patient

The postgress database only keeps state. The following microservices perform duties:
* cleaner_pool.py
* medical_staff.py
* patients.py
* porter_pool.py
* hospital_administration.py

Each can be run independently using:
```
cd service-name
source venv/bin/activate
python service-name.py
```

# Architecture

The architecture is fully decoupled, with independent services producing and consuming messages using kafka as the event bus.

![Micro-services event-driven architecture](https://github.com/evangraan/hospital-scheduling-microservices-event-driven-kafka-python-ubuntu/blob/master/architecture.png)

# Database schema
[schema](schema.md)

# Demo
You can see the services with kafka in action here: https://www.dropbox.com/s/zzytqvw6cao6ezj/hospital-demo.mov?dl=0 

# kafka
Note: replace localhost with the host of yoru kafke instance

## Installing
For this prototype I run kafka on Ubuntu 18.04 (ensure JDK is installed):
```
wget https://downloads.apache.org/kafka/2.5.0/kafka_2.12-2.5.0.tgz
tar xvfz kafka_2.12-2.5.0.tgz
cd kafka_2.12-2.5.0
```

## Running
```
bin/zookeeper-server-start.sh config/zookeeper.properties
bin/kafka-server-start.sh config/server.properties
bin/kafka-topics.sh --create --bootstrap-server 192.168.1.230:9092 --replication-factor 1 --partitions 1 --topic patients
bin/kafka-topics.sh --create --bootstrap-server 192.168.1.230:9092 --replication-factor 1 --partitions 1 --topic cleaners
bin/kafka-topics.sh --create --bootstrap-server 192.168.1.230:9092 --replication-factor 1 --partitions 1 --topic medical
bin/kafka-topics.sh --create --bootstrap-server 192.168.1.230:9092 --replication-factor 1 --partitions 1 --topic porters
```

## Inspecting

```
bin/kafka-console-consumer.sh --bootstrap-server 192.168.1.230:9092 --topic patients --group debug --from-beginning
{"event": "entrance", "subject": "patient", "id": "ef5a624e-bb17-11ea-b5a3-acde48001122"}
{"event": "entrance", "subject": "patient", "id": "f2565642-bb17-11ea-b5a3-acde48001122"}
```

## Maintaining

To clear out a topic ensure that config/server.properties has the following entry:
```
delete.topic.enable=true
```

Then delete a topic as follows, then wait a couple of minutes before using the topic again (or it will be unavailable:)
```
bin/kafka-topics.sh --zookeeper 192.168.1.230:2181 --delete --topic patients
bin/kafka-topics.sh --zookeeper 192.168.1.230:2181 --delete --topic cleaners
bin/kafka-topics.sh --zookeeper 192.168.1.230:2181 --delete --topic medical
bin/kafka-topics.sh --zookeeper 192.168.1.230:2181 --delete --topic porters
```

# Postgres
## Installation on Ubuntu
```
sudo apt-get install wget ca-certificates
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
sudo apt-get update
sudo apt-get -y install postgresql postgresql-contrib
sudo su - postgres
```

## User and role
```
sudo adduser kafka
sudo su - kafka
kafka=# CREATE ROLE kafka WITH LOGIN CREATEDB ENCRYPTED PASSWORD 'R!Z::x4Q7XrvTBC~';
kafka=# GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO kafka
kafka=# \q
createdb kafka 
```

## Serve to all IPs
```
sudo vi /etc/postgresql/12/main/postgresql.conf
    listen_addresses = '0.0.0.0'
sudo service postgresql restart
```

## Ensure you have access from your remote IP, e.g.
```
vi /etc/postgresql/12/main/pg_hba.conf
    host  all  all  192.168.1.178/24  trust
```

## Ensure you can access the database and tables from the command line:

```
psql -U postgres -h 192.168.1.230 kafka
psql (12.3)
SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, bits: 256, compression: off)
Type "help" for help.

kafka=# \dt;
       List of relations
 Schema | Name  | Type  | Owner 
--------+-------+-------+-------
 public | rooms | table | kafka
(1 row)

kafka=# select * from rooms;
 id | name | occupied 
----+------+----------
  1 | A1   | f
  2 | A2   | f
  3 | A3   | f
  4 | B1   | f
  5 | B2   | f
  6 | B3   | f
(6 rows)
```

## Managing

* Install pgadmin to log into and manage the database.
* Run pgadmin
* Browse to http://127.0.0.1:52626/browser/#

## Bootstrapping the database
```
cd orm
python bootstrap.py
```

# Notes
* On OSX, export the path to the SSL libraries, or psychopg2 will not install:
```
brew install openssl
export LDFLAGS="-L/usr/local/opt/openssl/lib"
export CPPFLAGS="-I/usr/local/opt/openssl/include"
pip install psycopg2
```

# Improvements
* This was a quick prototype and as such have many flaws
* services pools should instead be service workers, multiple of which can be spun up
* shared code imports should use proper modules and packages, not path hacks
* the database schema is very, very simple. Instead of 'occupied', staff and patients' ids should be used
* there should be proper one-to-many relationships where appropriate between tables
* Testing, preferably BDD using behave
* Instrumentation with a dashboard
* Use configuration files for kafka host, IP, postgres host, port, database and credentials
