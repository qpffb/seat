import random
import time
import streamlit as st

st.set_page_config(page_title="야바위 게임", page_icon="🎪", layout="centered")

st.title("🎪 진짜 야바위 게임")
st.write("공이 들어있는 컵을 맞춰보세요! 컵은 총 3개입니다.")

# 게임 상태 초기화
if "ball_position" not in st.session_state:
    st.session_state.ball_position = random.randint(0, 2)
if "score" not in st.session_state:
    st.session_state.score = 0
if "total_games" not in st.session_state:
    st.session_state.total_games = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "selected_cup" not in st.session_state:
    st.session_state.selected_cup = None

# 점수판 표시
col_score1, col_score2 = st.columns(2)
with col_score1:
    st.metric(label="맞힌 횟수", value=f"{st.session_state.score}회")
with col_score2:
    st.metric(label="전체 판수", value=f"{st.session_state.total_games}회")

st.divider()

# 컵 버튼 영역
cols = st.columns(3)

for i in range(3):
    with cols[i]:
        # 선택 전 / 선택 후 상태에 따라 컵 모양 표시
        if not st.session_state.game_over:
            cup_label = f"🥤 컵 {i + 1}"
        else:
            if i == st.session_state.ball_position:
                cup_label = f"⚽ (공 발견!)\n컵 {i + 1}"
            elif i == st.session_state.selected_cup:
                cup_label = f"❌ (꽝!)\n컵 {i + 1}"
            else:
                cup_label = f"🥤 컵 {i + 1}"

        if st.button(
            cup_label,
            key=f"cup_{i}",
            use_container_width=True,
            disabled=st.session_state.game_over,
        ):
            st.session_state.selected_cup = i
            st.session_state.total_games += 1
            st.session_state.game_over = True

            if i == st.session_state.ball_position:
                st.session_state.score += 1
                st.balloons()
            st.rerun()

# 게임 결과 및 다시하기 버튼
if st.session_state.game_over:
    if st.session_state.selected_cup == st.session_state.ball_position:
        st.success(
            f"🎉 축하합니다! {st.session_state.selected_cup + 1}번 컵에 공이 있었습니다!"
        )
    else:
        st.error(
            f"😅 틀렸습니다! {st.session_state.selected_cup + 1}번은 비어있고, 공은 {st.session_state.ball_position + 1}번 컵에 있었습니다."
        )

    if st.button("🔄 다음 판 하기", use_container_width=True):
        st.session_state.ball_position = random.randint(0, 2)
        st.session_state.game_over = False
        st.session_state.selected_cup = None
        st.rerun()
