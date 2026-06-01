# =========================================================
# 3. Apple 스타일 CSS 스크립트 테마 정의
# =========================================================
APPLE_STYLE = """
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

html, body, [class*="css"] {
    font-family: 'Pretendard', sans-serif;
    background: #050816;
    color: white;
}

/* 사이드바 */
section[data-testid="stSidebar"] {
    background: #0B1220;
}

/* 메인 영역 */
.block-container {
    max-width: 1600px;
    margin: auto;
    padding-top: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

/* 메인 타이틀 */
h1 {
    font-size: 56px !important;
    font-weight: 800 !important;
    letter-spacing: -1px;
}

/* KPI 카드 */
.kpi-card {
    background: linear-gradient(
        135deg,
        rgba(17,24,39,0.96),
        rgba(30,41,59,0.96)
    );
    border-radius: 24px;
    padding: 30px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 10px 25px rgba(0,0,0,0.18);
    min-height: 148px;
    transition: all .3s ease;
}

.kpi-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 16px rgba(0,0,0,0.45), 0 2px 4px rgba(0,0,0,0.25);
}

/* 테이블 */
table {
    width: 100%;
    border-collapse: collapse;
    background: #0F172A;
    border-radius: 16px;
    overflow: hidden;
    font-size: 14px;
}

/* 헤더 */
th {
    background: #111827;
    color: white;
    padding: 12px 10px;
    text-align: left;
    white-space: nowrap;
}

/* 셀 */
td {
    padding: 10px 8px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    color: white;
    vertical-align: middle;
}

/* Hover */
tr:hover {
    background: rgba(255,255,255,0.03);
}

/* 링크 */
a {
    color: #60A5FA !important;
    text-decoration: none;
    font-weight: 600;
}

a:hover {
    text-decoration: underline;
}
</style>
"""