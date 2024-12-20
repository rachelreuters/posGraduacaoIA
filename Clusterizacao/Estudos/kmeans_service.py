
from pandas import DataFrame
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot  as plt
from yellowbrick.cluster import SilhouetteVisualizer
from sklearn import metrics

class KmeansAnalysis:
     
    def __init__(self, original_df: DataFrame): 
        self.original_df = original_df
        self.silhouette_scores = []
        self.init_k = 0
        self.end_k = 0
        self.last_cluster_labels = []
        self.last_cluster_distances=[]
        self.df_with_last_cluster_labels= None
        self.last_k_setting = 0



    
    def test_multiple_k_silhuete(self, init_k, end_k):
        
        range_n_clusters = range(init_k, end_k)

        silhouette_scores = []

        for n_clusters in range_n_clusters:
            kmeans = KMeans(n_clusters=n_clusters, random_state=22)
            cluster_labels = kmeans.fit_predict(self.original_df)
            silhouette_avg = silhouette_score(self.original_df, cluster_labels)
            silhouette_scores.append(silhouette_avg)

        self.silhouette_scores = silhouette_scores
        self.init_k = init_k
        self.end_k = end_k


    def save_kmeans_results(self, k):
        kmeans = KMeans(n_clusters=k, random_state=22)
        self.last_cluster_labels = kmeans.fit_predict(self.original_df)
        self.last_cluster_distances = kmeans.transform(self.original_df)
        copy_original_df = self.original_df.copy(deep= True)
        copy_original_df['Cluster'] = self.last_cluster_labels
        self.df_with_last_cluster_labels = copy_original_df
        self.last_k_setting = k 


    def plot_silhuete_scores(self):

        range_n_clusters = range(self.init_k, self.end_k)
        plt.figure(figsize=(10, 6))
        plt.plot(range_n_clusters, self.silhouette_scores, marker='o', linestyle='--', color='b')

        for i, txt in enumerate(self.silhouette_scores): 
            plt.annotate(f'{txt:.4f}', (range_n_clusters[i], self.silhouette_scores[i]), textcoords="offset points", xytext=(0,10), ha='center')

        plt.title('Metrica de Silhueta ')
        plt.xlabel('K Clusters')
        plt.ylabel('Score da Silhueta')
        plt.xticks(range_n_clusters)
        plt.grid(True)
        plt.show()

    
    def plot_2_a_2_after_kmeans_apply(self, k):
        kmeans = KMeans(n_clusters=k,random_state=22)
        model= kmeans.fit(self.original_df)
        y_kmeans = kmeans.predict(self.original_df)

        centers = kmeans.cluster_centers_

        plt.figure(figsize=(90, 80))
        index=0
        for col1 in self.original_df.columns:
            for col2 in self.original_df.columns:
                if col1 != col2:
                    index+=1
                    plt.subplot(len(self.original_df.columns),len(self.original_df.columns),index)
                    plt.scatter(self.original_df[col1], self.original_df[col2], c=y_kmeans, s=50, cmap='viridis')
                    plt.xlabel(col1)
                    plt.ylabel(col2)
                    plt.scatter(centers[:, self.original_df.columns.get_loc(col1)], centers[:, self.original_df.columns.get_loc(col2)], c='black', s=200, alpha=0.7)
            index+=1


    def plot_silhuetes_visualizer(self, plot_x, plot_y):      
        model = KMeans()
        fig, axes = plt.subplots(plot_x, plot_y, figsize=(30, 20))
        axes = axes.flatten()
        for i, k in enumerate(range(self.init_k, self.end_k)):
            model = KMeans(n_clusters=k,random_state=22)
            visualizer = SilhouetteVisualizer(model,ax=axes[i])
            visualizer.fit(self.original_df)   
            visualizer.finalize()  
            silhouette_samples = metrics.silhouette_samples(self.original_df, model.labels_)
            axes[i].set_title(f"K={k}, Silhueta media= {silhouette_samples.mean()}")

        plt.tight_layout()
        plt.show()