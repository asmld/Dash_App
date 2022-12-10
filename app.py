import base64
import io

import dash
from dash import dcc, html, ctx, dash_table
from dash.dependencies import Input, Output, State

import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler


Neighborhood = ['Bloomington Heights', 'Bluestem', 'Briardale', 'Brookside', 'Clear Creek', 'College Creek', 'Crawford',
                'Edwards', 'Gilbert', 'Iowa DOT and Rail Road', 'Meadow Village', 'Mitchell', 'North Ames', 'Northridge',
                'Northpark Villa', 'Northridge Heights', 'Northwest Ames', 'Old Town', 'South & West of Iowa State University',
                'Sawyer', 'Sawyer West', 'Somerset', 'Stone Brook', 'Timberland', 'Veenker']
OverallQual = ['Very Excellent', 'Excellent', 'Very Good', 'Good', 'Above Average', 'Average', 'Below Average',
               'Fair', 'Poor', 'Very Poor']
df = pd.DataFrame()
df_result = pd.DataFrame()

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = '数据科学大作业——房价预测'

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children='🏡', className='header-emoji'),
                html.H1(children='房价预测&房源查询', className='header-title'),
                html.P(children='小组成员：陈培尧 刘广鹤 宋浩天 魏智光', className='header-description')
            ],
            className='header'
        ),
        html.Div(
            children=[
                dcc.Tabs(id='tabs', value='tab-1', children=[
                    dcc.Tab(label='模糊预测', value='tab-1'),
                    dcc.Tab(label='精准预测', value='tab-2'),
                    dcc.Tab(label='房源查询', value='tab-3'),
                    dcc.Tab(label='说明', value='tab-4')
                ],className='tabs-header'),
                html.Div(id='tabs-content')
            ],
            className='tabs'
        )
    ]
)

