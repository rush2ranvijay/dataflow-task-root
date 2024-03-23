######### Docker Build Of python project ##########

docker build -t rush2ranvijay/python_simple_task:0.1 .
docker push rush2ranvijay/python_simple_task:0.1

dataflow:>app register --type task  --name python-simple-task --uri docker://rush2ranvijay/python_simple_task:0.1
dataflow:>task create --name python-simple-task --definition "python-simple-task"
dataflow:>task launch --name python-simple-task

############################################## Manual installation ############################################

1. wget -O spring-cloud-dataflow-server-2.11.2.jar https://repo.maven.apache.org/maven2/org/springframework/cloud/spring-cloud-dataflow-server/2.11.2/spring-cloud-dataflow-server-2.11.2.jar

2. wget -O spring-cloud-dataflow-shell-2.11.2.jar https://repo.maven.apache.org/maven2/org/springframework/cloud/spring-cloud-dataflow-shell/2.11.2/spring-cloud-dataflow-shell-2.11.2.jar

3. wget -O spring-cloud-skipper-server-2.11.2.jar https://repo.maven.apache.org/maven2/org/springframework/cloud/spring-cloud-skipper-server/2.11.2/spring-cloud-skipper-server-2.11.2.jar

4. Run rabbitmq docker container

docker run -d --hostname rabbitmq --name rabbitmq -p 15672:15672 -p 5672:5672 rabbitmq:3.7

5. Launch spring-cloud-dataflow-server with external postgresDB connection details install on local machine

-- Copy line by line and then hit enter to run on powershell
-- Create database manually first on the postgres for example - dataflow

	a) java -jar spring-cloud-skipper-server-2.11.2.jar

=> (Use hostname "host.docker.internal" from within a Docker container to connect host machine)
	
	b) java -jar spring-cloud-dataflow-server-2.11.2.jar `
			--spring.datasource.url=jdbc:postgresql://host.docker.internal:5432/dataflow `
			--spring.datasource.username=postgres `
			--spring.datasource.password=postgres `
			--spring.datasource.driver-class-name=org.postgresql.Driver

	c) java -jar spring-cloud-dataflow-shell-2.11.2.jar
		
	d) (Optional): skipper-server with host db similar to dataflow-server

	java -jar spring-cloud-skipper-server-2.11.2.jar `
			--spring.datasource.url=jdbc:postgresql://localhost:5432/dataflow `
			--spring.datasource.username=postgres `
			--spring.datasource.password=postgres `
			--spring.datasource.driver-class-name=org.postgresql.Driver

###############  Working Dataflow Docker run Command ###################

docker run --network bridge --rm -e deployerId=python-simple-task-b5d92403-4473-4b59-b924-e7b64bc48805 -e SPRING_APPLICATION_JSON='{\"endpoints.jmx.unique-names\":\"true\",\"endpoints.shutdown.enabled\":\"true\",\"spring.datasource.driverClassName\":\"org.postgresql.Driver\",\"management.metrics.tags.application\":\"${spring.cloud.task.name:unknown}-${spring.cloud.task.executionid:unknown}\",\"spring.cloud.task.name\":\"python-simple-task\",\"spring.datasource.password\":\"postgres\",\"spring.cloud.deployer.bootVersion\":\"2\",\"management.metrics.tags.service\":\"task-application\",\"spring.datasource.username\":\"postgres\",\"spring.datasource.url\":\"jdbc:postgresql://localhost:5432/dataflow\",\"spring.cloud.task.initialize-enabled\":\"false\",\"server.port\":\"32353\",\"spring.cloud.task.schemaTarget\":\"boot2\",\"spring.batch.jdbc.table-prefix\":\"BATCH_\",\"spring.cloud.task.tablePrefix\":\"TASK_\",\"spring.jmx.default-domain\":\"python-simple-task-b5d92403-4473-4b59-b924-e7b64bc48805\"}' -p 32353:32353 rush2ranvijay/python_simple_task:0.2 --app.python-simple-task.spring.cloud.task.initialize-enabled=false --app.python-simple-task.spring.batch.jdbc.table-prefix=BATCH_ --app.python-simple-task.spring.cloud.task.tablePrefix=TASK_ --app.python-simple-task.spring.cloud.task.schemaTarget=boot2 --app.python-simple-task.spring.cloud.deployer.bootVersion=2 --spring.cloud.task.executionid=1

## Use the special hostname "host.docker.internal" to refer to the host machine from within a Docker container

docker run --network bridge --rm -e deployerId=python-simple-task-b5d92403-4473-4b59-b924-e7b64bc48805 -e SPRING_APPLICATION_JSON='{\"endpoints.jmx.unique-names\":\"true\",\"endpoints.shutdown.enabled\":\"true\",\"spring.datasource.driverClassName\":\"org.postgresql.Driver\",\"management.metrics.tags.application\":\"${spring.cloud.task.name:unknown}-${spring.cloud.task.executionid:unknown}\",\"spring.cloud.task.name\":\"python-simple-task\",\"spring.datasource.password\":\"postgres\",\"spring.cloud.deployer.bootVersion\":\"2\",\"management.metrics.tags.service\":\"task-application\",\"spring.datasource.username\":\"postgres\",\"spring.datasource.url\":\"jdbc:postgresql://host.docker.internal:5432/dataflow\",\"spring.cloud.task.initialize-enabled\":\"false\",\"server.port\":\"32353\",\"spring.cloud.task.schemaTarget\":\"boot2\",\"spring.batch.jdbc.table-prefix\":\"BATCH_\",\"spring.cloud.task.tablePrefix\":\"TASK_\",\"spring.jmx.default-domain\":\"python-simple-task-b5d92403-4473-4b59-b924-e7b64bc48805\"}' -p 32353:32353 rush2ranvijay/python_simple_task:0.2 --app.python-simple-task.spring.cloud.task.initialize-enabled=false --app.python-simple-task.spring.batch.jdbc.table-prefix=BATCH_ --app.python-simple-task.spring.cloud.task.tablePrefix=TASK_ --app.python-simple-task.spring.cloud.task.schemaTarget=boot2 --app.python-simple-task.spring.cloud.deployer.bootVersion=2 --spring.cloud.task.executionid=1

##########################################  TCP Connection issue for PostgresSQL  #############################################################

We might face TCP/IP connection issue while accessing the PostgresSQL or any other database from docker container 
of our python app, then we have to add docker container's IP in the pg_hba.conf file to allow remote machine/host 
connection to the database as below

# IPv4 local connections:
host    all             127.0.0.1/32            scram-sha-256
`host    all            192.168.1.5/32          scram-sha-256`