import streamlit as st
import pandas as pd
import random
import datetime

# --- 1. 動画データの設定 ---
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

if 'page' not in st.session_state:
    st.session_state.page = "consent"
    st.session_state.video_order = random.sample(VIDEO_DATA, len(VIDEO_DATA))
    st.session_state.current_idx = 0
    st.session_state.responses = []
    st.session_state.user_info = {}
    st.session_state.user_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

if st.session_state.page == "consent":
    st.title("調査へのご協力のお願い")
    st.info("""
    本調査に協力しないことによる不利益は一切ございません。
    また、調査の途中で気分を害された場合、途中で中止していただいて問題ありません。
    収集された回答は研究以外の目的に使用することはございません。

    文学部人文学科行動科学コース認知情報科学専修傳研究室３年小西健太
    """)
    if st.button("同意して次へ"):
        st.session_state.page = "demographics"
        st.rerun()

elif st.session_state.page == "demographics":
    st.title("属性情報の入力")
    gender = st.radio("質問：性別をお答えください。", ["男", "女", "回答しない", "その他"], index=None)
    age_input = st.text_input("質問：年齢をお答えください。（半角数字のみ）")
    if st.button("調査を開始する"):
        if gender and age_input:
            if age_input.isascii() and age_input.isdigit():
                st.session_state.user_info = {"gender": gender, "age": age_input}
                st.session_state.page = "experiment"
                st.rerun()
            else:
                st.error("年齢は必ず「半角」の数字で入力してください。")
        else:
            st.warning("すべての質問にお答えください。")

elif st.session_state.page == "experiment":
    current_item = st.session_state.video_order[st.session_state.current_idx]
    st.title(f"気まずさの評価 ({st.session_state.current_idx + 1} / {len(VIDEO_DATA)})")
    st.video(current_item["url"])
    score = st.radio("評価を選択（1=気まずくない、6=気まずい）", options=[1,2,3,4,5,6], horizontal=True, index=None, key=f"q_{st.session_state.current_idx}")
    if st.button("回答して次へ"):
        if score:
            st.session_state.responses.append({
                "user_id": st.session_state.user_id, "gender": st.session_state.user_info["gender"],
                "age": st.session_state.user_info["age"], "video_name": current_item["name"],
                "rating": score, "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            if st.session_state.current_idx + 1 < len(VIDEO_DATA):
                st.session_state.current_idx += 1
                st.rerun()
            else:
                st.session_state.page = "finish"
                st.rerun()

elif st.session_state.page == "finish":
    st.title("調査終了")
    st.write("全ての回答が完了しました。ご協力ありがとうございました。")
    df = pd.DataFrame(st.session_state.responses)
    csv = df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
    st.success("【重要】下のボタンを押して、回答ファイルを保存してください。")
    st.download_button(label="回答をダウンロード (.csv)", data=csv, file_name=f"res_{st.session_state.user_id}.csv", mime="text/csv")
    st.write("※保存したファイルを、調査担当者（小西）まで送付してください。")
