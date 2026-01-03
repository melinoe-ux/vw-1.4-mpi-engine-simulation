import numpy as np
import matplotlib.pyplot as plt
from engine_parameters import *
from geometry import cylinder_volume, cylinder_volume_cm3
from thermodynamics import OttoCycle
class CrankAngleSimulation:
    def __init__(self, T_intake=None, P_intake=None, Qin=None):
        self.T_intake = T_intake if T_intake is not None else T_AMBIENT
        self.P_intake = P_intake if P_intake is not None else P_AMBIENT
        otto = OttoCycle(T1=self.T_intake, P1=self.P_intake, Qin=Qin)
        self.Qin = otto.Qin
        self.m = otto.m
        self.theta = THETA_ARRAY
        self.n_steps = len(self.theta)
        self.P = np.zeros(self.n_steps)
        self.T = np.zeros(self.n_steps)
        self.V = np.zeros(self.n_steps)
        self._run_simulation()
    def _run_simulation(self):
        self.V = cylinder_volume(self.theta)
        idx_intake = (self.theta >= 0) & (self.theta <= 180)
        self.P[idx_intake] = self.P_intake
        self.T[idx_intake] = self.T_intake
        idx_compression = (self.theta > 180) & (self.theta < 360)
        V_BDC = cylinder_volume(180)
        P_BDC = self.P_intake
        T_BDC = self.T_intake
        for i in np.where(idx_compression)[0]:
            self.P[i] = P_BDC * (V_BDC / self.V[i]) ** GAMMA_AIR
            self.T[i] = T_BDC * (V_BDC / self.V[i]) ** (GAMMA_AIR - 1)
        idx_tdc = np.argmin(np.abs(self.theta - 360))
        P_before = P_BDC * (V_BDC / self.V[idx_tdc]) ** GAMMA_AIR
        T_before = T_BDC * (V_BDC / self.V[idx_tdc]) ** (GAMMA_AIR - 1)
        T_after = T_before + self.Qin / (self.m * CV_AIR)
        P_after = P_before * (T_after / T_before)
        self.P[idx_tdc] = P_after
        self.T[idx_tdc] = T_after
        idx_power = (self.theta > 360) & (self.theta <= 540)
        V_TDC = self.V[idx_tdc]
        P_TDC = P_after
        T_TDC = T_after
        for i in np.where(idx_power)[0]:
            self.P[i] = P_TDC * (V_TDC / self.V[i]) ** GAMMA_AIR
            self.T[i] = T_TDC * (V_TDC / self.V[i]) ** (GAMMA_AIR - 1)
        idx_exhaust = (self.theta > 540) & (self.theta <= 720)
        self.P[idx_exhaust] = self.P_intake
        T_EVO = self.T[np.argmin(np.abs(self.theta - 540))]
        self.T[idx_exhaust] = T_EVO
        self._calculate_performance()
    def _calculate_performance(self):
        idx_comp = (self.theta >= 180) & (self.theta <= 360)
        V_comp = self.V[idx_comp]
        P_comp = self.P[idx_comp]
        W_comp = np.trapezoid(P_comp, V_comp)
        idx_exp = (self.theta >= 360) & (self.theta <= 540)
        V_exp = self.V[idx_exp]
        P_exp = self.P[idx_exp]
        W_exp = np.trapezoid(P_exp, V_exp)
        self.W_indicated = W_exp + W_comp
        V_d = (MAX_VOLUME - MIN_VOLUME) / 1e6
        self.IMEP = self.W_indicated / V_d
        self.IMEP_bar = self.IMEP / 1e5
        N = ENGINE_SPEED
        self.P_indicated = self.W_indicated * N / (2 * 60)
        self.P_indicated_kW = self.P_indicated / 1000
        self.P_total = self.P_indicated * NUM_CYLINDERS
        self.P_total_kW = self.P_total / 1000
        self.eta_indicated = self.W_indicated / self.Qin
    def print_results(self):
        print("\n" + "=" * 70)
        print("CRANK-ANGLE RESOLVED SIMULATION RESULTS")
        print("=" * 70)
        print(f"\nEngine Configuration:")
        print(f"  Displacement:                {TOTAL_DISPLACEMENT:.2f} cm³ ({TOTAL_DISPLACEMENT/1000:.3f} L)")
        print(f"  Compression Ratio:           {COMPRESSION_RATIO:.1f}:1")
        print(f"  Engine Speed:                {ENGINE_SPEED} RPM")
        print(f"  Number of Cylinders:         {NUM_CYLINDERS}")
        print(f"\nPeak Values:")
        print(f"  Peak Pressure:               {np.max(self.P)/1e5:.2f} bar @ {self.theta[np.argmax(self.P)]:.1f}°")
        print(f"  Peak Temperature:            {np.max(self.T):.2f} K ({np.max(self.T)-273.15:.1f}°C)")
        print(f"\nPerformance (per cylinder):")
        print(f"  Indicated Work:              {self.W_indicated:.2f} J")
        print(f"  IMEP:                        {self.IMEP_bar:.2f} bar")
        print(f"  Indicated Power:             {self.P_indicated_kW:.2f} kW")
        print(f"  Indicated Efficiency:        {self.eta_indicated*100:.2f}%")
        print(f"\nTotal Engine Performance:")
        print(f"  Total Indicated Power:       {self.P_total_kW:.2f} kW ({self.P_total_kW*1.341:.2f} hp)")
        print("=" * 70)
    def plot_results(self, save_dir=None):
        fig, axes = plt.subplots(3, 1, figsize=(14, 12))
        ax1 = axes[0]
        ax1.plot(self.theta, self.P / 1e5, 'b-', linewidth=2)
        ax1.axvline(x=180, color='gray', linestyle='--', alpha=0.5, label='BDC')
        ax1.axvline(x=360, color='red', linestyle='--', alpha=0.5, label='TDC (combustion)')
        ax1.axvline(x=540, color='gray', linestyle='--', alpha=0.5)
        ax1.set_xlabel('Crank Angle [degrees]', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Pressure [bar]', fontsize=12, fontweight='bold')
        ax1.set_title('Cylinder Pressure vs. Crank Angle', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend(loc='best')
        ax1.set_xlim([0, 720])
        strokes = [
            (90, 'Intake', 'lightblue'),
            (270, 'Compression', 'lightcoral'),
            (450, 'Power', 'lightgreen'),
            (630, 'Exhaust', 'lightyellow')
        ]
        for angle, label, color in strokes:
            ax1.axvspan(angle - 90, angle + 90, alpha=0.1, color=color)
            ax1.text(angle, ax1.get_ylim()[1] * 0.95, label, 
                    ha='center', va='top', fontsize=10, style='italic')
        ax2 = axes[1]
        ax2.plot(self.theta, self.T, 'r-', linewidth=2)
        ax2.axvline(x=180, color='gray', linestyle='--', alpha=0.5)
        ax2.axvline(x=360, color='red', linestyle='--', alpha=0.5)
        ax2.axvline(x=540, color='gray', linestyle='--', alpha=0.5)
        ax2.set_xlabel('Crank Angle [degrees]', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Temperature [K]', fontsize=12, fontweight='bold')
        ax2.set_title('Cylinder Temperature vs. Crank Angle', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.set_xlim([0, 720])
        for angle, label, color in strokes:
            ax2.axvspan(angle - 90, angle + 90, alpha=0.1, color=color)
        ax3 = axes[2]
        idx_intake = (self.theta >= 0) & (self.theta <= 180)
        idx_comp = (self.theta > 180) & (self.theta <= 360)
        idx_power = (self.theta > 360) & (self.theta <= 540)
        idx_exhaust = (self.theta > 540) & (self.theta <= 720)
        V_cm3 = self.V * 1e6
        P_bar = self.P / 1e5
        ax3.plot(V_cm3[idx_intake], P_bar[idx_intake], 'b-', linewidth=2, label='Intake')
        ax3.plot(V_cm3[idx_comp], P_bar[idx_comp], 'r-', linewidth=2.5, label='Compression')
        ax3.plot(V_cm3[idx_power], P_bar[idx_power], 'g-', linewidth=2.5, label='Power')
        ax3.plot(V_cm3[idx_exhaust], P_bar[idx_exhaust], 'orange', linewidth=2, label='Exhaust')
        ax3.set_xlabel('Volume [cm³]', fontsize=12, fontweight='bold')
        ax3.set_ylabel('Pressure [bar]', fontsize=12, fontweight='bold')
        ax3.set_title(f'P-V Diagram (IMEP = {self.IMEP_bar:.2f} bar)', 
                     fontsize=14, fontweight='bold')
        ax3.grid(True, alpha=0.3)
        ax3.legend(loc='best')
        ax3.text(0.98, 0.98, 
                f'IMEP: {self.IMEP_bar:.2f} bar\n'
                f'Power: {self.P_total_kW:.2f} kW\n'
                f'η: {self.eta_indicated*100:.1f}%',
                transform=ax3.transAxes, fontsize=10,
                verticalalignment='top', horizontalalignment='right',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        plt.tight_layout()
        if save_dir:
            save_path = f"{save_dir}/crank_angle_simulation.png"
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"\n✓ Simulation plots saved to: {save_path}")
        plt.show()
if __name__ == "__main__":
    print_parameters()
    print("\nRunning crank-angle resolved simulation...")
    sim = CrankAngleSimulation()
    sim.print_results()
    sim.plot_results(save_dir='/Users/arda/Documents/ecyg/engine_cycle')