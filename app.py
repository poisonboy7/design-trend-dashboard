import os
import colorsys
import urllib.parse
import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# 1. 페이지 기본 설정
# =========================================================
st.set_page_config(
    page_title="Design Trend Dashboard",
    page_icon="🎨",
    layout="wide"
)

# =========================================================
# 2. 컬러 톤 맵
# =========================================================
TONE_COLORS = {
    '빨강': '#EF4444',
    '주황': '#F97316',
    '노랑': '#EAB308',
    '초록': '#22C55E',
    '파랑': '#3B82F6',
    '보라': '#A855F7',
    '무채색': '#9CA3AF',
    '알수없음': '#6B7280'
}

# =========================================================
# 3. Apple 스타일 CSS
# =========================================================
APPLE_STYLE = """
<style>

@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

html, body, [class*="css"]{
    font-family:'Pretendard', sans-serif;
    background:#050816;
    color:white;
}

/* 사이드바 */
section[data-testid="stSidebar"]{
    background:#0B1220;
}

/* 메인 영역 */
.block-container{
    max-width:1600px;
    margin:auto;
    padding-top:2rem;
    padding-left:3rem;
    padding-right:3rem;
}

/* 메인 타이틀 */
h1{
    font-size:56px !important;
    font-weight:800 !important;
    letter-spacing:-1px;
}

/* KPI 카드 */
.kpi-card{
    background:linear-gradient(
        135deg,
        rgba(17,24,39,0.96),
        rgba(30,41,59,0.96)
    );
    border-radius:24px;
    padding:30px;
    border:1px solid rgba(255,255,255,0.08);
    box-shadow:0 10px 25px rgba(0,0,0,0.18);
    min-height:148px;
    transition:all .3s ease;
}

.kpi-card:hover{
    transform:translateY(-5px);
    box-shadow:0 8px 16px rgba(0,0,0,0.45),
    0 2px 4px rgba(0,0,0,0.25);
}

/* 테이블 */
table{
    width:100%;
    border-collapse:collapse;
    background:#0F172A;
    border-radius:16px;
    overflow:hidden;
    font-size:14px;
}

/* 헤더 */
th{
    background:#111827;
    color:white;
    padding:12px 10px;
    text-align:left;
    white-space:nowrap;
}

/* 셀 */
td{
    padding:10px 8px;
    border-bottom:1px solid rgba(255,255,255,0.06);
    color:white;
    vertical-align:middle;
}

/* Hover */
tr:hover{
    background:rgba(255,255,255,0.03);
}

/* 링크 */
a{
    color:#60A5FA !important;
    text-decoration:none;
    font-weight:600;
}

a:hover{
    text-decoration:underline;
}

</style>
"""

st.markdown(APPLE_STYLE, unsafe_allow_html=True)

# =========================================================
# 4. 공통 함수
# =========================================================

# ---------------------------------------------------------
# 차트 공통 스타일
# ---------------------------------------------------------
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

        hoverlabel=dict(
            bgcolor="#111827",
            font_size=14
        ),

        xaxis=dict(
            gridcolor='rgba(255,255,255,0.05)'
        ),

        yaxis=dict(
            gridcolor='rgba(255,255,255,0.05)'
        )
    )

    return fig


# ---------------------------------------------------------
# 폰트 분류
# ---------------------------------------------------------
def classify_font(font):

    if pd.isna(font):
        return '기타'

    font = str(font).lower()

    gothic_keywords = [
        'gothic',
        'sans',
        'pretendard',
        'inter',
        'roboto',
        'sf pro'
    ]

    myeongjo_keywords = [
        'myeongjo',
        'serif',
        'batang'
    ]

    if any(x in font for x in gothic_keywords):
        return '고딕'

    if any(x in font for x in myeongjo_keywords):
        return '명조'

    return '기타'


