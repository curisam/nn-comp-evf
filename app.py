import os
import importlib
import yaml
import time
import logging
import pytorch_lightning as pl
from torch.utils.data import DataLoader
from pytorch_lightning.loggers import TensorBoardLogger
from pytorch_lightning.strategies import DDPStrategy
from flask import Flask, session, render_template, request, redirect, url_for, send_from_directory
from auth import auth, login_required
from project import project
from dashboard import dashboard
# from tasks import tasks
from models import models
from runs import runs  # Import the new experiments blueprint
from datasets import dataset
from optimize import optimizations  # Correct the import to match the Blueprint name
from monitor import monitor_bp
from deploy import deploy_bp

app = Flask(__name__, static_url_path='/static')
app.register_blueprint(auth, url_prefix='/auth')

app.register_blueprint(project, url_prefix='/project')
app.register_blueprint(dataset, url_prefix='/datasets')
app.register_blueprint(models, url_prefix='/models')
app.register_blueprint(optimizations, url_prefix='/optimizations')
app.register_blueprint(runs, url_prefix='/runs')  # Register the experiments blueprint

app.register_blueprint(monitor_bp, url_prefix='/monitor')
app.register_blueprint(dashboard, url_prefix='/dashboard')

app.register_blueprint(deploy_bp, url_prefix='/deploy')
# app.register_blueprint(jobs, url_prefix='/jobs')

app.secret_key = 'SECRET_KEY_!!!'
app.config['SECRET_KEY'] = app.secret_key  # for debugging tool

@app.route('/')
@login_required
def root():
    return redirect(url_for('dashboard.root'))

@app.route('/<path:path>')
def static_proxy(path):
    return app.send_static_file(path)  # send_static_file will guess the correct MIME type


@app.route('/favicon.ico')
def favicon():
    try:
        return send_from_directory(
            os.path.join(app.root_path, 'static', 'images'),
            'favicon.ico',
            mimetype='image/vnd.microsoft.icon'
        )
    except Exception as e:
        app.logger.error(f"Error serving favicon: {str(e)}")
        return '', 204  # Return no content instead of 500 error

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
