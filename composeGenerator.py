

#!/usr/bin/env python3

import csv
import re
import fileinput
import sys
import datetime

currentTime = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
yaml_compose_file = 'docker-compose-%s.yml' % (currentTime)
yaml_stack_file = 'docker-stack-%s.yml' % (currentTime)
#----------------static statements---------------------
csv_file_path = '/<Absolute_Path>/csvfile.csv'
#csv_file_path = input('Enter absolute path of CSV file: ')

versionControl_url = 'https://<repo>'
dotin_registry = 'registry/local'
compose_starter = '''version: '3.7'
services: '''
stackNetwork = '''
networks:
      hostnet:
           external: true
           name: my_network'''
stackVolumes = '''
volumes:
    my_log:
         driver: local
         driver_opts:
              o: bind
              type: none
              device: /appserver/my_log'''
#--------------------------------------------------------
original_stdout = sys.stdout # Save a reference to the original standard output

with open(yaml_compose_file, 'w') as composefile:
    sys.stdout = composefile # Change the standard output to the file we created.
    
    print(compose_starter)
    with open(csv_file_path) as csv_file:
        read_csv = csv.reader(csv_file, delimiter=',')
        for row in read_csv:
            artifact_name = row[0]
            artifact_version = row[1]

            compose_service = '''
  %s:
    build:
      context: ../%s/
      args:
        ARTIFACT: %s-%s.jar
        VCS_URL: "%s"
    image: %s/%s:%s'''
            print(compose_service % (artifact_name, artifact_name, artifact_name, artifact_version, versionControl_url, dotin_registry, artifact_name, artifact_version))

    sys.stdout = original_stdout
#-----------------------------------------------------------
original_stdout = sys.stdout # Save a reference to the original standard output

