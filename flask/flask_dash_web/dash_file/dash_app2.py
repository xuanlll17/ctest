from dash import Dash, html, dash_table, callback, Input, Output, dcc, State     #只有import後面的能用
import dash_bootstrap_components as dbc
import pandas as pd
from . import datasource  #在.py一定要用from . 根目錄 import


dash2 = Dash(requests_pathname_prefix="/dash/app2/", external_stylesheets=[dbc.themes.BOOTSTRAP])  #建立時一定要加路徑
dash2.title = "臺北市youbike及時資料"
current_data = datasource.lastest_datetime_data()
current_df = pd.DataFrame(current_data, columns=['站點名稱','更新時間','行政區','地址','總數','可借', '可還'])
current_df = current_df.reset_index()
current_df['站點名稱'] = current_df['站點名稱'].map(lambda name:name[11:])

#property layout
dash2.layout = html.Div(
    #要放多個,所以用list代替  #一定要把layout内容對齊
    [
        #html.A("Icon by doraclub", href="https://www.freepik.com/icon/bicycle_3918391#fromView=search&term=Favicon++bike&page=1&position=8&track=ais&uuid=4cefbc82-a159-4736-a7d2-705faa293b14", target='_blank')
        
        dbc.Container([
            #row
            html.Div([
                html.Div([
                    html.H1("台北市youbike及時資料")
                ],className="col text-center")
            ],
            className="row",
            style={"paddingTop":'2rem'}),
            html.Div([
                html.Div([
                    html.Div([
                        dbc.Label("站點名稱"),
                        dbc.Input(id='input_value',
                                  placeholder="請輸入站點名稱",
                                  type="text"),
                        ])
                ],className="col"),
                html.Div([
                    html.Button('確定', id='submit-val', className="btn btn-primary", n_clicks=None)
                    ],className="col"),
            ],
            className="row row-cols-auto align-items-end",
            style={"paddingTop":'2rem'}),
            html.Div([
                html.Div([
                    dash_table.DataTable(
                        #引數名稱,引數值
                        id='main_table',
                        #先轉list dict 才能輸出
                        page_size=20,
                        fixed_rows={'headers': True},
                        style_table={'height': '300px', 'overflowY': 'auto'},
                        style_cell_conditional=[
                            {   'if': {'column_id': 'index'},
                            'width':'6%'
                            },
                            {   'if': {'column_id': '站點名稱'},
                            'width': '25%'
                            },
                            {   'if': {'column_id': '總數'},
                            'width': '5%'
                            },
                            {   'if': {'column_id': '可借'},
                            'width': '5%'
                            },
                            {   'if': {'column_id': '可還'},
                            'width': '5%'
                            },
                        ],
                    row_selectable="single",
                    selected_rows=[],  #一開始選取的位置, [] -> index(0,1,2,....)
                ),  
                ],className="col text-center")
            ],
            className="row",
            style={"paddingTop":'0.5rem'}),
            html.Div([
                html.Div(children="",className="col",id='showMessage')
            ],
            className="row",
            style={"paddingTop":'2rem'}),
        ])
    ],
    className="container-lg",
    #style={'backgroundColor':'#666'}   #使用駝峰式命名法
    )

@callback(
        [Output('main_table', 'data'),Output('main_table', 'columns'),Output('main_table', 'selected_rows')],
        [Input('submit-val', 'n_clicks')],
        [State('input_value', 'value')]
)
def clickBtn(n_clicks:None | int, inputValue:str):
    global current_df  #使用外部的current_df(全域變數)  #須建立, global current_df
    if n_clicks is not None:  #檢查如果不是None
        #一定要先檢查有沒有按button
        searchData:list[tuple] = datasource.search_sitename(inputValue)
        current_df = pd.DataFrame(searchData, columns=['站點名稱','更新時間','行政區','地址','總數','可借', '可還'])
        current_df = current_df.reset_index()
        current_df['站點名稱'] = current_df['站點名稱'].map(lambda name:name[11:])
        #print("按確定")
        return current_df.to_dict('records'),[{"id": column, "name": column} for column in current_df.columns],[]

    #n_clicks is None
    #代表第一次啟動
    #print("第一次啟動")
    current_data = datasource.lastest_datetime_data()
    current_df = pd.DataFrame(current_data, columns=['站點名稱','更新時間','行政區','地址','總數','可借', '可還'])
    current_df = current_df.reset_index()
    current_df['站點名稱'] = current_df['站點名稱'].map(lambda name:name[11:])
    return current_df.to_dict('records'),[{"id": column, "name": column} for column in current_df.columns],[]


@callback(
        Output('showMessage', 'children'),  #output children(data) to id "showMessage"
        Input('main_table', 'selected_rows')  #id名稱,對應property
)
def selectedRow(selected_rows:list[int]):  #傳參數, selected_rows -> list
    #要有output和input才可以輸出
    #取得一個站點,series
    if len(selected_rows) != 0:  #不等於0,才執行, 一開始沒選擇時會是空的,所以設定if len !=0
        oneSite:pd.DataFrame = current_df.iloc[selected_rows]  #oneSite裡面儲存的是pd.Series(typeHint)  #僅取得非建立,不用global current_df
        oneTable:dash_table.DataTable = dash_table.DataTable(oneSite.to_dict('records'), [{"name": i, "id": i} for i in oneSite.columns])
        return [oneTable]
    
    return None
