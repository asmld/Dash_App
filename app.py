import base64
import io

import dash
from dash import dcc, html, ctx, dash_table
from dash.dependencies import Input, Output, State

import pickle
import numpy as np
import pandas as pd
from define import *

markdown = '''
# 房价预测&房源查询小程序

本网页框架基于python3的[Dash](https://dash.plotly.com/introduction)模块搭建，在[Render](https://dashboard.render.com/)的免费服务器上运行，源码详见[Github](https://github.com/asmld/Dash_App)。

## 模糊预测

设置街道、整体质量、居住面积等参数，点击开始预测便可得到模糊预测的房价。

+ 上述这些因素是从总共80多个参数中挑选出来的对房价影响最大和人们最关心的几个因素
+ 地面以上居住面积不可调整，默认为一层居住面积与二层居住面积之和
+ 在上述因素之外的七十多个因素默认取“平均值”
+ 模糊预测的结果是**深度神经网络**与**随机森林**两个模型预测结果的平均值

## 精准预测

使用所用的80多个因素进行精准预测，需下载示例的Excel表格进行编辑数据，编辑完成后上传，选择深度神经网络模型或者随机森林模型进行预测，输出的结果表格可下载为csv格式。

+ 示例的Excel表格自带数据筛选，可方便地设置各种因素的参数
+ 上传文件成功后将显示上传的文件名和上传的表格，支持csv格式以及xlsx、xls（须有Sheet1）等格式，不满足格式将报错
+ 选择合适的算法后点击开始预测，程序运行成功后会在下方显示结果表格，可下载csv格式文件
+ 若表格中的参数不符合要求，将会报错

## 房源查询

选择街道、整体质量，调整房间数、居住面积、房价等参数的取值范围，点击开始查询，便可查询合适的房源，输出的结果表格可下载为csv格式。

+ 房源数据来源为训练集数据以及经过准确率最高的模型（随机森林）预测后的训练数据
+ 地面以上居住面积不可调整，默认为一层居住面积与二层居住面积之和
+ 如果输出结果只有列名说明没有在房源数据集中找到合适的房源，尝试扩大各参数的范围

## 模型说明

### 深度神经网络

+ MLP是神经网络的一种，它最主要的特点是有多个神经元层，因此也叫**深度神经网络**。
+ 神经网络的预测能力来自网络的分层或多层结构，输入层接收数据，中间层计算数据，输出层输出结果。
+ 训练模型时，通过前向传播沿着计算图正向计算所有变量，**反向传播**时计算这些变量对应的梯度，交替进行前向传播和反向传播，利用反向传播给出的梯度来更新模型参数，直到得到最准确的预测结果，流程如下：
  1. 获取输入数据
  2. 设计网络结构：如设置隐藏层的数量、epoch次数以及学习率等等
  3. 训练模型并获得预测值
  4. 计算损失值：使用事先选好的损失函数来计算预测值与真值之间的差距
  5. 清零、计算并更新梯度
  6. 重复 3 ~ 5 的过程epoch次
+ Kaggle准确率：0.1646

### 随机森林

+ 随机森林就是通过集成学习的 Bagging 思想将多棵**决策树**集成在一起的一种算法
+ 基本单元就是决策树，将一个输入样本进行分类，就需要将它输入到每棵树中进行分类
+ 将若干个弱分类器的分类结果进行投票选择，从而组成一个**强分类器**，这就是随机森林 Bagging 的思想
+ 实现方法
  1. 一个样本容量为 N 的样本，有放回的抽取 N 次，每次抽取 1 个，最终形成了 N 个样本。这选择好了的 N 个样本用来训练一个决策树，作为决策树根节点处的样本。
  2. 当每个样本有 M 个属性时，在决策树的每个节点需要分裂时，随机从这 M 个属性中选取出 m 个属性，满足条件 m << M。然后从这 m 个属性中采用某种策略来选择 1 个属性作为该节点的分裂属性。
  3. 决策树形成过程中每个节点都要按照步骤 2 来分裂。一直到不能够再分裂为止，整个决策树形成过程中没有进行剪枝。
  4. 按照步骤 1~3 建立大量的决策树，就构成了随机森林。
+ 优点：
  1. 它可以判断特征的重要程度以及不同特征之间的相互影响
  2. 相比决策树不容易过拟合
  3. 训练速度比较快，实现简单
  4. 对缺失值不敏感，如果有很大一部分的特征遗失，仍可以维持准确度。
+ 缺点：
  1. 随机森林在某些噪音较大的分类或回归问题上会过拟合
  2. 对于有不同取值的属性的数据，取值划分较多的属性会对随机森林产生更大的影响，所以随机森林在这种数据上产出的属性权值是不可信的
+ Kaggle准确率：0.1458
'''

