import pandas as pd
from sklearn.decomposition import PCA
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def perform_pca(x_val, y_name, y_val, n_components=2):
    pca = PCA(n_components=n_components)
    principalComponents = pca.fit_transform(x_val)
    df = pd.DataFrame(
        data=principalComponents,
        columns=[f"principal component {i+1}" for i in range(n_components)],
    )
    df[y_name] = y_val
    return df, pca


def print_pca_exp_variance(pca):
    print("Expplained variance ratio")
    print(pca.explained_variance_ratio_)
    print()
    print("Total explained variance")
    print(f"{pca.explained_variance_ratio_.sum():.2%}")


def plot_pca_2d(df, y_name, title):
    plt.figure(figsize=(8, 6))
    sns.scatterplot(
        x=df["principal component 1"],
        y=df["principal component 2"],
        hue=df[y_name],
        palette=["red", "green", "blue"],
        alpha=0.7,
    )
    plt.xlabel("PC 1")
    plt.ylabel("PC 2")
    plt.title(title)
    plt.show()


def plot_pca_3d(df, y_name, title):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection="3d")

    species_codes = np.sort(df[y_name].unique())
    palette = ["red", "green", "blue"]

    for i, sp in enumerate(species_codes):
        subset = df[df[y_name] == sp]
        ax.scatter(
            subset["principal component 1"],
            subset["principal component 2"],
            subset["principal component 3"],
            color=palette[i],
            label=f"{y_name} {sp}",
            alpha=0.7,
        )

    plt.xlabel("PC 1")
    plt.ylabel("PC 2")
    ax.set_zlabel("PC 3")
    plt.title(title)
    plt.legend()
    plt.show()
