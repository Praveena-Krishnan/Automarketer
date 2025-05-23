import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

def find_optimal_k(df: pd.DataFrame, features: list, k_range=(2, 10)):
    """
    Use the silhouette score to find the optimal number of clusters.
    """
    scores = []
    for k in range(k_range[0], k_range[1]):
        model = KMeans(n_clusters=k, random_state=42)
        model.fit(df[features])
        score = silhouette_score(df[features], model.labels_)
        scores.append((k, score))
    
    best_k = max(scores, key=lambda x: x[1])[0]

    # Optional: plot
    plt.plot(*zip(*scores), marker='o')
    plt.xlabel('Number of Clusters (k)')
    plt.ylabel('Silhouette Score')
    plt.title('Optimal K')
    plt.grid(True)
    plt.show()

    return best_k

def apply_kmeans(df: pd.DataFrame, features: list, n_clusters: int = 4)->pd.DataFrame:
    """
    Apply KMeans clustering and return df with 'ClusterLabel'.
    """
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df=df.copy()
    df['ClusterLabel'] = kmeans.fit_predict(df[features])
    print("clustered")
    return df