@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    global df
    if tab == 'tab-1':
        return html.Div([
            html.Div([
                html.Label('街道：', className='option_label'),html.P(),
                dcc.Dropdown(options=Neighborhood, value='Northridge', id='neighbor', clearable=False),
                html.Label('整体质量：', className='option_label'),html.P(),
                dcc.Dropdown(options=OverallQual, value='Good', id='overall', clearable=False),
                html.Label('地面以上房间总数（不包括浴室）：', className='option_label'),html.P(),
                dcc.Slider(min=2, max=14, value=4, step=1, id='TotRsm')
            ],style={'columnCount': 3}),
            html.Div([
                html.P(),html.Label('地面以上总居住面积（平方英尺）：', className='option_label'),html.P(),
                dcc.Slider(min=300, max=8000, value=2000, step=1, marks=None, id='GrLiv', tooltip={"placement": "bottom", "always_visible": True}, disabled=True),
                html.P(),html.Label('一层总居住面积（平方英尺）：', className='option_label'),html.P(),
                dcc.Slider(min=300, max=6000, value=2000, step=1, marks=None, id='1stFlr', tooltip={"placement": "bottom", "always_visible": True}),
                html.P(),html.Label('二层总居住面积（平方英尺）：', className='option_label'),html.P(),
                dcc.Slider(min=0, max=2000, value=0, step=1, marks=None, id='2stFlr', tooltip={"placement": "bottom", "always_visible": True}),
                html.P(),html.Label('地下室总面积（平方英尺）：', className='option_label'),html.P(),
                dcc.Slider(min=0, max=6000, value=0, step=1, marks=None, id='TotBsm', tooltip={"placement": "bottom", "always_visible": True})
            ]),
            html.P(),
            html.Div([
                html.Button('开始预测', id='button1',style={'margin-right': '20px'}),
                dcc.Input(placeholder='......', type='text', value='', disabled=True, id='result1',style={'margin-right': '20px'}),
                html.Button('清除结果', id='clear1')
            ],style={'text-align': 'center'})
        ],className='t-content')
    elif tab == 'tab-2':
        print(df)
        return html.Div([
            html.Div([
                html.H1('使用更多参数对房价进行精准预测'),
                html.Button('点击此处下载示例文件', id='download1', style={'margin-right': '20px', 'margin-left': '20px'}),
                html.P('请点击上方按钮下载示例文件，填写完参数后于下方上传，选择算法进行精准预测'),
                dcc.Download(id='download-sample')
            ],style={'text-align': 'center'}),
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    '拖放或',
                    html.A('选择文件', style={'font-weight': 'bold'})
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                multiple=False
            ),
            html.Div(children=dash_table.DataTable(
                df.to_dict('records'),
                [{'name': i, 'id': i} for i in df.columns],
                style_table={'overflowX': 'auto', 'overflowY': 'auto'},
                editable=False,
                style_cell={'textAlign': 'center'}
            ),id='output-data-upload', style={'font-family': 'Lato'}),
            html.Div([
                dcc.RadioItems(['深度神经网络', '随机森林'], '深度神经网络', inline=True, id='algorithm'),
                html.Button('开始预测', id='button2', style={'margin-top': '10px', 'margin-bottom': '10px'}),
                html.Button('下载结果', id='download2', style={'margin-left': '20px'}, disabled=True)
            ], style={'text-align': 'center', 'margin-top': '10px'}),
            html.Div(children=dash_table.DataTable(
                df_result.to_dict('records'),
                [{'name': i, 'id': i} for i in df_result.columns],
                style_table={'overflowX': 'auto', 'overflowY': 'auto'},
                editable=False,
                style_cell={'textAlign': 'center'}
            ),id='output', style={'font-family': 'Lato'}),
            dcc.Download(id='download-result')
        ],className='t-content')
    elif tab == 'tab-3':
        return html.Div([
            html.Div([
                html.Label('街道：', className='option_label'),html.P(),
                dcc.Dropdown(options=Neighborhood, value='Northridge', id='neighbor_query', clearable=False),
                html.Label('整体质量：', className='option_label'),html.P(),
                dcc.Dropdown(options=OverallQual, value='Good', id='overall_query', clearable=False),
                html.Label('地面以上房间总数（不包括浴室）：', className='option_label'),html.P(),
                dcc.RangeSlider(min=2, max=14, value=[4, 6], step=1, id='TotRsm_query')
            ],style={'columnCount': 3}),
            html.Div([
                html.P(),html.Label('地面以上总居住面积（平方英尺）：', className='option_label'),html.P(),
                dcc.RangeSlider(min=300, max=8000, value=[2000, 4000], step=1, marks=None, id='GrLiv_query', tooltip={"placement": "bottom", "always_visible": True}, disabled=True),
                html.P(),html.Label('一层总居住面积（平方英尺）：', className='option_label'),html.P(),
                dcc.RangeSlider(min=300, max=6000, value=[2000, 4000], step=1, marks=None, id='1stFlr_query', tooltip={"placement": "bottom", "always_visible": True}),
                html.P(),html.Label('二层总居住面积（平方英尺）：', className='option_label'),html.P(),
                dcc.RangeSlider(min=0, max=2000, value=[0, 0], step=1, marks=None, id='2stFlr_query', tooltip={"placement": "bottom", "always_visible": True}),
                html.P(),html.Label('地下室总面积（平方英尺）：', className='option_label'),html.P(),
                dcc.RangeSlider(min=0, max=6000, value=[0, 0], step=1, marks=None, id='TotBsm_query', tooltip={"placement": "bottom", "always_visible": True}),
                html.P(),html.Label('房价（美元）：', className='option_label'),html.P(),
                dcc.RangeSlider(min=30000, max=800000, value=[100000, 200000], step=1, marks=None, id='price_query', tooltip={"placement": "bottom", "always_visible": True})
            ])
        ],className='t-content')
    elif tab == 'tab-4':
        return html.Div([
            html.H3('Tab content 4')
        ],className='t-content')

@app.callback(Output('GrLiv', 'value'),
              [Input('1stFlr', 'value'),
               Input('2stFlr', 'value')])
def cal_Tot(x, y):
    return x + y

@app.callback(Output('result1', 'value'),
              [Input('button1', 'n_clicks'),
               Input('clear1', 'n_clicks')],
              [State('neighbor', 'value'),
               State('overall', 'value'),
               State('TotRsm', 'value'),
               State('GrLiv', 'value'),
               State('1stFlr', 'value'),
               State('2stFlr', 'value'),
               State('TotBsm', 'value')])
