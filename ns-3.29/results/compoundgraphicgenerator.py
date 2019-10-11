import sys
import numpy as np
import matplotlib.pyplot as pyplot

SPECTATORS_PER_SECTOR = [4, 5, 6, 7]
NUMBER_OF_USER_EQUIPEMENTS = [20, 24, 28, 32]

DOWNLINK_GRAPHIC_TITLE = {
    0: 'Slice 1 - Downlink FTP UEs da quadra',
    1: 'Slice 2 - Downlink VoIP UEs espectadores [Recepção de Áudio]',
    2: 'Slice 3 - Downlink FTP UEs espectadores [ACK de envio de Imagem]',
    3: 'Slice 4 - Downlink FTP UEs espectadores [ACK de envio de Texto]'
}
UPLINK_GRAPHIC_TITLE = {
    0: 'Slice 11 - Uplink FTP UEs da quadra',
    1: 'Slice 12 - Uplink UDP UEs espectadores [Envio de Video]',
    2: 'Slice 13 - Uplink FTP UEs espectadores [Envio de Imagem]',
    3: 'Slice 14 - Uplink FTP UEs espectadores [Envio de Texto]'
}

DOWNLINK_GRAPHIC_FILES = {
    0: 'slice_01_quadra_ftp',
    1: 'slice_02_espectadores_voip_audio',
    2: 'slice_03_espectadores_ack_ftp_imagem',
    3: 'slice_04_espectadores_ack_ftp_texto'
}
UPLINK_GRAPHIC_FILES = {
    0: 'slice_11_quadra_ftp',
    1: 'slice_12_espectadores_udp_video',
    2: 'slice_13_espectadores_ftp_imagem',
    3: 'slice_14_espectadores_ftp_texto'
}

METRIC_AXIS = {
    'delay': 'delay [ms]',
    'jitter': 'jitter [ms]',
    'lost_packets': 'lost packets [%]',
    'throughput': 'throughput [bps]'
}

granularity = 'rbg'
channel = sys.argv[1]
metric = sys.argv[2]

# faulty input: abort
if granularity != 'rbg' and granularity != 'subframe':
    exit('Insert a valid granularity (rbg or subframe)')

if channel != 'downlink' and channel != 'uplink':
    exit('Insert a valid channel (downlink or uplink)')

if metric != 'delay' and \
   metric != 'jitter' and \
   metric != 'lost_packets' and \
   metric != 'throughput':
    exit('Insert a valid metric (delay, jitter, lost_packets or throughput)')

print()
print()
print('-------------------------------------------------------------')
print('Generating graphics on ' + granularity + '_' + channel + '_' + metric)
print('-------------------------------------------------------------')

# set execution models
dynamicExecutionModel = 'dinamico_' + granularity + '_'
staticExecutionModel = 'estatico_' + granularity + '_'

# initialize array to store metrics of each execution
metricsDynamic = []
metricsStatic = []

