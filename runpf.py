
import NetData
from YData import GetY
from InitateU import PolarU
from NewtonRaphson import PolarNR
from OutTxt import SingleTxt, StringTxt

from NetData_new import GetData
from delta_P import *
import numpy as np
# 获取支路参数

Out_Path = 'Cal-Process.txt'
Out_delta = 'Cal_delta.txt'
S0 = '-'

for i in range(130):
    S0 = S0+'-'
StringTxt(path=Out_Path, string=S0 + '\nInitialized Parameter :\n', fmt='w')
StringTxt(path=Out_delta, string=S0 + '\nFinal Result Difference Percentage: \n', fmt='w')



# case_name = 'case30'
npz_file = f'data/case30_testing_data.npz'
NodeDatas, LineDatas, PF0, QF0 = GetData(npz_file)
num_data = NodeDatas.shape[0]

ind = [4, 5, 8, 10,12,21, 24, 26,27]  # 剔除输入功率的界面编号。
abc= [2,22,23]

Y_1 = np.zeros((num_data, NodeDatas.shape[1], NodeDatas.shape[1]))*0
U_1 = NodeDatas[:, :, 1]*0
U_Real_1 = NodeDatas[:, :, 1]*0
Angle_1 = NodeDatas[:, :, 1]*0
Angle_Real_1 = NodeDatas[:, :, 1]*0
P_1 = NodeDatas[:, :, 1]*0
P_Real_1 = NodeDatas[:, :, 1]*0
Q_1 = NodeDatas[:, :, 1]*0
Q_Real_1 = NodeDatas[:, :, 1]*0
i_converge = 0

for i in range(num_data):


    NodeData = NodeDatas[i, :, :]
    LineData = LineDatas[i, :, :]
    U_Real = NodeData[:, 8]
    Angle_Real = NodeData[:, 9]
    PF_real = PF0[i, :]
    QF_real = QF0[i, :]
    P_real = -NodeData[:, 2]+NodeData[:, 4]  # 节点输入有功功率
    Q_real = -NodeData[:, 3]+NodeData[:, 5]  # 节点输入无功功率

    NodeData[ind, 2:3] = 0
    #NodeData[abc, 4:5] = 0

    # 节点导纳矩阵
    Y = GetY(NodeData, LineData, path=Out_Path, width=6)
    # 初始化
    U, Angle = PolarU(NodeData[:, 8], NodeData[:, 9], path=Out_Path, width=9)

    # 开始计算
    PQNode, PVNode, SlackNode, P_Real, Q_Real = NetData.GetNetData(NodeData, LineData, path=Out_Path)
    Iter = 0
    MaxIter = 10
    Tol = 1e-4
    while True:
        Iter = Iter+1
        StringTxt(path=Out_Path, string='\n\n'+S0)
        SingleTxt(Iter, path=Out_Path, string='Iterations ：')
        U, Angle, P, Q, MaxError = PolarNR(U, Angle, Y, PQNode, PVNode, SlackNode, P_Real, Q_Real, Tol, path=Out_Path, width=9)
        if Iter > MaxIter or MaxError < Tol:
            break
    # 结束循环，输出结果
    if MaxError < Tol:
        SingleTxt(Iter-1, path=Out_Path, string='The iteration is completed, and the number of updates is：')
        SingleTxt(MaxError, path=Out_Path, string='MaxError：')

        Y_1[i,:,:] = Y
        U_1[i,:] = U
        U_Real_1[i,:] = U_Real
        Angle_1[i,:] = Angle
        Angle_Real_1[i,:] = Angle_Real
        P_1[i,:] = P.reshape(-1)
        P_Real_1[i,:] = P_Real
        Q_1[i,:] = Q.reshape(-1)
        Q_Real_1[i,:] = Q_Real
        i_converge = i_converge+1

#        SingleTxt(i, path=Out_delta, string='组数：')
#        SingleTxt(MaxError, path=Out_delta, string='结果收敛!')
#        delta_p(Y, ind, U, U_Real, Angle, Angle_Real, P, P_real, Q, Q_real, Out_delta)
        # delta_p_read_pf(Y, U, U_Real, Angle, Angle_Real, P, P_Real, Q, Q_Real, LineData, PF_real, QF_real, Out_delta)

    else:
        SingleTxt(MaxError, path=Out_Path, string='The result is not convergent!')

        # SingleTxt(i, path=Out_delta, string='组数：')
        # SingleTxt(MaxError, path=Out_delta, string='结果不收敛!')
        # delta_p(Y, U, U_Real, Angle, Angle_Real, P, P_Real, Q, Q_Real, Out_delta)


SingleTxt(num_data, path=Out_delta, string='Total number of groups:')
SingleTxt(i_converge, path=Out_delta, string='Number of convergence groups:')
delta_p_ncase(Y_1, ind, U_1, U_Real_1, Angle_1, Angle_Real_1, P_1, P_Real_1, Q_1, Q_Real_1,
              LineDatas, PF0, QF0, Out_delta)
