# import streamlit as st
# import pandas as pd
# import pdfplumber
# import PyPDF2
# from io import BytesIO
# import openpyxl
# from openpyxl.styles import PatternFill
# from datetime import datetime
# import os
# from dotenv import load_dotenv

# # --- Core logic for Addon Covers is imported ---
# from create_addon import create_addon

# # Load environment variables
# load_dotenv()

# # --- Authentication and Helper Functions (Unchanged) ---

# def load_users_from_env():
#     """Load users from environment variables"""
#     users = {}
#     for i in range(1, 4):
#         username = os.getenv(f'USER{i}_NAME')
#         password = os.getenv(f'USER{i}_PASSWORD')
#         if username and password:
#             users[username] = password
#     return users

# def check_authentication(username, password, users):
#     """Check if username and password match"""
#     return username in users and users[username] == password

# def authentication_page():
#     """Display authentication page"""
#     users = load_users_from_env()
#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col2:
#         st.markdown("### 🔐 Authentication Required")
#         st.markdown("Please login to access the PDF to Excel Extractor")
#         st.markdown("---")
#         username = st.text_input("Username", placeholder="Enter your username", key="login_username")
#         password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
#         if st.button("🚀 Login", use_container_width=True, type="primary"):
#             if check_authentication(username, password, users):
#                 st.session_state.authenticated = True
#                 st.session_state.username = username
#                 st.success("✅ Login successful!")
#                 st.rerun()
#             else:
#                 st.error("❌ Invalid username or password!")
#         with st.expander("ℹ️ Test Users", expanded=False):
#             st.markdown("**Available Test Users:**")
#             if users:
#                 for user, pwd in users.items():
#                     st.code(f"👤 {user} | 🔒 {pwd}", language="text")
#             else:
#                 st.warning("No users found in .env file.")

# # --- Page Config (Unchanged) ---
# st.set_page_config(
#     page_title="PDF to Excel Extractor",
#     page_icon="🚀",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # --- COMPLETE CSS BLOCK RESTORED ---
# st.markdown("""
# <style>
#     /* Main app background */
#     [data-testid="stAppViewContainer"] {
#         background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
#     }
    
#     /* Sidebar background */
#     [data-testid="stSidebar"] {
#         background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
#     }
    
#     /* All text elements */
#     .stMarkdown, .stText, .stDataFrame, .stExpander, .stButton, .stTextInput {
#         color: white !important;
#         background: transparent !important;
#     }
    
#     /* Dataframes */
#     .stDataFrame > div {
#         background: rgba(255, 255, 255, 0.1) !important;
#         color: white !important;
#     }
    
#     /* Input fields */
#     .stTextInput > div > div > input {
#         background: rgba(255, 255, 255, 0.1) !important;
#         color: white !important;
#         border: 1px solid rgba(255, 255, 255, 0.2) !important;
#     }
    
#     .stTextInput > div > div > input::placeholder {
#         color: rgba(255, 255, 255, 0.6) !important;
#     }
    
#     /* Buttons */
#     .stButton > button {
#         background: rgba(255, 255, 255, 0.1) !important;
#         color: white !important;
#         border: 1px solid rgba(255, 255, 255, 0.2) !important;
#     }
    
#     /* Expanders */
#     .streamlit-expanderHeader {
#         background: rgba(255, 255, 255, 0.1) !important;
#         color: white !important;
#         border: 1px solid rgba(255, 255, 255, 0.2) !important;
#     }
    
#     /* Text areas */
#     .stTextArea > div > div > textarea {
#         background: rgba(255, 255, 255, 0.1) !important;
#         color: white !important;
#         border: 1px solid rgba(255, 255, 255, 0.2) !important;
#     }
    
#     /* File uploader */
#     .stFileUploader > div {
#         background: rgba(255, 255, 255, 0.1) !important;
#         color: white !important;
#         border: 1px solid rgba(255, 255, 255, 0.2) !important;
#     }
    
#     /* Success and error messages */
#     .stSuccess, .stError {
#         background: rgba(255, 255, 255, 0.1) !important;
#         color: white !important;
#         border: 1px solid rgba(255, 255, 255, 0.2) !important;
#     }
    