Neighborhood = ['Bloomington Heights', 'Bluestem', 'Briardale', 'Brookside', 'Clear Creek', 'College Creek', 'Crawford',
                'Edwards', 'Gilbert', 'Iowa DOT and Rail Road', 'Meadow Village', 'Mitchell', 'North Ames', 'Northridge',
                'Northpark Villa', 'Northridge Heights', 'Northwest Ames', 'Old Town', 'South & West of Iowa State University',
                'Sawyer', 'Sawyer West', 'Somerset', 'Stone Brook', 'Timberland', 'Veenker']
OverallQual = ['Very Excellent', 'Excellent', 'Very Good', 'Good', 'Above Average', 'Average', 'Below Average',
               'Fair', 'Poor', 'Very Poor']
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

num = [5.71377184e+01, 6.93057953e+01, 1.01681141e+04, 6.08907160e+00,
       5.56457691e+00, 1.97131278e+03, 1.98426447e+03, 1.02201312e+02,
       4.41423235e+02, 4.95822481e+01, 5.60772104e+02, 1.05177759e+03,
       1.15958171e+03, 3.36483727e+02, 4.69441590e+00, 1.50075985e+03,
       4.29893726e-01, 6.13644155e-02, 1.56800274e+00, 3.80267215e-01,
       2.86022610e+00, 1.04453580e+00, 6.45152449e+00, 5.97122302e-01,
       1.97811341e+03, 1.76662097e+00, 4.72874572e+02, 9.37098321e+01,
       4.74868106e+01, 2.30983213e+01, 2.60226105e+00, 1.60623501e+01,
       2.25179856e+00, 5.08259678e+01, 6.21308667e+00, 2.00779274e+03]

