import sqlite3

conn = sqlite3.connect('database.db')
conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)')
conn.close()
print("تم إنشاء قاعدة البيانات وجدول المستخدمين بنجاح.")
