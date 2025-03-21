import os
from flask import Flask
from app.models import db

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'uploads')
app.config['TEMP_IMAGE_FOLDER'] = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_images')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost：3307/checker'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# 确保临时目录存在
if not os.path.exists(app.config['TEMP_IMAGE_FOLDER']):
    os.makedirs(app.config['TEMP_IMAGE_FOLDER'])

from app import routes  # 导入路由
