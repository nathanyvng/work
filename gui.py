import tkinter as tk
from tkinter import ttk, messagebox
import calendar
from datetime import datetime
# from your_data_module import read_excel_to_dict  # or paste function here

EXCEL_PATH = "data.xlsx"

class ReportCalendar(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Daily Report Calendar")
        self.geometry("800x600")

        # self.data = read_excel_to_dict(EXCEL_PATH)
        self.data = {
        datetime(2025, 10, 10, 0, 0).date(): 
            {'status': 'Good', 'description': 'ok, system', 'entries': ['ok', 'system']},
        datetime(2025, 10, 11, 0, 0).date():
            {'status': 'Bad', 'description': 'error, error', 'entries': ['error', 'error']}
        }
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month

        self.header_frame = ttk.Frame(self)
        self.header_frame.pack(pady=10)
        self.calendar_frame = ttk.Frame(self)
        self.calendar_frame.pack(expand=True)

        self.create_header()
        self.show_calendar()

    def create_header(self):
        ttk.Button(self.header_frame, text="◀", command=self.prev_month).grid(row=0, column=0)
        self.month_label = ttk.Label(self.header_frame, text="", font=("Helvetica", 16, "bold"))
        self.month_label.grid(row=0, column=1, padx=20)
        ttk.Button(self.header_frame, text="▶", command=self.next_month).grid(row=0, column=2)

    def show_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        cal = calendar.Calendar()
        month_days = cal.monthdatescalendar(self.current_year, self.current_month)
        self.month_label.config(text=f"{calendar.month_name[self.current_month]} {self.current_year}")

        for r, week in enumerate(month_days):
            for c, day in enumerate(week):
                date_info = self.data.get(day)
                if day.month != self.current_month:
                    bg = "#ddd"
                elif date_info:
                    bg = "green" if date_info["status"].lower() == "good" else "red"
                else:
                    bg = "#f0f0f0"

                label = tk.Label(
                    self.calendar_frame,
                    text=day.day,
                    width=8,
                    height=3,
                    bg=bg,
                    relief="ridge",
                )
                label.bind("<Button-1>", lambda e, d=day: self.show_details(d))
                label.grid(row=r, column=c, padx=2, pady=2)

    def prev_month(self):
        self.current_month -= 1
        if self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1
        self.show_calendar()

    def next_month(self):
        self.current_month += 1
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        self.show_calendar()

    def show_details(self, day):
        info = self.data.get(day)
        if not info:
            messagebox.showinfo("No Data", f"No report for {day.strftime('%Y-%m-%d')}")
            return
        messagebox.showinfo(
            f"Report for {day.strftime('%Y-%m-%d')}",
            f"Status: {info['status']}\n\nDetails:\n{info['description']}"
        )

if __name__ == "__main__":
    app = ReportCalendar()
    app.mainloop()