#     /* Header styling for main app */
#     .main-header {
#         background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
#         padding: 1.5rem;
#         border-radius: 15px;
#         margin-bottom: 1rem;
#         text-align: center;
#         color: white !important;
#         box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
#     }
    
#     .main-header h1 {
#         margin: 0;
#         font-size: 2.5rem;
#         font-weight: 700;
#         text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
#         color: white !important;
#     }
    
#     .main-header p {
#         margin: 0.5rem 0 0 0;
#         font-size: 1.1rem;
#         opacity: 0.9;
#         color: white !important;
#     }
# </style>
# """, unsafe_allow_html=True)

# def extract_text_from_pdf(pdf_file):
#     """Extract text from uploaded PDF file (Unchanged)"""
#     try:
#         text = ""
#         pdf_file.seek(0)
#         with pdfplumber.open(pdf_file) as pdf:
#             for page in pdf.pages:
#                 page_text = page.extract_text()
#                 if page_text:
#                     text += page_text + "\n"
        
#         if len(text.strip()) < 100:
#             pdf_file.seek(0)
#             pdf_reader = PyPDF2.PdfReader(pdf_file)
#             text = ""
#             for page in pdf_reader.pages:
#                 text += page.extract_text() + "\n"
#         return text
#     except Exception as e:
#         st.error(f"Error reading PDF: {str(e)}")
#         return None

# def create_addon_excel_with_formatting(addon_data):
#     """Creates an Excel workbook with only the Addon Covers data and formatting."""
#     wb = openpyxl.Workbook()
#     if "Sheet" in wb.sheetnames:
#         del wb["Sheet"]
#     ws = wb.create_sheet(title="Addon Covers")
#     headers = list(pd.DataFrame(addon_data).columns)
#     header_fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
#     for col_num, header_title in enumerate(headers, 1):
#         cell = ws.cell(row=3, column=col_num, value=header_title)
#         cell.fill = header_fill
#         ws.column_dimensions[openpyxl.utils.get_column_letter(col_num)].width = 25
#     if addon_data:
#         for row_num, row_data in enumerate(pd.DataFrame(addon_data).values, 4):
#             for col_num, cell_value in enumerate(row_data, 1):
#                 ws.cell(row=row_num, column=col_num, value=cell_value)
#     return wb

# # --- Main Application Logic (Unchanged) ---
# def main():
#     if 'authenticated' not in st.session_state:
#         st.session_state.authenticated = False
    
#     if not st.session_state.authenticated:
#         authentication_page()
#         return
    
#     st.markdown(f"""
#     <div class="main-header">
#         <h1>🚀 PDF to Excel Extractor</h1>
#         <p>Welcome, <strong>{st.session_state.username}</strong>! This tool extracts Addon Cover details from your PDF.</p>
#     </div>
#     """, unsafe_allow_html=True)
    
#     with st.sidebar:
#         st.markdown("### 👤 User Session")
#         st.info(f"**Logged in as:** {st.session_state.username}")
#         if st.button("🚪 Logout", type="secondary", use_container_width=True):
#             st.session_state.authenticated = False
#             st.session_state.username = None
#             st.rerun()
#         st.markdown("---")
    
#     uploaded_file = st.sidebar.file_uploader(
#         "Choose a PDF file",
#         type=['pdf'],
#         help="Upload a PDF to extract Addon Cover information"
#     )
    
#     if uploaded_file is not None:
#         st.success(f"✅ File uploaded: {uploaded_file.name}")
        
#         with st.spinner("🔍 Extracting text from PDF..."):
#             text = extract_text_from_pdf(uploaded_file)
        
#         if text:
#             with st.spinner("🧠 Analyzing for Addon Covers..."):
#                 addon_data = create_addon(text)
            
#             st.subheader("📊 Extracted Addon Covers")
#             df_addon = pd.DataFrame(addon_data)
#             st.dataframe(df_addon, use_container_width=True, height=150)
            
