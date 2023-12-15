from dash import Dash, html, dash_table, callback, Input, Output, dcc
import dash_bootstrap_components as dbc
import pandas as pd
from . import data
import plotly.express as px

dash4 = Dash(
    requests_pathname_prefix="/dash/app4/", external_stylesheets=[dbc.themes.BOOTSTRAP]
)
dash4.title = "信用卡消費樣態"
lastest_data = data.incom_data()


lastest_df = pd.DataFrame(
    lastest_data, columns=["年", "月", "地區", "產業別", "年收入", "信用卡交易筆數", "信用卡交易金額"]
)


dash4.layout = html.Div(
    [
        dbc.Container(
            [
                html.Div(
                    [html.Div([html.H1("各年收入信用卡消費樣態")], className="col text-center")],
                    className="row",
                    style={"paddingTop": "2rem"},
                ),
                html.Div(
                    [
                        dbc.DropdownMenu(
                            label="資料類別",
                            children=[
                                dbc.DropdownMenuItem(
                                    "首頁", href="/dash/index/",external_link=True
                                ),
                                dbc.DropdownMenuItem(
                                    "教育程度", href="/dash/app/", external_link=True
                                ),
                                dbc.DropdownMenuItem(
                                    "年齡層", href="/dash/app1/", external_link=True
                                ),
                                dbc.DropdownMenuItem(
                                    "職業類別", href="/dash/app2/", external_link=True
                                ),
                                dbc.DropdownMenuItem(
                                    "性別", href="/dash/app3/", external_link=True
                                ),
                            ],
                            color="danger",
                            style={"marginRight": "1rem"},
                        ),
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("地區"),
                                dbc.Select(
                                    id="area",
                                    value="ALL",
                                    options=[
                                        {"label": "臺北市", "value": "臺北市"},
                                        {"label": "新北市", "value": "新北市"},
                                        {"label": "桃園市", "value": "桃園市"},
                                        {"label": "臺中市", "value": "臺中市"},
                                        {"label": "臺南市", "value": "臺南市"},
                                        {"label": "高雄市", "value": "高雄市"},
                                        {"label": "ALL", "value": "ALL"},
                                    ],
                                    style={"marginRight": "1rem"},
                                ),
                            ],
                     
                        ),
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("月份"),
                                dbc.Select(
                                    id="month",
                                    value="ALL",
                                    options=[
                                        {"label": "1月", "value": "1"},
                                        {"label": "2月", "value": "2"},
                                        {"label": "3月", "value": "3"},
                                        {"label": "4月", "value": "4"},
                                        {"label": "5月", "value": "5"},
                                        {"label": "6月", "value": "6"},
                                        {"label": "7月", "value": "7"},
                                        {"label": "8月", "value": "8"},
                                        {"label": "9月", "value": "9"},
                                        {"label": "ALL", "value": "ALL"},
                                    ],
                                    style={"marginRight": "1rem"},
                                ),
                            ],
                        
                        ),
                         dbc.InputGroup(
                            [
                                dbc.InputGroupText("產業別"),
                                dbc.Select(
                                    id="industry",
                                    value="ALL",
                                    options=[
                                        {"label": "食", "value": "食"},
                                        {"label": "衣", "value": "衣"},
                                        {"label": "住", "value": "住"},
                                        {"label": "行", "value": "行"},
                                        {"label": "文教康樂", "value": "文教康樂"},
                                        {"label": "百貨", "value": "百貨"},
                                        {"label": "ALL", "value": "ALL"},
                                    ],
                                    style={"marginRight": "1rem"},
                                ),
                            ],
       
                        ),
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("年收入"),
                                dbc.Select(
                                    id="incom",
                                    value="ALL",
                                    options=[
                                        {"label": "未達50萬", "value": "未達50萬"},
                                        {"label": "50(含)-75萬", "value": "50(含)-75萬"},
                                        {"label": "75(含)-100萬", "value": "75(含)-100萬"},
                                        {"label": "100(含)-125萬", "value": "100(含)-125萬"},
                                        {"label": "125(含)-150萬", "value": "125(含)-150萬"},
                                        {"label": "150(含)-175萬", "value": "150(含)-175萬"},
                                        {"label": "175(含)-200萬", "value": "175(含)-200萬"},
                                        {"label": "200(含)萬以上", "value": "200(含)萬以上"},
                                        {"label": "ALL", "value": "ALL"},
                                    ],
                                ),
                            ],
                        )
                    ],
                    className="d-flex justify-content-center",
                    style={"paddingTop": "2rem"},
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                dash_table.DataTable(
                                    id="data",
                                    data=lastest_df.to_dict("records"),
                                    columns=[
                                        {"id": column, "name": column}
                                        for column in lastest_df.columns
                                    ],
                                    page_size=20,
                                    fixed_rows={"headers": True},
                                    style_table={
                                        "height": "300px",
                                        "overflowY": "auto",
                                    },
                                    style_cell={
                                        "text_align": "center",
                                    },
                                ),
                            ],
                            className="col text-center",
                        )
                    ],
                    className="row",
                    style={"paddingTop": "2rem"},
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.P("來源："),
                                html.P("Data： 聯合信用卡處理中心Open API"),
                                html.P("Icon： Image by toffeomurice from Pixabay"),
                            ],
                            className="col",
                        )
                    ],
                    className="row",
                    style={
                        "paddingTop": "2rem",
                        "fontSize": "0.8rem",
                        "lineHeight": "0.3rem",
                    },
                ),
                html.Div([
                    dcc.Graph(id="graph"),
                    dcc.Graph(id="graph_line"),
                    dcc.Graph(id="graph_bar"),
                ])        
            ]
        )
    ],
    className="container-lg",
)