for spectators, userEquipiments in zip(SPECTATORS_PER_SECTOR,
                                       NUMBER_OF_USER_EQUIPEMENTS):

    # set the current scenario folder path
    dynamicScenarioFolderPath = dynamicExecutionModel + str(spectators) + '/'
    staticScenarioFolderPath = staticExecutionModel + str(spectators) + '/'

    # set path to seeds file
    dynamicSeedsFilePath = dynamicScenarioFolderPath + "seeds.txt"
    staticSeedsFilePath = staticScenarioFolderPath + "seeds.txt"

    # set path to the given metric file
    dynamicMetricFilePath = dynamicScenarioFolderPath + "monitoring_aggregated/"
    dynamicMetricFilePath = dynamicMetricFilePath + metric + "/"
    staticMetricFilePath = staticScenarioFolderPath + "monitoring_aggregated/"
    staticMetricFilePath = staticMetricFilePath + metric + "/"

    # get all seeds as an array
    seeds = open(dynamicSeedsFilePath, "r")
    seeds = seeds.read()
    seeds = seeds[1:-2].split(', ')

    # get the delay for each execution of that model
    scenarioMetrics = []
    for seed in seeds:

        # set metric file name
        metricFileName = channel + "_trace_" + dynamicExecutionModel + seed
        metricFileName = metricFileName + "_" + str(userEquipiments)

        # read metrics
        executionMetrics = open(dynamicMetricFilePath + metricFileName)
        executionMetrics = executionMetrics.read()
        executionMetrics = executionMetrics[:-1].split('\n')

        # append this seed metric to general metric
        scenarioMetrics.append(executionMetrics)

    # group by metric instead of seed
    transposedMetrics = [[], [], [], []]
    for i in range(10):
        transposedMetrics[0].append(scenarioMetrics[i][0])
        transposedMetrics[1].append(scenarioMetrics[i][1])
        transposedMetrics[2].append(scenarioMetrics[i][2])
        transposedMetrics[3].append(scenarioMetrics[i][3])

    # add this scenario execution metrics to total metrics
    metricsDynamic.append(transposedMetrics)

    # get all seeds as an array
    seeds = open(staticSeedsFilePath, "r")
    seeds = seeds.read()
    seeds = seeds[1:-2].split(', ')

    # get the delay for each execution of that model
    scenarioMetrics = []
    for seed in seeds:

        # set metric file name
        metricFileName = channel + "_trace_" + staticExecutionModel + seed
        metricFileName = metricFileName + "_" + str(userEquipiments)

        # read metrics
        executionMetrics = open(staticMetricFilePath + metricFileName)
        executionMetrics = executionMetrics.read()
        executionMetrics = executionMetrics[:-1].split('\n')

        # append this seed metric to general metric
        scenarioMetrics.append(executionMetrics)

    # group by metric instead of seed
    transposedMetrics = [[], [], [], []]
    for i in range(10):
        transposedMetrics[0].append(scenarioMetrics[i][0])
        transposedMetrics[1].append(scenarioMetrics[i][1])
        transposedMetrics[2].append(scenarioMetrics[i][2])
        transposedMetrics[3].append(scenarioMetrics[i][3])

    # add this scenario execution metrics to total metrics
    metricsStatic.append(transposedMetrics)

# set base path to store graphics
graphicBasePath = 'graphics/compound/' + metric + '/'

# for each slice, generate its graphic
for j in range(4):

    # initialize mean and standard deviations
    mean = []
    stdev = []

    # calculate metrics for each scenario
    for i in range(len(metricsDynamic)):

        # initialize result array
        integer_metrics = []

        # convert all 'good' values
        for entry in metricsDynamic[i][j]:
            if entry != '-':
                integer_metrics.append(float(entry))

        # calculate mean values and standard deviation for each scenario
        mean.append(np.mean(integer_metrics))
        if np.mean(integer_metrics) - np.std(integer_metrics) < 0:
            stdev.append(np.mean(integer_metrics))
        else:
            stdev.append(np.std(integer_metrics))

    # plot the graphic with the mean and standard deviation
    pyplot.errorbar(NUMBER_OF_USER_EQUIPEMENTS,
                    mean,
                    stdev,
                    color = 'blue',
                    linestyle='None',
                    marker='^')

    # initialize mean and standard deviations
    mean = []
    stdev = []

    # calculate metrics for each scenario
    for i in range(len(metricsStatic)):

        # initialize result array
        integer_metrics = []

        # convert all 'good' values
        for entry in metricsStatic[i][j]:
            if entry != '-':
                integer_metrics.append(float(entry))

        # calculate mean values and standard deviation for each scenario
        mean.append(np.mean(integer_metrics))
        if np.mean(integer_metrics) - np.std(integer_metrics) < 0:
            stdev.append(np.mean(integer_metrics))
        else:
            stdev.append(np.std(integer_metrics))

    # plot the graphic with the mean and standard deviation
    pyplot.errorbar(NUMBER_OF_USER_EQUIPEMENTS,
                    mean,
                    stdev,
                    color = 'red',
                    linestyle='None',
                    marker='^')

    # set graphic title based on its channel and slice id
    if (channel == 'downlink'):
        pyplot.title(DOWNLINK_GRAPHIC_TITLE[j])
    else:
        pyplot.title(UPLINK_GRAPHIC_TITLE[j])

    # set axis titles
    pyplot.xlabel('Number of User Equipements')
    pyplot.ylabel(METRIC_AXIS[metric])

    # save file with the desired filename
    if (channel == 'downlink'):
        graphicName = graphicBasePath + DOWNLINK_GRAPHIC_FILES[j]
    else:
        graphicName = graphicBasePath + UPLINK_GRAPHIC_FILES[j]
    pyplot.savefig(graphicName)

    # clear graphic
    pyplot.clf()
