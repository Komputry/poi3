import pandas as pd
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

features = pd.read_csv('combined_file.csv', sep=',', index_col=0)

X = features.iloc[:, 1:].values
Y = features.index.values
label_encoder = LabelEncoder()
Y_encoded = label_encoder.fit_transform(Y)

pca = PCA(n_components=3)
Xt = pca.fit_transform(X)

classifier = svm.SVC(gamma='auto')
x_train, x_test, y_train, y_test = train_test_split(Xt, Y_encoded, test_size=0.33)
classifier.fit(x_train, y_train)
y_pred = classifier.predict(x_test)
acc = accuracy_score(y_test, y_pred)
print(acc)
cm = confusion_matrix(y_test, y_pred, normalize='true')
print(cm)

disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=label_encoder.classes_)
disp.plot(cmap=plt.cm.Blues)
plt.show()