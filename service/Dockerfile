FROM maven:3.9.11
LABEL authors="gneg"

COPY vivida/pom.xml .
COPY vivida/src ./src

RUN mvn clean package -DskipTests

ENTRYPOINT ["java","-jar","./target/vivida-0.0.1-SNAPSHOT.jar"]