import customtkinter as ctk
from tkinter import messagebox, filedialog
import csv
from datetime import datetime
from db_manager import DBManager
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Set appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class GymApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("IRON GYM | ENTERPRISE COMMAND CENTER")
        self.geometry("1280x800")
        
        self.role = None
        self.username = None
        self.current_member_id = None
        
        self.show_login()

    # ==========================================
    # LOGIN UI (Professional Glass Style)
    # ==========================================
    def show_login(self):
        for w in self.winfo_children(): w.destroy()
        
        # Center login box
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        frame = ctk.CTkFrame(self, width=400, height=500, corner_radius=20, border_width=2, border_color="#1f6aa5")
        frame.grid(row=0, column=0)
        frame.pack_propagate(False)
        
        ctk.CTkLabel(frame, text="IRON GYM", font=("Orbitron", 32, "bold"), text_color="#1f6aa5").pack(pady=(50, 10))
        ctk.CTkLabel(frame, text="Command Center Login", font=("Segoe UI", 14), text_color="gray").pack(pady=(0, 40))
        
        self.ent_user = ctk.CTkEntry(frame, width=300, height=45, placeholder_text="Username / Member ID", corner_radius=10)
        self.ent_user.pack(pady=10)
        
        self.ent_pass = ctk.CTkEntry(frame, width=300, height=45, placeholder_text="Password", show="*", corner_radius=10)
        self.ent_pass.pack(pady=10)
        
        ctk.CTkButton(frame, text="AUTHENTICATE", width=300, height=50, font=("Segoe UI", 16, "bold"), 
                     corner_radius=10, command=self.handle_login).pack(pady=40)
        
        ctk.CTkLabel(frame, text="Hint: admin/admin | user/user", font=("Segoe UI", 10), text_color="gray").pack()

    def handle_login(self):
        u, p = self.ent_user.get(), self.ent_pass.get()
        if u == "admin" and p == "admin":
            self.role, self.username = "Admin", "Administrator"
            self.setup_main_ui()
        elif u == "user" and p == "user":
            self.role, self.username = "User", "Gym Staff"
            self.setup_main_ui()
        else:
            try:
                res = DBManager.execute_query("SELECT MEMBERID, FIRSTNAME FROM MEMBER WHERE MEMBERID = :1 AND PASSWORD = :2", (u, p))
                if res:
                    self.role, self.username, self.current_member_id = "Member", res[0][1], res[0][0]
                    self.setup_main_ui()
                    return
            except: pass
            messagebox.showerror("Auth Error", "Access Denied: Invalid Credentials")

    # ==========================================
    # MAIN NAVIGATION & SHELL
    # ==========================================
    def setup_main_ui(self):
        for w in self.winfo_children(): w.destroy()
        
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color="#1a1a1a")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        ctk.CTkLabel(self.sidebar, text="IRON GYM", font=("Orbitron", 24, "bold"), text_color="#1f6aa5").pack(pady=30)
        
        # Nav Buttons (Only for Staff/Admin)
        if self.role != "Member":
            self.add_nav_btn("📊  DASHBOARD", self.show_dashboard)
            self.add_nav_btn("👥  MEMBERS", self.show_members)
            self.add_nav_btn("💳  PAYMENTS", self.show_payments)
            self.add_nav_btn("💎  SUBSCRIPTIONS", self.show_plans)
            self.add_nav_btn("👔  STAFF", self.show_staff)
            self.add_nav_btn("⚙️  EQUIPMENT", self.show_equipment)
            self.add_nav_btn("📜  AUDIT LOGS", self.show_audit_logs)
        else:
            self.add_nav_btn("👤  MY PROFILE", self.show_member_portal)
            
        ctk.CTkButton(self.sidebar, text="LOGOUT", fg_color="transparent", border_width=1, command=self.show_login).pack(side="bottom", pady=20, padx=20)

        # Content Area
        self.content = ctk.CTkFrame(self, corner_radius=20, fg_color="#121212")
        self.content.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        self.show_dashboard() if self.role != "Member" else self.show_member_portal()

    def add_nav_btn(self, text, cmd):
        btn = ctk.CTkButton(self.sidebar, text=text, anchor="w", fg_color="transparent", 
                           font=("Segoe UI", 13, "bold"), height=45, corner_radius=10, command=cmd)
        btn.pack(fill="x", padx=15, pady=5)
        return btn

    # ==========================================
    # WORLD CLASS DASHBOARD (Phase 5)
    # ==========================================
    def show_dashboard(self):
        for w in self.content.winfo_children(): w.destroy()
        
        header = ctk.CTkFrame(self.content, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=20)
        ctk.CTkLabel(header, text="Enterprise Dashboard", font=("Segoe UI", 32, "bold")).pack(side="left")
        
        # Stats Cards
        card_f = ctk.CTkFrame(self.content, fg_color="transparent")
        card_f.pack(fill="x", padx=30)
        
        m_count = DBManager.execute_query("SELECT COUNT(*) FROM MEMBER")[0][0]
        revenue = DBManager.execute_query("SELECT SUM(AMOUNT) FROM PAYMENT")[0][0] or 0
        staff = DBManager.execute_query("SELECT COUNT(*) FROM STAFF")[0][0]
        
        self.create_kpi(card_f, "Active Members", str(m_count), "#1f6aa5")
        self.create_kpi(card_f, "Total Revenue", f"PKR {revenue:,}", "#2ecc71")
        self.create_kpi(card_f, "Gym Staff", str(staff), "#e67e22")

        # Chart Section
        chart_f = ctk.CTkFrame(self.content, corner_radius=15, fg_color="#1a1a1a")
        chart_f.pack(fill="both", expand=True, padx=30, pady=20)
        
        fig, ax = plt.subplots(figsize=(6, 3), facecolor="#1a1a1a")
        ax.set_facecolor("#1a1a1a")
        # Sample Trend (You can make this dynamic with SQL later)
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
        growth = [10, 25, 45, 60, m_count]
        ax.plot(months, growth, marker='o', color='#1f6aa5', linewidth=3)
        ax.set_title("Member Growth Trend", color='white', pad=20)
        ax.tick_params(colors='white')
        for spine in ax.spines.values(): spine.set_color('#333')
        
        canvas = FigureCanvasTkAgg(fig, master=chart_f)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    def create_kpi(self, parent, title, val, color):
        f = ctk.CTkFrame(parent, width=250, height=120, corner_radius=15, border_width=1, border_color=color)
        f.pack(side="left", padx=10, pady=10, expand=True)
        f.pack_propagate(False)
        ctk.CTkLabel(f, text=title, font=("Segoe UI", 14), text_color="gray").pack(pady=(20, 5))
        ctk.CTkLabel(f, text=val, font=("Segoe UI", 28, "bold"), text_color=color).pack()

    # ==========================================
    # CRM: MEMBER MANAGEMENT (Modern List)
    # ==========================================
    def show_members(self):
        for w in self.content.winfo_children(): w.destroy()
        
        header = ctk.CTkFrame(self.content, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=20)
        ctk.CTkLabel(header, text="Member Registry", font=("Segoe UI", 28, "bold")).pack(side="left")
        
        if self.role == "Admin":
            ctk.CTkButton(header, text="+ Register Member", width=160, command=self.add_member_window).pack(side="right", padx=10)
        
        # Search Box
        search_f = ctk.CTkFrame(self.content, fg_color="transparent")
        search_f.pack(fill="x", padx=30, pady=10)
        self.ent_search = ctk.CTkEntry(search_f, placeholder_text="Search by Name or ID...", width=400)
        self.ent_search.pack(side="left")
        ctk.CTkButton(search_f, text="Search", width=80, command=lambda: self.refresh_member_list(self.ent_search.get())).pack(side="left", padx=10)

        # List Area
        self.list_frame = ctk.CTkScrollableFrame(self.content, fg_color="#1a1a1a")
        self.list_frame.pack(fill="both", expand=True, padx=30, pady=10)
        self.refresh_member_list()

    def refresh_member_list(self, query=""):
        for w in self.list_frame.winfo_children(): w.destroy()
        sql = "SELECT * FROM MEMBER"
        if query:
            sql += f" WHERE FIRSTNAME LIKE '%{query}%' OR LASTNAME LIKE '%{query}%' OR MEMBERID LIKE '%{query}%'"
        sql += " ORDER BY MEMBERID DESC"
        
        data = DBManager.execute_query(sql)
        if data:
            for m in data:
                card = ctk.CTkFrame(self.list_frame, height=80, corner_radius=10)
                card.pack(fill="x", pady=5, padx=5)
                
                info = f"ID: {m[0]} | {m[1]} {m[2]} | {m[5]}"
                ctk.CTkLabel(card, text=info, font=("Segoe UI", 14, "bold")).pack(side="left", padx=20)
                
                if self.role == "Admin":
                    ctk.CTkButton(card, text="DELETE", fg_color="#e74c3c", width=80, 
                                 command=lambda i=m[0]: self.delete_rec(i, "MEMBER", self.show_members)).pack(side="right", padx=10)

    def add_member_window(self):
        # Professional Popup for Registration
        pop = ctk.CTkToplevel(self)
        pop.title("Register New Member")
        pop.geometry("450x650")
        pop.after(100, lambda: pop.lift()) # Ensure it's on top
        pop.after(200, lambda: pop.focus_force())
        pop.grab_set() # Block main window
        
        ctk.CTkLabel(pop, text="Member Details", font=("Segoe UI", 20, "bold")).pack(pady=20)
        
        e_fn = ctk.CTkEntry(pop, width=300, placeholder_text="First Name")
        e_fn.pack(pady=5)
        e_ln = ctk.CTkEntry(pop, width=300, placeholder_text="Last Name")
        e_ln.pack(pady=5)
        e_ph = ctk.CTkEntry(pop, width=300, placeholder_text="Phone Number")
        e_ph.pack(pady=5)
        e_em = ctk.CTkEntry(pop, width=300, placeholder_text="Email Address")
        e_em.pack(pady=5)
        e_gen = ctk.CTkComboBox(pop, width=300, values=["M", "F", "O"])
        e_gen.pack(pady=5)
        e_dob = ctk.CTkEntry(pop, width=300, placeholder_text="DOB (DD-MM-YYYY)")
        e_dob.pack(pady=5)
        e_pwd = ctk.CTkEntry(pop, width=300, placeholder_text="Portal Password")
        e_pwd.pack(pady=5)

        def save():
            try:
                dob = self.parse_date(e_dob.get())
                pwd = e_pwd.get() or "1234"
                DBManager.execute_query(
                    "INSERT INTO MEMBER (FIRSTNAME, LASTNAME, PHONE, EMAIL, GENDER, DATEOFBIRTH, PASSWORD) VALUES (:1, :2, :3, :4, :5, TO_DATE(:6, 'YYYY-MM-DD'), :7)",
                    (e_fn.get(), e_ln.get(), e_ph.get(), e_em.get(), e_gen.get(), dob, pwd), commit=True
                )
                pop.destroy()
                self.show_members()
                messagebox.showinfo("Success", "New member onboarded successfully!")
            except Exception as e: messagebox.showerror("Error", str(e))

        ctk.CTkButton(pop, text="CONFIRM REGISTRATION", width=300, height=45, command=save).pack(pady=30)

    # ==========================================
    # FINANCIALS: PAYMENTS (Ledger Style)
    # ==========================================
    def show_payments(self):
        for w in self.content.winfo_children(): w.destroy()
        
        header = ctk.CTkFrame(self.content, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=20)
        ctk.CTkLabel(header, text="Financial Ledger", font=("Segoe UI", 28, "bold")).pack(side="left")
        
        if self.role == "Admin":
            ctk.CTkButton(header, text="+ New Payment", width=150, command=self.add_payment_window).pack(side="right")

        # Table Header
        th = ctk.CTkFrame(self.content, fg_color="#1a1a1a", height=40)
        th.pack(fill="x", padx=30)
        ctk.CTkLabel(th, text="ID", width=50).pack(side="left", padx=10)
        ctk.CTkLabel(th, text="Member", width=150).pack(side="left", padx=10)
        ctk.CTkLabel(th, text="Amount", width=100).pack(side="left", padx=10)
        ctk.CTkLabel(th, text="Date", width=150).pack(side="left", padx=10)
        ctk.CTkLabel(th, text="Status", width=100).pack(side="left", padx=10)

        scroll = ctk.CTkScrollableFrame(self.content, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=30, pady=5)
        
        data = DBManager.execute_query("SELECT P.PAYMENTID, M.FIRSTNAME, P.AMOUNT, P.PAYMENT_DATE FROM PAYMENT P JOIN MEMBER M ON P.MEMBERID = M.MEMBERID ORDER BY P.PAYMENTID DESC")
        if data:
            for p in data:
                row = ctk.CTkFrame(scroll, fg_color="#1e1e1e", height=45)
                row.pack(fill="x", pady=2)
                ctk.CTkLabel(row, text=str(p[0]), width=50).pack(side="left", padx=10)
                ctk.CTkLabel(row, text=str(p[1]), width=150).pack(side="left", padx=10)
                ctk.CTkLabel(row, text=f"PKR {p[2]}", width=100, text_color="#2ecc71").pack(side="left", padx=10)
                ctk.CTkLabel(row, text=str(p[3]), width=150).pack(side="left", padx=10)
                ctk.CTkLabel(row, text="PAID ✅", width=100, text_color="#2ecc71").pack(side="left", padx=10)

    def add_payment_window(self):
        pop = ctk.CTkToplevel(self)
        pop.title("Collect Payment")
        pop.geometry("400x400")
        pop.after(100, lambda: pop.lift())
        pop.after(200, lambda: pop.focus_force())
        pop.grab_set()
        
        ctk.CTkLabel(pop, text="Payment Details", font=("Segoe UI", 20, "bold")).pack(pady=20)
        e_id = ctk.CTkEntry(pop, width=250, placeholder_text="Member ID")
        e_id.pack(pady=10)
        e_am = ctk.CTkEntry(pop, width=250, placeholder_text="Amount (PKR)")
        e_am.pack(pady=10)
        e_me = ctk.CTkComboBox(pop, width=250, values=["Cash", "Card", "Online"])
        e_me.pack(pady=10)
        
        def save():
            try:
                DBManager.execute_query("INSERT INTO PAYMENT (MEMBERID, AMOUNT, METHOD) VALUES (:1, :2, :3)", 
                                      (e_id.get(), e_am.get(), e_me.get()), commit=True)
                pop.destroy()
                self.show_payments()
            except Exception as e: messagebox.showerror("Error", str(e))
            
        ctk.CTkButton(pop, text="COLLECT", width=250, height=40, command=save).pack(pady=30)

    # ==========================================
    # SUBSCRIPTIONS: PRICING GALLERY
    # ==========================================
    def show_plans(self):
        for w in self.content.winfo_children(): w.destroy()
        header = ctk.CTkFrame(self.content, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=20)
        ctk.CTkLabel(header, text="Membership Subscriptions", font=("Segoe UI", 28, "bold")).pack(side="left")
        
        main_f = ctk.CTkFrame(self.content, fg_color="transparent")
        main_f.pack(fill="both", expand=True, padx=30)
        
        data = DBManager.execute_query("SELECT * FROM MEMBERSHIP_PLAN ORDER BY PRICE")
        if data:
            for p in data:
                card = ctk.CTkFrame(main_f, width=220, height=300, corner_radius=15, border_width=1, border_color="#1f6aa5")
                card.pack(side="left", padx=10, pady=10)
                card.pack_propagate(False)
                
                ctk.CTkLabel(card, text=p[1], font=("Segoe UI", 16, "bold"), text_color="#1f6aa5").pack(pady=20)
                ctk.CTkLabel(card, text=f"PKR {p[2]:,}", font=("Segoe UI", 24, "bold")).pack(pady=10)
                ctk.CTkLabel(card, text=f"Duration: {p[3]} Days", text_color="gray").pack(pady=10)
                ctk.CTkButton(card, text="Select Plan", width=160, fg_color="#1f6aa5").pack(side="bottom", pady=20)

    # ==========================================
    # OTHER MODULES (Staff, Equipment, Logs)
    # ==========================================
    def show_staff(self):
        for w in self.content.winfo_children(): w.destroy()
        header = ctk.CTkFrame(self.content, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=20)
        ctk.CTkLabel(header, text="Staff Directory", font=("Segoe UI", 28, "bold")).pack(side="left")
        
        scroll = ctk.CTkScrollableFrame(self.content, fg_color="#1a1a1a")
        scroll.pack(fill="both", expand=True, padx=30, pady=10)
        
        data = DBManager.execute_query("SELECT * FROM STAFF")
        if data:
            for s in data:
                card = ctk.CTkFrame(scroll, height=80, corner_radius=10)
                card.pack(fill="x", pady=5, padx=5)
                ctk.CTkLabel(card, text=f"{s[1]} {s[2]}", font=("Segoe UI", 14, "bold"), width=150).pack(side="left", padx=20)
                ctk.CTkLabel(card, text=f"Role: {s[3]}", text_color="#1f6aa5", width=100).pack(side="left", padx=20)
                ctk.CTkLabel(card, text=f"📞 {s[4]}", width=150).pack(side="left", padx=20)

    def show_equipment(self):
        for w in self.content.winfo_children(): w.destroy()
        header = ctk.CTkFrame(self.content, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=20)
        ctk.CTkLabel(header, text="Equipment Inventory", font=("Segoe UI", 28, "bold")).pack(side="left")
        
        # Use Scrollable Frame to handle many items
        scroll = ctk.CTkScrollableFrame(self.content, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=30, pady=10)
        
        data = DBManager.execute_query("SELECT * FROM EQUIPMENT ORDER BY STATUS")
        if data:
            # We will use a grid layout inside the scroll frame for a cleaner look
            for i, e in enumerate(data):
                color = "#2ecc71" if e[2] == "Working" else "#e74c3c"
                card = ctk.CTkFrame(scroll, width=220, height=180, corner_radius=15, border_width=1, border_color=color)
                # Auto-wrap: 4 cards per row
                card.grid(row=i//4, column=i%4, padx=15, pady=15)
                card.grid_propagate(False)
                
                ctk.CTkLabel(card, text=e[1], font=("Segoe UI", 16, "bold")).pack(pady=(30, 10))
                ctk.CTkLabel(card, text=e[2], text_color=color, font=("Segoe UI", 14, "bold")).pack()
                ctk.CTkLabel(card, text=f"ID: {e[0]}", text_color="gray", font=("Segoe UI", 10)).pack(side="bottom", pady=10)

    def show_audit_logs(self):
        for w in self.content.winfo_children(): w.destroy()
        ctk.CTkLabel(self.content, text="System Audit History", font=("Segoe UI", 28, "bold")).pack(pady=20, padx=30, anchor="w")
        
        scroll = ctk.CTkScrollableFrame(self.content, fg_color="#1a1a1a")
        scroll.pack(fill="both", expand=True, padx=30, pady=10)
        
        data = DBManager.execute_query("SELECT * FROM AUDIT_LOG ORDER BY ACTION_DATE DESC")
        if data:
            for row in data:
                row_f = ctk.CTkFrame(scroll, fg_color="transparent")
                row_f.pack(fill="x", pady=2)
                ctk.CTkLabel(row_f, text=f"[{row[2]}]", text_color="#1f6aa5", width=150).pack(side="left")
                ctk.CTkLabel(row_f, text=row[1], anchor="w").pack(side="left", padx=10)
                ctk.CTkLabel(row_f, text=f"by {row[3]}", text_color="gray").pack(side="right")

    # ==========================================
    # CUSTOMER PORTAL (High-End View)
    # ==========================================
    def show_member_portal(self):
        for w in self.content.winfo_children(): w.destroy()
        
        header = ctk.CTkFrame(self.content, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(40, 20))
        ctk.CTkLabel(header, text=f"Welcome Back, {self.username}", font=("Segoe UI", 36, "bold")).pack(side="left")
        
        main_f = ctk.CTkFrame(self.content, fg_color="transparent")
        main_f.pack(fill="both", expand=True, padx=40)
        
        # Left: Profile Card
        prof_c = ctk.CTkFrame(main_f, width=400, corner_radius=20, fg_color="#1a1a1a")
        prof_c.pack(side="left", fill="y", padx=(0, 20))
        
        res = DBManager.execute_query("""
            SELECT M.*, P.PLAN_NAME, P.DURATION_DAYS, (M.REGISTRATIONDATE + P.DURATION_DAYS) as EXPIRE_DATE
            FROM MEMBER M 
            JOIN MEMBERSHIP_PLAN P ON M.PLAN_ID = P.PLAN_ID
            WHERE M.MEMBERID = :1
        """, (self.current_member_id,))
        
        if res:
            m = res[0]
            expire_date = m[-1] # This is the calculated expiration date from SQL
            days_left = (expire_date - datetime.now()).days if isinstance(expire_date, datetime) else 0
            
            status = "ACTIVE ✅"
            status_color = "#2ecc71"
            if days_left < 0:
                status = "EXPIRED! ⚠️ PLEASE PAY FEE"
                status_color = "#e74c3c"
            
            ctk.CTkLabel(prof_c, text="My Membership Profile", font=("Segoe UI", 18, "bold"), text_color="#1f6aa5").pack(pady=30)
            items = [
                ("Member ID", m[0]), 
                ("Full Name", f"{m[1]} {m[2]}"), 
                ("Current Plan", m[-3]), 
                ("Expires On", expire_date.strftime("%d-%b-%Y") if expire_date else "N/A"),
                ("Account Status", status)
            ]
            for t, v in items:
                f = ctk.CTkFrame(prof_c, fg_color="transparent")
                f.pack(fill="x", padx=30, pady=5)
                ctk.CTkLabel(f, text=t, font=("Segoe UI", 12), text_color="gray").pack(side="left")
                val_color = "white" if t != "Account Status" else status_color
                ctk.CTkLabel(f, text=str(v), font=("Segoe UI", 14, "bold"), text_color=val_color).pack(side="right")

        # Right: Attendance
        att_c = ctk.CTkFrame(main_f, corner_radius=20, fg_color="#1a1a1a")
        att_c.pack(side="left", fill="both", expand=True)
        ctk.CTkLabel(att_c, text="My Attendance History", font=("Segoe UI", 18, "bold")).pack(pady=20)
        
        scroll = ctk.CTkScrollableFrame(att_c, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=10)
        
        try:
            data = DBManager.execute_query("SELECT ATTENDANCE_DATE, STATUS FROM ATTENDANCE WHERE MEMBERID = :1 ORDER BY ATTENDANCE_DATE DESC", (self.current_member_id,))
            if data:
                for a in data:
                    row = ctk.CTkFrame(scroll, fg_color="#252525", height=40)
                    row.pack(fill="x", pady=2)
                    ctk.CTkLabel(row, text=str(a[0]), width=150).pack(side="left", padx=10)
                    ctk.CTkLabel(row, text=str(a[1]), text_color="#2ecc71" if a[1]=="Present" else "#e74c3c").pack(side="left", padx=20)
        except: pass

    # ==========================================
    # HELPERS
    # ==========================================
    def parse_date(self, date_str):
        if not date_str or len(date_str) < 5: return None
        from datetime import datetime
        for fmt in ["%d-%m-%Y", "%d-%b-%Y", "%Y-%m-%d", "%d/%m/%Y"]:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime("%Y-%m-%d")
            except: continue
        return date_str

    def delete_rec(self, rid, table, refresh_cmd):
        if messagebox.askyesno("Security", f"Confirm permanent removal of record #{rid}?"):
            try:
                DBManager.execute_query(f"DELETE FROM {table} WHERE {table}ID = {rid}", commit=True)
                refresh_cmd()
            except Exception as e: messagebox.showerror("Error", str(e))





if __name__ == "__main__":
    app = GymApp()
    app.mainloop()