#             with st.sidebar:
#                 with st.spinner("Creating Excel file..."):
#                     try:
#                         wb = create_addon_excel_with_formatting(addon_data)
#                         excel_buffer = BytesIO()
#                         wb.save(excel_buffer)
#                         excel_buffer.seek(0)
#                         st.download_button(
#                             label="📥 Download Addon Excel",
#                             data=excel_buffer.getvalue(),
#                             file_name=f"Addon_Covers_{uploaded_file.name.split('.')[0]}_{datetime.now().strftime('%d-%m-%Y')}.xlsx",
#                             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#                         )
#                     except Exception as e:
#                         st.error(f"❌ Error generating Excel file: {str(e)}")
#     else:
#         st.info("Please upload a file to begin.")

# if __name__ == "__main__":
#     main()
# import streamlit as st
# import pandas as pd
# import pdfplumber
# import PyPDF2
# from io import BytesIO
# import openpyxl
# from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
# from datetime import datetime
# import os
# from dotenv import load_dotenv

# # --- Core logic for Addon Covers is imported ---
# from create_addon import create_addon

# # Load environment variables
# load_dotenv()

# # --- All Authentication and Helper Functions (Unchanged) ---
# def load_users_from_env():
#     """Load users from environment variables"""
#     users = {}
#     for i in range(1, 4):
#         username = os.getenv(f'USER{i}_NAME')
#         password = os.getenv(f'USER{i}_PASSWORD')
#         if username and password:
#             users[username] = password
#     return users

# def check_authentication(username, password, users):
#     """Check if username and password match"""
#     return username in users and users[username] == password

# def authentication_page():
#     """Display authentication page"""
#     users = load_users_from_env()
#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col2:
#         st.markdown("### 🔐 Authentication Required")
#         st.markdown("Please login to access the PDF to Excel Extractor")
#         st.markdown("---")
#         username = st.text_input("Username", placeholder="Enter your username", key="login_username")
#         password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
#         if st.button("🚀 Login", use_container_width=True, type="primary"):
#             if check_authentication(username, password, users):
#                 st.session_state.authenticated = True
#                 st.session_state.username = username
#                 st.success("✅ Login successful!")
#                 st.rerun()
#             else:
#                 st.error("❌ Invalid username or password!")
#         with st.expander("ℹ️ Test Users", expanded=False):
#             st.markdown("**Available Test Users:**")
#             if users:
#                 for user, pwd in users.items():
#                     st.code(f"👤 {user} | 🔒 {pwd}", language="text")

# # --- Page Config (Unchanged) ---
# st.set_page_config(
#     page_title="PDF to Excel Extractor",
#     page_icon="🚀",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # --- COMPLETE CSS BLOCK (Unchanged) ---
# st.markdown("""
# <style>
#     /* Main app background */
#     [data-testid="stAppViewContainer"] {
#         background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
#     }
    
#     /* Sidebar background */
#     [data-testid="stSidebar"] {
#         background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
#     }
    
#     /* All text elements */
#     .stMarkdown, .stText, .stDataFrame, .stExpander, .stButton, .stTextInput {
#         color: white !important;
#         background: transparent !important;
#     }
    
#     /* Dataframes */
#     .stDataFrame > div {
#         background: rgba(255, 255, 255, 0.1) !important;
#         color: white !important;
#     }
    
#     /* Input fields */
#     .stTextInput > div > div > input {
#         background: rgba(255, 255, 255, 0.1) !important;
#         color: white !important;
#         border: 1px solid rgba(255, 255, 255, 0.2) !important;
#     }
    
#     .stTextInput > div > div > input::placeholder {
#         color: rgba(255, 255, 255, 0.6) !important;
#     }
    
#     /* Buttons */
#     .stButton > button {
#         background: rgba(255, 255, 255, 0.1) !important;
#         color: white !important;
#         border: 1px solid rgba(255, 255, 255, 0.2) !important;
#     }
    
#     /* Expanders */
#     .streamlit-expanderHeader {
#         background: rgba(255, 255, 255, 0.1) !important;
#         color: white !important;
#         border: 1px solid rgba(255, 255, 255, 0.2) !important;
#     }
    
