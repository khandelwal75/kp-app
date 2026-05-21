import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.markdown("Balai Svyam Seva Sasthan       Surpura")  # ← Yahan se 📊 hata diya

def load_data():
    # --- A2 cell se date nikalne ke liye ---
    raw_df = pd.read_csv(r"e:\python\LTM.csv", header=None, nrows=2, encoding='latin-1')
    try:
        # Excel ka A2 cell = Row Index 1 (2nd row) aur Column Index 0 (A column)
        extracted_date = raw_df.iloc[1, 0] 
    except Exception:
        extracted_date = ""
    
    # Data loading (Header=2 se)
    df = pd.read_csv(r"e:\python\LTM.csv", header=2, encoding='latin-1').dropna(how='all')
    df.columns = df.columns.str.strip()
    
    # Phone number ko normal string rakhna taaki search sahi ho
    if 'phone' in df.columns:
        df['phone'] = df['phone'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
    
    # Baaki columns ke andar ke values ko number me badalna taaki total sahi nikle
    num_cols = ['Nest Lo.', 'Discount', 'Kist', 'K.P.', 'Loan', 'L.P.', 'Inter', 'Other', 'Total', 'L.Balance']
    for col in df.columns:
        if col in num_cols:
            df[col] = df[col].astype(str).str.replace(',', '').str.strip()
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    return df, extracted_date

# FUNCTION TO HIGHLIGHT TOTAL ROW IN RED
def highlight_total_row(row):
    if row.get('Name') == 'TOTAL':
        return ['background-color: #ffcccc; color: #cc0000; font-weight: bold'] * len(row)
    else:
        return [''] * len(row)

try:
    df, file_date = load_data()
    
    # --- INPUT TEXT KE BILKUL BARABAR RIGHT MEIN DATE ---
    st.markdown(
        f"""
        <div style='display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 8px;'>
            <label style='font-weight: 500; font-size: 16px; color: inherit; font-family: inherit;'>
                Mobile Number Enter Karein:
            </label>
            <div style='font-weight: bold; color: #1f77b4; font-size: 16px;'>
              List Date: {file_date}
            </div>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    val = st.text_input("Mobile Number Enter Karein:", label_visibility="collapsed")
    
    if val:
        if 'phone' not in df.columns:
            st.error("Phone column nahi mila!")
            st.write("Available columns:", df.columns.tolist())
        else:
            res = df[df['phone'].astype(str).str.contains(str(val), na=False, regex=False)].copy()
            
            if not res.empty:
                num_cols = ['Nest Lo.', 'Discount', 'Kist', 'K.P.', 'Loan', 'L.P.', 'Inter', 'Other', 'Total', 'L.Balance']
                existing_num_cols = [col for col in num_cols if col in df.columns]
                
                sums = {}
                for col in res.columns:
                    if col in existing_num_cols:
                        sums[col] = res[col].sum()
                    else:
                        sums[col] = ""
                
                # TOTAL AMOUNT CALCULATION
                total_amount = 0
                if 'Total' in res.columns:
                    total_amount = res['Total'].sum()
                
                sums['Name'] = "TOTAL"
                total_row = pd.DataFrame([sums])
                final = pd.concat([res, total_row], ignore_index=True)
                
                # Khali rows ya 0 ko blank karna taaki table saaf dikhe
                final = final.fillna('')
                final = final.replace({0: '', 0.0: ''})
                
                # --- FIXED: Yahan se total_amount se .00 hata diya gaya hai ---
                st.success(f"✅ {len(res)} records mile | 💰 Total Amount: ₹{int(total_amount):,d}")
                
                # Table se phone column ko show hone se hatana
                if 'phone' in final.columns:
                    final = final.drop(columns=['phone'])
                
                # Table ko bina .000000 ke aur bina phone number ke screen par dikhana
                styled_final = final.style.apply(highlight_total_row, axis=1).format(precision=0, na_rep="")
                st.dataframe(styled_final, use_container_width=True, hide_index=True)
            else:
                st.warning(f"❌ Number '{val}' nahi mila!")          
except Exception as e:
    st.error(f"Error: {e}")