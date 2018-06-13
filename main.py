from datset_utils import *
from probability_calc import *
from hmm import *
from preprocessing import *
from time_slice import *


# NOTA: per debuggare questo file senza usare la GUI
# decommentare il  if __name__ == '__main__': sotto il metodo calculate

# CREO TRAIN E TEST SET PER DATASET A
def create_set_A(mergedDataset, days):
    if days == 1:
        trainIndex = range(0, 367)
        testIndex = range(368, len(mergedDataset.index))
        train = mergedDataset.loc[trainIndex, :]
        test = mergedDataset.loc[testIndex, :]
    elif days == 2:
        trainIndex = range(68, len(mergedDataset.index))
        testIndex = range(0, 67)
        train = mergedDataset.loc[trainIndex, :]
        test = mergedDataset.loc[testIndex, :]
    elif days == 3:
        trainIndex = range(0, 247)
        train = mergedDataset.loc[trainIndex, :]
        train = train.append(mergedDataset.loc[range(319,len(mergedDataset.index)),:])
        testIndex = range(248, 318)
        test = mergedDataset.loc[testIndex, :]
    elif days == 4:
        trainIndex = range(0, 318)
        train = mergedDataset.loc[trainIndex, :]
        train = train.append(mergedDataset.loc[range(367, len(mergedDataset.index)), :])
        testIndex = range(319, 366)
        test = mergedDataset.loc[testIndex, :]
    elif days == 5:
        trainIndex = range(0, 105)
        train = mergedDataset.loc[trainIndex, :]
        train = train.append(mergedDataset.loc[range(159, len(mergedDataset.index)), :])
        testIndex = range(106, 158)
        test = mergedDataset.loc[testIndex, :]



    return train, test


def create_set_B(mergedDataset, days):
    if days == 1:
        trainIndex = range(0, 6673)
        train = mergedDataset.loc[trainIndex, :]
        train = train.append(mergedDataset.loc[range(9036, len(mergedDataset.index)), :])
        testIndex = range(6674, 9035)
        test = mergedDataset.loc[testIndex, :]
    elif days == 2:
        trainIndex = range(0, 22329)
        train = mergedDataset.loc[trainIndex, :]
        train = train.append(mergedDataset.loc[range(24809, len(mergedDataset.index)), :])
        testIndex = range(22330, 24808)
        test = mergedDataset.loc[testIndex, :]
    elif days == 3:
        trainIndex = range(0, 275)
        train = mergedDataset.loc[trainIndex, :]
        train = train.append(mergedDataset.loc[range(2672, len(mergedDataset.index)), :])
        testIndex = range(276, 2671)
        test = mergedDataset.loc[testIndex, :]
    elif days == 4:
        trainIndex = range(0, 21092)
        train = mergedDataset.loc[trainIndex, :]
        train = train.append(mergedDataset.loc[range(23564, len(mergedDataset.index)), :])
        testIndex = range(21091, 23563)
        test = mergedDataset.loc[testIndex, :]
    elif days == 5:
        trainIndex = range(0, 13164)
        train = mergedDataset.loc[trainIndex, :]
        train = train.append(mergedDataset.loc[range(15765, len(mergedDataset.index)), :])
        testIndex = range(13165, 15764)
        test = mergedDataset.loc[testIndex, :]


    return train,test


