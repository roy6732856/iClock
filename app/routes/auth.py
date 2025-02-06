from flask import Blueprint, request, jsonify
from app.models.admin import Admin
from app.utils.database import db
import jwt
from datetime import datetime, timedelta
from functools import wraps
import os

auth_bp = Blueprint('auth', __name__)

# JWT Configuration
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your-secret-key')  # 請在實際環境中使用環境變數
JWT_EXPIRATION_HOURS = 24

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            token = token.split(' ')[1]  # Remove 'Bearer ' prefix
            data = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
            current_admin = Admin.query.get(data['admin_id'])
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        
        return f(current_admin, *args, **kwargs)
    return decorated

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # 檢查必要欄位
    required_fields = ['username', 'email', 'password', 'role']
    if not all(field in data for field in required_fields):
        return jsonify({'message': '缺少必要欄位'}), 400
    
    # 驗證角色值
    if data['role'] not in [Admin.ROLE_ADMIN, Admin.ROLE_MANAGE]:
        return jsonify({'message': '無效的角色值，必須是 4 (admin) 或 8 (manage)'}), 400
    
    # 檢查使用者是否已存在
    if Admin.query.filter_by(username=data['username']).first():
        return jsonify({'message': '使用者名稱已存在'}), 400
    
    if Admin.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email已存在'}), 400
    
    # 創建新管理員
    new_admin = Admin(
        username=data['username'],
        email=data['email'],
        role=data['role']
    )
    new_admin.set_password(data['password'])
    
    db.session.add(new_admin)
    db.session.commit()
    
    return jsonify({
        'message': '註冊成功',
        'user': {
            'username': new_admin.username,
            'email': new_admin.email,
            'role': new_admin.role
        }
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': '缺少使用者名稱或密碼'}), 400
    
    admin = Admin.query.filter_by(username=data['username']).first()
    
    if not admin or not admin.check_password(data['password']):
        return jsonify({'message': '使用者名稱或密碼錯誤'}), 401
    
    if not admin.is_active:
        return jsonify({'message': '帳號已被停用'}), 401
    
    # 生成 JWT Token
    token = jwt.encode({
        'admin_id': admin.id,
        'username': admin.username,
        'role': admin.role,  # 加入角色資訊到 token 中
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    }, JWT_SECRET_KEY)
    
    return jsonify({
        'message': '登入成功',
        'token': token,
        'token_type': 'Bearer',
        'expires_in': JWT_EXPIRATION_HOURS * 3600,
        'user': {
            'username': admin.username,
            'role': admin.role
        }
    })
