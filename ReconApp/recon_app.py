import streamlit as st
import pandas as pd
from pathlib import Path
from recon_engine import generate_reconciliation_file

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(page_title="Recon File Generator", layout="wide")

# Base directory
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
LOGO_PATH = STATIC_DIR / "logo.png"

# ============================================
# CENTERED HEADER WITH LOGO + TITLE
# ============================================
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
LOGO_PATH = STATIC_DIR / "logo.png"   # adjust filename if needed (logo.png / company_logo.png)

# Try to show a centered row with logo left and title right but horizontally centered on page
# Column widths: left spacer, logo col, title col, right spacer
col_left, col_logo, col_title, col_right = st.columns([1, 1, 6, 1])

if LOGO_PATH.exists():
    # Put image in the small column and title in the larger column
    with col_logo:
        # width controls size; change 110 -> smaller/larger
        st.image(str(LOGO_PATH), width=110)

    with col_title:
        # left-align the title inside the title column, reduce margins so it's close to the logo
        st.markdown(
            "<h1 style='margin:0; padding-top:10px; text-align:left;'>Recon File Generator</h1>",
            unsafe_allow_html=True,
        )
else:
    # If logo missing, show title centered instead and a warning
    st.warning(f"⚠ Logo not found at: {LOGO_PATH}")
    st.markdown("<h1 style='text-align:center;'>Recon File Generator</h1>", unsafe_allow_html=True)

# small vertical gap before the rest of the UI
st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
# --- end header ---

# ============================================
# STEP 1 — INPUTS
# ============================================
st.markdown("## Step 1 — Upload Inputs")
trial_balance_file = st.file_uploader(
    "Upload Trial Balance file",
    type=["xlsx"],
    key="trial_balance_upload"
)

entries_file = st.file_uploader(
    "Upload All Entries file",
    type=["xlsx"],
    key="entries_upload"
)

icp_code = st.text_input("Enter ICP Code", placeholder="Example: SKPVAB").strip()

st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)

# ============================================
# STEP 2 — GENERATE
# ============================================
st.markdown("## Step 2 — Generate Recon File")

if st.button("Generate Recon File", type="primary"):

    if not trial_balance_file or not entries_file or not icp_code:
        st.error("Please upload both files and enter the ICP Code.")
        st.stop()

    with st.spinner("Generating file, please wait..."):
        try:
            output_bytes = generate_reconciliation_file(
                trial_balance_file,
                entries_file,
                icp_code.upper()
            )
        except Exception as e:
            st.error(f"❌ An error occurred:\n\n{e}")
            st.stop()

    st.success("✅ Reconciliation file generated successfully!")

    st.download_button(
        label="📥 Download Reconciliation Workbook",
        data=output_bytes,
        file_name="Reconciliation_Mapped.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.caption("European Energy — Internal Tool")


