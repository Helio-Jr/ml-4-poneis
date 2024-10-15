# %%
import pandas as pd

df = pd.read_parquet("../data/dados_clones.parquet")
df
# %%
## Como podemos descobrir onde está o problema?
# <Estatística descritiva>

df.groupby(["Status "])[['Estatura(cm)', 'Massa(em kilos)']].mean()

# %%
df['Status_bool'] = df['Status '] == 'Apto'
df

# %%
df.groupby(["Distância Ombro a ombro"])['Status_bool'].mean().sort_values(ascending=False)

# %%
df.groupby(["Tamanho do crânio"])['Status_bool'].mean().sort_values(ascending=False)

# %%
df.groupby(["Tamanho dos pés"])['Status_bool'].mean().sort_values(ascending=False)

# %%
df.groupby(["General Jedi encarregado"])['Status_bool'].mean().sort_values(ascending=False)

# %%

features = [
    "Estatura(cm)",
    "Massa(em kilos)",
    "Distância Ombro a ombro",
    "Tamanho do crânio",
    "Tamanho dos pés",
]

cat_features = ["Distância Ombro a ombro",
                "Tamanho do crânio",
                "Tamanho dos pés"]

X = df[features]

# %%

# Transformação de categorias para Numérico
from feature_engine import encoding
onehot = encoding.OneHotEncoder(variables=cat_features)
onehot.fit(X)
X = onehot.transform(X)
X

# %%

from sklearn import tree
arvore = tree.DecisionTreeClassifier(max_depth=3)
arvore.fit(X, df["Status "])

# %%

import matplotlib.pyplot as plt
plt.figure(dpi=600)
tree.plot_tree(arvore,
               class_names=arvore.classes_,
               feature_names=X.columns,
               filled=True,
               )
# %%
mask1 = (df["Estatura(cm)"] <= 180.555) & (df["Estatura(cm)"] >= 180.245)
mask2 = df["Massa(em kilos)"] <= 83.405
df_filtered = df[mask1 & mask2]
df_filtered['Status '].value_counts()
# %%
X