# ---------------------------------------------------------
# HEX → 컬러 톤
# ---------------------------------------------------------
def hex_to_tone(hex_val):

    if pd.isna(hex_val):
        return '알수없음'

    try:

        hex_val = str(hex_val).strip()

        if not hex_val.startswith('#'):
            hex_val = '#' + hex_val

        if len(hex_val) != 7:
            return '알수없음'

        r = int(hex_val[1:3], 16) / 255
        g = int(hex_val[3:5], 16) / 255
        b = int(hex_val[5:7], 16) / 255

        h, s, v = colorsys.rgb_to_hsv(r, g, b)

        if s < 0.15 or v < 0.2:
            return '무채색'

        h *= 360

        if h < 20 or h >= 330:
            return '빨강'

        if h < 45:
            return '주황'

        if h < 70:
            return '노랑'

        if h < 160:
            return '초록'

        if h < 260:
            return '파랑'

        return '보라'

    except:
        return '알수없음'


# ---------------------------------------------------------
# 컬러칩 생성
# ---------------------------------------------------------
def make_color_chip(hex_code):

    if pd.isna(hex_code):
        return ''

    hex_code = str(hex_code).strip()

    if not (
        hex_code.startswith('#')
        and len(hex_code) == 7
    ):
        return hex_code

    try:

        r = int(hex_code[1:3], 16)
        g = int(hex_code[3:5], 16)
        b = int(hex_code[5:7], 16)

        brightness = (
            r*299 + g*587 + b*114
        ) / 1000

        text_color = (
            'black'
            if brightness > 160
            else 'white'
        )

        return (
            f'<div style="'
            f'background:{hex_code};'
            f'color:{text_color};'
            f'padding:4px 8px;'
            f'border-radius:6px;'
            f'font-size:12px;'
            f'font-weight:600;'
            f'display:inline-block;'
            f'min-width:75px;'
            f'text-align:center;'
            f'">{hex_code}</div>'
        )

    except:
        return hex_code


# ---------------------------------------------------------
# 서비스명 링크
# ---------------------------------------------------------
def make_google_link(text):

    if pd.isna(text) or text == '':
        return ''

    text = str(text)

    query = urllib.parse.quote(text)

    search_url = (
        f"https://www.google.com/search?q={query}"
    )

    return (
        f'<a href="{search_url}" '
        f'target="_blank">{text}</a>'
    )


# ---------------------------------------------------------
# 폰트 링크
# ---------------------------------------------------------
def make_font_link(font_name):

    if pd.isna(font_name) or font_name == '':
        return ''

    font_name = str(font_name)

    query = urllib.parse.quote(
        f"{font_name} font"
    )

    search_url = (
        f"https://www.google.com/search?q={query}"
    )

    return (
        f'<a href="{search_url}" '
        f'target="_blank">{font_name}</a>'
    )


# ---------------------------------------------------------
# 최빈값
# ---------------------------------------------------------
def get_mode(series):

    series = series.dropna()

    return (
        series.mode()[0]
        if not series.empty
        else "데이터 없음"
    )


# =========================================================
# 5. 데이터 로드
# =========================================================
@st.cache_data
def load_data(file_source):

    df = pd.read_excel(
        file_source,
        engine="openpyxl"
    )

    df.columns = df.columns.str.strip()

    df = df.rename(columns={
        'header_color':'header_area_color',
        'hero_color':'main_visual_color'
    })

    df['font_type'] = (
        df['font_family']
        .apply(classify_font)
    )

    df['header_area_tone'] = (
        df['header_area_color']
        .apply(hex_to_tone)
    )

    df['main_visual_tone'] = (
        df['main_visual_color']
        .apply(hex_to_tone)
    )

    return df


# =========================================================
# 6. 파일 업로드
# =========================================================
st.sidebar.title("🎛️ Report")

uploaded_file = st.sidebar.file_uploader(
    "분석용 엑셀 파일 업로드",
    type=["xlsx"]
)

DEFAULT_FILE = "design_data.xlsx"

