# 🎆 GMR Fire Works Store Management App

💥 A modern Streamlit-based inventory and sales management system for firework stores — manage stocks, sales, reports, and logs all in one place!

🧠 Overview

GMR Fire Works Store is a fully functional Store Management Web App built using Python + Streamlit, designed to help admins and staff efficiently manage stock entries, sales records, daily reports, and history logs — all stored locally with modular database models.
It’s optimized for both desktop and mobile, with smooth UI elements, modern animations, and role-based access control.

⚙️ Tech Stack
Category	Tools / Libraries
Framework	Streamlit
Backend	Python (OOP Modules for Stock, Sales, History, Session, Auth)
Database	SQLite (via custom models)
UI Enhancements	Lottie Animations, HTML/CSS Styling
Data Handling	Pandas
Auth System	Custom username/password + Role-based (Admin/Staff)
Reports	Date-range based CSV Export

*************************************************************************************************
LIVE VIEW:https://gmrstore-jglstore122344.streamlit.app/
*************************************************************************************************
✨ Features

✅ Login & Registration System (Admin & Staff roles)
📦 Stock Management: Add, delete (soft delete), restore, and view items
💰 Sales Entry: Record daily sales with automatic total calculation
🗃️ Trash Bin: Restore accidentally deleted records
📆 Sales Reports: Filter by date range and export as CSV
📈 Stock Trends & Analytics: Visual line chart of stock flow
🧾 History Logs: Track all actions by users (Admins only)
📱 Mobile Responsive Layout: Optimized for any screen size
🎨 Modern UI: Custom CSS, Lottie animations, and smooth theme

👉installation & Setup
Clone this repository
git clone https://github.com/yourusername/gmr-fireworks.git
cd gmr-fireworks

Install dependencies
pip install -r requirements.txt

Run the app
streamlit run app.py

Login or Register
Register a new user (choose admin or staff role)
Log in and start managing stocks/sales

🖥️ Main Pages & Features
Page/Description
🔐 Login / Register	Create and log in to accounts with roles
🏠 Dashboard	View overall stock, low stock items, and sales analytics
📦 Stock	Add, view, delete, restore stock items
💸 Sales	Record and manage daily sales
📆 Reports	View total sales between selected dates
📊 Stock Report	Filter stock by item/date and export as CSV
📜 History Log	Admin-only view of all user actions

📊 Dashboard Highlights
Total Stock Quantity
Low Stock Alerts
Total Sales (₹)
Recent Sales Table
Line Chart of Stock Trends

🔒 Role-Based Access Control
Role	Permissions
Admin	Full access + view history logs
Staff	Limited access (no delete/restore privileges)

📱 Mobile Responsive UI
The app auto-detects mobile view and adjusts layout for smaller screens — ensuring a seamless experience everywhere.

💾 Data Handling
All data is stored in local SQLite via model classes
Soft delete system ensures safe recovery
Automatic action logging for transparency

🧾 License
This project is licensed under the MIT License — free to use and modify.

🌟 Support & Star
If this app helps you, don’t forget to ⭐ Star the repo and share it with your friends — it motivates me to build more cool Streamlit stuff 🚀
