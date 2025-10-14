import streamlit as st
from datetime import date
import pandas as pd
import os

from models.stock import StockManager
from models.sales import SalesManager
from models.history import HistoryLogger
from utils.session import SessionManager
from auth import create_user_table, add_user, login_user, get_user_role
from streamlit_lottie import st_lottie
import requests
from datetime import datetime
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
st.set_page_config(page_title="GMR Fire Works Store", layout="wide")
st.markdown("""

<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
<style>

html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 16px;
    background-color: #181818;
    color: #f5f5f5;
}

.block-container {
    padding: 1rem;
    max-width: 100%;
}

.main {
    background-color: #1e3a8a;  /* Blue background for better contrast */
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.16);
}
h1, h2, h3 {
    color: #2196f3;
    font-weight: 600;
    margin-bottom: 0.5rem;
}
button[kind="primary"] {
    background-color: #2196f3;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: bold;
    transition: all 0.3s ease-in-out;
}
button[kind="primary"]:hover {
    background-color: #1565c0;
    transform: scale(1.02);
}
input, textarea, select {
    border-radius: 6px !important;
    border: 1px solid #ccc !important;
    padding: 8px !important;
}
.stDataFrame {
    background-color: #ffffff;
    border-radius: 8px;
    padding: 0.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

@media only screen and (max-width: 768px) {
    .stButton>button,
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stDateInput>div>div>input,
    .stSelectbox>div>div {
        width: 100% !important;
        font-size: 16px !important;
    }

    .stForm {
        padding: 1rem 0.5rem;
    }

    h2 {
        font-size: 24px !important;
    }

    h3 {
        font-size: 18px !important;
    }

    .stColumn {
        width: 100% !important;
        display: block;
    }

    .css-1xarl3l, .css-1r6slb0, .stMarkdown {
        margin-bottom: 1rem !important;
    }
}
</style>
""", unsafe_allow_html=True)

if not os.path.exists("data"):
    os.makedirs("data")
stock_manager = StockManager()
sales_manager = SalesManager()
history_logger = HistoryLogger()
session = SessionManager(st.session_state)
create_user_table()
def login_page():
    st.title("🔐 GMR Fire Works Login")

    lottie = load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_t9gkkhz4.json")
    if lottie:
        st_lottie(lottie, height=220, speed=1)

    choice = st.selectbox("Login or Register", ["Login", "Register"])
    
    if choice == "Login":
        st.markdown("### 👤 Login to your account")
        user = st.text_input("Username")
        pwd = st.text_input("Password", type='password')
        if st.button("🔓 Login"):
            if login_user(user, pwd):
                session.login(user, get_user_role(user))
                st.success("✅ Login successful")
                st.rerun()
            else:
                st.error("❌ Invalid credentials")
    else:
        st.markdown("### 📝 Register a new account")
        new_user = st.text_input("New Username")
        new_pwd = st.text_input("New Password", type='password')
        role = st.selectbox("Select Role", ["admin", "staff"])
        if st.button("✅ Registered"):
            try:
                add_user(new_user, new_pwd, role)
                st.success("🎉 Registered successfully")
            except:
                st.error("⚠️ Username already exists")

def stock_entry():
    st.title("📦 Add Stock")
    with st.form("stock_form", clear_on_submit=True):
        item = st.text_input("Item")
        qty = st.number_input("Quantity", min_value=1, step=1)
        price = st.number_input("Cost Price", min_value=0.0)
        supplier = st.text_input("Supplier")
        d = st.date_input("Date", value=date.today())
        if st.form_submit_button("Add"):
            stock_manager.add_stock(item, qty, price, supplier, d.strftime("%Y-%m-%d"))
            history_logger.log("ADD_STOCK", item, qty, session.session.username)
            st.success("Stock added")

    st.subheader("📋 Current Stock")
    stock = stock_manager.get_all_stock()
    if stock:
        df = pd.DataFrame(stock, columns=["ID", "Item", "Qty", "Cost", "Supplier", "Date", "Deleted"])
        st.dataframe(df.drop(columns=["Deleted"]), use_container_width=True)
    del_id = st.text_input("Enter Stock ID to delete")
    if del_id.isdigit():
        if st.button(f"🗑️ Confirm Delete Stock ID {del_id}"):
            stock = stock_manager.get_stock_by_id(int(del_id))
            if stock:
                stock_manager.soft_delete_stock(int(del_id))
                history_logger.log("SOFT_DELETE_STOCK", stock[1], stock[2], session.session.username)
                st.warning(f"🗑️ Stock ID {del_id} moved to Trash")
                st.rerun()

    with st.expander("🗃️ View Deleted Stock (Trash Bin)"):
        trash = stock_manager.get_deleted_stock()
        if trash:
            df_trash = pd.DataFrame(trash, columns=["ID", "Item", "Qty", "Cost", "Supplier", "Date", "Deleted"])
            st.dataframe(df_trash.drop(columns=["Deleted"]), use_container_width=True)
            restore_id = st.text_input("Enter ID to restore")
            if restore_id.isdigit() and st.button("♻️ Restore Stock"):
                stock_manager.restore_stock(int(restore_id))
                st.success(f"Restored Stock ID {restore_id}")
                st.rerun()

