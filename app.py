import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import zipfile

# 頁面設定
st.set_page_config(page_title="Summer IG 工具")
st.title("🖼️ 自訂文字輪播圖生成")

# 側邊欄設定
st.sidebar.header("🎨 設定樣式")
user_input = st.sidebar.text_area("1. 輸入文字（一行一張）：", "第一頁內容\n第二頁內容\n第三頁內容")
text_color = st.sidebar.color_picker("2. 文字顏色", "#333333")
font_size = st.sidebar.slider("3. 文字大小", 20, 200, 80)
text_y = st.sidebar.slider("4. 上下位置", 0, 1080, 540)

# 生成按鈕
if st.button("🚀 產生圖片並預覽"):
    lines = user_input.split('\n')
    images = []
    
    # 這裡使用最基礎的預設字體，避免路徑報錯
    font = ImageFont.load_default()

    for i, line in enumerate(lines):
        if not line.strip(): continue
        
        # 建立 1080x1080 白色底
        img = Image.new("RGB", (1080, 1080), color="#FFFFFF")
        draw = ImageDraw.Draw(img)
        
        # 畫文字 (取消 anchor="mm" 避免部分版本不支援)
        draw.text((100, text_y), line, fill=text_color, font=font)
        
        # 頁碼
        draw.text((540, 1000), f"{i+1} / {len(lines)}", fill=text_color)
        
        images.append(img)
    
    if images:
        st.success("生成成功！")
        # 預覽第一張
        st.image(images[0], caption="預覽圖")
        
        # 製作 ZIP
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for i, img in enumerate(images):
                buf = io.BytesIO()
                img.save(buf, format='PNG')
                zip_file.writestr(f"slide_{i+1}.png", buf.getvalue())
        
        st.download_button("📥 下載 ZIP 包", zip_buffer.getvalue(), "carousel.zip")