@dash4.callback(
    Output("data", "data"),
    [Input("area", "value"), Input("month", "value"), Input("industry", "value"), Input("incom", "value")],
)
def update_table(selected_area, selected_month, selected_industry, selected_incom):
    print(selected_area, selected_industry, selected_month, selected_incom)
    filtered_data = [
        row
        for row in lastest_data
        if (selected_area is None or selected_area == "ALL" or row[2] == selected_area)
        and (selected_month is None or selected_month == "ALL" or str(row[1]) == selected_month)
        and (selected_industry is None or selected_industry == "ALL" or row[3] == selected_industry)
        and (selected_incom is None or selected_incom == "ALL" or str(row[4]) == selected_incom)
    ]

    update_df = pd.DataFrame(
        filtered_data, columns=["年", "月", "地區", "產業別", "年收入", "信用卡交易筆數", "信用卡交易金額"]
    )

    print(update_df)
    return update_df.to_dict("records")

@dash4.callback(
    Output("graph", "figure"),
    Input("industry","value")
)
def update_pie_chart(selected_value):
    global lastest_df
    if selected_value is None or selected_value == "ALL":
        # Group by industry and sum the transaction amounts
        industry_sum = lastest_df.groupby('產業別')['信用卡交易金額'].sum().reset_index()

        # Create a pie chart
        fig = px.pie(industry_sum, values='信用卡交易金額', names='產業別', title='各產業別信用卡交易金額總和')
        return fig
    else:
        filtered_df = lastest_df[lastest_df['產業別'] == f'{selected_value}']
        fig = px.pie(filtered_df, values='信用卡交易金額', names='年收入')
        return fig
    
@dash4.callback(
    Output("graph_line", "figure"),
    Input("incom","value")
)
def update_line_chart(selected_income):
    global lastest_df
    if selected_income is None or selected_income == "ALL":
        # 將資料按照年和月進行分組，計算每個月的信用卡消費金額總和
        monthly_total = lastest_df.groupby(['年', '月', '年收入'])['信用卡交易金額'].sum().reset_index()

        # 繪製折線圖
        fig = px.line(monthly_total, x="月", y="信用卡交易金額", color="年收入", title='每月信用卡消費金額變化', markers=True)

        return fig
    else:
        monthly_total = lastest_df.groupby(['年', '月', '年收入'])['信用卡交易金額'].sum().reset_index()
        filtered_df = monthly_total[monthly_total['年收入'] == f'{selected_income}']
        print(filtered_df)
        fig = px.line(filtered_df, x="月", y="信用卡交易金額", color="年收入", title='每月信用卡消費金額變化', markers=True)
        return fig

@dash4.callback(
    Output("graph_bar", "figure"),
    Input("area","value")
)
def update_line_chart(selected_area):
    global lastest_df
    if selected_area is None or selected_area == "ALL":
        region_sum = lastest_df.groupby('地區')['信用卡交易金額'].sum().reset_index()

        fig = px.bar(region_sum, x='地區', y='信用卡交易金額', title='Total Credit Card Transaction Amount by Region')

        return fig
    else:
        region_sum = lastest_df.groupby('地區')['信用卡交易金額'].sum().reset_index()

        fig = px.bar(region_sum, x='地區', y='信用卡交易金額', title='Total Credit Card Transaction Amount by Region')
        highlighted_region = selected_area
        fig.update_traces(marker_color=['blue' if region == highlighted_region else 'gray' for region in region_sum['地區']])
        return fig