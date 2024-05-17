import json
import random
from flask import Flask, jsonify
from threading import Timer

app = Flask(__name__)

# Function to generate random values for the variables
def generate_random_values():
    global var1, var2, var3
    var1 = random.randint(0, 100)
    var2 = random.randint(0, 100)
    var3 = random.randint(0, 100)

# Function to update the variables every 60 seconds
def update_variables():
    generate_random_values()
    print(f"Updated variables: {var1}, {var2}, {var3}")
    Timer(60, update_variables).start()

# Route to expose the JSON object
@app.route('/variables')
def get_variables():
    global var1, var2, var3
    data = {
        'otus_important_metrics_1': var1,
        'otus_important_metrics_2': var2,
        'otus_important_metrics_3': var3
    }
    return jsonify(data)

if __name__ == '__main__':
    # Initialize the variables with random values
    generate_random_values()

    # Start the update process
    update_variables()

    # Run the Flask app
    app.run()