active_file = (
    uploaded_file
    if uploaded_file
    else (
        DEFAULT_FILE
        if os.path.exists(DEFAULT_FILE)
        else None
    )
)

if active_file is None:

    st.title("🎨 Design Trend Dashboard")

    st.info(
        "왼쪽 사이드바에서 엑셀 파일을 업로드해주세요."
    )

    st.stop()

try:

    df = load_data(active_file)

except Exception as e:

    st.error(f"파일 로드 오류 : {e}")

    st.stop()


# =========================================================
# 7. 필터
# =========================================================
categories = ['전체'] + sorted(
    df['service_category']
    .dropna()
    .unique()
)

category = st.sidebar.selectbox(
    "서비스 카테고리",
    categories
)

filtered_df = (
    df
    if category == '전체'
    else df[
        df['service_category'] == category
    ]
)


# =========================================================
# 8. 대표 데이터
# =========================================================
top_font = get_mode(
    filtered_df['font_family']
)

top_title = get_mode(
    filtered_df['header_area_tone']
)

top_visual = get_mode(
    filtered_df['main_visual_tone']
)

top_font_type = classify_font(top_font)

badge_title_color = (
    TONE_COLORS.get(
        top_title,
        '#6B7280'
    )
)

badge_visual_color = (
    TONE_COLORS.get(
        top_visual,
        '#6B7280'
    )
)


# =========================================================
# 9. 헤더
# =========================================================
st.title("🎨 Design Trend Dashboard")

st.caption(
    "클릭 성과 기반 디자인 트렌드 분석"
)

# KPI 카드
c1, c2, c3 = st.columns(3)

def kpi_card(title, value, emoji, color):

    st.markdown(f"""
    <div class="kpi-card">

    <div style="
    font-size:18px;
    color:#9CA3AF;
    margin-bottom:10px;
    font-weight:600;
    ">
    {emoji} {title}
    </div>

    <div style="
    font-size:44px;
    font-weight:800;
    color:{color};
    text-shadow:0 0 2px {color};
    line-height:1;
    ">
    {value}
    </div>

    </div>
    """, unsafe_allow_html=True)


with c1:
    kpi_card(
        "대표 메인 타이틀 톤",
        top_title,
        "🎨",
        badge_title_color
    )

with c2:
    kpi_card(
        "가장 많이 사용된 폰트",
        top_font,
        "✍️",
        "#FFFFFF"
    )

with c3:
    kpi_card(
        "메인 비주얼 컬러 톤",
        top_visual,
        "🖼️",
        badge_visual_color
    )