with open(yaml_stack_file, 'w') as stackfile:
    sys.stdout = stackfile # Change the standard output to the file we created.
    
    print(compose_starter)
    with open(csv_file_path) as csv_file:
        read_csv = csv.reader(csv_file, delimiter=',')
        for row in read_csv:
            artifact_name = row[0]
            artifact_version = row[1]
            service_name = 'my-%s' % (artifact_name)

            stack_service = '''
     %s:
       image: %s/%s:%s
       hostname: %s
       environment:
         - "SPRING_PROFILES=prod"
         - "ZOOKEEPER_STRING=zoo1:2181,zoo2:2181,zoo3:2181"
         - "--zk.username=**"
         - "--zk.password=**"
       volumes:
         - my_log:/opt/log
       networks:
         hostnet: {}
       deploy:
         replicas: 1
         restart_policy:
            condition: on-failure
         placement:
            constraints:
                - node.labels.my == microservices'''

            api_gateway_service = '''
     my-api-gateway:
       image: %s/api-gateway:%s
       hostname: my-api-gateway
       environment:
         - "SPRING_PROFILES=prod"
         - "ZOOKEEPER_STRING=zoo1:2181,zoo2:2181,zoo3:2181"
         - "--zk.username=**"
         - "--zk.password=**"
       volumes:
         - my_log:/opt/log
       ports:
        - 2000:2000
       networks:
         hostnet: {}
       deploy:
         replicas: 2
         restart_policy:
            condition: on-failure
         placement:
            constraints:
                - node.labels.my == microservices'''
            
            naming_server_service = '''
     my-microservice5:
       image: %s/microservice5:%s
       hostname: my-microservice5
       environment:
         - "SPRING_PROFILES=prod"
         - "ZOOKEEPER_STRING=zoo1:2181,zoo2:2181,zoo3:2181"
         - "--zk.username=**"
         - "--zk.password=**"
       volumes:
         - my_log:/opt/log
       ports:
         - 2100:2100
       networks:
         hostnet: {}
       deploy:
         replicas: 1
         restart_policy:
            condition: on-failure
         placement:
            constraints:
                - node.labels.my == microservices'''

            api_admin_service = '''
     my-microservice6:
       image: %s/microservice6:%s
       hostname: my-microservice6
       environment:
         - "SPRING_PROFILES=prod"
         - "ZOOKEEPER_STRING=zoo1:2181,zoo2:2181,zoo3:2181"
         - "--eureka.client.service-url.defaultZone=http://**:**@my-microservice5:2100/eureka/"
         - "--zk.username=**"
         - "--zk.password=**"
       volumes:
         - my_log:/opt/log
       ports:
         - 2200:2200
       networks:
         hostnet: {}
       deploy:
         replicas: 1
         restart_policy:
            condition: on-failure
         placement:
            constraints:
                - node.labels.my == microservices'''

            adapter_sepah_service = '''
     my-microservice1:
       image: %s/microservice1:%s
       hostname: my-microservice1
       environment:
         - "SPRING_PROFILES=prod"
         - "ZOOKEEPER_STRING=zoo1:2181,zoo2:2181,zoo3:2181"
         - "--zk.username=**"
         - "--zk.password=**"
       volumes:
         - my_log:/opt/log
       extra_hosts:
         - "ha.hamidgholami.ir:10.10.10.10"
         - "gh.hamidgholami.ir:10.10.10.10"
       networks:
         hostnet: {}
       deploy:
         replicas: 3
         restart_policy:
            condition: on-failure
         placement:
            constraints:
                - node.labels.my == microservices'''

            adapter_hekmat_service = '''
     my-microservice3:
       image: %s/microservice3:%s
       hostname: my-microservice3
       environment:
         - "SPRING_PROFILES=prod"
         - "ZOOKEEPER_STRING=zoo1:2181,zoo2:2181,zoo3:2181"
         - "--zk.username=**"
         - "--zk.password=**"
       volumes:
         - my_log:/opt/log
       networks:
         hostnet: {}
       deploy:
         replicas: 2
         restart_policy:
            condition: on-failure
         placement:
            constraints:
                - node.labels.my == microservices'''

            adapter_mehr_service = '''
     my-microservice2:
       image: %s/microservice2:%s
       hostname: my-microservice2
       environment:
         - "SPRING_PROFILES=prod"
         - "ZOOKEEPER_STRING=zoo1:2181,zoo2:2181,zoo3:2181"
         - "--zk.username=**"
         - "--zk.password=**"
       volumes:
         - my_log:/opt/log
       networks:
         hostnet: {}
       deploy:
         replicas: 2
         restart_policy:
            condition: on-failure
         placement:
            constraints:
                - node.labels.my == microservices'''

            deposit_service = '''
     my-microservice4:
       image: %s/microservice4:%s
       hostname: my-microservice4
       environment:
         - "SPRING_PROFILES=prod"
         - "ZOOKEEPER_STRING=zoo1:2181,zoo2:2181,zoo3:2181"
         - "--zk.username=**"
         - "--zk.password=**"
       volumes:
         - my_log:/opt/log
       networks:
         hostnet: {}
       deploy:
         replicas: 3
         restart_policy:
            condition: on-failure
         placement:
            constraints:
                - node.labels.my == microservices'''

            if artifact_name == 'api-gateway':
                print(api_gateway_service % (dotin_registry, artifact_version))
            elif artifact_name == 'microservice5':
                print(naming_server_service % (dotin_registry, artifact_version))
            elif artifact_name == 'microservice6':
                print(api_admin_service % (dotin_registry, artifact_version))
            elif artifact_name == 'microservice1':
                print(adapter_sepah_service % (dotin_registry, artifact_version))
            elif artifact_name == 'microservice2':
                print(adapter_mehr_service % (dotin_registry, artifact_version))
            elif artifact_name == 'microservice3':
                print(adapter_hekmat_service % (dotin_registry, artifact_version))
            elif artifact_name == 'microservice4':
                print(deposit_service % (dotin_registry, artifact_version))
            else:
                print(stack_service % (service_name, dotin_registry, artifact_name, artifact_version, service_name))

    print(stackNetwork)
    print(stackVolumes)

    sys.stdout = original_stdout
