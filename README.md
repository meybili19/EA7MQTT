# EA7MQTT
 
## Docker
   - docker network create mqtt-network
   - docker build -t meybili/mqtt .
   - docker run --name mqtt-container --network mqtt-network -p 5000:5000 meybili/mqtt