import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px
from matplotlib import cm

from sklearn.preprocessing import QuantileTransformer
import numpy as np


Precision = [0.24,0.26,0.32,0.39,0.09,0.44,0.47,0.08,0.02,0.36,0.42,0.31,0.41,0.4,0.42,0.76,0.47]
Confusion = [0.03,0.015,0.033333333,0.046666667,0.135,0.07,0.06,-0.236666667,0.003333333,0.09,0.231666667,0.65,0.383333333,0.35,0.406666667,0.173333333,0.04]
Confusion = [abs(x) for x in Confusion]
totalWithPreprocessing = [7,6,107,1094,153443,386457,222674,16250282,0,807595,4,315544,485790,3024514,3095329,3,1083]


Precision = Precision[2:8]+Precision[9:]
Confusion = Confusion[2:8]+Confusion[9:]
totalWithPreprocessing = totalWithPreprocessing[2:8]+totalWithPreprocessing[9:]


QT = QuantileTransformer(n_quantiles=5, random_state=0)

PrecisionQ = QT.fit_transform(np.array(Precision).reshape(-1, 1))*5
ConfusionQ = QT.fit_transform(-np.array(Confusion).reshape(-1, 1))*5
RobustnessQ = ConfusionQ
FastnessQ =  QT.fit_transform(-np.array(totalWithPreprocessing).reshape(-1, 1))*5
 


print(PrecisionQ)
print()
print(RobustnessQ)
print()
print(FastnessQ)           