#     /* Text areas */
#     .stTextArea > div > div > textarea {
#         background: rgba(255, 255, 255, 0.1) !important;
#         color: white !important;
#         border: 1px solid rgba(255, 255, 255, 0.2) !important;
#     }
    
#     /* File uploader */
#     .stFileUploader > div {
#         background: rgba(255, 255, 255, 0.1) !important;
#         color: white !important;
#         border: 1px solid rgba(255, 255, 255, 0.2) !important;
#     }
    
#     /* Success and error messages */
#     .stSuccess, .stError {
#         background: rgba(255, 255, 255, 0.1) !important;
#         color: white !important;
#         border: 1px solid rgba(255, 255, 255, 0.2) !important;
#     }
    
#     /* Header styling for main app */
#     .main-header {
#         background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
#         padding: 1.5rem;
#         border-radius: 15px;
#         margin-bottom: 1rem;
#         text-align: center;
#         color: white !important;
#         box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
#     }
    
#     .main-header h1 {
#         margin: 0;
#         font-size: 2.5rem;
#         font-weight: 700;
#         text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
#         color: white !important;
#     }
    
#     .main-header p {
#         margin: 0.5rem 0 0 0;
#         font-size: 1.1rem;
#         opacity: 0.9;
#         color: white !important;
#     }
# </style>
# """, unsafe_allow_html=True)


# def extract_text_from_pdf(pdf_file):
#     """Extract text from uploaded PDF file"""
#     text = ""
#     try:
#         pdf_file.seek(0)
#         with pdfplumber.open(pdf_file) as pdf:
#             for page in pdf.pages:
#                 page_text = page.extract_text()
#                 if page_text:
#                     text += page_text + "\n"
#         if len(text.strip()) < 100:
#             pdf_file.seek(0)
#             pdf_reader = PyPDF2.PdfReader(pdf_file)
#             for page in pdf_reader.pages:
#                 text += page.extract_text() + "\n"
#         return text
#     except Exception as e:
#         st.error(f"Error reading PDF: {str(e)}")
#         return None

# # --- Function with Final Excel Formatting ---
# def create_addon_excel_with_formatting(addon_data):
#     """
#     Creates an Excel workbook with the final, detailed formatting to match the template image.
#     """
#     wb = openpyxl.Workbook()
#     ws = wb.active
#     ws.title = "Addon Covers"

#     # Define styles
#     yellow_fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
#     # MODIFICATION: Removed the bold_font definition as it's no longer needed
#     wrap_alignment = Alignment(wrap_text=True, vertical='center')
#     thin_border_all_sides = Border(left=Side(style='thin'), 
#                                    right=Side(style='thin'), 
#                                    top=Side(style='thin'), 
#                                    bottom=Side(style='thin'))

#     if not addon_data:
#         ws['A1'] = "No addon data was generated."
#         return wb
        
#     headers = list(addon_data[0].keys())
#     num_cols = len(headers)

#     # --- Row 1 & 2: Title and empty row formatted as solid bars ---
#     ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=num_cols)
#     title_cell = ws.cell(row=1, column=1, value="Addon Covers")
#     # MODIFICATION: Removed the line that applies bold font
#     title_cell.alignment = wrap_alignment

#     for row_num in [1, 2]:
#         for i in range(1, num_cols + 1):
#             cell = ws.cell(row=row_num, column=i)
#             cell.fill = yellow_fill
#             border_style = Border(
#                 top=Side(style='thin'), 
#                 bottom=Side(style='thin'),
#                 left=Side(style='thin') if i == 1 else None,
#                 right=Side(style='thin') if i == num_cols else None
#             )
#             cell.border = border_style

#     # --- Row 3: Column Headers with full borders ---
#     for col_num, header_title in enumerate(headers, 1):
#         cell = ws.cell(row=3, column=col_num, value=header_title)
#         cell.fill = yellow_fill
#         # MODIFICATION: Removed the line that applies bold font
#         cell.alignment = wrap_alignment
#         cell.border = thin_border_all_sides
#         ws.column_dimensions[openpyxl.utils.get_column_letter(col_num)].width = 18