def sales_entry(): 
    st.title("💰 Record Sale")
    with st.form("sales_form", clear_on_submit=True):
        item = st.text_input("Item Name")
        qty = st.number_input("Quantity", min_value=1, step=1)
        price = st.number_input("Selling Price", min_value=0.0)
        customer = st.text_input("Customer")
        d = st.date_input("Date", value=date.today())

        if st.form_submit_button("Record Sale"):
            sales_manager.add_sale(
                item, qty, price, customer,
                d.strftime("%Y-%m-%d"), session.session.username
            )
            history_logger.log("SALE", item, qty, session.session.username)
            st.success("Sale recorded")
    st.subheader("🧾 View & Manage Sales")

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=date.today())
    with col2:
        end_date = st.date_input("End Date", value=date.today())

    records = sales_manager.get_sales_by_date(
        start_date.strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d")
    )

    if records:
        df = pd.DataFrame(records, columns=["ID", "Item", "Qty", "Price", "Total", "Customer", "Date", "User", "Deleted"])
        st.dataframe(df.drop(columns=["Deleted"]), use_container_width=True)
        del_id = st.text_input("Enter Sale ID to delete")
        if del_id.isdigit() and st.button(f"🗑️ Confirm Delete Sale ID {del_id}"):
            sale = sales_manager.get_sale_by_id(int(del_id))
            if sale:
                sales_manager.soft_delete_sale(int(del_id))
                history_logger.log("SOFT_DELETE_SALE", sale[1], sale[2], session.session.username)
                st.warning(f"Sale ID {del_id} moved to Trash")
                st.rerun()
        with st.expander("🗃️ View Deleted Sales (Trash Bin)"):
            trash_sales = sales_manager.get_deleted_sales()
            if trash_sales:
                df_trash_sales = pd.DataFrame(trash_sales, columns=["ID", "Item", "Qty", "Price", "Total", "Customer", "Date", "User", "Deleted"])
                st.dataframe(df_trash_sales.drop(columns=["Deleted"]), use_container_width=True)

                restore_id = st.text_input("Enter Sale ID to restore")
                if restore_id.isdigit() and st.button("♻️ Restore Sale"):
                    sales_manager.restore_sale(int(restore_id))
                    st.success(f"Restored Sale ID {restore_id}")
                    st.rerun()
            else:
                st.info("Trash Bin is empty")
    else: 
        st.info("No sales found for the selected date range")

def dashboard():
    st.title("🎆GMR FireWorks Home")

    stock = stock_manager.get_all_stock()
    sales = sales_manager.get_sales()
    if st.session_state.get("is_mobile", False):
        col1 = st.container()
        col2 = st.container()
        col3 = st.container()
    else:
        col1, col2, col3 = st.columns(3)
    lottie_url = "https://assets10.lottiefiles.com/packages/lf20_5ngs2ksb.json"
    lottie = load_lottie_url(lottie_url)
    if lottie:
        st_lottie(lottie, height=120, speed=1, key="dashboard_anim")
    if stock:
        df = pd.DataFrame(stock, columns=["ID", "Item", "Qty", "Cost", "Supplier", "Date", "Deleted"])
        with col1:
            st.markdown("""
<div style='padding:1rem; background:#1e3a8a; border-radius:12px; box-shadow:0 4px 8px rgba(0,0,0,0.1); margin-bottom:1rem;'>
    <h3 style='margin-bottom:0; color:white; font-size:20px;'>📦 Total Stock</h3>
    <h2 style='color:#f97316; font-size:28px;'>{}</h2>
    <p style='color:#f5f5f5; font-size:14px;'>Items in inventory</p>
</div>
""".format(df["Qty"].sum()), unsafe_allow_html=True)
    with col2:
        low_stock = stock_manager.get_low_stock()
        st.markdown("""
<div style='padding:1rem; background:#1e3a8a; border-radius:12px; box-shadow:0 4px 8px rgba(0,0,0,0.1); margin-bottom:1rem;'>
    <h3 style='margin-bottom:0; color:white; font-size:20px;'>⚠️ Low Stock Items</h3>
    <h2 style='color:#ff6b6b; font-size:28px;'>{}</h2>
    <p style='color:#f5f5f5; font-size:14px;'>Items below threshold</p>
</div>
""".format(len(low_stock)), unsafe_allow_html=True)
    if sales:
        sdf = pd.DataFrame(sales, columns=["ID", "Item", "Qty", "Price", "Total", "Customer", "Date", "User", "Deleted"])
        with col3:
            st.markdown("""
<div style='padding:1rem; background:#1e3a8a; border-radius:12px; box-shadow:0 4px 8px rgba(0,0,0,0.1); margin-bottom:1rem;'>
    <h3 style='margin-bottom:0; color:white; font-size:20px;'>💸 Total Sales</h3>
    <h2 style='color:#4ade80; font-size:28px;'>₹{:.2f}</h2>
    <p style='color:#f5f5f5; font-size:14px;'>Sales revenue</p>
</div>
""".format(sdf['Total'].sum()), unsafe_allow_html=True)
    st.markdown("### 🕒 Recent Sales")
    if sales:
        recent_sales = sdf.sort_values("Date", ascending=False).head(5)
        st.dataframe(recent_sales[["Item", "Qty", "Total", "Customer", "Date"]], use_container_width=True, height=250)
    else:
        st.info("No sales records yet.")
    st.markdown("### 📈 Stock Trends")
    if stock:
        trend_df = df.groupby("Date")["Qty"].sum().reset_index()
        st.line_chart(trend_df.rename(columns={"Date": "Stock Date", "Qty": "Total Qty"}).set_index("Stock Date"))
    else:
        st.info("No stock data to show trends.")

    st.markdown("""
<script>
const setMobile = () => {
    if (window.innerWidth < 768) {
        window.parent.postMessage({type: 'streamlit:setSessionState', key: 'is_mobile', value: true}, '*');
    } else {
        window.parent.postMessage({type: 'streamlit:setSessionState', key: 'is_mobile', value: false}, '*');
    }
};
window.addEventListener('resize', setMobile);
setMobile();
</script>
""", unsafe_allow_html=True)

