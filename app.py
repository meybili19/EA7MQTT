from flask import Flask, render_template, request, jsonify
from flasgger import Swagger
import paho.mqtt.client as mqtt
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


app = Flask(__name__)
swagger = Swagger(app)

# MQTT Configuration
MQTT_BROKER = "test.mosquitto.org"
MQTT_TOPIC = "test/hello_world"

# Global variable to store the received message
latest_message = "No messages yet."

# MQTT Client
def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    global latest_message
    latest_message = msg.payload.decode()
    print(f"Received message: {msg.topic} -> {latest_message}")

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, 1883, 60)

# Routes
@app.route('/')
def index():
    """
    Main Page
    ---
    responses:
      200:
        description: Returns the main page with "Hello World"
    """
    global latest_message
    return render_template('index.html', message=latest_message)

@app.route('/publish', methods=['POST'])
def publish_message():
    """
    Publishes a message to the MQTT broker
    ---
    parameters:
      - name: message
        in: formData
        type: string
        required: true
        description: The message to be published to MQTT.
    responses:
      200:
        description: Message successfully published
    """
    user_message = request.form.get('message')
    if user_message:
        mqtt_client.publish(MQTT_TOPIC, user_message)
        return jsonify({"message": "Message published", "content": user_message}), 200
    return jsonify({"error": "No message provided"}), 400

if __name__ == '__main__':
    mqtt_client.loop_start()  
    # Print the URLs where the app and Swagger documentation can be accessed
    print("App running at: http://localhost:5000/")
    print("Swagger documentation available at: http://localhost:5000/apidocs")
    app.run(debug=True, host='0.0.0.0', port=5000)
