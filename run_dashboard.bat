@echo off
chcp 65001 > nul
cd /d "%~dp0"

:: 1. 필수 라이브러리가 이미 설치되어 있는지 파이썬 명령어로 무소음 검사
python -c "import streamlit, pandas, plotly, openpyxl" 2>nul
if %errorlevel% equ 0 (
    :: 이미 설치되어 있다면 설치 단계를 건너뛰고 즉시 실행으로 이동
    goto RUN_DASHBOARD
)

echo ==========================================
echo [안내] 필수 라이브러리가 없어 설치를 시작합니다.
echo      (최초 1회만 실행되며 약간의 시간이 소요됩니다)
echo ==========================================
python -m pip install --upgrade pip
python -m pip install streamlit pandas plotly openpyxl
cls

:RUN_DASHBOARD
echo ==========================================
echo   🎨 Design Trend Dashboard 실행 중...
echo ==========================================
python -m streamlit run app.py

pause