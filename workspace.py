from load_data import load_hpcc_result_set, hpcc_metric_mapping
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def compute_mean_sd(results) -> pd.DataFrame:
    concat = pd.concat(results, ignore_index=True)
    concat['value'] = pd.to_numeric(concat['value'], errors='coerce')

    stats = concat.groupby('metric')['value'].agg(['mean', 'std']).reset_index()

    stats['mean'] = stats['mean'].map('{:.6f}'.format)
    stats['std'] = stats['std'].map('{:.6f}'.format)
    stats['unit'] = stats['metric'].map(hpcc_metric_mapping)

    # Filter out any irrelevant data when computing mean and sd
    stats = stats.dropna()
    
    return stats

def filter_results(dir, metrics) -> pd.DataFrame:
    result_set = load_hpcc_result_set(dir)
    stats = compute_mean_sd(result_set)

    return stats[stats['metric'].isin(metrics)]    

def plot_stream_single():
    metrics = ["SingleSTREAM_Copy","SingleSTREAM_Scale", "SingleSTREAM_Add", "SingleSTREAM_Triad"]
    
    cloud_results = filter_results("cloud/runs/", metrics)
    snellius_results = filter_results("snellius/snellius_baseline/", metrics)

    cloud_results['mean'] = cloud_results['mean'].astype(float)
    snellius_results['mean'] = snellius_results['mean'].astype(float)

    cloud_means = [cloud_results.loc[cloud_results['metric'] == metric, 'mean'].values[0] for metric in metrics]
    snellius_means = [snellius_results.loc[snellius_results['metric'] == metric, 'mean'].values[0] for metric in metrics]

    labels = [metric.split('_')[1] for metric in metrics]
    fig, ax = plt.subplots()
    ind = np.arange(len(labels))

    ax.bar(ind - 0.35/2, cloud_means, 0.35, label='Cloud')
    ax.bar(ind + 0.35/2, snellius_means, 0.35, label='Snellius')
    ax.set_xlabel('SingleSTREAM')
    ax.set_ylabel('GB/s')
    ax.set_title('Comparison of SingleSTREAM: HPC Cloud vs Snellius')
    ax.set_xticks(ind)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.set_ylim(0, 34)

    plt.tight_layout()
    plt.savefig(f"plots/{plot_stream_single.__name__}.pdf")

def plot_stream_star():
    metrics = ["StarSTREAM_Copy","StarSTREAM_Scale", "StarSTREAM_Add", "StarSTREAM_Triad"]
    
    cloud_results = filter_results("cloud/runs/", metrics)
    snellius_results = filter_results("snellius/snellius_baseline/", metrics)

    cloud_results['mean'] = cloud_results['mean'].astype(float)
    snellius_results['mean'] = snellius_results['mean'].astype(float)

    cloud_means = [cloud_results.loc[cloud_results['metric'] == metric, 'mean'].values[0] for metric in metrics]
    snellius_means = [snellius_results.loc[snellius_results['metric'] == metric, 'mean'].values[0] for metric in metrics]

    labels = [metric.split('_')[1] for metric in metrics]
    fig, ax = plt.subplots()
    ind = np.arange(len(labels))

    ax.bar(ind - 0.35/2, cloud_means, 0.35, label='Cloud')
    ax.bar(ind + 0.35/2, snellius_means, 0.35, label='Snellius')
    ax.set_xlabel('StarSTREAM')
    ax.set_ylabel('GB/s')
    ax.set_title('Comparison of StarSTREAM: HPC Cloud vs Snellius')
    ax.set_xticks(ind)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.set_ylim(0, 18)

    plt.tight_layout()
    plt.savefig(f"plots/{plot_stream_star.__name__}.pdf")

def plot_hpl():
    metrics = ["HPL_Tflops"]
    
    cloud_results = filter_results("cloud/runs/", metrics)
    snellius_results = filter_results("snellius/snellius_baseline/", metrics)

    cloud_results['mean'] = cloud_results['mean'].astype(float)
    snellius_results['mean'] = snellius_results['mean'].astype(float)

    cloud_means = [cloud_results.loc[cloud_results['metric'] == metric, 'mean'].values[0] for metric in metrics]
    snellius_means = [snellius_results.loc[snellius_results['metric'] == metric, 'mean'].values[0] for metric in metrics]

    labels = [metric.split('_')[0] for metric in metrics]
    fig, ax = plt.subplots()
    ind = np.arange(len(labels))

    ax.bar(ind - 0.35/2, cloud_means, 0.35, label='Cloud')
    ax.bar(ind + 0.35/2, snellius_means, 0.35, label='Snellius')
    ax.set_ylabel('Tflop/s')
    ax.set_title('Comparison of HPL: HPC Cloud vs Snellius')
    ax.set_xticks(ind)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.set_ylim(0, 0.8)

    plt.tight_layout()
    plt.savefig(f"plots/{plot_hpl.__name__}.pdf")