def predict1(n1, n2, ng, oa, tr, gl, f1, f2, tb):
    msg = ''
    if 'button1' == ctx.triggered_id:
        m_ng = ['Blmngtn', 'Blueste', 'BrDale', 'BrkSide', 'ClearCr', 'CollgCr', 'Crawfor', 'Edwards', 'Gilbert', 'IDOTRR',
                'MeadowV', 'Mitchel', 'Names', 'NoRidge', 'NPkVill', 'NridgHt', 'NWAmes', 'OldTown', 'SWISU', 'Sawyer',
                'SawyerW', 'Somerst', 'StoneBr', 'Timber', 'Veenker']

        n_ng = ['Bloomington Heights', 'Bluestem', 'Briardale', 'Brookside', 'Clear Creek', 'College Creek', 'Crawford',
                'Edwards', 'Gilbert', 'Iowa DOT and Rail Road', 'Meadow Village', 'Mitchell', 'North Ames', 'Northridge',
                'Northpark Villa', 'Northridge Heights', 'Northwest Ames', 'Old Town',
                'South & West of Iowa State University',
                'Sawyer', 'Sawyer West', 'Somerset', 'Stone Brook', 'Timberland', 'Veenker']

        n_oa = ['Very Poor', 'Poor', 'Fair', 'Below Average', 'Average', 'Above Average', 'Good', 'Very Good', 'Excellent',
                'Very Excellent']

        for i in range(0, 25):
            if n_ng[i] == ng:
                ng = m_ng[i]
        for i in range(0, 10):
            if n_oa[i] == oa:
                oa = i + 1

        df_train = pd.read_csv(
            './train.csv',
            index_col='Id')
        df_test = pd.read_csv(
            './test.csv',
            index_col='Id')
        df_1 = pd.concat([df_train, df_test])
        df = pd.concat([df_1, df_1.iloc[-1:]])
        df.iloc[-1:] = np.nan
        df.iloc[-1, 11] = ng
        df.iloc[-1, 16] = oa
        df.iloc[-1, 53] = tr
        df.iloc[-1, 45] = gl
        df.iloc[-1, 42] = f1
        df.iloc[-1, 43] = f2
        df.iloc[-1, 37] = tb
        num_index = df.columns[df.dtypes != object].delete(-1)
        text_index = df.columns[df.dtypes == object]
        for column in num_index:
            mean_val = df[column].mean()
            df[column].fillna(mean_val, inplace=True)
        scaler = MinMaxScaler()
        num_data = scaler.fit_transform(df[num_index])
        enc = OneHotEncoder(sparse=False)
        text_data = []
        for column in text_index:
            if column == 'Neighborhood':
                m = np.array(df_1[column]).reshape(-1, 1)
                m_1 = np.array(df[column].iloc[-1]).reshape(-1, 1)
                enc = enc.fit(m)
                n = enc.transform(m_1)
                for i in range(0, len(n.T)):
                    text_data.append(n[0, i])
            else:
                m = np.array(df_1[column]).reshape(-1, 1)
                enc = enc.fit(m)
                n = enc.transform(m)
                for i in range(0, len(n.T)):
                    text_data.append(n[0:2919, i].mean())
        text_data = np.array(text_data, dtype=object).reshape(1, -1)
        data = np.concatenate([num_data[-1, :].reshape(1, -1), text_data], axis=1)

        with open('./model_OneHot1.pickle', 'rb') as file:
            model = pickle.load(file)
        result = model.predict(data)
        msg = '{:.2f}美元'.format(result[0])
    elif 'clear1' == ctx.triggered_id:
        msg = ''
    return  msg

@app.callback(Output('download-sample', 'data'),
              Input('download1', 'n_clicks'),
              prevent_initial_call=True)
def download1(n):
    return dcc.send_file('./sample.xlsx')

def parse_contents(contents, filename):
    global df
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded), sheet_name='Sheet1')
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns],
            style_table={'overflowX': 'auto', 'overflowY': 'auto'},
            editable=False,
            style_cell={'textAlign': 'center'}
        )
    ])

@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              prevent_initial_call=True)
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [parse_contents(list_of_contents, list_of_names)]
        return children

@app.callback(Output('download2', 'disabled'),
              Input('output', 'children'))
def able(x):
    if x:
        return False
    else:
        return True

def precise_pred(df):
    return pd.DataFrame({
        'Apple': [1,2,3,4],
        'Pear': [5,6,7,8]
    })

@app.callback(Output('output', 'children'),
              Input('button2', 'n_clicks'),
              State('algorithm', 'value'))
def output(n, algorithm):
    global df, df_result
    if not df.empty:
        df_result = precise_pred(df)
        return  dash_table.DataTable(
            df_result.to_dict('records'),
            [{'name': i, 'id': i} for i in df_result.columns],
            style_table={'overflowX': 'auto', 'overflowY': 'auto'},
            editable=False,
            style_cell={'textAlign': 'center'}
        )

@app.callback(Output('download-result', 'data'),
              Input('download2', 'n_clicks'),
              prevent_initial_call=True)
def download2(n):
    return dcc.send_data_frame(df_result.to_csv, "result.csv")

@app.callback(Output('GrLiv_query', 'value'),
              [Input('1stFlr_query', 'value'),
               Input('2stFlr_query', 'value')])
def cal_Tot(x, y):
    return [x[0]+y[0], x[1]+y[1]]


if __name__ == "__main__":
    app.run_server(debug=True)