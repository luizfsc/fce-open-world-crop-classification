#inserir a definição dos classificadores aqui

from sklearn import svm
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
from utils import ST_functions
func = ST_functions()


class alghms:

    def __init__(self, model_name, train, train_labels, test, test_labels, metric,
                 nclusters_train=9, nclusters_test=10, iteration = None, graph = False):

        #interaction --> usado para gerar os gráficos a cada iteração
        #graph --> habilita a exibição de gráficos se True
        #nclusters_train e nclusters_test --> aplicados na obtenção do kmeans para cálculo da silhueta

        if model_name == 'svm':
            self.probs, self.pred = self.svmClassification(train,train_labels, test)

        if metric == 'entropy':
            self.e = self.calc_class_entropy(self.probs)

        if metric == 'silhouette0':

            self.e = self.kmeans_for_new_class(train, test, 0, iteration, graph,
                                               nclusters_train, nclusters_test)

        if metric == 'silhouette1':

            self.e = self.kmeans_for_new_class(train, test, 1, iteration, graph,
                                               nclusters_train, nclusters_test)


    def svmClassification(self, train, train_labels, test):
        SVM = svm.SVC(tol=1.5, probability=True)
        SVM.fit(train, train_labels)
        probs = SVM.predict_proba(test)
        pred = SVM.predict(test)
        # print(np.around(probs,2))
        return [probs, pred]

    def calc_class_entropy(self, p):
        e = [0] * p.shape[0]
        c = len(p[0, :])
        for i in range(p.shape[0]):
            e[i] = - np.sum(p[i, :] * np.log2(p[i, :])) / np.log2(c)
        return e

    def kmeans_for_new_class(self, train, test, kmeans_approach, int, graph, nclusters_train, nclusters_test=10, threshold=0.8):
        kmeans = KMeans(n_clusters=nclusters_train,  # numero de clusters
                        init='k-means++', n_init=10,
                        # método de inicialização dos centróides que permite convergencia mais rápida
                        max_iter=300)  # numero de iterações do algoritmo

        kmeans_test = KMeans(n_clusters=nclusters_test,  # numero de clusters
                             init='k-means++', n_init=10,
                             # método de inicialização dos centróides que permite convergencia mais rápida
                             max_iter=300)  # numero de iterações do algoritmo

        # Visualização do K-means para os dois conjuntos de dados

        pred_train = kmeans.fit_predict(train)
        kmeans_train_center = kmeans.cluster_centers_
        objs_train_to_center_clusters = kmeans.fit_transform(
            train)  # calcula a distancia de cada ponto até os centros de cada cluster

        pred_test = kmeans_test.fit_predict(test)
        kmeans_test_center = kmeans_test.cluster_centers_
        objs_test_to_center_clusters = kmeans_test.fit_transform(test)

        if graph:
            # Visualização do K-means para os dois conjuntos de dados
            # -------------------------------------------------------

            plt.scatter(train[:, 0], train[:, 1], c=pred_train)  # posicionamento dos eixos x e y

            # plt.xlim(-75, -30) #range do eixo x
            # plt.ylim(-50, 10) #range do eixo y
            plt.grid()  # função que desenha a grade no nosso gráfico
            plt.scatter(kmeans_train_center[:, 0], kmeans_train_center[:, 1], s=70,
                        c='red')  # posição de cada centroide no gráfico
            plt.title('Conjunto de treinamento')
            plt.savefig('kmeans_train_' + str(int))
            plt.show()

            plt.figure()

            plt.scatter(test[:, 0], test[:, 1], c=pred_test)  # posicionamento dos eixos x e y
            # plt.xlim(-75, -30) #range do eixo x
            # plt.ylim(-50, 10) #range do eixo y
            plt.grid()  # função que desenha a grade no nosso gráfico
            plt.scatter(kmeans_test_center[:, 0], kmeans_test_center[:, 1], s=70,
                        c='red')  # posição de cada centroide no gráfico
            plt.title('Conjunto de teste')
            plt.savefig('kmeans_test_' + str(int))
            plt.show()

            #------------------------------------------

        data, data_labels, data_centers, data_dists, silhouette = func.augment_data(2, train, pred_train,
                                                                               kmeans_train_center,
                                                                               objs_train_to_center_clusters, test,
                                                                               pred_test, kmeans_test_center,
                                                                               objs_test_to_center_clusters,
                                                                               kmeans_approach, threshold)

        return silhouette