text = [0.00856457690990065, 0.047619047619047616, 0.008907159986296678, 0.775950668036999, 0.15758821514217197,
        0.0013703323055841042, 0.0041109969167523125, 0.9958890030832477, 0.041109969167523124, 0.02672147995889003,
        0.9321685508735869, 0.3316204179513532, 0.02603631380609798, 0.005481329222336417, 0.6368619390202124,
        0.040082219938335044, 0.041109969167523124, 0.020554984583761562, 0.8982528263103803, 0.998972250770812,
        0.00034258307639602604, 0.0006851661527920521, 0.1750599520383693, 0.06029462144570058,
        0.029119561493662214,
        0.004796163069544364, 0.7307297019527236, 0.9516957862281603, 0.042822884549503254, 0.005481329222336417,
        0.009592326139088728, 0.0034258307639602604, 0.010277492291880781, 0.03699897225077081,
        0.015073655361425145,
        0.09146968139773895, 0.03528605686879068, 0.06646111682082904, 0.0565262076053443, 0.03186022610483042,
        0.012675573826652964, 0.03905447070914697, 0.15176430284343953, 0.0078794107571086, 0.04487838300787941,
        0.024323398424117848, 0.05686879068174032, 0.08187735525865023, 0.01644398766700925, 0.05173004453579993,
        0.042822884549503254, 0.06235011990407674, 0.017471736896197326, 0.024665981500513873, 0.008221993833504625,
        0.0315176430284344, 0.05618362452894827, 0.8602261048304214, 0.006851661527920521, 0.013360739979445015,
        0.009592326139088728, 0.0171291538198013, 0.0020554984583761563, 0.003083247687564234,
        0.0017129153819801302,
        0.004453579993148339, 0.9897225077081192, 0.0013703323055841042, 0.0013703323055841042,
        0.00034258307639602604,
        0.00034258307639602604, 0.0006851661527920521, 0.8307639602603631, 0.021240150736553613,
        0.03734155532716684,
        0.0328879753340185, 0.0777663583418979, 0.10757108598835217, 0.006509078451524495, 0.5039397053785543,
        0.0027406646111682084, 0.008221993833504625, 0.2987324426173347, 0.02843439534087016, 0.043850633778691334,
        0.006851661527920521, 0.7913669064748201, 0.0075368276807125725, 0.18876327509421034, 0.0037684138403562863,
        0.0017129153819801302, 0.00034258307639602604, 0.9852689277149709, 0.00034258307639602604,
        0.00034258307639602604, 0.00034258307639602604, 0.0078794107571086, 0.003083247687564234,
        0.002398081534772182,
        0.015073655361425145, 0.0006851661527920521, 0.0020554984583761563, 0.029804727646454265,
        0.0006851661527920521,
        0.04316546762589928, 0.1514217197670435, 0.00034258307639602604, 0.15416238437821173, 0.07571085988352175,
        0.0006851661527920521, 0.01473107228502912, 0.3511476533059267, 0.1408016443987667, 0.019184652278177457,
        0.00034258307639602604, 0.01301815690304899, 0.0013703323055841042, 0.0075368276807125725,
        0.016101404590613225,
        0.0010277492291880781, 0.04316546762589928, 0.13908872901678657, 0.0051387461459403904, 0.15313463514902365,
        0.00034258307639602604, 0.09249743062692703, 0.0020554984583761563, 0.016101404590613225,
        0.3473792394655704,
        0.13394998287084617, 0.02774922918807811, 0.00034258307639602604, 0.00856457690990065, 0.3011305241521069,
        0.5967797190818773, 0.08530318602261049, 0.008221993833504625, 0.03665638917437478, 0.011990407673860911,
        0.3353888317917095, 0.6159643713600548, 0.0041109969167523125, 0.022953066118533743, 0.10243233984241179,
        0.0010277492291880781, 0.869475847893114, 0.1065433367591641, 0.42309009934909214, 0.44809866392600206,
        0.016786570743405275, 0.0037684138403562863, 0.0017129153819801302, 0.08838643371017471,
        0.03014731072285029,
        0.4141829393627955, 0.4395340870161014, 0.02774922918807811, 0.03562863994518671, 0.041795135320315174,
        0.0017129153819801302, 0.8927714970880438, 0.028091812264474134, 0.14319972593353889, 0.09455292908530319,
        0.08187735525865023, 0.6522781774580336, 0.028091812264474134, 0.14696813977389517, 0.09215484755053101,
        0.2908530318602261, 0.05275779376498801, 0.0986639260020555, 0.29153819801301817, 0.027064063035286058,
        0.017814319972593355, 0.023295649194929772, 0.011647824597464886, 0.029804727646454265, 0.03597122302158273,
        0.8540596094552929, 0.027406646111682084, 0.00034258307639602604, 0.9845837615621789, 0.009249743062692703,
        0.003083247687564234, 0.0006851661527920521, 0.0020554984583761563, 0.5114765330592669, 0.0315176430284344,
        0.16238437821171633, 0.0010277492291880781, 0.2935936964713943, 0.0671462829736211, 0.9328537170263789,
        0.0644056183624529, 0.0171291538198013, 0.0027406646111682084, 0.00034258307639602604, 0.9150393970537856,
        0.00034258307639602604, 0.07022953066118534, 0.023980815347721823, 0.39431312093182597, 0.5111339499828709,
        0.00034258307639602604, 0.006509078451524495, 0.003083247687564234, 0.022267899965741692,
        0.023980815347721823,
        0.011990407673860911, 0.0006851661527920521, 0.9307982185680027, 0.0006851661527920521, 0.01473107228502912,
        0.025351147653305928, 0.25488180883864336, 0.0157588215142172, 0.20280918122644742, 0.48646796848235696,
        0.0078794107571086, 0.5902706406303528, 0.012332990750256937, 0.06372045220966084, 0.0051387461459403904,
        0.26687221651250426, 0.05378554299417609, 0.24631723192874272, 0.2778348749571771, 0.42137718396711205,
        0.05447070914696814, 0.0010277492291880781, 0.042480301473107225, 0.008221993833504625,
        0.0017129153819801302,
        0.8920863309352518, 0.05447070914696814, 0.0010277492291880781, 0.025351147653305928, 0.0051387461459403904,
        0.004796163069544364, 0.9092154847550531, 0.05447070914696814, 0.07399794450154162, 0.021240150736553613,
        0.9047619047619048, 0.0013703323055841042, 0.0006851661527920521, 0.0013703323055841042, 0.9965741692360397,
        0.04042480301473107, 0.03836930455635491, 0.11270983213429256, 0.0041109969167523125, 0.8043850633778691,
        0.0017129153819801302, 0.0013703323055841042, 0.03254539225762247, 0.00034258307639602604,
        0.9640287769784173,
        0.029804727646454265, 0.0041109969167523125, 0.0017129153819801302, 0.008907159986296678,
        0.003083247687564234,
        0.0027406646111682084, 0.08187735525865023, 0.002398081534772182, 0.8650222678999657,
        0.00034258307639602604,
        0.06509078451524494, 0.0041109969167523125, 0.008221993833504625, 0.0157588215142172, 0.8228845495032545,
        0.08393285371702638]
