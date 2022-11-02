#----------------------------LineData------------------------#
# LineData:fbus  tbus   r    x    b    ratio
# fbus为起始节点
# tbus为终止节点
# r为支路电阻
# x为支路电抗
# b为节点对地导纳
# ratio为变压器变比

import utils
import numpy as np
import pypower.api as pp

case_name = 'case30'
def GetData(file):

    mpc = utils.load_case(case_name)
    mpc = pp.ext2int(mpc)

    with np.load(file, allow_pickle=True) as npz:
        data = npz['data'].item()

    # ----------------------------NodeData-------------------------#
    # NodeData: bus_i type Pd Qd Pg Qg Gs Bs Vm Va
    # bus_i为节点编号
    # Pd和Qd为节点的负荷功率
    # Pg和Qg为节点的发电机输出功率
    # Gs和Bs为节点对地电导和电纳
    # Vm为电压幅值，Va为电压相角
    NodeData = np.zeros((data['P'].shape[0], data['P'].shape[1], 10))
    LineData = np.zeros((data['PF'].shape[0], data['PF'].shape[1], 6))

    NodeData[:, :, 0] = np.expand_dims(mpc['bus'][:, 0].T+1, 0).repeat(data['P'].shape[0], axis=0)
    NodeData[:, :, 1] = np.expand_dims(mpc['bus'][:, 1].T, 0).repeat(data['P'].shape[0], axis=0)
    NodeData[:, :, 2] = data['PD']/100
    NodeData[:, :, 3] = data['QD']/100
    NodeData[:, :, 4] = data['PG']/100
    NodeData[:, :, 5] = data['QG']/100
    NodeData[:, :, 6] = data['QG']*0  # Gs 给定为0
    NodeData[:, :, 7] = data['QG']*0  # Bs 给定为0
    NodeData[:, :, 8] = data['V']
    NodeData[:, :, 9] = data['Va']*0

    # ----------------------------LineData------------------------#
    # LineData:fbus  tbus   r    x    b    ratio
    # fbus为起始节点
    # tbus为终止节点
    # r为支路电阻
    # x为支路电抗
    # b为节点对地导纳
    # ratio为变压器变比

    LineData[:, :, 0] = np.expand_dims(mpc['branch'][:, 0].T+1, 0).repeat(data['P'].shape[0], axis=0)
    LineData[:, :, 1] = np.expand_dims(mpc['branch'][:, 1].T+1, 0).repeat(data['P'].shape[0], axis=0)
    LineData[:, :, 2] = data['BR_R']
    LineData[:, :, 3] = data['BR_X']
    LineData[:, :, 4] = data['BR_B']/2
    LineData[:, :, 5] = data['TAP']

    PF = data['PF']/100
    QF = data['QF']/100

    return NodeData, LineData, PF, QF