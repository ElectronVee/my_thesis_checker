import os
from flask import Flask

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'uploads')
app.config['TEMP_IMAGE_FOLDER'] = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_images')

# 确保临时目录存在
if not os.path.exists(app.config['TEMP_IMAGE_FOLDER']):
    os.makedirs(app.config['TEMP_IMAGE_FOLDER'])

from app import routes  # 导入路由
