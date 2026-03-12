from ai import AIDoc
from docStore import DocumentStore
from flask import Flask, request, render_template, redirect, url_for
from flask_socketio import SocketIO, emit
import logging
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.debug = True

doc = DocumentStore()
ai = AIDoc(doc)

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = 'var/files/'

conversation_history = []

uploaded_documents = {}

socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/read-form', methods=['POST'])
def read_form():
    global conversation_history

    conversation_history = []
    ai.reset()

    if 'documents' not in request.files:
        return {
            'doc': 'No file part'
        }
    else:
        for file in request.files.getlist("documents"):
            if file:
                filename = secure_filename(file.filename)
                
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                ai.load_documents(filepath)

    return redirect(url_for('chat'))

@app.route('/chat', methods=['GET'])
def chat():
    return render_template('chat.html')

@socketio.on('send_message')
def send_message(request_data):
    try:
        user_message = {
            'role': 'user',
            'content': request_data['message'],
        }
        conversation_history.append(user_message)

        response = ai.chat(request_data['message'])

        text_response = ''
        for token in response:
            try:
                text_response += token
                # Send each chunk as it arrives
                emit('ai_response_chunk', {
                    'chunk': token
                })
            except:
                logging.error('Something went wrong: ' + token)

        logging.error('='*200)
        ai.show_sources(request_data['message'])
        ai_message = {
            'role': 'assistant',
            'content': text_response,
        }
        conversation_history.append(ai_message)
        
        emit('ai_response_complete', {})
    except Exception as e:
        logging.error(e)
        emit('error', {
            'message': f'Error: {str(e)}'
        })
    
@socketio.on('get_messages')
def handle_get_messages():
    emit('previous_messages', {'messages': conversation_history})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
