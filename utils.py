import colorsys
import urllib.parse
import pandas as pd

# 차트 공통 스타일 적용 함수
def apply_chart_style(fig, height=500):
    fig.update_layout(
        paper_bgcolor='#050816',
        plot_bgcolor='#050816',
        font_color='white',
        height=height,
        legend_title_text='',
        xaxis_title='',
        yaxis_title='',
        margin=dict(l=20, r=20, t=40, b=20),
        hoverlabel=dict(bgcolor="#111827", font_size=14),
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)')
    )
    return fig


# 폰트 대분류 함수
def classify_font(font):
    if pd.isna(font):
        return '기타'
    
    font = str(font).lower()
    if any(x in font for x in ['gothic', 'sans', 'pretendard', 'inter', 'roboto', 'sf pro']):
        return '고딕'
    if any(x in font for x in ['myeongjo', 'serif', 'batang']):
        return '명조'
    return '기타'


# HEX → 인간의 컬러 톤 변환 함수
def hex_to_tone(hex_val):
    if pd.isna(hex_val):
        return '알수없음'
        
    try:
        hex_val = str(hex_val).strip()
        if not hex_val.startswith('#'):
            hex_val = '#' + hex_val

        if len(hex_val) != 7:
            return '알수없음'

        r = int(hex_val[1:3], 16) / 255.0
        g = int(hex_val[3:5], 16) / 255.0
        b = int(hex_val[5:7], 16) / 255.0

        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        if s < 0.15 or v < 0.2:
            return '무채색'

        h *= 360
        if h < 20 or h >= 330:
            return '빨강'
        elif h < 45:
            return '주황'
        elif h < 70:
            return '노랑'
        elif h < 160:
            return '초록'
        elif h < 260:
            return '파랑'
        return '보라'
    except Exception:
        return '알수없음'


# 데이터 테이블 내 컬러칩 컴포넌트 생성 함수
def make_color_chip(hex_code):
    if pd.isna(hex_code):
        return ''

    hex_code = str(hex_code).strip()
    if not (hex_code.startswith('#') and len(hex_code) == 7):
        return hex_code

    try:
        r = int(hex_code[1:3], 16)
        g = int(hex_code[3:5], 16)
        b = int(hex_code[5:7], 16)

        brightness = (r * 299 + g * 587 + b * 114) / 1000
        text_color = 'black' if brightness > 160 else 'white'

        return f'<div style="background:{hex_code}; color:{text_color}; padding:4px 8px; border-radius:6px; font-size:12px; font-weight:600; display:inline-block; min-width:75px; text-align:center;">{hex_code}</div>'
    except Exception:
        return hex_code


# 구글 연동 다이렉트 하이퍼링크 생성 함수
def make_google_link(text, suffix=""):
    if pd.isna(text) or text == '':
        return ''
    text = str(text)
    query = urllib.parse.quote(f"{text} {suffix}".strip())
    return f'<a href="https://www.google.com/search?q={query}" target="_blank">{text}</a>'


# 최빈값(가장 높은 빈도수) 연산 함수
def get_mode(series):
    active_series = series.dropna()
    return active_series.mode().iloc[0] if not active_series.empty else "데이터 없음"