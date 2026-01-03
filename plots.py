import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from engine_parameters import *
def plot_comparison(sim_ideal, sim_real=None, save_path=None):
    fig = plt.figure(figsize=(16, 12))
    gs = GridSpec(3, 2, figure=fig, hspace=0.3, wspace=0.3)
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(sim_ideal.theta, sim_ideal.P / 1e5, 'b-', linewidth=2.5, 
            label='Ideal (Instantaneous Combustion)', alpha=0.7)
    if sim_real is not None:
        ax1.plot(sim_real.theta, sim_real.P / 1e5, 'r-', linewidth=2.5,
                label='Real (Wiebe + Heat Transfer)')
    ax1.axvline(x=180, color='gray', linestyle='--', alpha=0.3)
    ax1.axvline(x=360, color='gray', linestyle='--', alpha=0.3, label='TDC')
    ax1.axvline(x=540, color='gray', linestyle='--', alpha=0.3)
    ax1.set_xlabel('Crank Angle [degrees]', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Pressure [bar]', fontsize=12, fontweight='bold')
    ax1.set_title('Cylinder Pressure Comparison', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='best', fontsize=10)
    ax1.set_xlim([0, 720])
    strokes = [(90, 'Intake'), (270, 'Compression'), (450, 'Power'), (630, 'Exhaust')]
    for angle, label in strokes:
        ax1.text(angle, ax1.get_ylim()[1] * 0.95, label,
                ha='center', va='top', fontsize=9, style='italic', color='darkblue')
    ax2 = fig.add_subplot(gs[1, 0])
    idx_comp_ideal = (sim_ideal.theta >= 180) & (sim_ideal.theta <= 360)
    idx_exp_ideal = (sim_ideal.theta >= 360) & (sim_ideal.theta <= 540)
    ax2.plot(sim_ideal.V[idx_comp_ideal] * 1e6, sim_ideal.P[idx_comp_ideal] / 1e5,
            'b-', linewidth=2.5, label='Ideal - Compression', alpha=0.7)
    ax2.plot(sim_ideal.V[idx_exp_ideal] * 1e6, sim_ideal.P[idx_exp_ideal] / 1e5,
            'b--', linewidth=2.5, label='Ideal - Expansion', alpha=0.7)
    if sim_real is not None:
        idx_comp_real = (sim_real.theta >= 180) & (sim_real.theta <= 360)
        idx_exp_real = (sim_real.theta >= 360) & (sim_real.theta <= 540)
        ax2.plot(sim_real.V[idx_comp_real] * 1e6, sim_real.P[idx_comp_real] / 1e5,
                'r-', linewidth=2.5, label='Real - Compression')
        ax2.plot(sim_real.V[idx_exp_real] * 1e6, sim_real.P[idx_exp_real] / 1e5,
                'r--', linewidth=2.5, label='Real - Expansion')
    ax2.set_xlabel('Volume [cm³]', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Pressure [bar]', fontsize=12, fontweight='bold')
    ax2.set_title('P-V Diagram', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc='best', fontsize=9)
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.plot(sim_ideal.theta, sim_ideal.T, 'b-', linewidth=2.5,
            label='Ideal', alpha=0.7)
    if sim_real is not None:
        ax3.plot(sim_real.theta, sim_real.T, 'r-', linewidth=2.5,
                label='Real')
    ax3.axvline(x=360, color='gray', linestyle='--', alpha=0.3)
    ax3.set_xlabel('Crank Angle [degrees]', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Temperature [K]', fontsize=12, fontweight='bold')
    ax3.set_title('Cylinder Temperature', fontsize=14, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    ax3.legend(loc='best', fontsize=10)
    ax3.set_xlim([0, 720])
    ax4 = fig.add_subplot(gs[2, :])
    metrics_labels = ['Peak P\n[bar]', 'Peak T\n[K]', 'IMEP\n[bar]', 
                     'Power\n[kW]', 'Efficiency\n[%]']
    ideal_values = [
        np.max(sim_ideal.P) / 1e5,
        np.max(sim_ideal.T),
        sim_ideal.IMEP_bar,
        sim_ideal.P_total_kW,
        sim_ideal.eta_indicated * 100
    ]
    x = np.arange(len(metrics_labels))
    width = 0.35
    bars1 = ax4.bar(x - width/2, ideal_values, width, label='Ideal',
                   color='skyblue', edgecolor='black', linewidth=1.5)
    if sim_real is not None:
        real_values = [
            np.max(sim_real.P) / 1e5,
            np.max(sim_real.T),
            sim_real.IMEP_bar,
            sim_real.P_total_kW,
            sim_real.eta_indicated * 100
        ]
        bars2 = ax4.bar(x + width/2, real_values, width, label='Real',
                       color='lightcoral', edgecolor='black', linewidth=1.5)
        for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
            height1 = bar1.get_height()
            height2 = bar2.get_height()
            ax4.text(bar1.get_x() + bar1.get_width()/2., height1,
                    f'{ideal_values[i]:.1f}',
                    ha='center', va='bottom', fontsize=8)
            ax4.text(bar2.get_x() + bar2.get_width()/2., height2,
                    f'{real_values[i]:.1f}',
                    ha='center', va='bottom', fontsize=8)
    else:
        for i, bar in enumerate(bars1):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'{ideal_values[i]:.1f}',
                    ha='center', va='bottom', fontsize=8)
    ax4.set_ylabel('Value', fontsize=12, fontweight='bold')
    ax4.set_title('Performance Metrics Comparison', fontsize=14, fontweight='bold')
    ax4.set_xticks(x)
    ax4.set_xticklabels(metrics_labels, fontsize=10)
    ax4.legend(loc='best', fontsize=10)
    ax4.grid(True, alpha=0.3, axis='y')
    plt.suptitle(f'VW 1.4 MPI Engine Cycle Analysis @ {ENGINE_SPEED} RPM',
                fontsize=16, fontweight='bold', y=0.995)
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"\n✓ Comparison plots saved to: {save_path}")
    plt.show()
def print_performance_summary(sim_ideal, sim_real=None):
    print("\n" + "=" * 80)
    print("COMPREHENSIVE PERFORMANCE SUMMARY")
    print("=" * 80)
    print(f"\nEngine: VW 1.4 MPI")
    print(f"Displacement: {TOTAL_DISPLACEMENT:.2f} cm³ ({TOTAL_DISPLACEMENT/1000:.3f} L)")
    print(f"Compression Ratio: {COMPRESSION_RATIO:.1f}:1")
    print(f"Engine Speed: {ENGINE_SPEED} RPM")
    print(f"Number of Cylinders: {NUM_CYLINDERS}")
    print("\n" + "-" * 80)
    print(f"{'Metric':<40} {'Ideal':<20} {'Real':<20}")
    print("-" * 80)
    metrics = [
        ("Peak Cylinder Pressure [bar]", np.max(sim_ideal.P) / 1e5),
        ("Peak Cylinder Temperature [K]", np.max(sim_ideal.T)),
        ("Indicated Work per Cycle [J]", sim_ideal.W_indicated),
        ("IMEP [bar]", sim_ideal.IMEP_bar),
        ("Indicated Power (total) [kW]", sim_ideal.P_total_kW),
        ("Indicated Power (total) [hp]", sim_ideal.P_total_kW * 1.341),
        ("Indicated Efficiency [%]", sim_ideal.eta_indicated * 100),
    ]
    for metric_name, ideal_val in metrics:
        if sim_real is not None:
            if "Pressure" in metric_name:
                real_val = np.max(sim_real.P) / 1e5
            elif "Temperature" in metric_name:
                real_val = np.max(sim_real.T)
            elif "Work" in metric_name:
                real_val = sim_real.W_indicated
            elif "IMEP" in metric_name:
                real_val = sim_real.IMEP_bar
            elif "Power" in metric_name and "kW" in metric_name:
                real_val = sim_real.P_total_kW
            elif "Power" in metric_name and "hp" in metric_name:
                real_val = sim_real.P_total_kW * 1.341
            elif "Efficiency" in metric_name:
                real_val = sim_real.eta_indicated * 100
            else:
                real_val = 0
            print(f"{metric_name:<40} {ideal_val:>18.2f}  {real_val:>18.2f}")
        else:
            print(f"{metric_name:<40} {ideal_val:>18.2f}")
    print("-" * 80)
    if sim_real is not None:
        pressure_loss = (np.max(sim_ideal.P) - np.max(sim_real.P)) / np.max(sim_ideal.P) * 100
        power_loss = (sim_ideal.P_total_kW - sim_real.P_total_kW) / sim_ideal.P_total_kW * 100
        efficiency_loss = sim_ideal.eta_indicated - sim_real.eta_indicated
        print(f"\nLosses (Ideal → Real):")
        print(f"  Peak Pressure Reduction:     {pressure_loss:.2f}%")
        print(f"  Power Reduction:             {power_loss:.2f}%")
        print(f"  Efficiency Reduction:        {efficiency_loss*100:.2f} percentage points")
    print("=" * 80)
if __name__ == "__main__":
    print("Plots module - use from main simulation")
    print("This module provides visualization functions for engine cycle analysis")