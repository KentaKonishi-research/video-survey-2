import streamlit as st
import pandas as pd
import random
import datetime
from streamlit_gsheets import GSheetsConnection

# --- 1. スプレッドシート接続設定 ---
conn = st.connection("gsheets", type=GSheetsConnection)

def save_to_gsheets(data_dict):
    """画面に進行状況を出しながら保存する"""
    # 画面の右下に小さな通知（トースト）を出します
    st.toast(f"保存を開始します: {data_dict['video_name']}")
    try:
        # スプレッドシートを読み込む
        df = conn.read(ttl=0)
        # 新しい行を作成
        new_row = pd.DataFrame([data_dict])
        # 既存データと結合
        updated_df = pd.concat([df, new_row], ignore_index=True)
        # スプレッドシート全体を更新
        conn.update(data=updated_df)
        st.toast("✅ スプレッドシートの保存に成功しました！", icon="🎉")
        return True
    except Exception as e:
        # 失敗した場合は画面に大きくエラーを出す
        st.error(f"【重大なエラー】保存に失敗しました。この画面をスクリーンショットして管理者に送ってください: {e}")
        return False

# --- 2. 動画データの設定 ---
VIDEO_DATA = [
    {"name": "C001_002 沈黙①", "url": "https://youtu.be/-YLyHXWdpwA"},
    {"name": "C001_002 沈黙②", "url": "https://youtu.be/pODWvK-WDCw"},
    {"name": "K001_004 沈黙①", "url": "https://youtu.be/5GvTP5ZsHGc"},
    {"name": "K001_004 沈黙②", "url": "https://youtu.be/T7VrMyrQTcg"},
    {"name": "K002_016 沈黙①", "url": "https://youtu.be/goiuyPzMLBM"},
    {"name": "K002_016 沈黙②", "url": "https://youtu.be/5mM-5vMFpEQ"},
    {"name": "K006_023 沈黙①", "url": "https://youtu.be/UXCatH2-HVo"},
    {"name": "K006_023 沈黙②", "url": "https://youtu.be/oRl-oxeKtsc"},
    {"name": "K009_007 沈黙①", "url": "https://youtu.be/is5AvUX9xI8"},
    {"name": "K009_007 沈黙②", "url": "https://youtu.be/sL2FLEmvJGU"},
    {"name": "K010_006 沈黙①", "url": "https://youtu.be/ceeu3npo9Hs"},
    {"name": "K010_006 沈黙②", "url": "https://youtu.be/VWKiuUMlM6Q"},
    {"name": "K010_013b 沈黙①", "url": "https://youtu.be/J_PbqYE4uos"},
    {"name": "K010_013b 沈黙②", "url": "https://youtu.be/QKX8KcGVmq0"},
    {"name": "K012_001 沈黙①", "url": "https://youtu.be/J9M5A6TYC5k"},
    {"name": "K012_001 沈黙②", "url": "https://youtu.be/bDryDIcuXto"},
    {"name": "K012_002d 沈黙①", "url": "https://youtu.be/B_WtYFZMvss"},
    {"name": "K012_002d 沈黙②", "url": "https://youtu.be/uBgkTO9qu1A"},
    {"name": "T008_022c 沈黙①", "url": "https://youtu.be/2jl8mRNE3uA"},
    {"name": "T008_022c 沈黙②", "url": "https://youtu.be/1nVxZ_tN5Fw"},
    {"name": "T010_013 沈黙①", "url": "https://youtu.be/j_RtuDmBv9A"},
    {"name": "T010_013 沈黙②", "url": "https://youtu.be/fLPhBTsm5tA"},
    {"name": "T022_005 沈黙①", "url": "https://youtu.be/NbFnWbbByMk"},
    {"name": "T022_005 沈黙②", "url": "https://youtu.be/TT4UPh-Xbk0"},
    {"name": "T022_012 沈黙①", "url": "https://youtu.be/XrwElJHHACI"},
    {"name": "T022_012 沈黙②", "url": "https://youtu.be/A0jLMrK99ZU"},
    {"name": "T023_007 沈黙①", "url": "https://youtu.be/tXXRX1aKg_U"},
    {"name": "T023_007 沈黙②", "url": "https://youtu.be/XmmipswjZPE"},
]

# --- 3. セッション管理 ---
if 'page' not in st.session_state:
    st.session_state.page = "consent"
    st.session_state.video_order = random.sample(VIDEO_DATA, len(VIDEO_DATA))
    st.session_state.current_idx = 0
    st.session_state.user_info = {}
    st.session_state.user_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# --- 4. 画面制御 ---
if st.session_state.page == "consent":
    st.title("調査へのご協力のお願い")
    st.info("本調査に協力しないことによる不利益は一切ございません。収集された回答は研究以外の目的に使用することはございません。\n\n文学部人文学科行動科学コース認知情報科学専修傳研究室３年小西健太")
    if st.button("同意して次へ"):
        st.session_state.page = "demographics"; st.rerun()

elif st.session_state.page == "demographics":
    st.title("属性情報の入力")
    gender = st.radio("質問：性別をお答えください。", ["男", "女", "回答しない", "その他"], index=None)
    age = st.text_input("質問：年齢をお答えください。（半角数字のみ）")
    if st.button("調査を開始する"):
        if gender and age and age.isascii() and age.isdigit():
            st.session_state.user_info = {"gender": gender, "age": age}
            st.session_state.page = "experiment"; st.rerun()
        else:
            st.error("入力に不備があります。年齢は半角数字で入力してください。")

elif st.session_state.page == "experiment":
    current = st.session_state.video_order[st.session_state.current_idx]
    st.title(f"評価 ({st.session_state.current_idx + 1} / {len(VIDEO_DATA)})")
    st.video(current["url"])
    score = st.radio("動画の最終部分の沈黙について、評価を選択してください。（1=気まずくない、6=気まずい）", [1,2,3,4,5,6], horizontal=True, index=None, key=f"q_{st.session_state.current_idx}")
    
    if st.button("回答して次へ"):
        if score:
            # 保存実行
            save_to_gsheets({
                "user_id": st.session_state.user_id,
                "gender": st.session_state.user_info["gender"],
                "age": st.session_state.user_info["age"],
                "video_name": current["name"],
                "rating": score,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            if st.session_state.current_idx + 1 < len(VIDEO_DATA):
                st.session_state.current_idx += 1; st.rerun()
            else:
                st.session_state.page = "finish"; st.rerun()
        else:
            st.warning("評価を選択してください。")

elif st.session_state.page == "finish":
    st.title("調査終了")
    st.success("回答はすべてスプレッドシートに自動保存されました。ご協力ありがとうございました。")
