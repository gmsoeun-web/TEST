import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# 페이지 설정 (모바일 환경에 맞게 레이아웃 조정)
st.set_page_config(page_title="현장 자재 관리", layout="centered")

# 데이터베이스 연결 및 테이블 생성 함수
def init_db():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    # 자재 입출고 기록 테이블
    c.execute('''
        CREATE TABLE IF NOT EXISTS material_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            user_name TEXT,
            material_name TEXT,
            action_type TEXT,
            quantity INTEGER,
            memo TEXT
        )
    ''')
    conn.commit()
    return conn

conn = init_db()

# 데이터 삽입 함수
def insert_log(user, material, action, qty, memo):
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO material_logs (timestamp, user_name, material_name, action_type, quantity, memo) VALUES (?, ?, ?, ?, ?, ?)",
              (timestamp, user, material, action, qty, memo))
    conn.commit()

# 전체 기록 조회 함수
def load_data():
    return pd.read_sql("SELECT * FROM material_logs ORDER BY timestamp DESC", conn)