# =========================================================
# 데이터 존재 시 분석
# =========================================================
if not filtered_df.empty:

    # =====================================================
    # 상위 데이터
    # =====================================================
    st.subheader(
        "📋 성과 상위 데이터 TOP20"
    )

    top_data = (
        filtered_df
        .sort_values(
            by='word_count',
            ascending=False
        )
        .head(20)
    )

    display_df = (
        top_data
        .copy()
        .fillna('')
    )

    display_df['service_name'] = (
        display_df['service_name']
        .apply(make_google_link)
    )

    display_df['font_family'] = (
        display_df['font_family']
        .apply(make_font_link)
    )

    display_df['header_area_color'] = (
        display_df['header_area_color']
        .apply(make_color_chip)
    )

    display_df['main_visual_color'] = (
        display_df['main_visual_color']
        .apply(make_color_chip)
    )

    st.caption(
        "※ word_count는 클릭 성과 기반 핵심 지표입니다."
    )

    st.markdown(
        display_df.to_html(
            escape=False,
            index=False
        ),
        unsafe_allow_html=True
    )

    st.divider()

    # =====================================================
    # 차트
    # =====================================================
    col1, col2 = st.columns(2)

    # 메인 타이틀 성과
    with col1:

        st.subheader(
            "🎨 메인 타이틀 톤별 평균 클릭 성과"
        )

        tone_perf = (
            filtered_df
            .groupby('header_area_tone')['word_count']
            .mean()
            .reset_index()
            .sort_values(
                by='word_count',
                ascending=False
            )
            .head(5)
        )

        fig1 = px.bar(
            tone_perf,
            x='header_area_tone',
            y='word_count',
            color='header_area_tone',
            color_discrete_map=TONE_COLORS
        )

        st.plotly_chart(
            apply_chart_style(fig1, 420),
            use_container_width=True
        )

    # 폰트 TOP5
    with col2:

        st.subheader(
            "🏆 가장 많이 사용된 폰트 TOP5"
        )

        font_rank = (
            filtered_df['font_family']
            .value_counts()
            .head(5)
            .reset_index()
        )

        font_rank.columns = [
            'font',
            'count'
        ]

        fig2 = px.bar(
            font_rank,
            x='font',
            y='count',
            color='count',
            color_continuous_scale='Blues'
        )

        st.plotly_chart(
            apply_chart_style(fig2, 420),
            use_container_width=True
        )

    # =====================================================
    # 메인 비주얼 컬러 비율
    # =====================================================
    st.subheader(
        "🖼️ 메인 비주얼 컬러 비율"
    )

    visual = (
        filtered_df['main_visual_tone']
        .value_counts()
        .reset_index()
    )

    visual.columns = [
        'tone',
        'count'
    ]

    fig3 = px.pie(
        visual,
        names='tone',
        values='count',
        color='tone',
        color_discrete_map=TONE_COLORS,
        hole=0.6
    )

    st.plotly_chart(
        apply_chart_style(fig3, 520),
        use_container_width=True
    )

    # =====================================================
    # RGB 설명
    # =====================================================
    st.markdown("""
    <div style="
    background:#111827;
    padding:24px;
    border-radius:20px;
    border:1px solid rgba(255,255,255,0.08);
    margin:30px 0;
    line-height:2;
    font-size:15px;
    color:#D1D5DB;
    ">

    <h3 style="
    margin-top:0;
    color:white;
    font-size:24px;
    ">
    💡 RGB → HSV 톤 분류 기준
    </h3>

    HEX 컬러값을 HSV 색상 체계로 변환 후
    Hue 각도를 기준으로 자동 분류합니다.

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

    # =====================================================
    # 자동 생성 인사이트
    # =====================================================
    st.divider()

    st.subheader(
        "🤖 자동 생성 인텔리전스 디자인 인사이트"
    )

    st.markdown(f"""
    <div style="
    background:linear-gradient(
    135deg,
    rgba(17,24,39,0.95),
    rgba(30,41,59,0.95)
    );
    padding:32px;
    border-radius:24px;
    border:1px solid rgba(255,255,255,0.08);
    box-shadow:0 10px 30px rgba(0,0,0,0.35);
    ">

    <h3 style="
    margin-top:0;
    color:white;
    font-size:28px;
    font-weight:800;
    ">
    📊 [{category}] 자동화 비주얼 전략 분석 리포트
    </h3>

    <div style="
    margin-top:28px;
    line-height:2.4;
    font-size:18px;
    color:#E5E7EB;
    ">

    🎨 대표 메인 타이틀 :
    <b>{top_title}</b><br>

    🖼️ 대표 메인 비주얼 :
    <b>{top_visual}</b><br>

    ✍️ 대표 폰트 :
    <b>{top_font}</b>
    ({top_font_type} 계열)

    </div>

    <hr style="
    border:none;
    border-top:1px solid rgba(255,255,255,0.08);
    margin:28px 0;
    ">

    <div style="
    color:#CBD5E1;
    font-size:16px;
    line-height:1.9;
    ">

    AI 분석 결과 현재 카테고리에서는 위 조합이
    가장 높은 사용자 반응과 클릭 성과를 보이는
    디자인 패턴으로 분석됩니다.

    </div>

    </div>
    """, unsafe_allow_html=True)

else:

    st.info(
        "조건에 맞는 데이터가 없습니다."
    )