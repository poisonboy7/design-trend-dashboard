@echo off
chcp 65001 > nul

cd /d %~dp0

echo =========================
echo 라이브러리 설치중...
echo =========================

python -m pip install --upgrade pip
python -m pip install streamlit pandas plotly openpyxl

echo =========================
echo Dashboard 실행중...
echo =========================

python -m streamlit run app.py

pause