def plot_dgemm():
    metrics = ["SingleDGEMM_Gflops", "StarDGEMM_Gflops"]
    
    cloud_results = filter_results("cloud/runs/", metrics)
    snellius_results = filter_results("snellius/snellius_baseline/", metrics)

    cloud_results['mean'] = cloud_results['mean'].astype(float)
    snellius_results['mean'] = snellius_results['mean'].astype(float)

    cloud_means = [cloud_results.loc[cloud_results['metric'] == metric, 'mean'].values[0] for metric in metrics]
    snellius_means = [snellius_results.loc[snellius_results['metric'] == metric, 'mean'].values[0] for metric in metrics]

    labels = [metric.split('_')[0] for metric in metrics]
    fig, ax = plt.subplots()
    ind = np.arange(len(labels))

    ax.bar(ind - 0.35/2, cloud_means, 0.35, label='Cloud')
    ax.bar(ind + 0.35/2, snellius_means, 0.35, label='Snellius')
    ax.set_ylabel('Gflop/s')
    ax.set_title('Comparison of DGEMM: HPC Cloud vs Snellius')
    ax.set_xticks(ind)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.set_ylim(0, 50)

    plt.tight_layout()
    plt.savefig(f"plots/{plot_dgemm.__name__}.pdf")

def plot_ptrans():
    metrics = ["PTRANS_GBs"]
    
    cloud_results = filter_results("cloud/runs/", metrics)
    snellius_results = filter_results("snellius/snellius_baseline/", metrics)

    cloud_results['mean'] = cloud_results['mean'].astype(float)
    snellius_results['mean'] = snellius_results['mean'].astype(float)

    cloud_means = [cloud_results.loc[cloud_results['metric'] == metric, 'mean'].values[0] for metric in metrics]
    snellius_means = [snellius_results.loc[snellius_results['metric'] == metric, 'mean'].values[0] for metric in metrics]

    labels = [metric.split('_')[0] for metric in metrics]
    fig, ax = plt.subplots()
    ind = np.arange(len(labels))

    ax.bar(ind - 0.35/2, cloud_means, 0.35, label='Cloud')
    ax.bar(ind + 0.35/2, snellius_means, 0.35, label='Snellius')
    ax.set_ylabel('GB/s')
    ax.set_title('Comparison of PTRANS: HPC Cloud vs Snellius')
    ax.set_xticks(ind)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.set_ylim(0, 8)

    plt.tight_layout()
    plt.savefig(f"plots/{plot_ptrans.__name__}.pdf")

def plot_fft():
    metrics = ["SingleFFT_Gflops", "StarFFT_Gflops", "MPIFFT_Gflops"]
    
    cloud_results = filter_results("cloud/runs/", metrics)
    snellius_results = filter_results("snellius/snellius_baseline/", metrics)

    cloud_results['mean'] = cloud_results['mean'].astype(float)
    snellius_results['mean'] = snellius_results['mean'].astype(float)

    cloud_means = [cloud_results.loc[cloud_results['metric'] == metric, 'mean'].values[0] for metric in metrics]
    snellius_means = [snellius_results.loc[snellius_results['metric'] == metric, 'mean'].values[0] for metric in metrics]

    labels = [metric.split('_')[0] for metric in metrics]
    fig, ax = plt.subplots()
    ind = np.arange(len(labels))

    ax.bar(ind - 0.35/2, cloud_means, 0.35, label='Cloud')
    ax.bar(ind + 0.35/2, snellius_means, 0.35, label='Snellius')
    ax.set_ylabel('Gflop/s')
    ax.set_title('Comparison of FFT: HPC Cloud vs Snellius')
    ax.set_xticks(ind)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.set_ylim(0, 28)

    plt.tight_layout()
    plt.savefig(f"plots/{plot_fft.__name__}.pdf")

def plot_randomaccess():
    metrics = ["SingleRandomAccess_GUPs", "StarRandomAccess_GUPs", "MPIRandomAccess_GUPs"]
    
    cloud_results = filter_results("cloud/runs/", metrics)
    snellius_results = filter_results("snellius/snellius_baseline/", metrics)

    cloud_results['mean'] = cloud_results['mean'].astype(float)
    snellius_results['mean'] = snellius_results['mean'].astype(float)

    cloud_means = [cloud_results.loc[cloud_results['metric'] == metric, 'mean'].values[0] for metric in metrics]
    snellius_means = [snellius_results.loc[snellius_results['metric'] == metric, 'mean'].values[0] for metric in metrics]

    labels = [metric.split('_')[0] for metric in metrics]
    fig, ax = plt.subplots()
    ind = np.arange(len(labels))

    ax.bar(ind - 0.35/2, cloud_means, 0.35, label='Cloud')
    ax.bar(ind + 0.35/2, snellius_means, 0.35, label='Snellius')
    ax.set_ylabel('GUP/s')
    ax.set_title('Comparison of RandomAccess: HPC Cloud vs Snellius')
    ax.set_xticks(ind)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.set_ylim(0, 0.3)

    plt.tight_layout()
    plt.savefig(f"plots/{plot_randomaccess.__name__}.pdf")

def main():
    pd.set_option('display.max_rows', None)  # None means unlimited rows will be displayed
    pd.set_option('display.max_columns', None)  # None means unlimited columns will be displayed
    
    plot_stream_single()
    plot_stream_star()
    plot_hpl()
    plot_dgemm()
    plot_ptrans()
    plot_fft()
    plot_randomaccess()

if __name__ == "__main__":
    main()

