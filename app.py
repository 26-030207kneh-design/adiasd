import os
import random
import pandas as pd
import streamlit as st

LEADERBOARD_FILE = "leaderboard.csv"


# 랭킹 데이터 로드 및 저장 함수
def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        return pd.read_csv(LEADERBOARD_FILE)
    return pd.DataFrame(columns=["이름", "시도 횟수"])


def save_leaderboard(name, attempts):
    df = load_leaderboard()
    new_data = pd.DataFrame([{"이름": name, "시도 횟수": attempts}])
    df = pd.concat([df, new_data], ignore_index=True)
    df = df.sort_values(by="시도 횟수").reset_index(drop=True)
    df.to_csv(LEADERBOARD_FILE, index=False)


# 페이지 설정
st.set_page_config(page_title="숫자 맞추기 게임", page_icon="🎲")
st.title("🎲 1부터 100 사이 숫자 맞추기")

# 세션 상태 초기화
if "target_number" not in st.session_state:
    st.session_state.target_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.game_over = False

# Sidebar - 랭킹 표시
st.sidebar.header("🏆 명예의 전당")
leaderboard = load_leaderboard()
if not leaderboard.empty:
    st.sidebar.dataframe(
        leaderboard.head(10), hide_index=True, use_container_width=True
    )
else:
    st.sidebar.info("아직 등록된 기록이 없습니다!")

# 메인 게임 로직
if not st.session_state.game_over:
    guess = st.number_input(
        "1부터 100 사이의 숫자를 입력하세요:",
        min_value=1,
        max_value=100,
        step=1,
    )

    if st.button("정답 확인"):
        st.session_state.attempts += 1

        if guess < st.session_state.target_number:
            st.warning("📈 UP! 더 큰 숫자입니다.")
        elif guess > st.session_state.target_number:
            st.warning("📉 DOWN! 더 작은 숫자입니다.")
        else:
            st.success(
                f"🎉 정답입니다! **{st.session_state.attempts}번** 만에 맞추셨습니다!"
            )
            st.session_state.game_over = True
            st.rerun()

# 게임 종료 후 랭킹 등록
else:
    player_name = st.text_input("랭킹에 등록할 이름을 입력하세요:")
    if st.button("기록 저장하기"):
        if player_name.strip():
            save_leaderboard(player_name, st.session_state.attempts)
            st.success("랭킹에 기록되었습니다!")

            # 게임 리셋
            st.session_state.target_number = random.randint(1, 100)
            st.session_state.attempts = 0
            st.session_state.game_over = False
            st.rerun()
        else:
            st.error("이름을 입력해주세요.")
