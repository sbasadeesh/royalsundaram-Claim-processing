import streamlit as st
import pandas as pd
import openpyxl
import io
from datetime import datetime

# --- Helper functions (no changes here) ---

def check_specific_datatype(value):
    """Determines the specific data type of a given value for reporting."""
    if value is None or str(value).strip() == '':
        return "Empty"
    if isinstance(value, (int, float)): 
        return "Numeric"
    if isinstance(value, str):
        if str(value).lower() in ['yes', 'no', 'y', 'n', 'true', 'false']: 
            return "Binary(Yes/No)"
        return "Text"
    if isinstance(value, datetime): 
        return "Date"
    try:
        float(value)
        return "Numeric"
    except (ValueError, TypeError):
        return "Other"
    
def validate_value_against_type(rule, value):
    """Checks if a value conforms to a data type rule string."""
    if value is None or str(value).strip() == '': 
        return True
    if not isinstance(rule, str): 
        return False
    
    rule = rule.lower().strip()
    
    if "numeric" in rule or "decimal" in rule:
        if isinstance(value, (int, float)): return True
        try:
            float(str(value)); return True
        except (ValueError, TypeError):
            return False
    if "text" in rule:
        return isinstance(value, str)
    if "binary" in rule:
        return str(value).lower() in ['yes', 'no', 'y', 'n', 'true', 'false']
    if "date" in rule:
        return isinstance(value, datetime)
    return False

# --- UPDATED: Core Logic to Skip Empty Template/Output Cells ---
def compare_excel_files(input_file, output_file):
    results = {}
    try:
        input_wb = openpyxl.load_workbook(input_file, data_only=True)
        output_wb = openpyxl.load_workbook(output_file, data_only=True)
    except Exception as e:
        st.error(f"Fatal Error: Could not open or read the Excel files. Please check if they are valid. Details: {e}")
        return {}

    common_sheets = sorted(list(set(input_wb.sheetnames).intersection(set(output_wb.sheetnames))))

    for sheet_name in common_sheets:
        try:
            results[sheet_name] = {"correct_cells": [], "discrepancies": []}
            input_ws = input_wb[sheet_name]
            output_ws = output_wb[sheet_name]
            
            num_data_cols = input_ws.max_column
            headers = {c: input_ws.cell(row=3, column=c).value for c in range(1, num_data_cols + 1)}
            rules = {col: input_ws.cell(row=4, column=col).value for col in range(1, num_data_cols + 1)}

            # 1. HEADER VALUE CHECK (Row 3)
            for col in range(1, num_data_cols + 1):
                template_cell = input_ws.cell(row=3, column=col)
                
                # --- NEW: Skip if the template header cell is empty ---
                if template_cell.value is None or str(template_cell.value).strip() == '':
                    continue
                
                output_cell = output_ws.cell(row=3, column=col)
                column_name = headers.get(col)
                error_base = {"Cell": output_cell.coordinate, "Column": column_name}
                
                if template_cell.value != output_cell.value:
                    results[sheet_name]["discrepancies"].append({**error_base, "Reason": "Header Value Mismatch", "Template_Value": template_cell.value, "Output_Value": output_cell.value})
                else:
                    results[sheet_name]["correct_cells"].append({**error_base, "Template_Value": template_cell.value, "Output_Value": output_cell.value})

            # 2. DATA TYPE CHECK (Row 4 onwards)
            for row_idx in range(4, output_ws.max_row + 1):
                row_cells = [output_ws.cell(row=row_idx, column=c).value for c in range(1, num_data_cols + 1)]
                if all(cell is None or str(cell).strip() == "" for cell in row_cells):
                    continue

                for col_idx in range(1, num_data_cols + 1):
                    rule_string = rules.get(col_idx)
                    output_cell = output_ws.cell(row=row_idx, column=col_idx)
                    
                    # --- NEW: Skip if the template rule is empty OR the output data is empty ---
                    if (rule_string is None or str(rule_string).strip() == '') or \
                       (output_cell.value is None or str(output_cell.value).strip() == ''):
                        continue

                    column_name = headers.get(col_idx, f"Column_{col_idx}")
                    error_base = {"Cell": output_cell.coordinate, "Column": column_name}
                    
                    if not validate_value_against_type(rule_string, output_cell.value):
                        detected_type = check_specific_datatype(output_cell.value)
                        results[sheet_name]["discrepancies"].append({**error_base, "Reason": "Datatype Mismatch", "Template_Value": rule_string, "Output_Value": detected_type})
                    else:
                        results[sheet_name]["correct_cells"].append({**error_base, "Template_Value": rule_string, "Output_Value": output_cell.value})
        
        except Exception as e:
            st.warning(f"Could not process sheet '{sheet_name}'. The following error occurred: {e}")
            if sheet_name in results:
                del results[sheet_name]
            continue
    
    return results

