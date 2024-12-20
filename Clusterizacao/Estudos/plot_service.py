
import matplotlib.pyplot  as plt
import seaborn as sns

def plot_distributions_clusters(list_of_lists, list_names, ax, ay):
    
    fig, axes = plt.subplots(ax ,ay, figsize=(12, 6))

    for i in range(len(list_of_lists)):
        pl = sns.countplot(x=list_of_lists[i],  ax= axes[i])
        pl.set_title(f"Distribution Of The Clusters with k = {list_names[i]}")

    plt.tight_layout()
    plt.show()