#     # --- Row 4: Data with full borders ---
#     df = pd.DataFrame(addon_data)[headers]
#     for row_index, row_data in enumerate(df.values, 4):
#         for col_index, cell_value in enumerate(row_data, 1):
#             cell = ws.cell(row=row_index, column=col_index, value=cell_value)
#             cell.alignment = wrap_alignment
#             cell.border = thin_border_all_sides
    
#     return wb

# # --- Main Application Logic (Unchanged) ---
# def main():
#     if 'authenticated' not in st.session_state:
#         st.session_state.authenticated = False
    
#     if not st.session_state.authenticated:
#         authentication_page()
#         return
    
#     st.markdown(f"""
#     <div class="main-header">
#         <h1>🚀 PDF to Excel Extractor</h1>
#         <p>Welcome, <strong>{st.session_state.username}</strong>! This tool extracts Addon Cover details from your PDF.</p>
#     </div>
#     """, unsafe_allow_html=True)
    
#     with st.sidebar:
#         st.markdown("### 👤 User Session")
#         st.info(f"**Logged in as:** {st.session_state.username}")
#         if st.button("🚪 Logout", type="secondary", use_container_width=True):
#             st.session_state.authenticated = False
#             st.session_state.username = None
#             st.rerun()
#         st.markdown("---")

#     uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type=['pdf'])
    
#     if uploaded_file is not None:
#         st.success(f"✅ File uploaded: {uploaded_file.name}")
#         with st.spinner("🔍 Extracting text from PDF..."):
#             text = extract_text_from_pdf(uploaded_file)
#         if text:
#             with st.spinner("🧠 Analyzing for Addon Covers..."):
#                 addon_data = create_addon(text)
#             st.subheader("📊 Extracted Addon Covers")
#             df_addon = pd.DataFrame(addon_data)
#             st.dataframe(df_addon, use_container_width=True, height=150)
#             with st.sidebar:
#                 with st.spinner("Creating Excel file..."):
#                     try:
#                         wb = create_addon_excel_with_formatting(addon_data)
#                         excel_buffer = BytesIO()
#                         wb.save(excel_buffer)
#                         excel_buffer.seek(0)
#                         st.download_button(
#                             label="📥 Download Addon Excel",
#                             data=excel_buffer.getvalue(),
#                             file_name=f"Addon_Covers_{datetime.now().strftime('%d-%m-%Y')}.xlsx",
#                             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#                         )
#                     except Exception as e:
#                         st.error(f"❌ Error generating Excel file: {str(e)}")

# if __name__ == "__main__":
#     main()
import streamlit as st
import pandas as pd
import pdfplumber
import PyPDF2
from io import BytesIO
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from datetime import datetime
import os
from dotenv import load_dotenv

# --- Core logic for both sheets is now imported ---
from create_addon import create_addon
from create_addon_coverages import create_addon_coverages

# Load environment variables
load_dotenv()

# --- All Authentication and Helper Functions (Unchanged) ---
def load_users_from_env():
    users = {}
    for i in range(1, 4):
        username = os.getenv(f'USER{i}_NAME')
        password = os.getenv(f'USER{i}_PASSWORD')
        if username and password:
            users[username] = password
    return users

def check_authentication(username, password, users):
    return username in users and users[username] == password

def authentication_page():
    users = load_users_from_env()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🔐 Authentication Required")
        st.markdown("Please login to access the PDF to Excel Extractor")
        st.markdown("---")
        username = st.text_input("Username", placeholder="Enter your username", key="login_username")
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
        if st.button("🚀 Login", use_container_width=True, type="primary"):
            if check_authentication(username, password, users):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password!")
        with st.expander("ℹ️ Test Users", expanded=False):
            st.markdown("**Available Test Users:**")
            if users:
                for user, pwd in users.items():
                    st.code(f"👤 {user} | 🔒 {pwd}", language="text")

