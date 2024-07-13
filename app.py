import os
import logging
from flask import Flask, request, jsonify
from datetime import datetime
from dotenv import load_dotenv
from celery import Celery
from tasks import send_email
from celery.result import AsyncResult

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure Celery
celery = Celery(
    'tasks',
    broker=os.getenv('CELERY_BROKER_URL'),
    backend=os.getenv('CELERY_RESULT_BACKEND')
)

# Configure logging
log_file_path= '/var/log/messaging_system.log'
logging.basicConfig(
    filename=log_file_path,  # Ensure the log path is correct and writable
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Add a logging statementto ensure logging is set up correctly
logging.info('Starting the Flask Application and logging setup is complete.')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logging.getLogger().addHandler(console_handler)

@app.route('/')
def index():
    sendmail = request.args.get('sendmail')
    talktime = request.args.get('talktime')

    if sendmail and talktime:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f'Current time: {current_time}')
        task = send_email.delay(sendmail)
        logging.info(f'Email task queued with task id: {task.id}')
        return jsonify({
            'message': 'Email task has been queued.',
            'task_id': task.id
        }), 200
    logging.warning('Both sendmail and talktime parameters are required.')
    return jsonify({'message': 'Both sendmail and talktime parameters are required.'}), 400

@app.route('/task_status/<task_id>')
def get_task_status(task_id):
    task = AsyncResult(task_id, app=celery)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Task is waiting for execution or unknown'
        }
    elif task.state == 'FAILURE':
        response = {
            'state': task.state,
            'status': str(task.info),  # this is the exception raised
        }
    else:
        response = {
            'state': task.state,
            'status': task.info,  # this is the return value of your task
        }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
