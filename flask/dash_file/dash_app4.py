from dash import Dash, html, dash_table, callback, Input, Output, dcc
import dash_bootstrap_components as dbc
import pandas as pd
from . import data

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
                                    "教育程度", href="/dash/app/", external_link=True
                                ),
                                dbc.DropdownMenuItem(
                                    "年齡層", href="/dash/app1/", external_link=True
                                ),
                                dbc.DropdownMenuItem(
                                    "職業類別", href="/dash/app2/", external_link=True
                                ),
                                dbc.DropdownMenuItem(
                                    "兩性", href="/dash/app3/", external_link=True
                                ),
                            ],
                        ),
                        dcc.Dropdown(
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
                            style={"width": "29%"},
                        ),
                        dcc.Dropdown(
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
                            style={"width": "29%"},
                        ),
                        dcc.Dropdown(
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
                            style={"width": "29%"},
                        ),
                        
                    ],
                    className="row row-cols-auto align-items-end",
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
            ]
        )
    ],
    className="container-lg",
)


@dash4.callback(
    Output("data", "data"),
    [Input("area", "value"), Input("month", "value"), Input("industry", "value")],
)
def update_table(selected_area, selected_month, selected_industry):
    #print(selected_area, selected_industry, selected_month)
    filtered_data = [
        row
        for row in lastest_data
        if (selected_area is None or selected_area == "ALL" or row[2] == selected_area)
        and (selected_month is None or selected_month == "ALL" or str(row[1]) == selected_month)
        and (selected_industry is None or selected_industry == "ALL" or row[3] == selected_industry)
    ]

    update_df = pd.DataFrame(
        filtered_data, columns=["年", "月", "地區", "產業別", "年收入", "信用卡交易筆數", "信用卡交易金額"]
    )

    print(update_df)
    return update_df.to_dict("records")