# --- Page Config (Unchanged) ---
st.set_page_config(
    page_title="PDF to Excel Extractor",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- COMPLETE CSS BLOCK (Unchanged) ---
st.markdown("""
<style>
    /* Main app background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
    }
    /* Sidebar background */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
    }
    /* All text elements */
    .stMarkdown, .stText, .stDataFrame, .stExpander, .stButton, .stTextInput {
        color: white !important;
        background: transparent !important;
    }
    /* Dataframes */
    .stDataFrame > div {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
    }
    /* Input fields */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
    }
    /* Buttons */
    .stButton > button {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    /* Expanders */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    /* Text areas */
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    /* File uploader */
    .stFileUploader > div {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    /* Success and error messages */
    .stSuccess, .stError {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    /* Header styling for main app */
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        text-align: center;
        color: white !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        color: white !important;
    }
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file"""
    text = ""
    try:
        pdf_file.seek(0)
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        if len(text.strip()) < 100:
            pdf_file.seek(0)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return None

def create_addon_excel_with_formatting(covers_result):
    """Creates the 'Addon Covers' sheet with detailed formatting."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Addon Covers"
    yellow_fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
    wrap_alignment = Alignment(wrap_text=True, vertical='center')
    thin_border_all_sides = Border(left=Side(style='thin'),
                                   right=Side(style='thin'),
                                   top=Side(style='thin'),
                                   bottom=Side(style='thin'))
    if not covers_result:
        ws['A1'] = "No addon data was generated."
        return wb
    headers = list(covers_result[0].keys())
    num_cols = len(headers)

    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=num_cols)
    title_cell = ws.cell(row=1, column=1, value="Addon Covers")
    title_cell.alignment = wrap_alignment

    for row_num in [1, 2]:
        for i in range(1, num_cols + 1):
            cell = ws.cell(row=row_num, column=i)
            cell.fill = yellow_fill
            border_style = Border(top=Side(style='thin'), bottom=Side(style='thin'),
                                  left=Side(style='thin') if i == 1 else None,
                                  right=Side(style='thin') if i == num_cols else None)
            cell.border = border_style

    for col_num, header_title in enumerate(headers, 1):
        cell = ws.cell(row=3, column=col_num, value=header_title)
        cell.fill = yellow_fill
        cell.alignment = wrap_alignment
        cell.border = thin_border_all_sides
        ws.column_dimensions[openpyxl.utils.get_column_letter(col_num)].width = 18

    df = pd.DataFrame(covers_result)[headers]
    for row_index, row_data in enumerate(df.values, 4):
        for col_index, cell_value in enumerate(row_data, 1):
            cell = ws.cell(row=row_index, column=col_index, value=cell_value)
            cell.alignment = wrap_alignment
            cell.border = thin_border_all_sides
    return wb

def create_final_excel_workbook(covers_result, coverages_result):
    """Creates the workbook with final corrected layout and conditional logic."""
    wb = create_addon_excel_with_formatting(covers_result)
    ws = wb.create_sheet(title="Addon Coverages")

    # --- Define Styles and Helpers ---
    yellow_fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
    wrap_alignment = Alignment(wrap_text=True, vertical='center', horizontal='center')
    thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))

    def draw_table(start_col, title, headers, data_keys, data_dict):
        table_width = len(headers)
        # Apply formatting to all cells in the table's range
        for c in range(start_col, start_col + table_width):
            ws.column_dimensions[openpyxl.utils.get_column_letter(c)].width = 20
            for r in range(3, 6):
                cell = ws.cell(row=r, column=c)
                cell.alignment = wrap_alignment
                cell.border = thin_border
        
        ws.merge_cells(start_row=3, start_column=start_col, end_row=3, end_column=start_col + table_width - 1)
        ws.cell(row=3, column=start_col, value=title).fill = yellow_fill
        
        for i, header in enumerate(headers):
            col = start_col + i
            ws.cell(row=4, column=col, value=header).fill = yellow_fill
            value = data_dict.get(data_keys[i], "")
            data_cell = ws.cell(row=5, column=col, value=value)
            if "Percentage" in header and value:
                data_cell.number_format = '0.00%'
        
        return table_width

    # --- Define tables to draw based on data ---
    tables_to_draw = []
    if "Ambulance Cover" in coverages_result:
        tables_to_draw.append({
            "title": "Ambulance Cover",
            "headers": ["Number Of Trips", "Sum Insured", "% Limit Applicable On", "Limit Percentage", "Limit Amount", "Applicability"],
            "keys": ["Number of Trips", "Sum Insured", "% Limit Applicable On", "Limit Percentage", "Limit Amount", "Applicability"],
            "data": coverages_result["Ambulance Cover"]
        })
    if "Convalescence Benefit" in coverages_result:
        tables_to_draw.append({
            "title": "Convalescence Benefit",
            "headers": ["Minimum LOS in days", "Applicable From", "Sum Insured", "Benefit Amount"],
            "keys": ["Minimum LOS in days", "Applicable From", "Sum Insured", "Benefit Amount"],
            "data": coverages_result["Convalescence Benefit"]
        })

    # --- Draw the Sheet ---
    # Row 1: Title in merged cells up to Column J
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=10) # Merge to J
    title_cell = ws.cell(row=1, column=1, value="Addon Coverages")
    title_cell.fill = yellow_fill
    # Apply border to all merged cells in the title
    for i in range(1, 11):
        ws.cell(row=1, column=i).border = thin_border

    # Draw all tables and calculate total width
    current_col = 1
    total_width = 0
    for table in tables_to_draw:
        width = draw_table(current_col, table["title"], table["headers"], table["keys"], table["data"])
        total_width += width
        current_col += width
    
    # Row 2: Empty Yellow Row, colored only to the end of the last table
    if total_width > 0:
      for i in range(1, total_width + 1):
          ws.cell(row=2, column=i).fill = yellow_fill

    return wb

def main():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        authentication_page()
        return
    
    st.markdown(f"""
    <div class="main-header">
        <h1>🚀 PDF to Excel Extractor</h1>
        <p>Welcome, <strong>{st.session_state.username}</strong>! This tool extracts Addon Cover details from your PDF.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("### 👤 User Session")
        st.info(f"**Logged in as:** {st.session_state.username}")
        if st.button("🚪 Logout", type="secondary", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.rerun()
        st.markdown("---")

    uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type=['pdf'])
    
    if uploaded_file is not None:
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        with st.spinner("🔍 Extracting text from PDF..."):
            text = extract_text_from_pdf(uploaded_file)
        
        if text:
            addon_covers_result = create_addon(text)
            
            st.subheader("📊 Extracted Addon Covers (Yes/No)")
            df_addon = pd.DataFrame(addon_covers_result)
            st.dataframe(df_addon, use_container_width=True, height=150)

            with st.spinner("🧠 Extracting detailed coverage data..."):
                if addon_covers_result:
                    addon_coverages_result = create_addon_coverages(text, addon_covers_result[0])
                else:
                    addon_coverages_result = {}
            
            st.subheader("📋 Extracted Addon Coverages Details")
            if addon_coverages_result:
                display_data = []
                all_covers_to_display = ["Ambulance Cover", "Convalescence Benefit"]
                for cover_name in all_covers_to_display:
                    if cover_name in addon_coverages_result:
                        row = {"Coverage": cover_name}
                        row.update(addon_coverages_result[cover_name])
                        display_data.append(row)
                
                if display_data:
                    df_coverages = pd.DataFrame(display_data).fillna('')
                    st.dataframe(df_coverages, use_container_width=True)
            else:
                st.info("No detailed coverage data extracted.")

            with st.sidebar:
                with st.spinner("Creating final Excel file..."):
                    try:
                        wb = create_final_excel_workbook(addon_covers_result, addon_coverages_result)
                        excel_buffer = BytesIO()
                        wb.save(excel_buffer)
                        excel_buffer.seek(0)
                        
                        st.download_button(
                            label="📥 Download Full Excel Report",
                            data=excel_buffer.getvalue(),
                            file_name=f"Full_Report_{uploaded_file.name.split('.')[0]}_{datetime.now().strftime('%d-%m-%Y')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                    except Exception as e:
                        st.error(f"❌ Error generating Excel file: {str(e)}")
    else:
        st.info("Please upload a file to begin.")

if __name__ == "__main__":
    main()
