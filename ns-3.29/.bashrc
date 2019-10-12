bashSimulationHelp()
{
    printf "cleanSimulation SPECTATORS[int] DYNAMIC[bool] GRANULARITY[bool] SEED[int]\n"
    printf "simulateFutsal SIM_TIME(ms)[int] SPECTATORS[int] DYNAMIC[bool] GRANULARITY[bool] INTIAL_SEED[int] FINAL_SEED(included)[int]\n"
}

cleanSimulation()
{
    local spectators="$1"
    local dynamic="$2"
    local granularity="$3"
    local seed="$4"
    local result_dir
    local delete_path

    if [ "$dynamic" = "true" ]
    then
        if [ "$granularity" = "true" ]
        then
            result_dir="results/dinamico_rbg_$spectators"
        else
            result_dir="results/dinamico_subframe_$spectators"
        fi
    else
        if [ "$granularity" = "true" ]
        then
            result_dir="results/estatico_rbg_$spectators"
        else
            result_dir="results/estatico_subframe_$spectators"
        fi
    fi

    delete_path=$result_dir"/monitoring_per_second/*_"$seed"_*"
    rm -rf $delete_path
    delete_path=$result_dir"/monitoring_per_second/delay/*_"$seed"_*"
    rm -rf $delete_path
    delete_path=$result_dir"/monitoring_per_second/jitter/*_"$seed"_*"
    rm -rf $delete_path
    delete_path=$result_dir"/monitoring_per_second/lost_packets/*_"$seed"_*"
    rm -rf $delete_path
    delete_path=$result_dir"/monitoring_per_second/throughput/*_"$seed"_*"
    rm -rf $delete_path
    delete_path=$result_dir"/monitoring_aggregated/delay/*_"$seed"_*"   
    rm -rf $delete_path
    delete_path=$result_dir"/monitoring_aggregated/jitter/*_"$seed"_*"  
    rm -rf $delete_path
    delete_path=$result_dir"/monitoring_aggregated/lost_packets/*_"$seed"_*"
    rm -rf $delete_path
    delete_path=$result_dir"/monitoring_aggregated/throughput/*_"$seed"_*"   
    rm -rf $delete_path

}

generateGraphics()
{
    rm -rf ./graphics/dinamico_rbg/delay/*
    rm -rf ./graphics/dinamico_rbg/jitter/*
    rm -rf ./graphics/dinamico_rbg/lost_packets/*
    rm -rf ./graphics/dinamico_rbg/throughput/*
    
    rm -rf ./graphics/estatico_rbg/delay/*
    rm -rf ./graphics/estatico_rbg/jitter/*
    rm -rf ./graphics/estatico_rbg/lost_packets/*
    rm -rf ./graphics/estatico_rbg/throughput/*


    
    python3 graphicgenerator.py dinamico downlink delay
    python3 graphicgenerator.py dinamico uplink delay

    python3 graphicgenerator.py dinamico downlink jitter
    python3 graphicgenerator.py dinamico uplink jitter

    python3 graphicgenerator.py dinamico downlink lost_packets
    python3 graphicgenerator.py dinamico uplink lost_packets

    python3 graphicgenerator.py dinamico downlink throughput
    python3 graphicgenerator.py dinamico uplink throughput



    python3 graphicgenerator.py estatico downlink delay
    python3 graphicgenerator.py estatico uplink delay

    python3 graphicgenerator.py estatico downlink jitter
    python3 graphicgenerator.py estatico uplink jitter

    python3 graphicgenerator.py estatico downlink lost_packets
    python3 graphicgenerator.py estatico uplink lost_packets

    python3 graphicgenerator.py estatico downlink throughput
    python3 graphicgenerator.py estatico uplink throughput
}

generateCompoundGraphics()
{
    rm -rf ./graphics/compound/delay/*
    rm -rf ./graphics/compound/jitter/*
    rm -rf ./graphics/compound/lost_packets/*
    rm -rf ./graphics/compound/throughput/*

    python3 compoundgraphicgenerator.py downlink delay
    python3 compoundgraphicgenerator.py uplink delay

    python3 compoundgraphicgenerator.py downlink jitter
    python3 compoundgraphicgenerator.py uplink jitter

    python3 compoundgraphicgenerator.py downlink lost_packets
    python3 compoundgraphicgenerator.py uplink lost_packets

    python3 compoundgraphicgenerator.py downlink throughput
    python3 compoundgraphicgenerator.py uplink throughput
}

simulateFutsal()
{
    local sim_time="$1"
    local spectators="$2"
    local dynamic="$3"
    local granularity="$4"
    local executions_start="$5"
    local executions_end="$6"
    local result_dir

    rm -rf monitoring_aggregated
    rm -rf monitoring_per_second
    mkdir monitoring_aggregated
    mkdir monitoring_aggregated/delay
    mkdir monitoring_aggregated/jitter
    mkdir monitoring_aggregated/throughput
    mkdir monitoring_aggregated/lost_packets
    mkdir monitoring_per_second
    mkdir monitoring_per_second/delay
    mkdir monitoring_per_second/jitter
    mkdir monitoring_per_second/throughput
    mkdir monitoring_per_second/lost_packets

    if [ "$dynamic" = "true" ]
    then
        if [ "$granularity" = "true" ]
        then
            result_dir="dinamico_rbg_$spectators"
        else
            result_dir="dinamico_subframe_$spectators"
        fi
    else
        if [ "$granularity" = "true" ]
        then
            result_dir="estatico_rbg_$spectators"
        else
            result_dir="estatico_subframe_$spectators"
        fi
    fi
    mkdir results/$result_dir

    printf "\n\nRunning Simulation seeds $executions_start - $executions_end for $sim_time ms with $result_dir\n\n" 

    for (( i=$executions_start ; i<=$executions_end ; i++ ))
    do
        printf "\nRuning $i simulation\n"
	./waf --run="futsal-simple-scenario --simTime=$sim_time --spectators=$spectators --dynamicSlicing=$dynamic --rgbGranulatiry=$granularity --seed=$i"
    done

    cp -r monitoring_per_second results/$result_dir
    cp -r monitoring_aggregated results/$result_dir
}