# predizione sul dataset dt
def calculate(dt, days, method):

    if method==1:
        # NO TIME SLICE
        if dt == 1:
            dataset = 'Dataset/OrdonezA_ADLs.txt'
            sensor = 'Dataset/OrdonezA_Sensors.txt'
        else:
            dataset = 'Dataset/OrdonezB_ADLs.txt'
            sensor = 'Dataset/OrdonezB_Sensors.txt'

        mergedDataset = merge_dataset(dataset, sensor)

        # CREO TRAIN E TEST SET
        if dataset == 'Dataset/OrdonezA_ADLs.txt':
            train, test = create_set_A(mergedDataset, days)
        else:
            train, test = create_set_B(mergedDataset, days)

        startProb = get_start_prob(train)
        transProb = get_trans_prob(train, dt)
        obsProb = get_obs_prob(train, dt)

        # CONVERTO OSSERVAZIONI IN NUMERI
        evidences = mergedDataset['Evidence'].unique().tolist()
        emissions = test['Evidence'].values.flatten()
        for idx, val in enumerate(emissions):
            emissions[idx] = evidences.index(val)

        # CONVERTO GLI STATI IN NUMERI
        states = mergedDataset['Activity'].unique().tolist()
        giusti = test['Activity'].values.flatten()
        for idx, val in enumerate(giusti):
            giusti[idx] = states.index(val)

        # VITERBI
        viterbi_result, b, c = hmm.viterbi(emissions, transProb.values, obsProb.values, startProb.values.flatten())

        # CONTO QUANTI STATI HO INDOVINATO
        result = 0
        for ind, val in enumerate(viterbi_result):
            if val == giusti[ind]:
                result = result + 1

        print("DATASET: {}".format(dataset))
        print("Stati effettivi: {}".format(giusti))
        print("Stati predetti: {}".format(viterbi_result))
        print("Stati corretti: {} su {}".format(result, len(test)))


        accuracy = (result * 100) / len(test)
        print("Accuratezza: {}".format(accuracy))


    else:
        # TIME SLICE
        giusti, viterbi_result, accuracy = slice_prob(dt, days)




    return viterbi_result, giusti, accuracy






if __name__ == '__main__':
    # 1=dataset A, 2=dataset B
    # datset, days, method(1=no Time Slice)
    calculate(1, 2, 2)





# if __name__ == '__main__':
#
#     # DATASET
#     datasetList = ['Dataset/OrdonezA_ADLs.txt', 'Dataset/OrdonezB_ADLs.txt']
#     sensorList = ['Dataset/OrdonezA_Sensors.txt', 'Dataset/OrdonezB_Sensors.txt']
#
#     for dataset in datasetList:
#         mergedDataset = merge_dataset(dataset, sensorList[datasetList.index(dataset)])
#
#         # CREO TRAIN E TEST SET
#         if dataset == 'Dataset/OrdonezA_ADLs.txt':
#             trainIndex = range(0, 367)
#             testIndex = range(367, len(mergedDataset.index))
#             train = mergedDataset.loc[trainIndex, :]
#             test = mergedDataset.loc[testIndex, :]
#         else:
#             trainIndex = range(0, 2079)
#             testIndex = range(2079, len(mergedDataset.index))
#             train = mergedDataset.loc[trainIndex, :]
#             test = mergedDataset.loc[testIndex, :]
#         startProb = get_start_prob(train)
#         transProb = get_trans_prob(train)
#         obsProb = get_obs_prob(train) # passare mergedDataset
#
#         # CONVERTO OSSERVAZIONI IN NUMERI
#         evidences = mergedDataset['Evidence'].unique().tolist()
#         emissions = test['Evidence'].values.flatten()
#         for idx, val in enumerate(emissions):
#             emissions[idx] = evidences.index(val)
#
#
#         # CONVERTO GLI STATI IN NUMERI
#         evidences = mergedDataset['Activity'].unique().tolist()
#         giusti = test['Activity'].values.flatten()
#         for idx, val in enumerate(giusti):
#             giusti[idx] = evidences.index(val)
#
#
#         # VITERBI
#         viterbi_result,b,c = viterbi(emissions,transProb.values,obsProb.values,startProb.values.flatten())
#
#         # CONTO QUANTI STATI HO INDOVINATO
#         result = 0
#         for ind, val in enumerate(viterbi_result):
#             if val == giusti[ind]:
#                 result = result + 1
#
#
#         print("DATASET: {}".format(dataset))
#         print("Stati effettivi: {}".format(giusti))
#         print("Stati predetti: {}".format(viterbi_result))
#         print("Stati corretti: {} su {}".format(result, len(test)))
#
#
#
#         test_forward()
#
#         print("FILTERING")
#
#         # FILTERING
#         filtering = forward(emissions, transProb.values, obsProb.values, startProb.values.flatten())
#
#         print(filtering)
#
#
