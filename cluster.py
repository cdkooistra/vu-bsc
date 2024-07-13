from load_data import load_cloudnoise, cloudnoise_metric_mapping
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

def patch_violinplot(palette, n):
    from matplotlib.collections import PolyCollection
    ax = plt.gca()
    violins = [art for art in ax.get_children() if isinstance(art, PolyCollection)]
    colors = sns.color_palette(palette, n_colors=n) * (len(violins)//n)
    for i in range(len(violins)):
        violins[i].set_edgecolor(colors[i])

def plot_noise(df_snellius, df_cloud, data_type, output):
    fig, ax = plt.subplots(figsize=(8, 6))
    message_sizes = sorted(df_snellius['Message Size'].unique())
    bp_snellius_inset_lat = None
    bp_snellius_inset_bw = None
    bp_cloud_inset = None

    if data_type == 'noise_lat':
        rtt_data_cloud = [df_cloud[df_cloud['Message Size'] == size]['RTT/2 (us)'].values for size in message_sizes]
        rtt_data_snellius = [df_snellius[df_snellius['Message Size'] == size]['RTT/2 (us)'].values for size in message_sizes]
        
        bp_cloud = ax.boxplot(rtt_data_cloud, positions=np.arange(len(message_sizes))-0.2, widths=0.4, showfliers=False, patch_artist=True, boxprops=dict(facecolor="#1f77b4"))
        bp_snellius = ax.boxplot(rtt_data_snellius, positions=np.arange(len(message_sizes))+0.2, widths=0.4, showfliers=False, patch_artist=True, boxprops=dict(facecolor="#fe7f0e"))

        ax.set_ylabel('RTT/2 (us)')

        zoom_inset_position = [0.65, 0.35, 0.15, 0.35]
        ax_inset = fig.add_axes(zoom_inset_position)
        bp_snellius_inset_lat = ax_inset.boxplot(rtt_data_snellius, positions=np.arange(len(message_sizes)), widths=0.7, showfliers=False, patch_artist=True, boxprops=dict(facecolor="#fe7f0e"))
        
        ax_inset.set_xticks(np.arange(len(message_sizes)))
        ax_inset.set_xticklabels(message_sizes)
        ax_inset.set_xlim(-1, len(message_sizes))
        ax_inset.set_ylim(1.2, 1.6)
        ax_inset.grid(True, linestyle='--', alpha=0.6)

        fig.suptitle('Network Latency Comparison: Cloud vs Snellius')
    
    elif data_type == 'noise_bw':
        bandwidth_data_cloud = [df_cloud[df_cloud['Message Size'] == size]['Bandwidth (Gb/s)'].values for size in message_sizes]
        bandwidth_data_snellius = [df_snellius[df_snellius['Message Size'] == size]['Bandwidth (Gb/s)'].values for size in message_sizes]
        
        bp_cloud = ax.boxplot(bandwidth_data_cloud, positions=np.arange(len(message_sizes))-0.2, widths=0.4, showfliers=False, patch_artist=True, boxprops=dict(facecolor="#1f77b4"))
        bp_snellius = ax.boxplot(bandwidth_data_snellius, positions=np.arange(len(message_sizes))+0.2, widths=0.4, showfliers=False, patch_artist=True, boxprops=dict(facecolor="#fe7f0e"))

        ax.set_ylabel('Bandwidth (Gb/s)')

        zoom_inset_position_snellius = [0.65, 0.35, 0.15, 0.35]
        ax_inset_snellius = fig.add_axes(zoom_inset_position_snellius)
        
        bp_snellius_inset_bw = ax_inset_snellius.boxplot(bandwidth_data_snellius, positions=np.arange(len(message_sizes)), widths=0.7, showfliers=False, patch_artist=True, boxprops=dict(facecolor="#fe7f0e"))

        ax_inset_snellius.set_xticks(np.arange(len(message_sizes)))
        ax_inset_snellius.set_xticklabels(message_sizes)
        ax_inset_snellius.set_xlim(-1, len(message_sizes))
        ax_inset_snellius.set_ylim(98.2, 98.3)
        ax_inset_snellius.grid(True, linestyle='--', alpha=0.6)

        zoom_inset_position_cloud = [0.25, 0.35, 0.15, 0.35]
        ax_inset_cloud = fig.add_axes(zoom_inset_position_cloud)
        
        bp_cloud_inset = ax_inset_cloud.boxplot(bandwidth_data_cloud, positions=np.arange(len(message_sizes)), widths=0.7, showfliers=False, patch_artist=True, boxprops=dict(facecolor="#1f77b4"))

        ax_inset_cloud.set_xticks(np.arange(len(message_sizes)))
        ax_inset_cloud.set_xticklabels(message_sizes)
        ax_inset_cloud.set_xlim(-1, len(message_sizes))
        ax_inset_cloud.set_ylim(14, 18)
        ax_inset_cloud.grid(True, linestyle='--', alpha=0.6)

        fig.suptitle('Network Bandwidth Comparison: Cloud vs Snellius')

    ax.set_xticks(np.arange(len(message_sizes)))
    ax.set_xticklabels(message_sizes)
    ax.set_xlabel('Message Size')
    ax.legend([bp_cloud["boxes"][0], bp_snellius["boxes"][0]], ['Cloud', 'Snellius'], loc='upper right')

    bp_list = [bp_cloud, bp_snellius]
    if bp_snellius_inset_lat: bp_list.append(bp_snellius_inset_lat)
    if bp_snellius_inset_bw: bp_list.append(bp_snellius_inset_bw)
    if bp_cloud_inset: bp_list.append(bp_cloud_inset)

    for bp in bp_list:
        for element in ['medians']:
            plt.setp(bp[element], color='black')

        for whisker in bp['whiskers']:
            plt.setp(whisker, color='black', linewidth=1, linestyle='--')

    ax.grid(True, linestyle='--', alpha=0.6)
    plt.savefig(output, format='pdf')
    plt.close()

def get_noise_single(df, data_type):
    df_tmp = df   
    df_tmp["Time (min)"] = (df_tmp["Sample"] / len(df_tmp)) * 60.0       

    if "lat" in data_type:
        df_tmp["Normalized Latency"] = df_tmp["RTT/2 (us)"] / df_tmp["RTT/2 (us)"].min()
        df_tmp["Latency (us)"] = df_tmp["RTT/2 (us)"]
        top_net = 0.001
        df_tmp = df_tmp.nlargest(int(len(df_tmp) * top_net), 'Normalized Latency')
    elif "bw" in data_type:
        df_tmp["Normalized Bandwidth"] = df_tmp["Bandwidth (Gb/s)"] / df_tmp["Bandwidth (Gb/s)"].max()
        top_net = 0.001
        df_tmp = df_tmp.nsmallest(int(len(df_tmp) * top_net), 'Normalized Bandwidth')
    else:
        top_os = 0.01
        df_tmp = df_tmp.nlargest(int(len(df_tmp) * top_os), 'Detour (us)')
    
    df_tmp.reset_index(inplace=True, drop=True)
    return df_tmp

def plot_scatter(df_cloud, df_snellius, data_type, output):
    df_cloud = get_noise_single(df_cloud, data_type)
    df_snellius = get_noise_single(df_snellius, data_type)

    plt.figure(figsize=(10, 6))
    
    if "lat" in data_type:
        sns.scatterplot(data=df_cloud, x='Time (min)', y='Normalized Latency', color='#1f77b4', label='Cloud', s=50, edgecolor=None)
        sns.scatterplot(data=df_snellius, x='Time (min)', y='Normalized Latency', color='#fe7f0e', label='Snellius', s=50, edgecolor=None)
        plt.ylabel('Normalized Latency')
        plt.title('Normalized Latency over Time for Cloud and Snellius')

    elif "bw" in data_type:
        sns.scatterplot(data=df_cloud, x='Time (min)', y='Normalized Bandwidth', color='#1f77b4', label='Cloud', s=50, edgecolor=None)
        sns.scatterplot(data=df_snellius, x='Time (min)', y='Normalized Bandwidth', color='#fe7f0e', label='Snellius', s=50, edgecolor=None)
        plt.ylabel('Normalized Bandwidth')
        plt.title('Normalized Bandwidth over Time for Cloud and Snellius')
        
    plt.xlabel('Time (min)')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    
    plt.savefig(output, format='pdf')
    plt.close()

def plot_uni_vs_bi(output):
    providers = ["cloud", "snellius"]
    metrics = ["unidirectional_bw", "bidirectional_bw"]
    opt_msg_size = "16MiB"
    handles = None
    labels = None
    df = pd.DataFrame()

    for metric in metrics:
        for provider in providers:
            dfc = load_cloudnoise(f"{provider}/cloudnoise/", metric + "x1")           
            dfc = dfc[dfc["Message Size"] == opt_msg_size]
            dfc["Type"] = "Unidirectional" if "unidirectional" in metric else "Bidirectional"
            dfc["Provider"] = provider
            df = pd.concat([df, dfc])

    df.reset_index(inplace=True, drop=True)           
    fig, axes = plt.subplots(1, 1, figsize=(4, 5), sharex=True, sharey=True)
    ax = sns.violinplot(data=df, x="Provider", y="Bandwidth (Gb/s)", hue="Type", split=True, inner="quartile",
                        palette={"Unidirectional": "#1f77b4", "Bidirectional": "#fe7f0e"},
                        linewidth=1)
    patch_violinplot(sns.color_palette(), df["Type"].nunique())
    ax.legend_.set_title(None)
    ax.set_xlabel(None)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    fig.tight_layout()
    fig.savefig(output, format='pdf')
    plt.clf()

def main():
    df_cloud_lat = load_cloudnoise("cloud/cloudnoise/", "noise_lat")
    df_snellius_lat = load_cloudnoise("snellius/cloudnoise/", "noise_lat")

    df_cloud_bw = load_cloudnoise("cloud/cloudnoise/", "noise_bw")
    df_snellius_bw = load_cloudnoise("snellius/cloudnoise/", "noise_bw")

    # plot_noise(df_snellius_lat, df_cloud_lat, "noise_lat", "plots/network_latency.pdf")
    # plot_noise(df_snellius_bw, df_cloud_bw, "noise_bw", "plots/network_bandwidth.pdf")

    plot_scatter(df_cloud_lat, df_snellius_lat, "noise_lat", "plots/plot_noise_latency.pdf")
    plot_scatter(df_cloud_bw, df_snellius_bw, "noise_bw", "plots/plot_noise_bandwidth.pdf")

    plot_uni_vs_bi("plots/plot_uni_vs_bi.pdf")

if __name__ == "__main__":
    main()
