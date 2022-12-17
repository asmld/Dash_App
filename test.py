import numpy as np
import pandas as pd
import pickle
df = pd.read_csv('../test.csv')
print(df)
def predict2(df, algorithm):
    num_index = df.columns[df.dtypes != object].delete(0)
    text_index = df.columns[df.dtypes == object]
    num_index = np.array(num_index)
    with open('enc1.pickle', 'rb') as file:
        enc1 = pickle.load(file)
    text_data = enc1.transform(df[text_index])
    for column in num_index:
        mean_val = df[column].mean()
        df[column].fillna(mean_val, inplace=True)
    with open('scaler.pickle', 'rb') as file:
        scaler = pickle.load(file)
    num_data = scaler.transform(df[num_index])

    data = np.concatenate([np.array(num_data), np.array(text_data)], axis=1)
    if algorithm == '深度神经网络':
        with open('model_OneHot1.pickle', 'rb') as file:
            model = pickle.load(file)
    else:
        with open('model_rf.pickle', 'rb') as file:
            model = pickle.load(file)
    target = model.predict(data)
    Id = np.array(df['Id'])
    m = {'Id': Id, 'SalePrice': target}
    m = pd.DataFrame(m)
    m.set_index('Id', inplace=True)
    return m

print(predict2(df, '随机森林'))