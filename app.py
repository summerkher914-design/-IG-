import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import zipfile

st.set_page_config(page_title="Summer IG 生成器")
st.title("🎨 IG 輪播圖一鍵生成")
st.write("輸入文字，一行代表一張圖。")

user_input = st.text_area("內容：", "第一頁\n第二頁\n第三頁")

if st.button("🚀 生成圖片"):
    lines = user_input.split('\n')
    images = []
    
    for i, line in enumerate(lines):
        if not line.strip(): continue
        # 建立 1080x1080 白色底圖
        img = Image.new("RGB", (1080, 1080), "#FFFFFF")
        draw = ImageDraw.Draw(img)
        # 簡單畫出文字
        draw.text((540, 540), line, fill="#333333", anchor="mm")
        # 頁碼
        draw.text((540, 1000), f"{i+1}/{len(lines)}", fill="#999999", anchor="mm")
        images.append(img)
    
    if images:
        st.image(images[0], caption="預覽第一張")
        
        # 壓縮成 ZIP
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for i, img in enumerate(images):
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='PNG')
                zip_file.writestr(f"slide_{i+1}.png", img_byte_arr.getvalue())
        
        st.download_button("📥 下載 ZIP 檔", zip_buffer.getvalue(), "carousel.zip", "application/zip")
