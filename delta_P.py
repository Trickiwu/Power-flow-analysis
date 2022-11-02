import numpy as np
from OutTxt import SingleTxt, StringTxt


def delta_p_read_pf(y, u, u_real, angle, angle_real, p, p_real, q, q_real, LineData,PF, QF, out_delta):
    # P Q、PF、QF计算前后的误差。
    # y 为导纳矩阵， *_real 为初始值， *为计算值。 out_delta 为输出的路径。
    #pF = y*0
    #pF_real = y*0
    #qF = y*0
    #qF_real = y*0
    #for i in range(y.shape[0]):
    #    pF[i, :, :], qF[i, :, :] = Cal_PF_QF(y[i,:,:], u[i,:], angle[i,:])
    #    pF_real[i, :, :], qF_real[i, :, :] = Cal_PF_QF(y[i,:,:], u_real[i,:], angle_real[i,:])
    pF, qF = Cal_PF_QF(y, u, angle)
    pF = pF[LineData[:, 0].astype(dtype='int')-1, LineData[:, 1].astype(dtype='int')-1]
    qF = qF[LineData[:, 0].astype(dtype='int')-1, LineData[:, 1].astype(dtype='int')-1]

    pF_real = PF
    qF_real = QF
    # pF_real, qF_real = Cal_PF_QF(y, u_real, angle_real)

    temp = np.absolute((u - u_real) / u_real)
    temp = remove_nan_inf_cols_new(temp)
    delta = temp.mean() * 100
    SingleTxt(delta, path=out_delta, string='\tU 误差百分比：')

    delta = np.absolute((angle - angle_real)).mean()
    # temp = remove_nan_inf_cols_new(temp)
    SingleTxt(delta, path=out_delta, string='\tAngle 误差：')

    temp = np.absolute((pF - pF_real) / pF_real)
    temp = remove_nan_inf_cols_new(temp)
    delta = temp.mean() * 100
    SingleTxt(delta, path=out_delta, string='\tPF 误差百分比：')

    temp = np.absolute((qF - qF_real) / qF_real)
    temp = remove_nan_inf_cols_new(temp)
    delta = temp.mean() * 100
    SingleTxt(delta, path=out_delta, string='\tQF 误差百分比：')

    p[np.absolute(p)<1e-06] = 0
    p_real = np.expand_dims(p_real, axis=1)
    temp = np.absolute((p - p_real) / p_real)
    temp = remove_nan_inf_cols_new(temp)
    delta = temp.mean() * 100

    delta1 = np.absolute(p-p_real).mean()
    SingleTxt(delta1, path=out_delta, string='\tP 误差：')
    SingleTxt(delta,  path=out_delta, string='\tP 误差百分比：')

    q[np.absolute(q) < 1e-06] = 0
    q_real = np.expand_dims(q_real, axis=1)
    temp = np.absolute((q - q_real) / q_real)
    temp = remove_nan_inf_cols_new(temp)
    delta = temp.mean() * 100

    delta1 = np.absolute(q - q_real).mean()
    SingleTxt(delta1, path=out_delta, string='\tQ 误差：')
    SingleTxt(delta,  path=out_delta, string='\tQ 误差百分比：')
    StringTxt(path=out_delta, string='\n')

    return 0


def delta_p(y, ind, u, u_real, angle, angle_real, p, p_real, q, q_real, out_delta):
    # P Q、PF、QF计算前后的误差。
    # y 为导纳矩阵， *_real 为初始值， *为计算值。 out_delta 为输出的路径。
    # pF = y*0
    # pF_real = y*0
    # qF = y*0
    # qF_real = y*0
    # for i in range(y.shape[0]):
    #    pF[i, :, :], qF[i, :, :] = Cal_PF_QF(y[i,:,:], u[i,:], angle[i,:])
    #    pF_real[i, :, :], qF_real[i, :, :] = Cal_PF_QF(y[i,:,:], u_real[i,:], angle_real[i,:])
    pF, qF = Cal_PF_QF(y, u, angle)
    pF_real, qF_real = Cal_PF_QF(y, u_real, angle_real)

    temp = np.absolute((u[ind] - u_real[ind]) / u_real[ind])
    temp = remove_nan_inf_cols_new(temp)
    delta = temp.mean() * 100
    SingleTxt(delta, path=out_delta, string='\tU 误差百分比：')

    delta = np.absolute((angle[ind] - angle_real[ind])).mean()
    # temp = remove_nan_inf_cols_new(temp)
    SingleTxt(delta, path=out_delta, string='\tAngle 误差：')

    temp = np.absolute((pF[ind] - pF_real[ind]) / pF_real[ind])
    temp = remove_nan_inf_cols_new(temp)
    delta = temp.mean() * 100
    SingleTxt(delta, path=out_delta, string='\tPF 误差百分比：')

    temp = np.absolute((qF[ind] - qF_real[ind]) / qF_real[ind])
    temp = remove_nan_inf_cols_new(temp)
    delta = temp.mean() * 100
    SingleTxt(delta, path=out_delta, string='\tQF 误差百分比：')

    p[np.absolute(p)<1e-06] = 0
    p_real = np.expand_dims(p_real, axis=1)
    temp = np.absolute((p[ind] - p_real[ind]) / p_real[ind])
    temp = remove_nan_inf_cols_new(temp)
    delta = temp.mean() * 100

    delta1 = np.absolute(p[ind]-p_real[ind]).mean()
    SingleTxt(delta1, path=out_delta, string='\tP 误差：')
    SingleTxt(delta,  path=out_delta, string='\tP 误差百分比：')

    q[np.absolute(q) < 1e-06] = 0
    q_real = np.expand_dims(q_real, axis=1)
    temp = np.absolute((q[ind] - q_real[ind]) / q_real[ind])
    temp = remove_nan_inf_cols_new(temp)
    delta = temp.mean() * 100

    delta1 = np.absolute(q[ind] - q_real[ind]).mean()
    SingleTxt(delta1, path=out_delta, string='\tQ 误差：')
    SingleTxt(delta,  path=out_delta, string='\tQ 误差百分比：')
    StringTxt(path=out_delta, string='\n')

    return 0


