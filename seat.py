import time
import streamlit as st

st.set_page_config(page_title="온라인 1대1 오목 대전", page_icon="⚪", layout="centered")

st.title("⚪⚫ 온라인 1대1 오목 대전")
st.caption(
    "두 대의 기기(노트북/모바일)에서 접속하여 실시간으로 오목을 즐겨보세요!"
)

BOARD_SIZE = 15


# 서버 공용 데이터 저장소 (모든 연결된 사용자가 실시간 공유)
@st.cache_resource
def get_game_store():
    return {
        "board": [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)],
        "turn": 1,  # 1: 흑돌(Black), 2: 백돌(White)
        "players": {"black": None, "white": None},
        "last_move": None,
        "winner": 0,  # 0: 진행중, 1: 흑 승, 2: 백 승, 3: 무승부
        "move_count": 0,
    }


game = get_game_store()

# 세션 구분 ID 생성
if "user_id" not in st.session_state:
    st.session_state.user_id = str(time.time())


# 5목 승리 판정 함수
def check_win(board, r, c, player):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        # 정방향 탐색
        nr, nc = r + dr, c + dc
        while (
            0 <= nr < BOARD_SIZE
            and 0 <= nc < BOARD_SIZE
            and board[nr][nc] == player
        ):
            count += 1
            nr += dr
            nc += dc
        # 역방향 탐색
        nr, nc = r - dr, c - dc
        while (
            0 <= nr < BOARD_SIZE
            and 0 <= nc < BOARD_SIZE
            and board[nr][nc] == player
        ):
            count += 1
            nr -= dr
            nc -= dc
        if count >= 5:
            return True
    return False


# 플레이어 역할 확인
user_role = None
if game["players"]["black"] == st.session_state.user_id:
    user_role = 1
elif game["players"]["white"] == st.session_state.user_id:
    user_role = 2

# 참가 신청 사이드바
st.sidebar.header("🎮 대전 참가")
if user_role is None:
    st.sidebar.write("역할을 선택하여 게임에 참가하세요:")
    col_b, col_w = st.sidebar.columns(2)
    with col_b:
        if game["players"]["black"] is None:
            if st.button("⚫ 흑돌 참가"):
                game["players"]["black"] = st.session_state.user_id
                st.rerun()
        else:
            st.sidebar.caption("⚫ 흑돌: (참가완료)")

    with col_w:
        if game["players"]["white"] is None:
            if st.button("⚪ 백돌 참가"):
                game["players"]["white"] = st.session_state.user_id
                st.rerun()
        else:
            st.sidebar.caption("⚪ 백돌: (참가완료)")
else:
    role_str = "⚫ 흑돌 (선공)" if user_role == 1 else "⚪ 백돌 (후공)"
    st.sidebar.success(f"당신은 **{role_str}** 입니다.")

# 게임 리셋 버튼
if st.sidebar.button("🔄 게임 초기화 / 방 새로고침", use_container_width=True):
    game["board"] = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    game["turn"] = 1
    game["players"] = {"black": None, "white": None}
    game["last_move"] = None
    game["winner"] = 0
    game["move_count"] = 0
    st.rerun()

# 상단 대전 상태 정보 표시
st.divider()
status_col1, status_col2 = st.columns(2)

with status_col1:
    if game["winner"] == 0:
        if game["turn"] == 1:
            st.subheader("현재 턴: ⚫ 흑돌")
        else:
            st.subheader("현재 턴: ⚪ 백돌")
    elif game["winner"] == 1:
        st.success("🎉 ⚫ 흑돌 승리!")
    elif game["winner"] == 2:
        st.success("🎉 ⚪ 백돌 승리!")
    elif game["winner"] == 3:
        st.warning("🤝 무승부!")

with status_col2:
    ready_b = "✅ 준비완료" if game["players"]["black"] else "⏳ 대기중..."
    ready_w = "✅ 준비완료" if game["players"]["white"] else "⏳ 대기중..."
    st.write(f"⚫ 흑돌 플레이어: {ready_b}")
    st.write(f"⚪ 백돌 플레이어: {ready_w}")

# 내 턴인지 체크
is_my_turn = (
    (user_role == game["turn"])
    and (game["winner"] == 0)
    and (game["players"]["black"] is not None)
    and (game["players"]["white"] is not None)
)

if not is_my_turn and game["winner"] == 0:
    if user_role is None:
        st.info(
            "💡 관전 중입니다. 대전에 참가하시려면 좌측 사이드바에서 돌을 선택하세요."
        )
    elif game["players"]["black"] is None or game["players"]["white"] is None:
        st.info("💡 상대방이 들어오기를 기다리는 중입니다...")
    else:
        st.info("⏳ 상대방이 돌을 두기를 기다리는 중입니다...")

# 15x15 오목 바둑판
grid_container = st.container()

for r in range(BOARD_SIZE):
    cols = grid_container.columns(BOARD_SIZE)
    for c in range(BOARD_SIZE):
        cell_val = game["board"][r][c]

        if cell_val == 1:
            label = "⚫"
        elif cell_val == 2:
            label = "⚪"
        else:
            label = " "

        # 착수된 가장 마지막 수 강조
        if game["last_move"] == (r, c):
            if cell_val == 1:
                label = "⬛"
            elif cell_val == 2:
                label = "⬜"

        can_click = is_my_turn and (cell_val == 0)

        if cols[c].button(
            label,
            key=f"cell_{r}_{c}",
            disabled=not can_click,
            use_container_width=True,
        ):
            game["board"][r][c] = user_role
            game["last_move"] = (r, c)
            game["move_count"] += 1

            if check_win(game["board"], r, c, user_role):
                game["winner"] = user_role
            elif game["move_count"] >= BOARD_SIZE * BOARD_SIZE:
                game["winner"] = 3
            else:
                game["turn"] = 2 if user_role == 1 else 1

            st.rerun()

# 상대방 턴일 때 자동 폴링 (2초마다 화면 새로고침하여 수 확인)
if not is_my_turn and game["winner"] == 0:
    time.sleep(2)
    st.rerun()
