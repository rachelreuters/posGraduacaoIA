from sklearn.decomposition import PCA
import matplotlib.pyplot  as plt 
import pandas as pd


class PCAAnalys:
    def __init__(self, components, original_df): 
        self.components = components 
        self.pca_df = None
        self.original_df = original_df

    def apply_pca(self):
        pca = PCA(n_components=self.components)
        data_pca = pca.fit_transform(self.original_df)
        pca_df = pd.DataFrame(data_pca, columns=["col1","col2", "col3"])
        self.pca_df = pca_df
        return pca_df


    def plot_pca(self):    
        y =self.pca_df["col2"]
        z =self.pca_df["col3"]
        x =self.pca_df["col1"]
        fig = plt.figure(figsize=(10,8))
        ax = fig.add_subplot(111, projection="3d")
        ax.scatter(x,y,z, c="maroon", marker="o" )
        ax.set_title(f"Reducao pra {self.components} dimensoes ")
        plt.show()
    
    