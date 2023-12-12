import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb
from ttkbootstrap import Style
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import data
import os
import seaborn as sns


class Window(tk.Tk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title("信用卡消費樣態")
        self.conn = sqlite3.connect("creditcard.db")
        plt.rcParams["font.family"] = "Microsoft JhengHei"
        style = Style("lumen")

        # ------------介面-----------#
        mainFrame = tk.Frame(self, relief=tk.GROOVE, borderwidth=1)
        tk.Label(mainFrame, text="信用卡消費樣態", font=("arial", 20), fg="#333333").pack(
            padx=10, pady=10
        )
        mainFrame.pack(padx=5, pady=10, fill="both")

        # ------------搜尋------------#
        topFrame = ttk.Labelframe(self, text="搜尋")
        # ------Label------#
        # self.dataLabel = ttk.Label(topFrame, text="資料類別:").grid(
        # row=0, column=0, padx=(1, 0), pady=(20, 10), sticky="w"
        # )

        self.areaLabel = ttk.Label(topFrame, text="地區:").grid(
            row=0, column=1, padx=(450, 10), pady=10, sticky="w"
        )
        self.industryLabel = ttk.Label(topFrame, text="產業別:").grid(
            row=0, column=3, padx=(50, 10), pady=10, sticky="w"
        )
        self.ageLabel = ttk.Label(topFrame, text="年齡層:").grid(
            row=0, column=5, padx=(50, 10), pady=10, sticky="w"
        )
        # ------StringVar------#
        # self.data = ttk.Label(
        # topFrame,
        # text="年齡層",
        # ).grid(row=0, column=1, padx=10, pady=(20, 10))

        self.area_var = tk.StringVar()
        self.area_var.set("請選擇地區")
        self.area = ttk.Combobox(
            topFrame,
            textvariable=self.area_var,
            values=[
                "臺北市",
                "高雄市",
                "新北市",
                "臺中市",
                "臺南市",
                "桃園市",
                "ALL",
            ],
        )
        self.area.grid(row=0, column=2, padx=1, pady=10)
        self.area.bind("<<ComboboxSelected>>", self.load_data)

        self.industry_var = tk.StringVar()
        self.industry_var.set("請選擇產業別")
        self.industry = ttk.Combobox(
            topFrame,
            textvariable=self.industry_var,
            values=["食", "衣", "住", "行", "文教康樂", "百貨", "ALL"],
        )
        self.industry.grid(row=0, column=4, padx=1, pady=10)
        self.industry.bind("<<ComboboxSelected>>", self.load_data)

        self.age_var = tk.StringVar()
        self.age_var.set("請選擇年齡層")
        self.age = ttk.Combobox(
            topFrame,
            textvariable=self.age_var,
            values=[
                "未滿20歲",
                "20(含)-25歲",
                "25(含)-30歲",
                "30(含)-35歲",
                "35(含)-40歲",
                "40(含)-45歲",
                "45(含)-50歲",
                "50(含)-55歲",
                "55(含)-60歲",
                "60(含)-65歲",
                "65(含)-70歲",
                "70(含)-75歲",
                "75(含)-80歲",
                "80(含)歲以上",
                "ALL",
            ],
        )
        self.age.grid(row=0, column=6, padx=(0, 50), pady=10)
        self.age.bind("<<ComboboxSelected>>", self.load_data)

        # state="active"->按鈕可以點擊,command按鈕被點擊時執行self.load_data
        # self.botton = tk.Button(
        # topFrame, text="搜尋", state="active", command=self.load_data, width=30
        # ).grid(row=5, column=0, padx=10, pady=20, columnspan=2)
        topFrame.pack(padx=(5, 5), fill="x")

        # ------------圖表-------------#
        self.charFrame = ttk.LabelFrame(self)
        self.charFrame.pack(side=tk.LEFT, padx=5, pady=(0, 5), expand=True, fill="both")
        self.bottomFrame1 = ttk.Labelframe(self.charFrame, text="圓餅圖")
        self.bottomFrame1.grid(row=1, column=1, padx=(3, 3), pady=(0, 5), sticky="nsew")

        self.bottomFrame2 = ttk.Labelframe(self.charFrame, text="地區")
        self.bottomFrame2.grid(row=1, column=2, padx=(0, 3), pady=(0, 5), sticky="nsew")

        self.bottomFrame3 = ttk.Labelframe(self.charFrame, text="折線圖")
        self.bottomFrame3.grid(row=1, column=3, padx=(0, 3), pady=(0, 5), sticky="nsew")

        self.bottomFrame4 = ttk.Labelframe(self.charFrame, text="熱力圖")
        self.bottomFrame4.grid(row=2, column=1, padx=(3, 3), pady=(0, 5), sticky="nsew")

        self.bottomFrame5 = ttk.Labelframe(self.charFrame, text="產業別")
        self.bottomFrame5.grid(row=2, column=2, padx=(0, 3), pady=(0, 5), sticky="nsew")

        self.bottomFrame6 = ttk.Labelframe(self.charFrame, text="年齡層")
        self.bottomFrame6.grid(row=2, column=3, padx=(0, 3), pady=(0, 5), sticky="nsew")

        self.show_line_charts()
        self.show_pie_charts()
        # self.show_heatmap_charts()
        self.show_area_charts()
        self.show_industry_charts()
        self.show_age_charts()

    def load_data(self, event):
        selected_area = self.area_var.get()
        selected_age = self.age_var.get()
        selected_industry = self.industry_var.get()
        if selected_area != "請選擇地區":
            self.show_area_charts()

        if selected_age != "請選擇年齡層":
            self.show_age_charts()
            self.show_line_charts()

        if selected_industry != "請選擇產業別":
            self.show_industry_charts()

    # ------------折線圖------------#
    def show_line_charts(self):
        conn = sqlite3.connect("creditcard.db")
        selected_age = self.age_var.get()
        fig, ax = plt.subplots(figsize=(6.5, 3))
        fig.subplots_adjust(bottom=0.1, top=0.9)

        if selected_age != "請選擇年齡層" and selected_age != "ALL":
            sql = f"SELECT 年, 年齡層, SUM(信用卡金額) AS 信用卡交易總金額 FROM age WHERE 年齡層 = '{selected_age}' GROUP BY 年, 年齡層"

        else:
            sql = """
                    SELECT
                        年,
                        年齡層,
                        SUM(信用卡金額) AS 信用卡交易總金額
                    FROM
                        age
                    GROUP BY
                        年,
                        年齡層
            """
        df = pd.read_sql_query(sql, conn)
        pivot_df = df.pivot(index="年", columns=f"年齡層", values="信用卡交易總金額")
        pivot_df.plot(kind="line", marker="o", linestyle="-", ax=ax)
        ax.set_title(f"各年齡層信用卡交易金額趨勢")
        ax.set_ylabel("信用卡交易總金額")
        ax.set_xticks(df["年"])
        ax.legend().set_visible(False)

        # ------create canvas------#
        if not hasattr(self, "canvas_line_chart"):
            self.canvas_line_chart = FigureCanvasTkAgg(fig, master=self.bottomFrame3)
            canvas_widget = self.canvas_line_chart.get_tk_widget()
            canvas_widget.grid(row=1, column=3, padx=(0, 3), pady=(0, 5), sticky="nsew")
        else:
            # ------update canvas content------#
            self.canvas_line_chart.get_tk_widget().destroy()
            self.canvas_line_chart = FigureCanvasTkAgg(fig, master=self.bottomFrame3)
            canvas_widget = self.canvas_line_chart.get_tk_widget()
            canvas_widget.grid(row=1, column=3, padx=(0, 3), pady=(0, 5), sticky="nsew")

        self.canvas_line_chart.draw()

    # ------------圓餅圖------------#
    def show_pie_charts(self):
        conn = sqlite3.connect("creditcard.db")

        fig, ax = plt.subplots(figsize=(3.85, 3))
        fig.subplots_adjust(bottom=0.1, top=0.9)

        sql = """
            SELECT 
                性別, SUM(信用卡金額) AS 信用卡交易金額
            FROM 
                age
            GROUP BY 
                性別
        """
        df = pd.read_sql_query(sql, conn)
        ax.pie(
            df["信用卡交易金額"],
            labels=df["性別"],
            textprops={"fontsize": 10},
            autopct="%1.1f%%",
        )
        ax.set_title(f"不同性別的信用卡交易金額分布")

        # ------create canvas------#
        if not hasattr(self, "canvas_pie_chart"):
            self.canvas_pie_chart = FigureCanvasTkAgg(fig, master=self.bottomFrame1)
            canvas_widget = self.canvas_pie_chart.get_tk_widget()
            canvas_widget.grid(row=1, column=1, padx=(3, 5), pady=(0, 5), sticky="nsew")
        # ------update canvas content------#
        else:
            self.canvas_pie_chart.get_tk_widget().destroy()
            self.canvas_pie_chart = FigureCanvasTkAgg(fig, master=self.bottomFrame1)
            canvas_widget = self.canvas_pie_chart.get_tk_widget()
            canvas_widget.grid(row=1, column=1, padx=(3, 5), pady=(0, 5), sticky="nsew")

        self.canvas_pie_chart.draw()

    # ------------熱力圖------------#
    def show_heatmap_charts(self):
        # ------create canvas------#
        if not hasattr(self, "canvas_heatmap_chart"):
            self.canvas_heatmap_chart = FigureCanvasTkAgg(fig, master=self.bottomFrame4)
            canvas_widget = self.canvas_heatmap_chart.get_tk_widget()
            canvas_widget.grid(row=1, column=2, padx=(0, 5), pady=(0, 5), sticky="nsew")
        # ------update canvas content------#
        else:
            self.canvas_heatmap_chart.get_tk_widget().destroy()
            self.canvas_heatmap_chart = FigureCanvasTkAgg(fig, master=self.bottomFrame4)
            canvas_widget = self.canvas_heatmap_chart.get_tk_widget()
            canvas_widget.grid(row=1, column=2, padx=(0, 5), pady=(0, 5), sticky="nsew")

        self.canvas_heatmap_chart.draw()

    def show_area_charts(self):
        selected_area = self.area_var.get()
        conn = sqlite3.connect("creditcard.db")

        if (
            selected_area != "請選擇地區"
            and selected_area != "ALL"
        ):
            sql = f"SELECT 地區, 信用卡金額 AS 信用卡交易金額, SUM(信用卡金額) / SUM(信用卡交易筆數) AS 平均交易金額 FROM age WHERE 地區 = '{selected_area}' AND 產業別 != '其他' GROUP BY 地區"

        else:
            sql = """
                SELECT
                    地區,
                    SUM(信用卡金額) AS 信用卡交易金額,
                    SUM(信用卡金額) / SUM(信用卡交易筆數) AS 平均交易金額
                FROM
                    age
                WHERE 
                    地區 in ('臺北市', '新北市', '桃園市', '臺中市', '臺南市', '高雄市') AND 產業別 != '其他'                    
                GROUP BY
                    地區
            """

        df = pd.read_sql_query(sql, conn)
        fig, ax = plt.subplots(figsize=(6, 3))

        sns.barplot(x="地區", y="信用卡交易金額", data=df, ax=ax)
        ax.set_title("不同地區的信用卡交易金額")
        ax.set_ylabel("信用卡交易金額")

        ax2 = ax.twinx()
        sns.lineplot(x="地區", y="平均交易金額", data=df, color="red", marker="o", ax=ax2)
        ax2.set_ylabel("平均交易金額")

        ax.tick_params(axis="y", labelsize=10)
        ax2.tick_params(axis="y", labelsize=10)

        # Set an empty string as xlabel
        ax.set_xlabel("")
        ax2.set_xlabel("")

        # ------create canvas------#
        if not hasattr(self, "canvas_area_chart"):
            self.canvas_area_chart = FigureCanvasTkAgg(fig, master=self.bottomFrame2)
            canvas_widget = self.canvas_area_chart.get_tk_widget()
            canvas_widget.grid(row=2, column=1, padx=(0, 3), pady=(0, 5), sticky="nsew")
        # ------update canvas content------#
        else:
            self.canvas_area_chart.get_tk_widget().destroy()
            self.canvas_area_chart = FigureCanvasTkAgg(fig, master=self.bottomFrame2)
            canvas_widget = self.canvas_area_chart.get_tk_widget()
            canvas_widget.grid(row=2, column=1, padx=(0, 3), pady=(0, 5), sticky="nsew")

        self.canvas_area_chart.draw()

    def show_industry_charts(self):
        selected_industry = self.industry_var.get()
        conn = sqlite3.connect("creditcard.db")
        if selected_industry != "請選擇產業別" and selected_industry != "ALL":
            sql = f"SELECT 產業別, SUM(信用卡金額) AS 信用卡交易金額, SUM(信用卡金額) / SUM(信用卡交易筆數) AS 平均交易金額 FROM age WHERE 產業別 = '{selected_industry}' GROUP BY 產業別"
        else:
            sql = """
                SELECT
                    產業別,
                    SUM(信用卡金額) AS 信用卡交易金額,
                    SUM(信用卡金額) / SUM(信用卡交易筆數) AS 平均交易金額
                FROM
                    age
                WHERE
                    產業別 != '其他'
                GROUP BY
                    產業別;
            """
        df = pd.read_sql_query(sql, conn)

        fig, ax = plt.subplots(figsize=(6, 3))

        sns.barplot(x="產業別", y="信用卡交易金額", data=df, ax=ax)
        ax.set_title("不同產業別的信用卡交易金額")
        ax.set_xlabel("產業別")
        ax.set_ylabel("信用卡交易金額")

        ax2 = ax.twinx()
        sns.lineplot(x="產業別", y="平均交易金額", data=df, color="red", marker="o", ax=ax2)
        ax2.set_ylabel("平均交易金額")

        ax.tick_params(axis="y", labelsize=10)
        ax2.tick_params(axis="y", labelsize=10)

        # Set an empty string as xlabel
        ax.set_xlabel("")
        ax2.set_xlabel("")

        # ------create canvas------#
        if not hasattr(self, "canvas_industry_chart"):
            self.canvas_industry_chart = FigureCanvasTkAgg(
                fig, master=self.bottomFrame5
            )
            canvas_widget = self.canvas_industry_chart.get_tk_widget()
            canvas_widget.grid(row=2, column=1, padx=(0, 3), pady=(0, 5), sticky="nsew")
        # ------update canvas content------#
        else:
            self.canvas_industry_chart.get_tk_widget().destroy()
            self.canvas_industry_chart = FigureCanvasTkAgg(
                fig, master=self.bottomFrame5
            )
            canvas_widget = self.canvas_industry_chart.get_tk_widget()
            canvas_widget.grid(row=2, column=1, padx=(0, 3), pady=(0, 5), sticky="nsew")

        self.canvas_industry_chart.draw()

    def show_age_charts(self):
        selected_age = self.age_var.get()
        conn = sqlite3.connect("creditcard.db")
        if selected_age != "請選擇年齡層" and selected_age != "ALL":
            sql = f"SELECT 年齡層, SUM(信用卡金額) AS 信用卡交易金額, SUM(信用卡金額) / SUM(信用卡交易筆數) AS 平均交易金額 FROM age WHERE 年齡層 = '{selected_age}' AND 產業別 != '其他'"
        else:
            sql = """
                    SELECT
                        CASE
                            WHEN 年齡層 LIKE '%未滿20%' THEN '-20'
                            WHEN 年齡層 LIKE '%20(含)-25%' THEN '20-25'
                            WHEN 年齡層 LIKE '%25(含)-30%' THEN '25-30'
                            WHEN 年齡層 LIKE '%30(含)-35%' THEN '30-35'
                            WHEN 年齡層 LIKE '%35(含)-40%' THEN '35-40'
                            WHEN 年齡層 LIKE '%40(含)-45%' THEN '40-45'
                            WHEN 年齡層 LIKE '%45(含)-50%' THEN '45-50'
                            WHEN 年齡層 LIKE '%50(含)-55%' THEN '50-55'
                            WHEN 年齡層 LIKE '%55(含)-60%' THEN '55-60'
                            WHEN 年齡層 LIKE '%60(含)-65%' THEN '60-65'
                            WHEN 年齡層 LIKE '%65(含)-70%' THEN '65-70'
                            WHEN 年齡層 LIKE '%70(含)-75%' THEN '70-75'
                            WHEN 年齡層 LIKE '%75(含)-80%' THEN '75-80'
                            WHEN 年齡層 LIKE '%80%' THEN '80+'
                        END 年齡層,
                        SUM(信用卡金額) AS 信用卡交易金額,
                        SUM(信用卡金額) / SUM(信用卡交易筆數) AS 平均交易金額
                    FROM
                        age
                    WHERE
                        產業別 != '其他'
                    GROUP BY
                        年齡層
                    ORDER BY
                        年齡層 ASC
                """
        df = pd.read_sql_query(sql, conn)
        fig, ax = plt.subplots(figsize=(6.5, 3))

        sns.barplot(x="年齡層", y="信用卡交易金額", data=df, ax=ax)
        ax.set_title("不同年齡層的信用卡交易金額")
        ax.set_ylabel("信用卡交易金額")

        ax2 = ax.twinx()
        sns.lineplot(x="年齡層", y="平均交易金額", data=df, color="red", marker="o", ax=ax2)
        ax2.set_ylabel("平均交易金額")

        ax.tick_params(axis="x", labelsize=7.5)
        ax.tick_params(axis="y", labelsize=10)
        ax2.tick_params(axis="y", labelsize=10)

        ax.set_xlabel("")
        ax2.set_xlabel("")

        # ------create canvas------#
        if not hasattr(self, "canvas_age_chart"):
            self.canvas_age_chart = FigureCanvasTkAgg(fig, master=self.bottomFrame6)
            canvas_widget = self.canvas_age_chart.get_tk_widget()
            canvas_widget.grid(row=2, column=1, padx=(0, 3), pady=(0, 5), sticky="nsew")
        # ------update canvas content------#
        else:
            self.canvas_age_chart.get_tk_widget().destroy()
            self.canvas_age_chart = FigureCanvasTkAgg(fig, master=self.bottomFrame6)
            canvas_widget = self.canvas_age_chart.get_tk_widget()
            canvas_widget.grid(row=2, column=1, padx=(0, 3), pady=(0, 5), sticky="nsew")

        self.canvas_age_chart.draw()


def main():
    #data.csv_to_database()

    def on_closing():
        print("window關閉")
        # 將canvas關閉
        if hasattr(window, "canvas_line_chart"):
            window.canvas_line_chart.get_tk_widget().destroy()
        if hasattr(window, "canvas_pie_chart"):
            window.canvas_pie_chart.get_tk_widget().destroy()
        if hasattr(window, "canvas_bar_chart"):
            window.canvas_bar_chart.get_tk_widget().destroy()
        # 將所有matplotlib圖表關閉
        plt.close("all")
        window.destroy()

    window = Window()
    window.protocol("WM_DELETE_WINDOW", on_closing)  # 關閉視窗時會執行on_closing
    window.resizable(width=False, height=False)  # 固定視窗大小,不能更改
    window.mainloop()


if __name__ == "__main__":
    main()