def delta_p_ncase(y, ind, u, u_real, angle, angle_real, p, p_real, q, q_real,
                  LineData, pf0, qf0, out_delta):
    # P Q、PF、QF计算前后的误差。
    # y 为导纳矩阵， *_real 为初始值， *为计算值。 out_delta 为输出的路径。
    pF = y*0
    pF_real = y*0
    qF = y*0
    qF_real = y*0
    for i in range(y.shape[0]):
        pF[i, :, :], qF[i, :, :] = Cal_PF_QF(y[i,:,:], u[i,:], angle[i,:])
        # pF_real[i, :, :], qF_real[i, :, :] = Cal_PF_QF(y[i,:,:], u_real[i,:], angle_real[i,:])

        pF_real[i, LineData[i, :, 0].astype(dtype='int')-1, LineData[i, :, 1].astype(dtype='int')-1] = pf0[i, :]
        qF_real[i, LineData[i, :, 0].astype(dtype='int')-1, LineData[i, :, 1].astype(dtype='int')-1] = qf0[i, :]
    # pF, qF = Cal_PF_QF(y, u, angle)
    # pF_real, qF_real = Cal_PF_QF(y, u_real, angle_real)


    temp = np.absolute((u[:, ind] - u_real[:, ind]) / u_real[:, ind])
    temp = remove_nan_inf_cols_new(temp)
    delta = temp.mean() * 100
    SingleTxt(delta, path=out_delta, string='\tU Error Percentage:')

    delta = np.absolute((angle[:, ind] - angle_real[:, ind])).mean()
    # temp = remove_nan_inf_cols_new(temp)
    SingleTxt(delta, path=out_delta, string='\tAngle Error:')

    delta1 = np.absolute(pF[:, ind, :] - pF_real[:, ind, :]).mean()
    delta2 = np.absolute(pF[:, :, ind] - pF_real[:, :, ind]).mean()
    SingleTxt(delta1+delta2, path=out_delta, string='\tPF Error:')

    delta1 = np.absolute(qF[:, ind, :] - qF_real[:, ind, :]).mean()
    delta2 = np.absolute(qF[:, :, ind] - qF_real[:, :, ind]).mean()
    SingleTxt(delta1+delta2, path=out_delta, string='\tQF Error:')

    # p[np.absolute(p)<1e-06] = 0
    # p_real = np.expand_dims(p_real, axis=1)
    temp = np.absolute((p[:, ind] - p_real[:, ind]) / p_real[:, ind])
    temp = remove_nan_inf_cols_new(temp)
    delta = temp.mean() * 100

    delta1 = np.absolute(p[:, ind]-p_real[:, ind]).mean()
    SingleTxt(delta1, path=out_delta, string='\tP Error:')
    SingleTxt(delta,  path=out_delta, string='\tP Error Percentage:')

    # q[np.absolute(q) < 1e-06] = 0
    # q_real = np.expand_dims(q_real, axis=1)
    temp = np.absolute((q[:, ind] - q_real[:, ind]) / q_real[:, ind])
    temp = remove_nan_inf_cols_new(temp)
    delta = temp.mean() * 100

    delta1 = np.absolute(q[:, ind] - q_real[:, ind]).mean()
    SingleTxt(delta1, path=out_delta, string='\tQ Error:')
    SingleTxt(delta,  path=out_delta, string='\tQ Error Percentage:')
    StringTxt(path=out_delta, string='\n')

    return 0


def Cal_PF_QF(y, u, angle):
    n = y.shape[0]
    Y = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i is not j:
                Y[i, j] = -y[i, j]
            else:
                Y[i, j] = sum(y[i, :])

    # 计算支路功率
    U1 = np.zeros((n), dtype='complex')
    Sij = np.zeros((n, n), dtype='complex')
    for i in range(n):
        U1[i] = complex(u[i] * np.cos(angle[i]), u[i] * np.sin(angle[i]))
        for j in range(n):
            U1[j] = complex(u[j] * np.cos(angle[j]), u[j] * np.sin(angle[j]))
            Sij[i, j] = U1[i] * np.conj((U1[i] - U1[j]) * y[i, j])

    pf = Sij.real
    qf = Sij.imag

    return pf, qf


def remove_nan_inf_cols_new(arr):

    index = np.isnan(arr)
    arr = arr[~index]

    index = np.isinf(arr)
    arr = arr[~index]

    return arr
