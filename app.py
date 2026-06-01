import os
import streamlit as st
import pandas as pd
import plotly.express as px

# 💡 우리가 분리한 3개의 부품 파일(.py)에서 필요한 재료들을 소환합니다!
from config import TONE_COLORS
from styles import APPLE_STYLE
from utils import (
    apply_chart_style, classify_font, hex_to_tone, 
    make_color_chip, make_google_link, get_mode
)

# =========================================================
# 1. 페이지 레이아웃 세팅 및 CSS 주입
# =========================================================
st.set_page_config(
    page_title="Design Trend Dashboard",
    page_icon="🎨",
    layout="wide"
)

st.markdown(APPLE_STYLE, unsafe_allow_html=True)


# =========================================================
# 5. 데이터 캐싱 로드 및 전처리
# =========================================================
@st.cache_data
def load_data(file_source):
    df = pd.read_excel(file_source, engine="openpyxl")
    df.columns = df.columns.str.strip()
    
    # 데이터 컬럼 구조 표준화 리네이밍
    df = df.rename(columns={'header_color': 'header_area_color', 'hero_color': 'main_visual_color'})
    
    # 분리된 조립용 모듈(utils)의 함수 적용
    df['font_type'] = df['font_family'].apply(classify_font)
    df['header_area_tone'] = df['header_area_color'].apply(hex_to_tone)
    df['main_visual_tone'] = df['main_visual_color'].apply(hex_to_tone)
    
    return df


# =========================================================
# 6. 인풋 소스 유효성 확인 및 로드 실행
# =========================================================
st.sidebar.title("🎛️ Report")

uploaded_file = st.sidebar.file_uploader("분석용 엑셀 파일 업로드", type=["xlsx"])
DEFAULT_FILE = "design_data.xlsx"

active_file = uploaded_file if uploaded_file else (DEFAULT_FILE if os.path.exists(DEFAULT_FILE) else None)

if active_file is None:
    st.title("🎨 Design Trend Dashboard")
    st.info("왼쪽 사이드바에서 엑셀 파일을 업로드해주세요.")
    st.stop()

try:
    df = load_data(active_file)
except Exception as e:
    st.error(f"파일 로드 오류 : {e}")
    st.stop()


# =========================================================
# 7. 카테고리 필터 필터링 제어
# =========================================================
categories = ['전체'] + sorted(df['service_category'].dropna().unique())
category = st.sidebar.selectbox("서비스 카테고리", categories)

filtered_df = df if category == '전체' else df[df['service_category'] == category]


# =========================================================
# 8. 대시보드 대표 스코어보드 변수 연산
# =========================================================
top_font = get_mode(filtered_df['font_family'])
top_title = get_mode(filtered_df['header_area_tone'])
top_visual = get_mode(filtered_df['main_visual_tone'])
top_font_type = classify_font(top_font)

badge_title_color = TONE_COLORS.get(top_title, '#6B7280')
badge_visual_color = TONE_COLORS.get(top_visual, '#6B7280')


# =========================================================
# 9. 메인 타이틀 및 상단 KPI 카드 컴포넌트 렌더링
# =========================================================
st.title("🎨 Design Trend Dashboard")
st.caption("클릭 성과 기반 디자인 트렌드 분석")

c1, c2, c3 = st.columns(3)

def kpi_card(title, value, emoji, color):
    st.markdown(f"""
    <div class="kpi-card">
        <div style="font-size:18px; color:#9CA3AF; margin-bottom:10px; font-weight:600;">
            {emoji} {title}
        </div>
        <div style="font-size:44px; font-weight:800; color:{color}; text-shadow:0 0 2px {color}; line-height:1;">
            {value}
        </div>
    </div>
    """, unsafe_allow_html=True)

with c1:
    kpi_card("대표 메인 타이틀 톤", top_title, "🎨", badge_title_color)
with c2:
    kpi_card("가장 많이 사용된 폰트", top_font, "✍️", "#FFFFFF")
with c3:
    kpi_card("메인 비주얼 컬러 톤", top_visual, "🖼️", badge_visual_color)