# --- Report Generation (no changes here) ---
def generate_excel_report(results, epic_number):
    output_stream = io.BytesIO()
    writer = pd.ExcelWriter(output_stream, engine='xlsxwriter')
    workbook = writer.book

    all_results_list = []
    
    for sheet_name, sheet_results in results.items():
        if sheet_results:
            for error in sheet_results.get("discrepancies", []):
                all_results_list.append({
                    "EPIC #": epic_number, "SHEET": sheet_name, "CELL": error.get("Cell", "N/A"),
                    "FIELD": error.get("Column", "N/A"), "EXPECTED VALUE": str(error.get("Template_Value", "")),
                    "TEST VALUE": str(error.get("Output_Value", "")), "RIGHT/WRONG": "WRONG",
                    "Correct fields": "", "Wrong fields": error.get("Reason", "Unknown Error")
                })
            for correct in sheet_results.get("correct_cells", []):
                 all_results_list.append({
                    "EPIC #": epic_number, "SHEET": sheet_name, "CELL": correct.get("Cell", "N/A"),
                    "FIELD": correct.get("Column", "N/A"), "EXPECTED VALUE": str(correct.get("Template_Value", "")),
                    "TEST VALUE": str(correct.get("Output_Value", "")), "RIGHT/WRONG": "RIGHT",
                    "Correct fields": "OK", "Wrong fields": ""
                })

    columns = ["EPIC #", "SHEET", "CELL", "FIELD", "EXPECTED VALUE", "TEST VALUE", "RIGHT/WRONG", "Correct fields", "Wrong fields"]
    if not all_results_list:
        detailed_df = pd.DataFrame(columns=columns)
    else:
        detailed_df = pd.DataFrame(all_results_list, columns=columns)

    # Overall KPI calculations (includes headers)
    correct_count = len(detailed_df[detailed_df["RIGHT/WRONG"] == "RIGHT"])
    wrong_count = len(detailed_df[detailed_df["RIGHT/WRONG"] == "WRONG"])
    total_count = correct_count + wrong_count
    performance_score = (correct_count / total_count * 100) if total_count > 0 else 100

    # Accuracy KPI for data cells only
    if not detailed_df.empty:
        data_rows_df = detailed_df[pd.to_numeric(detailed_df['CELL'].str.extract(r'(\d+)')[0], errors='coerce') >= 4]
        correct_data_count = len(data_rows_df[data_rows_df["RIGHT/WRONG"] == "RIGHT"])
        total_data_count = len(data_rows_df)
        accuracy_score = (correct_data_count / total_data_count * 100) if total_data_count > 0 else 100
    else:
        accuracy_score = 100.0

    # Create Sheet 1: QA Dashboard
    dashboard_sheet = workbook.add_worksheet("QA Dashboard")
    title_format = workbook.add_format({'bold': True, 'font_size': 20, 'align': 'center', 'valign': 'vcenter'})
    kpi_format = workbook.add_format({'bold': True, 'font_size': 28, 'align': 'center', 'valign': 'vcenter'})
    kpi_label_format = workbook.add_format({'font_size': 12, 'align': 'center', 'font_color': '#595959'})

    dashboard_sheet.merge_range('B2:G3', 'Quality Assurance Dashboard', title_format)
    dashboard_sheet.merge_range('B5:D7', f"{performance_score:.1f}%", kpi_format)
    dashboard_sheet.merge_range('B8:D8', 'Overall Performance Score (All Checks)', kpi_label_format)
    dashboard_sheet.merge_range('E5:G7', f"{accuracy_score:.1f}%", kpi_format)
    dashboard_sheet.merge_range('E8:G8', 'Overall Accuracy Score (Data Only)', kpi_label_format)
    dashboard_sheet.merge_range('B10:D12', correct_count, kpi_format)
    dashboard_sheet.merge_range('B13:D13', 'Total Correct Fields', kpi_label_format)
    dashboard_sheet.merge_range('E10:G12', wrong_count, kpi_format)
    dashboard_sheet.merge_range('E13:G13', 'Total Wrong Fields', kpi_label_format)
    
    dashboard_sheet.set_column('B:G', 22)
    
    # Create Sheet 2: Detailed Test Results
    detailed_df.to_excel(writer, sheet_name="Detailed Test Results", index=False, startrow=1, header=False)
    worksheet = writer.sheets["Detailed Test Results"]

    header_format_yellow = workbook.add_format({'bold': True, 'font_color': '#000000', 'bg_color': '#FFFF00', 'align': 'center', 'valign': 'vcenter', 'border': 1})
    header_format_red = workbook.add_format({'bold': True, 'font_color': 'white', 'bg_color': '#FF0000', 'align': 'center', 'valign': 'vcenter', 'border': 1})
    header_format_green = workbook.add_format({'bold': True, 'font_color': 'white', 'bg_color': '#70AD47', 'align': 'center', 'valign': 'vcenter', 'border': 1})

    for col_num, col_name in enumerate(detailed_df.columns):
        if col_num < 3:
            worksheet.write(0, col_num, col_name, header_format_yellow)
        elif col_num < 6:
            worksheet.write(0, col_num, col_name, header_format_red)
        else:
            worksheet.write(0, col_num, col_name, header_format_green)
    
    worksheet.set_column('A:I', 22)

    writer.close()
    output_stream.seek(0)
    return output_stream