def sales_reports_page():
    st.title("📆 Sales Report")
    from_date = st.date_input("From", value=date.today())
    to_date = st.date_input("To", value=date.today())
    if from_date > to_date:
        st.warning("From date should be earlier than To date")
        return
    records = sales_manager.get_sales_by_date(from_date.strftime("%Y-%m-%d"), to_date.strftime("%Y-%m-%d"))
    if records:
        df = pd.DataFrame(records, columns=["ID", "Item", "Qty", "Price", "Total", "Customer", "Date", "User", "Deleted"])
        st.dataframe(df.drop(columns=["Deleted"]), use_container_width=True)
        st.success(f"Total Sales: ₹{df['Total'].sum():.2f}")
    else:
        st.info("No sales records for this period")

def stock_report_page():
    st.title("📦 Stock Report")

    stock = stock_manager.get_all_stock()
    if not stock:
        st.info("No stock data available.")
        return

    df = pd.DataFrame(stock, columns=["ID", "Item", "Qty", "Cost", "Supplier", "Date", "Deleted"])
    df = df[df["Deleted"] == 0]

    st.subheader("🔍 Filter")
    item_filter = st.text_input("Filter by item name").lower()
    from_date = st.date_input("From Date", value=date.today())
    to_date = st.date_input("To Date", value=date.today())

    if item_filter:
        df = df[df["Item"].str.lower().str.contains(item_filter)]

    df['Date'] = pd.to_datetime(df['Date'])
    df = df[(df['Date'] >= pd.to_datetime(from_date)) & (df['Date'] <= pd.to_datetime(to_date))]

    st.dataframe(df.drop(columns=["Deleted"]), use_container_width=True)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", csv, "stock_report.csv", "text/csv")

def history_page():
    if not session.is_admin():
        st.warning("Access Denied: Admins only")
        return

    st.title("📜 Action History Log")
    selected_date = st.date_input("Select Date to View History", value=date.today())
    selected_str = selected_date.strftime("%Y-%m-%d")

    logs = history_logger.get_logs()
    
    if logs:
        df = pd.DataFrame(logs, columns=["ID", "Action", "Item", "Qty", "User", "Time"])

        # Filter by date
        df["Date"] = pd.to_datetime(df["Time"]).dt.date.astype(str)
        filtered_df = df[df["Date"] == selected_str]

        if not filtered_df.empty:
            st.dataframe(filtered_df.drop(columns=["Date"]), use_container_width=True)
        else:
            st.info(f"No history logs found for {selected_str}")
    else:
        st.info("No logs found")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

if not st.session_state.logged_in:
    login_page()
else:
    st.sidebar.title("Navigation")
    st.sidebar.write(f"👤 {st.session_state.username} ({st.session_state.role})")
    opt = st.sidebar.radio("Go to", ["Dashboard", "Stock", "Sales", "Reports", "Stock Report", "History"])
    if st.sidebar.button("Logout"):
        session.logout()
        st.rerun()

    if opt == "Dashboard":
        dashboard()
    elif opt == "Stock":
        stock_entry()
    elif opt == "Sales":
        sales_entry()
    elif opt == "Reports":
        sales_reports_page()
    elif opt == "Stock Report":
        stock_report_page()
    elif opt == "History":
        history_page()

