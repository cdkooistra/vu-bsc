import json, os, sys
import pandas as pd

cloudnoise_metric_mapping={
    'noise_lat': 'RTT/2 (us)',
    'noise_bw': 'Bandwidth (GB/s)',
    'unidirectional_lat': 'RTT/2 (us)',
    'unidirectional_bw': 'Bandwidth (GB/s)',
    'bidirectional_lat': 'RTT/2 (us)',
    'bidirectional_bw': 'Bandwidth (GB/s)'
}

hpcc_metric_mapping={
    'HPL_Tflops': 'Tflop/s',
    'HPL_time': 'seconds',
    'MPIRandomAccess_time': 'seconds',
    'MPIRandomAccess_CheckTime': 'seconds',
    'MPIRandomAccess_ExeUpdates': 'updates',
    'MPIRandomAccess_GUPs': 'GUP/s',
    'MPIRandomAccess_LCG_time': 'seconds',
    'MPIRandomAccess_LCG_CheckTime': 'seconds',
    'MPIRandomAccess_LCG_ExeUpdates': 'updates',
    'MPIRandomAccess_LCG_GUPs': 'GUP/s',
    'MPIFFT_Gflops': 'Gflop/s',
    'MPIFFT_time0': 'seconds',
    'MPIFFT_time1': 'seconds',
    'MPIFFT_time2': 'seconds',
    'MPIFFT_time3': 'seconds',
    'MPIFFT_time4': 'seconds',
    'MPIFFT_time5': 'seconds',
    'MPIFFT_time6': 'seconds',
    'PTRANS_GBs': 'GB/s',
    'PTRANS_time': 'seconds',
    'SingleDGEMM_Gflops': 'Gflop/s',
    'SingleFFT_Gflops': 'Gflop/s',
    'SingleRandomAccess_GUPs': 'GUP/s',
    'SingleRandomAccess_LCG_GUPs': 'GUP/s',
    'SingleSTREAM_Copy': 'GB/s',
    'SingleSTREAM_Scale': 'GB/s',
    'SingleSTREAM_Add': 'GB/s',
    'SingleSTREAM_Triad': 'GB/s',
    'StarDGEMM_Gflops': 'Gflop/s',
    'StarFFT_Gflops': 'Gflop/s',
    'StarRandomAccess_GUPs': 'GUP/s',
    'StarRandomAccess_LCG_GUPs': 'GUP/s',
    'StarSTREAM_Copy': 'GB/s',
    'StarSTREAM_Scale': 'GB/s',
    'StarSTREAM_Add': 'GB/s',
    'StarSTREAM_Triad': 'GB/s',
    'End to End Runtime': 'seconds'
}

def hr_size(size) -> str:
    if size < 1024:
        return str(int(size)) + "B"
    elif size < 1024*1024:
        return str(int(size / 1024)) + "KiB"
    elif size < 1024*1024*1024:
        return str(int(size / (1024*1024))) + "MiB"
    else:
        sys.exit("Too large size: " + str(size))

def load_hpcc_cloud(file_path) -> pd.DataFrame:
    data = []

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()

            if any(metric in line for metric in ("RandomAccess", "PTRANS", "DGEMM", "STREAM", "MPIFFT", "HPL", "End to End Runtime")):    
                entry = json.loads(line)
                data.append(entry)
    
    df = pd.DataFrame(data)[['metric','value','unit']]
    return df

def load_hpcc_snellius(file_path) -> pd.DataFrame:
    data = []
    in_summary = False
    
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()

            if line.startswith("Begin of Summary section."): 
                in_summary = True
                continue

            if line.startswith("End of Summary section."):
                break

            if in_summary and any(metric in line for metric in ("RandomAccess", "PTRANS", "DGEMM", "STREAM", "FFT", "HPL")):
                metric, value = line.split('=')
                data.append({'metric': metric, 'value':value})
    
    df = pd.DataFrame(data)[['metric','value']]
    return df

def load_cloudnoise(directory, data_type):
    filename = ""
    if data_type == "noise_lat":
        filename = "ng_netnoise_mpi_lat.out"
    elif data_type == "noise_bw":
        filename = "ng_netnoise_mpi_bw.out"
    elif "unidirectional_lat" in data_type or "unidirectional_bw" in data_type:
        if "x" in data_type:
            filename = "ng_one_one_mpi_stripe" + data_type.split("x")[1] + ".out"
        elif "y" in data_type:
            filename = "ng_one_one_mpi_conc" + data_type.split("y")[1] + ".out"
        elif "mpi" in data_type:
            filename = "ng_one_one_mpi_stripe1.out"       
        elif "tcp" in data_type or "udp" in data_type or "ib" in data_type:
            filename = "ng_one_one_" + data_type.split("_")[2] + ".out"       
    elif "bidirectional_lat" in data_type or "bidirectional_bw" in data_type:
        if "x" in data_type:
            filename = "ng_one_one_mpi_bidirect_mpi_stripe" + data_type.split("x")[1] + ".out"
        else:
            filename = "ng_one_one_mpi_bidirect_mpi_conc" + data_type.split("y")[1] + ".out"
    else:
        sys.exit("Unknown data type " + data_type)

    col_names = ["Message Size", "RTT/2 (us)"]
    df = pd.read_csv(f"{directory}{filename}", comment="#", sep="\t", names=col_names)
    df["RTT/2 (us)"] = df["RTT/2 (us)"].astype(float)
    df["Bandwidth (Gb/s)"] = ((df["Message Size"]*8) / (df["RTT/2 (us)"]*1000.0)).astype(float)
    df["Message Size"] = df.apply(lambda x: hr_size(x["Message Size"]), axis=1)
    df["Time (us)"] = df["RTT/2 (us)"].cumsum()
    df["Sample"] = range(len(df))

    return df

def load_hpcc_result_set(dir) -> pd.DataFrame:
    result_set = []

    for folder in os.listdir(dir):
        if "cloud" in dir:
            result_set.append(load_hpcc_cloud(f"{dir}{folder}/perfkitbenchmarker_results.json"))
        elif "snellius" in dir:
            result_set.append(load_hpcc_snellius(f"{dir}{folder}/hpccoutf.txt"))

    return result_set