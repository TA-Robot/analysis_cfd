import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
st.set_page_config(layout="wide")

df = pd.read_csv("./202402032337456960966158464b89267c06067b034d34b24.csv", encoding="shift-jis")

実現損益 = "実現損益"
x_実現損益 = "実現損益"
x_銘柄名 = "銘柄名"
x_約定日時 = "約定日時"

df_reward = df[[x_銘柄名, x_実現損益, x_約定日時]].dropna()
df_reward[x_約定日時] = df_reward[x_約定日時].str[:4]
df_reward = df_reward[df_reward[x_実現損益] != 0]


reward_rank = df_reward.groupby([x_約定日時, x_銘柄名]).sum().sort_values(x_実現損益, ascending=False)


# ここから先で、streamlitをつかって、一年単位でreward_rankのなかの結果を表として表示したものを、横に並べるように配置する
# 年ごとにデータを分割する
unique_years = df_reward[x_約定日時].unique()
unique_years.sort()  # 年を昇順に並べ替える

# 各年のデータ用のStreamlit列を最小の間隔で作成
# 列の幅は全体の幅を年の数で割ったもの
col_width = 1 / len(unique_years)
columns = st.columns([col_width] * len(unique_years))

for i, year in enumerate(unique_years):
    # 各列に年ごとのデータを表示
    year_data = reward_rank.loc[reward_rank.index.get_level_values(x_約定日時) == year]
    # 年の情報を取り除く
    year_data = year_data.reset_index(level=x_約定日時, drop=True)

    # 年ごとの合計損益を計算
    total_profit_loss = year_data[x_実現損益].sum()
    # 各列に年ごとのデータと合計損益を表示
    title = f"{year}年のデータ (合計損益: {total_profit_loss:,.0f}円)"

    columns[i].write(title)
    columns[i].dataframe(year_data, width=2000, height=2000)

