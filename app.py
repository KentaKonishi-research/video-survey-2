import streamlit as st
import pandas as pd
import random
import datetime
from streamlit_gsheets import GSheetsConnection

# --- 1. スプレッドシート接続設定 ---
conn = st.connection("gsheets", type=GSheetsConnection)

def save_to_gsheets(data_dict):
    """スプレッドシートに1行追加し、ログに詳細を出力する"""
    # この print 内容が Streamlit Cloud の右下「Manage app」内の「Logs」に表示されます
    print(f"\n>>> 保存プロセス開始: {data_dict['video_name']}")
    try:
        # スプレッドシートを読み込む（キャッシュを無視して最新を取得）
        df = conn.read(ttl=0)
        print(f"現在のスプレッドシート行数: {len(df)}")
        
        # 新しい行を作成
        new_row = pd.DataFrame([data_dict])
        
        # 既存データに新しい行をくっつける
        updated_df = pd.concat([df, new_row], ignore_index=True)
        
        # スプレッドシート全体を更新（書き込み）
        conn.update(data=updated_df)
        print(">>> 【成功】スプレッドシートの更新が完了しました！")
        return True
    except Exception as e:
        # 失敗した場合はログと画面にエラーを出す
        print(f">>> 【失敗】エラー内容: {str(e)}")
        st.error(f"データの保存に失敗しました。エラー: {e}")
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

# --- 3. セッション状態の初期化 ---
if 'page' not in st.session_state:
    st.session_state.page = "consent"
    st.session_state.video_order = random.sample(VIDEO_DATA, len(VIDEO_DATA))
    st.session_state.current_idx = 0
    st.session_state.user_info = {}
    st.session_state.user_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# --- 4. 画面表示の制御 ---

# A. 説明と同意
if st.session_state.page == "consent":
    st.title("調査へのご協力のお願い")
    st.info("本調査に協力しないことによる不利益は一切ございません。また、途中で中止していただいて問題ありません。回答は研究目的以外には使用しません。文学部人文学科行動科学コース認知情報科学専修傳研究室3年 小西健太")
    if st.button("同意して次へ"):
        st.session_state.page = "demographics"
        st.rerun()

# B. 属性質問
elif st.session_state.page == "demographics":
    st.title("属性情報の入力")
    gender = st.radio("性別", ["男", "女", "回答しない", "その他"], index=None)
    age = st.text_input("年齢（半角数字のみ）")
    if st.button("調査を開始する"):
        if gender and age and age.isascii() and age.isdigit():
            st.session_state.user_info = {"gender": gender, "age": age}
            st.session_state.page = "experiment"
            st.rerun()
        else:
            st.error("入力に不備があります。")

# C. 実験
elif st.session_state.page == "experiment":
    current = st.session_state.video_order[st.session_state.current_idx]
    st.title(f"気まずさの評価 ({st.session_state.current_idx + 1} / {len(VIDEO_DATA)})")
    st.video(current["url"])
    score = st.radio("動画の最終部分の沈黙について気まずさを評価してください。（1=気まずくない、6=気まずい）", [1,2,3,4,5,6], horizontal=True, index=None, key=f"q_{st.session_state.current_idx}")
    
    if st.button("回答して次へ"):
        if score:
            # 【重要】ここでスプレッドシートに保存する関数を呼んでいます
            save_to_gsheets({
                "user_id": st.session_state.user_id,
                "gender": st.session_state.user_info["gender"],
                "age": st.session_state.user_info["age"],
                "video_name": current["name"],
                "rating": score,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            if st.session_state.current_idx + 1 < len(VIDEO_DATA):
                st.session_state.current_idx += 1
                st.rerun()
            else:
                st.session_state.page = "finish"
                st.rerun()
        else:
            st.warning("評価を選択してください。")

elif st.session_state.page == "finish":
    st.title("調査終了")
    st.write("回答は自動的に保存されました。ご協力ありがとうございました。")
