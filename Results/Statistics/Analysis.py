import numpy as np
import networkx as nx 
from LoadBase import loadGraphs
from scipy import stats

def run(OS, OF, titleData):
    O0 = OS[0]
    O1 = OS[1]
    O2 = OF[0]
    O3 = OF[1]
    
    ND = []
    ED = []
    MD = []
    TMD = []
    
    
    for OX in [O0,O1,O2,O3]:
        N,E,M,TM,B = loadGraphs(OX)
        ND.extend(N)
        ED.extend(E)
        MD.extend(M)
        TMD.extend(TM)
    
    print(titleData)
    
    for x in ND:
        if x == 10000:
            print(x)
    
    print(sum(ND))
    print(stats.describe(ND))
    print(stats.describe(ED))
    print(stats.describe(MD))
    
    
    
if __name__ == '__main__':
    import sys
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GBigOptions")
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GBigVersions")
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GCoreutilsVersions")
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GCoreutilsOptions")
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GUtilsVersions")
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GUtilsOptions")
    
    from makeBenchBO import benchmarkBO
    from makeBenchBV import benchmarkBV
    from makeBenchCV import benchmarkCV
    from makeBenchCO import benchmarkCO
    from makeBenchUV import benchmarkUV
    from makeBenchUO import benchmarkUO

    run(benchmarkBO("O0","O1"),benchmarkBO("O2","O3"),"BO")
    run(benchmarkBV("V0","V1"),benchmarkBV("V2","V3"),"BV")
    run(benchmarkCO("O0","O1"),benchmarkCO("O2","O3"),"CO")
    run(benchmarkCV("V0","V1"),benchmarkCV("V2","V3"),"CV")
    run(benchmarkUO("O0","O1"),benchmarkUO("O2","O3"),"UO")
    run(benchmarkUV("V0","V1"),benchmarkUV("V2","V3"),"UV")

"""
BO
246161
N DescribeResult(nobs=84, minmax=(80, 25334), mean=2930.4880952380954, variance=13098030.084193919, skewness=3.198313760631558, kurtosis=15.80831024452289)
E DescribeResult(nobs=84, minmax=(72, 54440), mean=8493.345238095239, variance=100439948.8070855, skewness=1.7529657741043825, kurtosis=3.929932786030311)
M DescribeResult(nobs=246161, minmax=(1, 3031), mean=10.83169145396712, variance=1821.0938650009314, skewness=20.344098269241684, kurtosis=680.5393414591532)
BV
181475
DescribeResult(nobs=84, minmax=(36, 9226), mean=2160.4166666666665, variance=5056312.559236947, skewness=1.1786425209586369, kurtosis=0.7520244573792989)
DescribeResult(nobs=84, minmax=(28, 29158), mean=6576.690476190476, variance=54761894.481353976, skewness=1.0877530425902449, kurtosis=0.11505138825333994)
DescribeResult(nobs=181475, minmax=(1, 3959), mean=11.94443862791018, variance=2085.8974771850794, skewness=24.775485509117388, kurtosis=1319.7997733998625)
CO
90967
DescribeResult(nobs=416, minmax=(124, 667), mean=218.67067307692307, variance=8060.992487256717, skewness=2.206391651704973, kurtosis=5.9993148972557115)
DescribeResult(nobs=416, minmax=(151, 1279), mean=343.1105769230769, variance=33081.54918906395, skewness=2.2412245672069893, kurtosis=5.748489926545092)
DescribeResult(nobs=90967, minmax=(1, 697), mean=6.93272285554102, variance=716.4760269097894, skewness=10.185806778905736, kurtosis=128.40189500583568)
CV
56964
DescribeResult(nobs=348, minmax=(91, 440), mean=163.68965517241378, variance=4427.206002186226, skewness=1.727533577840786, kurtosis=3.1588140982989596)
DescribeResult(nobs=348, minmax=(115, 959), mean=282.4109195402299, variance=25554.294635463248, skewness=1.6814323296465605, kurtosis=2.9124836217538457)
DescribeResult(nobs=56964, minmax=(1, 684), mean=8.616424408398286, variance=954.1386667367151, skewness=8.73796732577655, kurtosis=100.48514438566986)
UO
128140
DescribeResult(nobs=88, minmax=(174, 3642), mean=1456.1363636363637, variance=916482.21107628, skewness=0.1969167011865856, kurtosis=-0.9104356235817765)
DescribeResult(nobs=88, minmax=(270, 10474), mean=3908.7045454545455, variance=7896850.969174503, skewness=0.19796348974545697, kurtosis=-0.9242089334979235)
DescribeResult(nobs=128140, minmax=(1, 1231), mean=17.645356641173716, variance=2362.0429657419013, skewness=8.299899166579713, kurtosis=96.55287458588089)
UV
107568
DescribeResult(nobs=88, minmax=(158, 2412), mean=1222.3636363636363, variance=608845.0156739812, skewness=-0.24713277382729834, kurtosis=-1.6085282440031259)
DescribeResult(nobs=88, minmax=(227, 7229), mean=3389.715909090909, variance=5667833.860893416, skewness=-0.11182749590192745, kurtosis=-1.4860848456220257)
DescribeResult(nobs=107568, minmax=(1, 1160), mean=18.82731853339283, variance=2751.865176510991, skewness=7.9750035868898115, kurtosis=87.19011015816727)
246161+181475+90967+56964+128140+107568
"""















