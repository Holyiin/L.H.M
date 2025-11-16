import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# ============================
# 1. 기본 스타일 설정
# ============================
st.set_page_config(page_title="우울 지표 심리학 대시보드", layout="wide")

# Custom CSS (부드러운 톤)
st.markdown("""
    <style>
        body {
            background-color: #F7F9FC;
        }
        .css-18e3th9 {
            padding-top: 2rem;
        }
        h1, h2, h3, h4 {
            color: #34495E;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🌿 우울감 경험률 & 우울증상 유병률 심리학 분석 대시보드")
st.caption("부드럽고 안정적인 색감 기반 — 2008~2023년 전국·지역·지표 비교 분석")

# ============================
# 2. CSV 자동 로드
# ============================
csv_path = "우울_지표_통합.csv"

if not os.path.exists(csv_path):
    st.error(f"❌ CSV 파일이 없습니다. 같은 폴더에 `{csv_path}` 를 넣어주세요.")
    st.stop()

df = pd.read_csv(csv_path, encoding="utf-8-sig")

# 숫자형 변환
for col in ["조사년도", "조율"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# ============================
# 3. 데이터 미리보기
# ============================
st.subheader("📌 데이터 미리보기")
st.dataframe(df.head(20))

# ============================
# 4. 필터 구성
# ============================
indicators = df["지표명"].unique().tolist()
indicator = st.sidebar.selectbox("지표 선택", indicators)

df_ind = df[df["지표명"] == indicator]

years = sorted(df_ind["조사년도"].dropna().unique())
year_selected = st.sidebar.slider("연도 선택", int(min(years)), int(max(years)), int(max(years)))

regions = sorted(df_ind[df_ind["지역구분"] == "시도"]["광역시도"].dropna().unique())
region_selected = st.sidebar.selectbox("지역 선택 (시도)", regions)

# 공통 색상 팔레트
pastel_palette = px.colors.qualitative.Pastel

# ============================
# 5. 전국 전체 지표 비교
# ============================
st.subheader("🌈 1. 전국 전체 지표 비교 (2008~2023)")

df_nat = df[df["지역구분"] == "전국"]
pivot_nat = df_nat.pivot_table(index="조사년도", columns="지표명", values="조율")

fig1 = px.line(
    pivot_nat,
    markers=True,
    color_discrete_sequence=pastel_palette,
    labels={"value": "조율 (%)", "조사년도": "연도"},
    title="전국 주요 지표 변화 추세"
)
fig1.update_layout(template="simple_white")
st.plotly_chart(fig1, use_container_width=True)

# ============================
# 6. 선택 지표 전국 추세
# ============================
st.subheader(f"💙 2. 전국 {indicator} 추세 (2008~2023)")

df_nat_ind = df_ind[df_ind["지역구분"] == "전국"].sort_values("조사년도")

fig2 = px.line(
    df_nat_ind,
    x="조사년도",
    y="조율",
    markers=True,
    title=f"전국 {indicator} 연도별 변화",
    color_discrete_sequence=["#6C5CE7"]
)
fig2.update_layout(template="simple_white")
st.plotly_chart(fig2, use_container_width=True)

# ============================
# 7. 특정 연도 시도별 그래프
# ============================
st.subheader(f"💚 3. {year_selected}년 시도별 {indicator} 비교")

df_year = df_ind[
    (df_ind["조사년도"] == year_selected) &
    (df_ind["지역구분"] == "시도")
].dropna(subset=["조율"])

fig3 = px.bar(
    df_year.sort_values("조율"),
    x="조율",
    y="광역시도",
    orientation="h",
    color="조율",
    color_continuous_scale=px.colors.sequential.Blues,
    title=f"{year_selected}년 시도별 {indicator}"
)
fig3.update_layout(template="simple_white")
st.plotly_chart(fig3, use_container_width=True)

# ============================
# 8. 전체 조율 히스토그램
# ============================
st.subheader("💜 4. 전체 시도 조율 분포 (히스토그램)")

df_hist = df_ind[df_ind["지역구분"] == "시도"]["조율"].dropna()

fig4 = px.histogram(
    df_hist,
    nbins=25,
    color_discrete_sequence=["#A29BFE"],
    title="전체 기간 조율 분포"
)
fig4.update_layout(template="simple_white")
st.plotly_chart(fig4, use_container_width=True)

# ============================
# 9. 특정 연도 박스플롯
# ============================
st.subheader(f"💛 5. {year_selected}년 시도 조율 박스플롯")

fig5 = go.Figure()
fig5.add_trace(go.Box(
    x=df_year["조율"],
    name="조율",
    marker_color="#FDCB6E"
))
fig5.update_layout(
    template="simple_white",
    title=f"{year_selected}년 시도 조율 분포"
)
st.plotly_chart(fig5, use_container_width=True)

# ============================
# 10. 선택 지역의 연도별 변화
# ============================
st.subheader(f"🌿 6. {region_selected} 지역 {indicator} 추세")

df_region = df_ind[
    (df_ind["지역구분"] == "시도") &
    (df_ind["광역시도"] == region_selected)
].sort_values("조사년도")

fig6 = px.line(
    df_region,
    x="조사년도",
    y="조율",
    markers=True,
    title=f"{region_selected} 지역 {indicator} 추세",
    color_discrete_sequence=["#55EFC4"]
)
fig6.update_layout(template="simple_white")
st.plotly_chart(fig6, use_container_width=True)

# ============================
st.markdown("---")
st.caption("🌱 부드러운 파스텔 컬러 기반의 심리학적 우울감 분석 대시보드")
st.markdown("""
---

## 🔍 자료 분석의 의의 및 활용 가치

### 1. 심리학적 관점에서의 의의
- 우울감 경험률과 우울증상 유병률은 개인의 정서적 어려움뿐 아니라 사회·환경적 스트레스 요인을 반영하는 핵심 지표입니다.  
- 특정 연도 또는 특정 지역에서 상승하는 패턴이 반복된다면, 이는 구조적 스트레스 요인(경제 불안, 사회적 고립, 감염병 유행 등)이 실제 심리 건강에 영향을 주고 있음을 시사합니다.
- 지역별 편차는 심리적 자원(심리상담 접근성, 지역 커뮤니티, 사회적 지지체계)의 차이를 보여주며, 예방·개입 전략의 필요성을 확인할 수 있습니다.

### 2. 보건·역학적 관점
- 우울증은 만성화되기 전 ‘우울감 경험’이라는 초기 신호가 존재하며, 두 지표를 함께 살피면 조기 위험 탐지(Early Detection)에 도움이 됩니다.
- 연도별 추세 분석은 특정 시기에 위험이 급증하는 이유를 규명하는 데 기초 자료가 됩니다.  
  예: 사회적 사건, 정책 변화, 감염병 유행 등.
- 지표 간 변동성을 분석하면 정신건강 정책의 효과성 또한 간접적으로 평가할 수 있습니다.

### 3. 정책적 활용 가치
- 지역 간 격차는 지자체 단위의 맞춤형 정신건강 정책 도입의 근거가 됩니다.  
  예: 상담센터 확충, 취약지역 집중 개입 등.
- 장기 추세 데이터(2008~2023)는 정책 변화 전후의 인구 정신건강 상태의 개선·악화를 비교하는 데 매우 유용합니다.
- 연령·지역별로 취약군(potential risk group)을 선별하여 예방 중심의 접근을 가능하게 합니다.

### 4. 본 대시보드가 제공하는 가치
- 복잡한 정신건강 데이터를 누구나 쉽게 접근·해석할 수 있도록 시각화하여 인지적 부담을 줄였습니다.
- 과거부터 현재까지 연속적으로 변화하는 데이터를 비교함으로써, 단일 연도 분석보다 훨씬 깊이 있는 통찰을 제공합니다.
- 시도별 분석과 전국 추세 비교는 “정책적 우선순위” 설정에 도움을 줍니다.
- 연구자, 보건소, 정책 담당자뿐 아니라 일반 국민도 자신이 속한 지역의 정신건강 현황을 쉽게 이해할 수 있습니다.

---

### 🧠 결론
우울감·우울증 유병률 데이터는 단순한 숫자가 아니라  
**사람들의 심리 상태, 사회적 환경, 지역 특성, 정책 효과**가 반영된 복합적 지표입니다.  
대시보드를 통해 이러한 변화를 시각적으로 확인함으로써  
**보다 정확한 문제 인식과 효과적인 정신건강 지원 전략 수립**이 가능합니다.

---
""")
