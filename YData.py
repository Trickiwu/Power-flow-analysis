# coding=UTF-8
# 形成节点导纳矩阵
# NodeData: bus_i type Pd Qd Pg Qg Gs Bs Vm Va
# LineData: fbus  tbus r  x  b_2  ratio
import numpy as np
import OutTxt
def GetY(NodeData,LineData,**Option):
    NumNode = NodeData.shape[0]
    NumLine = LineData.shape[0]
    Y = np.zeros([NumNode,NumNode])+np.zeros([NumNode,NumNode])*1j
    G0 = NodeData[:,6]  # 节点对地电导
    B0 = NodeData[:,7]  # 节点对地电纳
    for i in range(NumLine):
        Node1 = int(LineData[i,0]-1)
        Node2 = int(LineData[i,1]-1)
        # print(Node1,Node2)
        R = LineData[i,2] 
        X = LineData[i,3] 
        if LineData[i,5]==0:   # 普通线路，无变压器
            B_2 = LineData[i,4] 
            Y[Node1,Node1] = Y[Node1,Node1]+B_2 *1j+1/(R+1j*X) 
            Y[Node2,Node2] = Y[Node2,Node2]+B_2*1j+1/(R+1j*X) 
            Y[Node1,Node2] = Y[Node1,Node2]-1/(R+1j*X) 
            Y[Node2,Node1] = Y[Node2,Node1]-1/(R+1j*X) 
        else:  # 有变压器支路
            K  = LineData[i,5] 
            YT = 1/(R+1j*X) 
            Y[Node1,Node1] = Y[Node1,Node1]+(K-1)/K*YT+YT/K 
            Y[Node2,Node2] = Y[Node2,Node2]+(1-K)/K**2*YT+YT/K 
            Y[Node1,Node2] = Y[Node1,Node2]-1/K*YT 
            Y[Node2,Node1] = Y[Node2,Node1]-1/K*YT 
    for i in range(NumNode):
        Node = int(NodeData[i,0]-1)   # 第一列为节点编号
        Y[Node,Node] = Y[Node,Node]+G0[i]+1j*B0[i] 
    #----------输出到txt文件--------#
    if 'string' not in Option:
        Option['string'] = 'Y矩阵：\n'
    OutTxt.Complex(Y,**Option)  # 元组
    return(Y)