with open('scaler.pickle', 'rb') as file:
    scaler = pickle.load(file)
with open('enc.pickle', 'rb') as file:
    enc = pickle.load(file)
with open('model_OneHot1.pickle', 'rb') as file:
    model = pickle.load(file)
with open('model_rf.pickle','rb') as file:
    model_rf = pickle.load(file)
with open('enc1.pickle', 'rb') as file:
    enc1 = pickle.load(file)
df = pd.DataFrame()
df_result = pd.DataFrame()
df_query = pd.DataFrame()
df_source = pd.read_csv('./source.csv')

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = '数据科学大作业——房价预测'
server = app.server

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
    global df, df_result, df_query
    if tab == 'tab-1':
        return html.Div([
            html.Div([
                html.Label('街道：', className='option_label'),html.P(),
                dcc.Dropdown(options=Neighborhood, value='Northridge', id='neighbor', clearable=False),
                html.P(),
                html.Label('整体质量：', className='option_label'),html.P(),
                dcc.Dropdown(options=OverallQual, value='Good', id='overall', clearable=False),
                html.P(),
                html.Label('地面以上房间总数（不包括浴室）：', className='option_label'),html.P(),
                dcc.Slider(min=2, max=14, value=4, step=1, id='TotRsm')
            ],style={'columnCount': 1}),
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
                html.P(),
                html.Label('整体质量：', className='option_label'),html.P(),
                dcc.Dropdown(options=OverallQual, value='Good', id='overall_query', clearable=False),
                html.P(),
                html.Label('地面以上房间总数（不包括浴室）：', className='option_label'),html.P(),
                dcc.RangeSlider(min=2, max=14, value=[2, 10], step=1, id='TotRsm_query')
            ],style={'columnCount': 1}),
            html.Div([
                html.P(),html.Label('地面以上总居住面积（平方英尺）：', className='option_label'),html.P(),
                dcc.RangeSlider(min=300, max=8000, value=[300, 7000], step=1, marks=None, id='GrLiv_query', tooltip={"placement": "bottom", "always_visible": True}, disabled=True),
                html.P(),html.Label('一层总居住面积（平方英尺）：', className='option_label'),html.P(),
                dcc.RangeSlider(min=300, max=6000, value=[300, 6000], step=1, marks=None, id='1stFlr_query', tooltip={"placement": "bottom", "always_visible": True}),
                html.P(),html.Label('二层总居住面积（平方英尺）：', className='option_label'),html.P(),
                dcc.RangeSlider(min=0, max=2000, value=[0, 1000], step=1, marks=None, id='2stFlr_query', tooltip={"placement": "bottom", "always_visible": True}),
                html.P(),html.Label('地下室总面积（平方英尺）：', className='option_label'),html.P(),
                dcc.RangeSlider(min=0, max=6000, value=[0, 6000], step=1, marks=None, id='TotBsm_query', tooltip={"placement": "bottom", "always_visible": True}),
                html.P(),html.Label('房价（美元）：', className='option_label'),html.P(),
                dcc.RangeSlider(min=30000, max=800000, value=[100000, 500000], step=1, marks=None, id='price_query', tooltip={"placement": "bottom", "always_visible": True})
            ]),
            html.Div([
                html.Button('开始查询', id='button3',style={'margin-right': '20px'}),
                html.Button('下载结果', id='download3', disabled=True)
            ],style={'text-align': 'center', 'margin-top': '10px', 'margin-bottom': '20px'}),
            html.Div(children=dash_table.DataTable(
                df_query.to_dict('records'),
                [{'name': i, 'id': i} for i in df_query.columns],
                style_table={'overflowX': 'auto', 'overflowY': 'auto'},
                editable=False,
                style_cell={'textAlign': 'center'}
            ),id='output2', style={'font-family': 'Lato', 'marigin-top': '10px'}),
            dcc.Download(id='download-query')
        ],className='t-content')
    elif tab == 'tab-4':
        return html.Div([
            dcc.Markdown(markdown, mathjax=True)
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
    global m_ng,n_ng,n_oa,num,text,scaler,enc,model,model_rf
    msg = ''
    if 'button1' == ctx.triggered_id:
        for i in range(0, 25):
            if n_ng[i] == ng:
                ng = m_ng[i]
        for i in range(0, 10):
            if n_oa[i] == oa:
                oa = i + 1
        num1 = np.array(num)
        num1[3] = oa
        num1[12] = f1
        num1[13] = f2
        num1[15] = gl
        num1[22] = tr
        num1[11] = tb
        num1 = scaler.transform(num1.reshape(1, -1))
        text1 = np.array(text)
        ng_1 = []
        ng_1.append(ng)
        ng = np.array(ng_1).reshape(-1, 1)
        ng = (enc.transform(ng)).reshape(-1, 1)
        for i in range(30, 55):
            text1[i] = ng[i - 30]
        data = np.concatenate([num1.reshape(1, -1), text1.reshape(1, -1)], axis=1)
        msg = model.predict(data)
        msg_rf = model_rf.predict(data)
        msg = (msg + msg_rf)/2
        msg = '{:.2f}美元'.format(msg[0])
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
        df = pd.DataFrame()
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

def predict_precise(df, algorithm):
    num_index = df.columns[df.dtypes != object]
    text_index = df.columns[df.dtypes == object].delete(0)
    print(df)
    num_index = np.array(num_index)
    text_data = enc1.transform(df[text_index])
    for column in num_index:
        mean_val = df[column].mean()
        df[column].fillna(mean_val, inplace=True)
    num_data = scaler.transform(df[num_index])

    data = np.concatenate([np.array(num_data), np.array(text_data)], axis=1)
    if algorithm == '深度神经网络':
        target = model.predict(data)
    else:
        target = model_rf.predict(data)
    Id = np.array(df['Id'])
    m = {'Id': Id, 'SalePrice': target}
    m = pd.DataFrame(m)
    return m

@app.callback(Output('output', 'children'),
              Input('button2', 'n_clicks'),
              State('algorithm', 'value'))
def output(n, algorithm):
    global df, df_result
    if not df.empty:
        df1 = df.copy(deep=True)
        for col in df1.columns:
            try:
                df1[col] = df1[col].replace(eval('dict_'+col))
            except:
                pass
        try:
            df_result = predict_precise(df1, algorithm)
            return  dash_table.DataTable(
                df_result.to_dict('records'),
                [{'name': i, 'id': i} for i in df_result.columns],
                style_table={'overflowX': 'auto', 'overflowY': 'auto'},
                editable=False,
                style_cell={'textAlign': 'center'})
        except Exception as e:
            return html.P('Error:'+str(e))

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

@app.callback(Output('download3', 'disabled'),
              Input('output2', 'children'),
              )
def able2(x):
    if x['props']['data']:
        return False
    else:
        return True

@app.callback(Output('output2', 'children'),
              Input('button3', 'n_clicks'),
              [State('neighbor_query', 'value'),
               State('overall_query', 'value'),
               State('TotRsm_query', 'value'),
               State('1stFlr_query', 'value'),
               State('2stFlr_query', 'value'),
               State('TotBsm_query', 'value'),
               State('price_query', 'value')],
              prevent_initial_call=True)
def query(n, ng, oa, tr_value, f1_value, f2_value, tb_value, pr_value):
    global df_query, df_source
    ng = dict_Neighborhood[ng]
    oa = dict_OverallQual[oa]
    tr_min, tr_max = tr_value
    f1_min, f1_max = f1_value
    f2_min, f2_max = f2_value
    tb_min, tb_max = tb_value
    pr_min, pr_max = pr_value
    df_query = df_source[(df_source["Neighborhood"]==ng)&(df_source["OverallQual"]==oa)&
                         (df_source["TotRmsAbvGrd"]>=tr_min)&(df_source["TotRmsAbvGrd"]<=tr_max)&
                         (df_source["1stFlrSF"]>=f1_min)&(df_source["1stFlrSF"]<f1_max)&
                         (df_source["2ndFlrSF"]>=f2_min)&(df_source["2ndFlrSF"]<=f2_max)&
                         (df_source["TotalBsmtSF"]>=tb_min)&(df_source["TotalBsmtSF"]<=tb_max)&
                         (df_source["SalePrice"]>=pr_min)&(df_source["SalePrice"]<=pr_max)]
    return  dash_table.DataTable(
        df_query.to_dict('records'),
        [{'name': i, 'id': i} for i in df_query.columns],
        style_table={'overflowX': 'auto', 'overflowY': 'auto'},
        editable=False,
        style_cell={'textAlign': 'center'}
    )

@app.callback(Output('download-query', 'data'),
              Input('download3', 'n_clicks'),
              prevent_initial_call=True)
def download2(n):
    return dcc.send_data_frame(df_query.to_csv, "result_query.csv")




if __name__ == "__main__":
    app.run_server(debug=True)