import sys  
from pathlib import Path  
file = Path(__file__).resolve()
package_root_directory = file.parents [1]  
sys.path.append(str(package_root_directory))  

from flask_restful import Api
from flask import Flask
from line_api import LineApi
from dotenv import load_dotenv
import os

# Load all env
load_dotenv()
DEBUG=os.environ['DEBUG']


app = Flask(__name__)
api = Api(app)

api.add_resource(LineApi, '/api/v1/webhook')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=DEBUG)