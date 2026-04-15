import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.markdown("Balai Svyam Seva Sasthan       Surpura")  # ← Yahan se 📊 hata diya

def load_data():
    # encoding fix aur khali rows hatana
    df = pd.read_csv("LTM.csv", header=2, encoding='latin-1').dropna(how='all')
    df.columns = df.columns.str.strip()
    
    if 'phone' in df.columns:
        df['phone'] = df['phone'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
    
    # Sabhi 'None' ya 'NaN' values ko khali string se badal dena
    df = df.fillna('')
    return df

# FUNCTION TO HIGHLIGHT TOTAL ROW IN RED
def highlight_total_row(row):
    if row.get('Name') == 'TOTAL':
        return ['background-color: #ffcccc; color: #cc0000; font-weight: bold'] * len(row)
    else:
        return [''] * len(row)

try:
    df = load_data()
    
    val = st.text_input("Mobile Number Enter Karein:")
    
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
                        clean_col = res[col].astype(str).str.replace(',', '').replace('', '0')
                        sums[col] = pd.to_numeric(clean_col, errors='coerce').sum()
                    else:
                        sums[col] = ""
                
                # TOTAL AMOUNT CALCULATION
                total_amount = 0
                if 'Total' in res.columns:
                    total_clean = res['Total'].astype(str).str.replace(',', '').replace('', '0')
                    total_amount = pd.to_numeric(total_clean, errors='coerce').sum()
                
                sums['Name'] = "TOTAL"
                total_row = pd.DataFrame([sums])
                final = pd.concat([res, total_row], ignore_index=True)
                
                final = final.fillna('')
                final = final.replace({0: '', '0': '', '0.0': '', 0.0: ''})
                
                st.success(f"✅ {len(res)} records mile | 💰 Total Amount: ₹{total_amount:,.2f}")
                
                styled_final = final.style.apply(highlight_total_row, axis=1)
                st.dataframe(styled_final, use_container_width=True, hide_index=True)
            else:
                st.warning(f"❌ Number '{val}' nahi mila!")          
except Exception as e:
    st.error(f"Error: {e}")