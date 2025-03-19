import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = pd.read_csv("medical_examination.csv")

# 2
df['bmi'] = (df['weight'])/((df['height']/100)**2)
df['overweight'] = 0
df.loc[df['bmi'] > 25, 'overweight'] = 1
df = df.drop(['bmi'], axis = 'columns')


# 3
df.loc[df['cholesterol'] == 1, 'cholesterol'] = 0
df.loc[df['cholesterol'] > 1, 'cholesterol'] = 1
df.loc[df['gluc'] == 1, 'gluc'] = 0
df.loc[df['gluc'] > 1, 'gluc'] = 1

# 4
def draw_cat_plot():
    # 5
    df_cat0 = pd.melt(df, id_vars=['cardio'], value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])

    # 6
    df_cat1 = df_cat0.groupby(['cardio', 'variable'])['value'].value_counts().reset_index(name='total')

    # 7
    df_plot = sns.catplot(data=df_cat1, x="variable", y="total", hue="value", col="cardio", kind="bar")

    # 8
    fig = df_plot.figure

    # 9
    fig.savefig('catplot.png')
    return fig


# 10
def draw_heat_map():
    # 11
    df_heat = df.loc[(df['ap_lo'] <= df['ap_hi'])
                      & (df['height'] >= df['height'].quantile(0.025))
                      & (df['height'] <= df['height'].quantile(0.975))
                      & (df['weight'] >= df['weight'].quantile(0.025))
                      & (df['weight'] <= df['weight'].quantile(0.975))]

    # 12
    corr = df_heat.corr()

    # 13
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # 14
    #fs = int(corr.size ** 0.5)
    fig, ax = plt.subplots(figsize=(14, 14))

    # 15
    fig = sns.heatmap(corr,
                      mask=mask,
                      annot=True,
                      fmt=".1f",
                      square=True,
                      xticklabels="auto",
                      yticklabels="auto",
                      cbar_kws={'shrink': 0.5},
                      center=0.0,
                      linewidths=0.5,
                      vmin=-0.16,
                      vmax=0.32)
    cbar = fig.collections[0].colorbar
    cbar.set_ticks([-0.08, 0.00, 0.08, 0.16, 0.24])
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    fig = fig.figure
    # 16
    fig.savefig('heatmap.png')
    return fig

# Note 1: guidance on achieving the correct data layout for the catplot found on this freeCodeCamp forum: https://forum.freecodecamp.org/t/medical-data-visualizer-confusion/410074
# Note 2: the use of the .reset_index() option adapted from anky's reply in this discussion thread: https://stackoverflow.com/questions/62557981/in-python-pandas-how-do-i-store-column-name-for-value-counts
# Note 3: code for maksing upper triangle of correlation matrix and plotting heatmap adapted from the following Google search: https://www.google.com/search?q=python+pandas+masking+half+of+correlation+matrix&sca_esv=6ea6144f878bdea6&sxsrf=AHTn8zrBsvvdVqkUAPeRarqcELAKc55vzQ%3A1742407049002&ei=iAXbZ4XpPPbdwN4PzeaRgAY&ved=0ahUKEwiFzdaJ3JaMAxX2LtAFHU1zBGAQ4dUDCBI&uact=5&oq=python+pandas+masking+half+of+correlation+matrix&gs_lp=Egxnd3Mtd2l6LXNlcnAiMHB5dGhvbiBwYW5kYXMgbWFza2luZyBoYWxmIG9mIGNvcnJlbGF0aW9uIG1hdHJpeDIFECEYoAEyBRAhGKABMgUQIRirAjIFECEYqwIyBRAhGJ8FMgUQIRifBTIFECEYnwUyBRAhGJ8FMgUQIRifBTIFECEYnwVImXJQ5wJYmXBwB3gAkAECmAGPAqABvziqAQY1LjQwLjW4AQPIAQD4AQGYAi-gAvUvwgIKEAAYsAMY1gQYR8ICChAjGIAEGCcYigXCAgYQABgWGB7CAggQABiABBiiBMICBRAAGO8FwgIFEAAYgATCAgQQIxgnwgIKEAAYgAQYFBiHAsICCxAAGIAEGJECGIoFwgILEAAYgAQYhgMYigXCAggQABiiBBiJBZgDAIgGAZAGCJIHBzEwLjMyLjWgB82iA7IHBjMuMzIuNbgH1C8&sclient=gws-wiz-serp
# Note 4: code for adjusting heatmap cbar tick values adapted from results to the following Google search: https://www.google.com/search?q=python+seaborn+heatmap+changing+cbar+line+values&sca_esv=6ea6144f878bdea6&sxsrf=AHTn8zpqCx7FTzgASZNVDaVprMVnl7sdXA%3A1742411420521&ei=nBbbZ6e4H-G0wN4P86almQQ&ved=0ahUKEwin9pau7JaMAxVhGtAFHXNTKUMQ4dUDCBI&uact=5&oq=python+seaborn+heatmap+changing+cbar+line+values&gs_lp=Egxnd3Mtd2l6LXNlcnAiMHB5dGhvbiBzZWFib3JuIGhlYXRtYXAgY2hhbmdpbmcgY2JhciBsaW5lIHZhbHVlczIFECEYoAEyBRAhGKABSLMbUPsEWKIacAV4AJABAJgBwQGgAesLqgEDMy45uAEDyAEA-AEBmAIQoALRC8ICChAAGLADGNYEGEfCAgQQIxgnwgIIEAAYgAQYogTCAgUQABjvBcICCBAAGKIEGIkFwgIFECEYqwKYAwCIBgGQBgiSBwQ2LjEwoAeIO7IHBDEuMTC4B78L&sclient=gws-wiz-serp
# Note 5: code for rotation of axis tick mark labels adapted from results to the following Google search: https://www.google.com/search?q=python+seaborn+heatmap+changing+axis+tick+label+orientation&sca_esv=6ea6144f878bdea6&sxsrf=AHTn8zrBkpNxvQ5FpmCQtD6t164cxX7zBg%3A1742411457789&ei=wRbbZ5rrL8XIp84Pst7b2AQ&ved=0ahUKEwjaz_m_7JaMAxVF5MkDHTLvFksQ4dUDCBI&uact=5&oq=python+seaborn+heatmap+changing+axis+tick+label+orientation&gs_lp=Egxnd3Mtd2l6LXNlcnAiO3B5dGhvbiBzZWFib3JuIGhlYXRtYXAgY2hhbmdpbmcgYXhpcyB0aWNrIGxhYmVsIG9yaWVudGF0aW9uMgUQIRirAjIFECEYqwJIlJkCUKkHWNmWAnAaeAGQAQCYAcoBoAGNO6oBBzE0LjQzLjG4AQPIAQD4AQGYAlSgApw-wgIKEAAYsAMY1gQYR8ICBBAjGCfCAggQABiABBiiBMICBRAAGO8FwgIIEAAYogQYiQXCAgUQABiABMICBhAAGBYYHsICBRAhGKABwgIFECEYnwXCAgcQIRigARgKmAMAiAYBkAYIkgcHMzQuNDguMqAHrM4DsgcGOC40OC4yuAeuPQ&sclient=gws-wiz-serp
# Note 6: code for changing plots into figures using the ".figure" option inspired by economy's response in the following discussion thread: https://stackoverflow.com/questions/33616557/barplot-savefig-returning-an-attributeerror