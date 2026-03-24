import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import zipfile

# --- 1. 頁面基本設定 ---
st.set_page_config(page_title="Summer 自訂圖文生成器")
st.title("🖼️ 自訂文字輪播貼文生成")

# --- 2. 側邊欄：讓用戶自行打字、調整樣式 ---
st.sidebar.header("🎨 文字樣式設定")

# 文字內容
user_input = st.sidebar.text_area("1. 請輸入貼文文字內容（一行代表一張圖）：", 
                         "第一頁：如何建立原子習慣？\n第二頁：每天進步 1%，一年後強大 37 倍。\n第三頁：專注於系統，而非目標。\n第四頁：環境比意志力更重要。\n第五頁：現在就開始你的第一步！")

# 樣式設定
st.sidebar.header("位置與顏色")
text_color = st.sidebar.color_picker("文字和頁碼顏色", "#333333")
font_size = st.sidebar.slider("文字大小", 30, 150, 70)
text_x = st.sidebar.slider("文字左右位置 (X)", 0, 1080, 540)
text_y = st.sidebar.slider("文字上下位置 (Y)", 0, 1080, 540)

# --- 3. 核心圖片生成邏輯 ---
def generate_images(text_list, text_color, font_size, text_x, text_y):
    generated_images = []
    img_size = (1080, 1080)
    
    # 使用預設字體
    font = ImageFont.load_default()

    for i, line in enumerate(text_list):
        if not line.strip(): continue
        
        # 建立白色空白畫布
        img = Image.new("RGB", img_size, color="#FFFFFF")
        draw = ImageDraw.Draw(img)
        
        # 畫上文字 (使用自訂位置、顏色)
        draw.text((text_x, text_y), line, fill=text_color, anchor="mm", font=font)
        
        # 加上頁碼 (與文字顏色一致)
        page_text = f"{i+1} / {len(text_list)}"
        draw.text((540, 1030), page_text, fill=text_color, anchor="mm")
        
        generated_images.append(img)
        
    return generated_images

# --- 4. 執行與下載 ---
if st.button("🚀 產生圖片"):
    # 執行生成邏輯
    lines = user_input.split('\n')
    images = generate_images(lines, text_color, font_size, text_x, text_y)
    
    if images:
        st.success(f"✅ 成功生成 {len(images)} 張圖片！")
        
        # 預覽第一張圖
        st.image(images[0], caption="第一張圖片預覽 (實際下載會是全部頁面)", use_container_width=True)
        
        # 製作 ZIP 壓縮包供下載
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for i, img in enumerate(images):
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='PNG')
                zip_file.writestr(f"slide_{i+1}.png", img_byte_arr.getvalue())
        
        st.download_button(
            label="📥 點我下載所有圖片 (ZIP 檔)",
            data=zip_buffer.getvalue(),
            file_name="growithsummer_carousel.zip",
            mime="application/zip"
        )
