import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import zipfile
import textwrap

# --- 頁面基本設定 ---
st.set_page_config(page_title="Summer 的 IG 輪播圖生成器", layout="centered")
st.title("🎨 IG 輪播圖一鍵生成工具")
st.write("輸入文字，每行會自動生成一張圖片。讓內容創作變得超簡單！")

# --- 側邊欄樣式設定 ---
st.sidebar.header("🎨 視覺樣式設定")
bg_color = st.sidebar.color_picker("選擇背景顏色", "#FFFFFF")
text_color = st.sidebar.color_picker("選擇文字顏色", "#333333")
font_size = st.sidebar.slider("文字大小", 40, 150, 80)

# --- 使用者輸入文字 ---
user_input = st.text_area("請輸入貼文內容（一行代表一張圖）：", 
                         "第一頁：如何開始斷捨離？\n第二頁：從書桌的角落開始。\n第三頁：丟掉不再讓你心動的東西。\n第四頁：找回生活的掌控感。\n第五頁：我是 Summer，陪你一起成長。")

# --- 核心圖片生成邏輯 ---
def generate_images(text_list, bg_color, text_color, font_size):
    generated_images = []
    img_size = (1080, 1080)
    
    # 使用預設字體
    font = ImageFont.load_default()

    for i, line in enumerate(text_list):
        if not line.strip(): continue
        
        img = Image.new("RGB", img_size, color=bg_color)
        draw = ImageDraw.Draw(img)
        
        # 自動換行
        wrapped_lines = textwrap.wrap(line, width=12)
        text_to_draw = "\n".join(wrapped_lines)
        
        # 繪製中心文字
        draw.multiline_text((540, 540), text_to_draw, fill=text_color, anchor="mm", align="center")
        
        # 加上底部的頁碼
        page_text = f"{i+1} / {len(text_list)}"
        draw.text((540, 1000), page_text, fill=text_color, anchor="mm")
        
        generated_images.append(img)
        
    return generated_images

# --- 執行與下載 ---
if st.button("🚀 點我開始生成圖片"):
    lines = user_input.split('\n')
    images = generate_images(lines, bg_color, text_color, font_size)
    
    if images:
        st.success(f"✅ 成功生成 {len(images)} 張圖片！")
        st.image(images[0], caption="第一張圖片預覽", use_container_width=True)
        
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for i, img in enumerate(images):
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='PNG')
                zip_file.writestr(f"slide_{i+1}.png", img_byte_arr.getvalue())
        
        st.download_button(
            label="📥 點我下載所有圖片 (ZIP 檔)",
            data=zip_buffer.getvalue(),
            file_name="summer_carousel.zip",
            mime="application/zip"
        )
