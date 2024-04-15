from flask import Flask, render_template, request, jsonify, send_from_directory
import os

app = Flask(__name__,static_folder='templates')

# File to store chat messages
MESSAGE_FILE = 'messages.txt'

# Load existing messages from file if it exists
if os.path.exists(MESSAGE_FILE):
    with open(MESSAGE_FILE, 'r') as f:
        messages = f.read().splitlines()
else:
    messages = []

@app.route('/')
def index():
    return render_template('session.html', messages=messages)

@app.route('/send_message', methods=['POST'])
def send_message():
    if request.method == 'POST':
        message = request.form['message']
        username = request.form['username']
        messages.append({'username': username, 'message': message,})  # Send message object with username and message
        save_messages()  # Save messages to file
        return jsonify({'message': 'Message sent successfully!'})
    

    
@app.route('/get_messages')
def get_messages():
    last_message_index = int(request.args.get('last_message_index', 0))
    return jsonify(messages[last_message_index:])

def save_messages():
    with open(MESSAGE_FILE, 'a') as h:
        for message in messages:
            h.write(f"{message['username']}: {message['message']}\n")

@app.route('/',methods=['POST'])
def clearmessages():
    with open(MESSAGE_FILE,'w') as d:
        d.write('/n')
    messages.clear()
    return render_template('session.html',messages=messages)
    
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
