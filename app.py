from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DATABASE = 'database.db'

# وظيفة للحصول على اتصال بقاعدة البيانات
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# الصفحة الرئيسية
@app.route('/')
def home():
    return "مرحباً، السيرفر يعمل بنجاح!"

# API لإنشاء حساب
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    if not username or not password or not confirm_password:
        return jsonify({"error": "يرجى إدخال جميع الحقول"}), 400

    if password != confirm_password:
        return jsonify({"error": "كلمات المرور غير متطابقة"}), 400

    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        return jsonify({"success": "تم إنشاء الحساب بنجاح"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "اسم المستخدم موجود بالفعل"}), 400
    finally:
        conn.close()

# API لتسجيل الدخول
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "يرجى إدخال اسم المستخدم وكلمة المرور"}), 400

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
    conn.close()

    if user:
        return jsonify({"success": f"مرحباً {username}!"}), 200
    return jsonify({"error": "بيانات تسجيل الدخول غير صحيحة"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