# =========================================================
# 10. 반응형 인터랙티브 차트 및 스태틱 테이블 뷰 출력
# =========================================================
if not filtered_df.empty:

    # 성과 지표 기준 상위 20 랭킹 테이블 렌더링
    st.subheader("📋 성과 상위 데이터 TOP20")
    
    top_data = filtered_df.sort_values(by='word_count', ascending=False).head(20)
    display_df = top_data.copy().fillna('')

    # 가독성을 높이기 위한 유틸리티 맵핑 컴파일
    display_df['service_name'] = display_df['service_name'].apply(lambda x: make_google_link(x))
    display_df['font_family'] = display_df['font_family'].apply(lambda x: make_google_link(x))
    display_df['header_area_color'] = display_df['header_area_color'].apply(make_color_chip)
    display_df['main_visual_color'] = display_df['main_visual_color'].apply(make_color_chip)

    st.caption("※ word_count는 클릭 성과 기반 핵심 지표입니다.")
    st.markdown(display_df.to_html(escape=False, index=False), unsafe_allow_html=True)
    st.divider()

    # 다단 정렬 차트 시각화 레이아웃
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🎨 메인 타이틀 톤별 평균 클릭 성과")
        tone_perf = filtered_df.groupby('header_area_tone')['word_count'].mean().reset_index()
        tone_perf = tone_perf.sort_values(by='word_count', ascending=False).head(5)

        fig1 = px.bar(
            tone_perf, x='header_area_tone', y='word_count',
            color='header_area_tone', color_discrete_map=TONE_COLORS
        )
        st.plotly_chart(apply_chart_style(fig1, 420), use_container_width=True)

    with col2:
        st.subheader("🏆 가장 많이 사용된 폰트 TOP5")
        font_rank = filtered_df['font_family'].value_counts().head(5).reset_index()
        font_rank.columns = ['font', 'count']

        fig2 = px.bar(font_rank, x='font', y='count', color='count', color_continuous_scale='Blues')
        st.plotly_chart(apply_chart_style(fig2, 420), use_container_width=True)

    # 비주얼 파이 차트 및 분석 기준 설명문
    st.subheader("🖼️ 메인 비주얼 컬러 비율")
    visual = filtered_df['main_visual_tone'].value_counts().reset_index()
    visual.columns = ['tone', 'count']

    fig3 = px.pie(
        visual, names='tone', values='count', 
        color='tone', color_discrete_map=TONE_COLORS, hole=0.6
    )
    st.plotly_chart(apply_chart_style(fig3, 520), use_container_width=True)

    st.markdown("""
    <div style="background:#111827; padding:24px; border-radius:20px; border:1px solid rgba(255,255,255,0.08); margin:30px 0; line-height:2; font-size:15px; color:#D1D5DB;">
        <h3 style="margin-top:0; color:white; font-size:24px;">💡 RGB → HSV 톤 분류 기준</h3>
        HEX 컬러값을 HSV 색상 체계로 변환 후 Hue 각도를 기준으로 자동 분류합니다.
        <ul>
            <li>🔴 빨강 : 0° ~ 20° / 330° ~ 360°</li>
            <li>🟠 주황 : 20° ~ 45°</li>
            <li>🟡 노랑 : 45° ~ 70°</li>
            <li>🟢 초록 : 70° ~ 160°</li>
            <li>🔵 파랑 : 160° ~ 260°</li>
            <li>🟣 보라 : 260° ~ 330°</li>
            <li>⚪ 무채색 : Saturation &lt; 0.15</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # 자동 리포트 생성 섹션
    st.divider()
    st.subheader("🤖 자동 생성 인텔리전스 디자인 인사이트")
    st.markdown(f"""
    <div style="background:linear-gradient(135deg, rgba(17,24,39,0.95), rgba(30,41,59,0.95)); padding:32px; border-radius:24px; border:1px solid rgba(255,255,255,0.08); box-shadow:0 10px 30px rgba(0,0,0,0.35);">
        <h3 style="margin-top:0; color:white; font-size:28px; font-weight:800;">📊 [{category}] 자동화 비주얼 전략 분석 리포트</h3>
        <div style="margin-top:28px; line-height:2.4; font-size:18px; color:#E5E7EB;">
            🎨 대표 메인 타이틀 : <b>{top_title}</b><br>
            🖼️ 대표 메인 비주얼 : <b>{top_visual}</b><br>
            ✍️ 대표 폰트 : <b>{top_font}</b> ({top_font_type} 계열)
        </div>
        <hr style="border:none; border-top:1px solid rgba(255,255,255,0.08); margin:28px 0;">
        <div style="color:#CBD5E1; font-size:16px; line-height:1.9;">
            AI 분석 결과 현재 카테고리에서는 위 조합이 가장 높은 사용자 반응과 클릭 성과를 보이는 디자인 패턴으로 분석됩니다.
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    st.info("조건에 맞는 데이터가 없습니다.")