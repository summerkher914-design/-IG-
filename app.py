import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import zipfile
import textwrap

# --- 1. 頁面基本設定 ---
st.set_page_config(page_title="Summer 的 IG 輪播圖生成器", layout="centered")
st.title("🎨 IG 輪播圖一鍵生成工具")
st.write("輸入文字，每行會自動生成一張圖片。讓內容創作變得超簡單！")

# --- 2. 側邊欄：讓使用者自定義樣式 ---
st.sidebar.header("🎨 視覺樣式設定")
bg_color = st.sidebar.color_picker("選擇背景顏色", "#FFFFFF")
text_color = st.sidebar.color_picker("選擇文字顏色", "#333333")
font_size = st.sidebar.slider("文字大小", 40, 100, 70)

# --- 3. 使用者輸入文字 ---
user_input = st.text_area("請輸入貼文內容（一行代表一張圖）：", 
                         "第一頁：如何開始斷捨離？\n第二頁：從書桌的角落開始。\n第三頁：丟掉不再讓你心動的東西。\n第四頁：找回生活的掌控感。\n第五頁：我是 Summer，陪你一起成長。")

# --- 4. 核心圖片生成邏輯 ---
def generate_images(text_list, bg_color, text_color, font_size):
    generated_images = []
    img_size = (1080, 1080)
    
    # 嘗試載入字體 (如果沒上傳字體，會使用預設字體，但中文可能變框框)
    try:
        # 如果你在 GitHub 上傳了 NotoSansTC-Regular.otf，請改名
        font = ImageFont.truetype("msjh.ttc", font_size) 
    except:
        font = ImageFont.load_default()

    for i, line in enumerate(text_list):
        if not line.strip(): continue
        
        # 建立 1080x1080 的空白畫布
        img = Image.new("RGB", img_size, color=bg_color)
        draw = ImageDraw.Draw(img)
        
        # 自動換行處理 (避免文字太長超出螢幕)
        wrapped_lines = textwrap.wrap(line, width=12) # 每行約 12 個中文字
        text_to_draw = "\n".join(wrapped_lines)
        
        # 計算文字置中位置
        left, top, right, bottom = draw.multiline_textbbox((0, 0), text_to_draw, font=font, spacing=20)
        text_w = right - left
        text_h = bottom - top
        position = ((img_size[0] - text_w) / 2, (img_size[1] - text_h) / 2)
        
        # 畫上文字
        draw.multiline_text(position, text_to_draw, fill=text_color, font=font, align="center", spacing=20)
        
        # 加上底部的頁碼 (例如: 1 / 5)
        page_text = f"{i+1} / {len(text_list)}"
        draw.text((500, 1000), page_text, fill=text_color, font= streamlit
Pillow
