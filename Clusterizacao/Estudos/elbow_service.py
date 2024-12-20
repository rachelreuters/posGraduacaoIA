
from sklearn.cluster import KMeans
import matplotlib.pyplot  as plt 

from yellowbrick.cluster import KElbowVisualizer


def plot_all_elbows(start_kmeans, end_kmeans, dataframe):
    model = KMeans(random_state=22)
    fig, axes = plt.subplots(1, 3, figsize=(12, 6))

    visualizer = KElbowVisualizer(model,ax=axes[0], k=(start_kmeans,end_kmeans), timings=False)

    visualizer.fit(dataframe)   
    visualizer.finalize()  

    visualizer2 = KElbowVisualizer(model,ax=axes[1], k=(start_kmeans,end_kmeans), metric='silhouette', timings=False)

    visualizer2.fit(dataframe)   
    visualizer2.finalize()  


    visualizer3 = KElbowVisualizer(model,ax=axes[2], k=(start_kmeans,end_kmeans), metric='calinski_harabasz', timings=False)

    visualizer3.fit(dataframe)   
    visualizer3.finalize()  


    plt.tight_layout()
    plt.show()
        