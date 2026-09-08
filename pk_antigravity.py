import streamlit as st
import cv2
import numpy as np
import plotly.graph_objects as go
import time
from PIL import Image
import io
import datetime
import os

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="MorphoVision Pro",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- 🎨 BEAUTIFUL GRADIENT CSS ----------
st.markdown("""
<style>
    /* Hide Streamlit junk */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* ========== MAIN BACKGROUND - WARM GRADIENT ========== */
    .stApp {
        background: radial-gradient(ellipse at 30% 20%, #1a0a2e 0%, #2d1b3d 30%, #1a1208 60%, #0a0a12 100%);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* ========== GLOWING ORBS ========== */
    .stApp::after {
        content: '';
        position: fixed;
        top: -20%;
        right: -10%;
        width: 600px;
        height: 600px;
        background: radial-gradient(circle, rgba(201, 168, 76, 0.1) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
        z-index: 0;
        animation: orbFloat 10s ease-in-out infinite alternate;
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        bottom: -20%;
        left: -10%;
        width: 500px;
        height: 500px;
        background: radial-gradient(circle, rgba(118, 75, 162, 0.08) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
        z-index: 0;
        animation: orbFloat 12s ease-in-out infinite alternate-reverse;
    }
    
    @keyframes orbFloat {
        0% { transform: translate(0, 0) scale(1); }
        100% { transform: translate(40px, -30px) scale(1.2); }
    }
    
    /* ========== GLASS SIDEBAR ========== */
    .css-1d391kg, .css-163i15w {
        background: rgba(10, 10, 18, 0.7) !important;
        backdrop-filter: blur(30px) !important;
        -webkit-backdrop-filter: blur(30px) !important;
        border-right: 1px solid rgba(201, 168, 76, 0.08) !important;
    }
    
    /* ========== TITLE ========== */
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #c9a84c, #f5d37c, #f7e4a0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
        margin-bottom: 0;
    }
    
    .main-subtitle {
        color: #8892b0;
        font-size: 1rem;
        font-weight: 300;
        letter-spacing: 2px;
    }
    
    /* ========== GLASS CARDS ========== */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 20px;
        padding: 20px 24px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.4s ease;
        text-align: center;
        position: relative;
        z-index: 1;
    }
    
    .glass-card:hover {
        transform: translateY(-4px);
        border-color: rgba(201, 168, 76, 0.2);
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.4);
    }
    
    .card-value {
        font-size: 2.2rem;
        font-weight: 700;
        font-variant-numeric: tabular-nums;
    }
    
    .card-value.gold { color: #c9a84c; }
    .card-value.green { color: #4ade80; }
    .card-value.blue { color: #60a5fa; }
    .card-value.purple { color: #a78bfa; }
    
    .card-label {
        font-size: 0.7rem;
        font-weight: 500;
        color: #6b7a8f;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 4px;
        border-top: 1px solid rgba(255,255,255,0.04);
        padding-top: 8px;
    }
    
    /* ========== IMAGES ========== */
    .stImage {
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.4s ease;
    }
    
    .stImage:hover {
        border-color: rgba(201, 168, 76, 0.2);
        transform: scale(1.01);
    }
    
    /* ========== BUTTONS ========== */
    .stButton button {
        background: linear-gradient(135deg, #c9a84c, #f5d37c) !important;
        color: #0a0a12 !important;
        font-weight: 700 !important;
        border-radius: 30px !important;
        border: none !important;
        padding: 12px 32px !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 32px rgba(201, 168, 76, 0.3) !important;
    }
    
    /* ========== SLIDER ========== */
    div.stSlider label {
        color: #c8d0dc !important;
        font-weight: 500 !important;
    }
    
    div.stSlider > div > div > div {
        background: rgba(255, 255, 255, 0.06) !important;
        height: 4px !important;
    }
    
    div.stSlider > div > div > div > div {
        background: linear-gradient(90deg, #c9a84c, #f5d37c) !important;
        height: 4px !important;
    }
    
    div.stSlider > div > div > div > div > div {
        background: #ffffff !important;
        border: 3px solid #c9a84c !important;
        box-shadow: 0 0 20px rgba(201, 168, 76, 0.3) !important;
        width: 18px !important;
        height: 18px !important;
        margin-top: -7px !important;
    }
    
    /* ========== RADIO ========== */
    div.stRadio label {
        color: #c8d0dc !important;
        font-weight: 400 !important;
    }
    
    /* ========== TABS ========== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 16px;
        padding: 6px;
        border: 1px solid rgba(255, 255, 255, 0.04);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px !important;
        padding: 8px 24px !important;
        color: #6b7a8f !important;
        font-weight: 500 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(201, 168, 76, 0.15) !important;
        color: #ffffff !important;
    }
    
    /* ========== UPLOAD ========== */
    div.stFileUploader > div > div {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 2px dashed rgba(255, 255, 255, 0.06) !important;
        border-radius: 20px !important;
        padding: 40px 20px !important;
        transition: all 0.4s ease !important;
    }
    
    div.stFileUploader > div > div:hover {
        border-color: rgba(201, 168, 76, 0.3) !important;
        background: rgba(255, 255, 255, 0.04) !important;
    }
    
    /* ========== DIVIDER ========== */
    hr {
        border: none !important;
        border-top: 1px solid rgba(255, 255, 255, 0.04) !important;
        margin: 25px 0 !important;
    }
    
    /* ========== SCROLLBAR ========== */
    ::-webkit-scrollbar {
        width: 4px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.02);
    }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #c9a84c, #f5d37c);
        border-radius: 2px;
    }
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("""
<div style="padding: 20px 0 10px 0; position: relative; z-index: 1;">
    <div class="main-title">🔬 MorphoVision Pro</div>
    <div class="main-subtitle">Advanced Salt &amp; Pepper Noise Removal · Research Grade</div>
</div>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("""
    <div style="padding: 10px 0 20px 0;">
        <div style="font-size: 11px; font-weight: 600; color: #6b7a8f; text-transform: uppercase; letter-spacing: 2px; border-bottom: 1px solid rgba(255,255,255,0.04); padding-bottom: 12px;">
            ⚙️ Control Panel
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded = st.file_uploader("📤 Upload Image", type=["jpg", "png", "jpeg"])
    
    st.markdown('<div style="font-size: 11px; font-weight: 600; color: #6b7a8f; text-transform: uppercase; letter-spacing: 1.5px; margin-top: 20px; margin-bottom: 8px;">Noise Settings</div>', unsafe_allow_html=True)
    noise_percent = st.slider("Density", 0, 40, 7, 1, format="%d%%")
    density = noise_percent / 100.0
    
    st.markdown('<div style="font-size: 11px; font-weight: 600; color: #6b7a8f; text-transform: uppercase; letter-spacing: 1.5px; margin-top: 15px; margin-bottom: 8px;">Filter Settings</div>', unsafe_allow_html=True)
    filter_type = st.radio("Algorithm", ["Morphological (Open-Close)", "Median Filter"], index=0)
    ksize = st.slider("Kernel Size", 3, 15, 3, 2)
    shape_choice = st.selectbox("Structure Element", ["Rectangle", "Ellipse", "Cross"])
    
    st.divider()
    
    st.markdown('<div style="font-size: 11px; font-weight: 600; color: #6b7a8f; text-transform: uppercase; letter-spacing: 1.5px; margin-top: 5px; margin-bottom: 8px;">Live Mode</div>', unsafe_allow_html=True)
    use_webcam = st.checkbox("Enable Webcam Processing")
    
    st.divider()
    
    process_btn = st.button("🚀 Process Image", use_container_width=True)

# ---------- CORE FUNCTIONS ----------
def add_noise(image, density):
    noisy = image.copy()
    total = image.size
    num_salt = int(density * total / 2)
    coords = [np.random.randint(0, i, num_salt) for i in image.shape]
    noisy[coords[0], coords[1]] = 255
    num_pepper = int(density * total / 2)
    coords = [np.random.randint(0, i, num_pepper) for i in image.shape]
    noisy[coords[0], coords[1]] = 0
    return noisy

def morphological_clean(image, ksize, shape_choice):
    shape_map = {"Rectangle": cv2.MORPH_RECT, "Ellipse": cv2.MORPH_ELLIPSE, "Cross": cv2.MORPH_CROSS}
    kernel = cv2.getStructuringElement(shape_map[shape_choice], (ksize, ksize))
    opened = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)
    return closed

def median_benchmark(image, ksize):
    return cv2.medianBlur(image, ksize)

def calculate_metrics(original, processed):
    mse = np.mean((original.astype(float) - processed.astype(float)) ** 2)
    psnr = 20 * np.log10(255.0 / np.sqrt(mse)) if mse > 0 else float('inf')
    ssim = np.corrcoef(original.flatten(), processed.flatten())[0, 1]
    return round(psnr, 2), round(ssim, 4)

def edge_preservation(original, processed):
    edges_orig = cv2.Canny(original, 50, 150)
    edges_proc = cv2.Canny(processed, 50, 150)
    inter = np.logical_and(edges_orig, edges_proc).sum()
    union = np.logical_or(edges_orig, edges_proc).sum()
    return round(inter / union, 3) if union > 0 else 0

def create_3d_surface(image, title="3D Terrain"):
    small = image[::4, ::4]
    x, y = np.meshgrid(range(small.shape[1]), range(small.shape[0]))
    fig = go.Figure(data=[go.Surface(z=small, x=x, y=y, colorscale='Viridis')])
    fig.update_layout(
        title=dict(text=title, font=dict(color='#c8d0dc', size=16)),
        template='plotly_dark',
        height=450,
        paper_bgcolor='rgba(0,0,0,0)',
        scene=dict(
            xaxis=dict(showgrid=False, color='#2a2a3a', title=''),
            yaxis=dict(showgrid=False, color='#2a2a3a', title=''),
            zaxis=dict(showgrid=False, color='#2a2a3a', title=''),
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
        )
    )
    return fig

# ---------- PDF REPORT ----------
from fpdf import FPDF
def generate_report(orig, proc, psnr, ssim, edge, density, ksize):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 20)
    pdf.set_text_color(40, 40, 60)
    pdf.cell(200, 20, "MorphoVision Pro Report", ln=True, align='C')
    pdf.set_font("Arial", "", 12)
    pdf.set_text_color(80, 80, 100)
    pdf.cell(200, 10, f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(40, 40, 60)
    pdf.cell(100, 10, "Parameter", 0, 0)
    pdf.cell(90, 10, "Value", 0, 1, 'R')
    pdf.set_font("Arial", "", 12)
    pdf.set_text_color(60, 60, 80)
    
    pdf.cell(100, 8, "Noise Density", 0, 0)
    pdf.cell(90, 8, f"{density*100}%", 0, 1, 'R')
    pdf.cell(100, 8, "Kernel Size", 0, 0)
    pdf.cell(90, 8, f"{ksize}", 0, 1, 'R')
    pdf.cell(100, 8, "PSNR", 0, 0)
    pdf.cell(90, 8, f"{psnr} dB", 0, 1, 'R')
    pdf.cell(100, 8, "SSIM", 0, 0)
    pdf.cell(90, 8, f"{ssim}", 0, 1, 'R')
    pdf.cell(100, 8, "Edge Preservation", 0, 0)
    pdf.cell(90, 8, f"{edge}", 0, 1, 'R')
    
    cv2.imwrite("temp_orig.png", orig)
    cv2.imwrite("temp_proc.png", proc)
    pdf.ln(10)
    pdf.image("temp_orig.png", x=10, y=160, w=90)
    pdf.image("temp_proc.png", x=110, y=160, w=90)
    pdf.output("Report.pdf")
    os.remove("temp_orig.png")
    os.remove("temp_proc.png")
    return "Report.pdf"

# ---------- MAIN PROCESSING ----------
if uploaded is not None and process_btn:
    file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
    original = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)
    
    status = st.empty()
    status.info("⏳ Processing image...")
    time.sleep(0.3)
    
    noisy = add_noise(original, density)
    
    if "Morphological" in filter_type:
        processed = morphological_clean(noisy, ksize, shape_choice)
    else:
        processed = median_benchmark(noisy, ksize)
    
    status.success("✅ Processing complete!")
    time.sleep(0.3)
    status.empty()
    
    psnr, ssim = calculate_metrics(original, processed)
    edge_score = edge_preservation(original, processed)
    diff_map = cv2.absdiff(original, processed)
    diff_map = cv2.normalize(diff_map, None, 0, 255, cv2.NORM_MINMAX)
    efficiency = round((1 - (np.var(noisy - processed) / np.var(noisy - original))) * 100, 1)
    
    # ---------- RESULTS ----------
    st.markdown("""
    <div style="margin: 10px 0 20px 0;">
        <h2 style="color: #ffffff; font-weight: 600; font-size: 24px;">Processing Results</h2>
        <p style="color: #6b7a8f; font-weight: 300;">Real-time analysis and quality metrics</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image(original, caption="Original", use_container_width=True, clamp=True)
    with col2:
        st.image(noisy, caption=f"Noisy ({noise_percent}%)", use_container_width=True, clamp=True)
    with col3:
        st.image(processed, caption="Denoised", use_container_width=True, clamp=True)
    
    st.divider()
    
    # ---------- METRICS ----------
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="glass-card">
                <div class="card-value gold">{psnr}</div>
                <div class="card-label">PSNR (dB)</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="glass-card">
                <div class="card-value green">{ssim}</div>
                <div class="card-label">SSIM</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="glass-card">
                <div class="card-value blue">{edge_score}</div>
                <div class="card-label">Edge Preservation</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="glass-card">
                <div class="card-value purple">{efficiency}%</div>
                <div class="card-label">Efficiency</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # ---------- TABS ----------
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Histogram", "🔥 Difference Map", "🌌 3D Surface", "📄 Report"])
    
    with tab1:
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=original.flatten(), name='Original', marker_color='#c9a84c', opacity=0.7))
        fig.add_trace(go.Histogram(x=processed.flatten(), name='Denoised', marker_color='#4ade80', opacity=0.7))
        fig.update_layout(
            template='plotly_dark',
            barmode='overlay',
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#c8d0dc')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        col_a, col_b = st.columns(2)
        with col_a:
            st.image(diff_map, caption="Difference Map", use_container_width=True, clamp=True)
        with col_b:
            overlay = cv2.applyColorMap(diff_map, cv2.COLORMAP_JET)
            overlay = cv2.addWeighted(cv2.cvtColor(original, cv2.COLOR_GRAY2BGR), 0.6, overlay, 0.4, 0)
            st.image(overlay, caption="Overlay on Original", use_container_width=True, clamp=True)
    
    with tab3:
        col_a, col_b = st.columns(2)
        with col_a:
            st.plotly_chart(create_3d_surface(original, "Original Terrain"), use_container_width=True)
        with col_b:
            st.plotly_chart(create_3d_surface(processed, "Denoised Terrain"), use_container_width=True)
        st.caption("🖱️ Click, drag, and zoom to explore the 3D pixel terrain")
    
    with tab4:
        if st.button("📄 Generate PDF Report"):
            with st.spinner("Generating report..."):
                path = generate_report(original, processed, psnr, ssim, edge_score, density, ksize)
                with open(path, "rb") as f:
                    st.download_button(
                        "⬇️ Download Report (PDF)",
                        data=f,
                        file_name="MorphoVision_Report.pdf",
                        mime="application/pdf"
                    )
                os.remove(path)

# ---------- WEBCAM ----------
if use_webcam:
    st.divider()
    st.markdown("""
    <div style="background: rgba(255,255,255,0.02); border-radius: 20px; padding: 30px; border: 1px solid rgba(255,255,255,0.04);">
        <h3 style="color: #ffffff; font-weight: 600; margin-bottom: 10px;">📹 Live Webcam Processing</h3>
        <p style="color: #6b7a8f; font-weight: 300; margin-bottom: 20px;">Real-time denoising with morphological filtering</p>
    """, unsafe_allow_html=True)
    
    if st.button("▶️ Start Webcam"):
        cap = cv2.VideoCapture(0)
        frame_place = st.empty()
        stop = st.button("⏹️ Stop")
        while not stop:
            ret, frame = cap.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            noisy_f = add_noise(gray, 0.05)
            clean_f = morphological_clean(noisy_f, 3, "Rectangle")
            combined = np.hstack([gray, noisy_f, clean_f])
            frame_place.image(combined, caption="Original  |  Noisy  |  Denoised", use_container_width=True, clamp=True)
            time.sleep(0.03)
        cap.release()
        frame_place.empty()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- FOOTER ----------
st.divider()
st.markdown("""
<div style="text-align: center; padding: 15px 0 5px 0; color: #3d4a5c; font-size: 12px; font-weight: 300; letter-spacing: 0.5px;">
    <span style="color: #c9a84c;">◆</span> MorphoVision Pro 2026 — Built with OpenCV · Streamlit · Plotly
</div>
""", unsafe_allow_html=True)