import matplotlib.pyplot as plt

plt.ion()
plt.figure(figsize=(12, 6))


def plot_progress(scores, mean_scores, actions_taken):
    plt.clf() # Efface la figure actuelle
    # plt.figure(figsize=(12, 6))

    # Graphique du score
    plt.subplot(1, 2, 1)
    plt.plot(scores, label='Score par épisode')
    plt.plot(mean_scores, label='Score moyen (100 épisodes)', linestyle='--')
    plt.title('Progression du Score')
    plt.xlabel('Nombre d\'épisodes')
    plt.ylabel('Score')
    plt.legend()
    plt.grid(True)

    # Graphique des actions prises
    plt.subplot(1, 2, 2)
    plt.plot(actions_taken, label='Actions prises par épisode', color='orange')
    plt.title('Nombre d\'Actions par Épisode')
    plt.xlabel('Nombre d\'épisodes')
    plt.ylabel('Nombre d\'actions')
    plt.legend()
    plt.grid(True)

    plt.tight_layout() # Ajuste l'espacement
    # plt.show(block=False) # Affiche sans bloquer
    plt.pause(0.1) # Petite pause pour l'affichage