# --- UI (no changes here) ---
st.set_page_config(page_title="Excel Validator Tool", layout="wide")
st.title("Excel Validator Tool")

if 'ran_comparison' not in st.session_state:
    st.session_state.ran_comparison = False
if 'results' not in st.session_state:
    st.session_state.results = {}
if 'epic_number' not in st.session_state:
    st.session_state.epic_number = ""

epic_number = st.text_input("Enter EPIC #")
input_file = st.file_uploader("Upload Input (Template) Excel", type=['xlsx'])
output_file = st.file_uploader("Upload Output (File to Test) Excel", type=['xlsx'])

if epic_number and input_file and output_file:
    if st.button("Run Full Validation", type="primary"):
        st.session_state.epic_number = epic_number
        with st.spinner("Performing validation..."):
            st.session_state.results = compare_excel_files(input_file, output_file)
        st.session_state.ran_comparison = True

if st.session_state.ran_comparison:
    results = st.session_state.get('results', {})
    if results:
        correct_count = sum(len(sheet.get('correct_cells', [])) for sheet in results.values() if sheet)
        wrong_count = sum(len(sheet.get('discrepancies', [])) for sheet in results.values() if sheet)
        total_count = correct_count + wrong_count
        
        performance_score = (correct_count / total_count * 100) if total_count > 0 else 100

        st.header("On-Screen Validation Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric(label="📊 Performance Score", value=f"{performance_score:.2f}%")
        col2.metric(label="✅ Correct Fields", value=correct_count)
        col3.metric(label="❌ Wrong Fields", value=wrong_count, delta_color="inverse")
                
        st.markdown("---")
        st.download_button(
            label="📄 Download Full Business Report (Excel)", 
            data=generate_excel_report(results, st.session_state.epic_number), 
            file_name=f"EPIC_{st.session_state.epic_number}_Validation_Report_{datetime.now().strftime('%d-%m-%Y_%H-%M')}.xlsx", 
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

