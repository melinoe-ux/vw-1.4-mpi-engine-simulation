import numpy as np
import matplotlib.pyplot as plt
from engine_parameters import *
class WiebeCombustion:
    def __init__(self, theta_start=-15, duration=50, a=5.0, m=2.0):
        self.theta_start = 360 + theta_start
        self.duration = duration
        self.theta_end = self.theta_start + duration
        self.a = a
        self.m = m
    def burned_mass_fraction(self, theta):
        xb = np.zeros_like(theta, dtype=float)
        mask_before = theta < self.theta_start
        xb[mask_before] = 0.0
        mask_during = (theta >= self.theta_start) & (theta <= self.theta_end)
        if np.any(mask_during):
            theta_rel = (theta[mask_during] - self.theta_start) / self.duration
            xb[mask_during] = 1.0 - np.exp(-self.a * (theta_rel ** (self.m + 1)))
        mask_after = theta > self.theta_end
        xb[mask_after] = 1.0
        return xb
    def heat_release_rate(self, theta, Q_total):
        theta_array = np.atleast_1d(theta)
        scalar_input = theta_array.ndim == 0 or (theta_array.ndim == 1 and len(theta_array) == 1)
        dQ_dtheta = np.zeros_like(theta_array, dtype=float)
        mask_during = (theta_array >= self.theta_start) & (theta_array <= self.theta_end)
        if np.any(mask_during):
            theta_rel = (theta_array[mask_during] - self.theta_start) / self.duration
            dxb_dtheta_rel = self.a * (self.m + 1) * (theta_rel ** self.m) * \
                            np.exp(-self.a * (theta_rel ** (self.m + 1)))
            dxb_dtheta = dxb_dtheta_rel / self.duration
            dQ_dtheta[mask_during] = Q_total * dxb_dtheta
        if scalar_input:
            return dQ_dtheta[0]
        return dQ_dtheta
    def cumulative_heat_release(self, theta, Q_total):
        xb = self.burned_mass_fraction(theta)
        return Q_total * xb
    def plot_combustion(self, Q_total=1000, save_path=None):
        theta_plot = np.linspace(self.theta_start - 20, self.theta_end + 20, 500)
        xb = self.burned_mass_fraction(theta_plot)
        Q_cum = self.cumulative_heat_release(theta_plot, Q_total)
        dQ_dtheta = self.heat_release_rate(theta_plot, Q_total)
        fig, axes = plt.subplots(3, 1, figsize=(12, 10))
        ax1 = axes[0]
        ax1.plot(theta_plot, xb, 'b-', linewidth=2.5)
        ax1.axvline(x=360, color='red', linestyle='--', alpha=0.5, label='TDC')
        ax1.axvline(x=self.theta_start, color='green', linestyle='--', alpha=0.5, 
                   label=f'Ignition ({self.theta_start-360:.0f}° BTDC)')
        ax1.axhline(y=0.5, color='gray', linestyle=':', alpha=0.5, label='50% burned')
        ax1.set_xlabel('Crank Angle [degrees]', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Burned Mass Fraction', fontsize=12, fontweight='bold')
        ax1.set_title('Wiebe Burned Mass Fraction', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend(loc='best')
        ax1.set_ylim([0, 1.1])
        ax2 = axes[1]
        ax2.plot(theta_plot, Q_cum, 'g-', linewidth=2.5)
        ax2.axvline(x=360, color='red', linestyle='--', alpha=0.5, label='TDC')
        ax2.axvline(x=self.theta_start, color='green', linestyle='--', alpha=0.5)
        ax2.set_xlabel('Crank Angle [degrees]', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Cumulative Heat Release [J]', fontsize=12, fontweight='bold')
        ax2.set_title('Cumulative Heat Release', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.legend(loc='best')
        ax3 = axes[2]
        ax3.plot(theta_plot, dQ_dtheta, 'r-', linewidth=2.5)
        ax3.axvline(x=360, color='red', linestyle='--', alpha=0.5, label='TDC')
        ax3.axvline(x=self.theta_start, color='green', linestyle='--', alpha=0.5)
        idx_peak = np.argmax(dQ_dtheta)
        theta_peak = theta_plot[idx_peak]
        ax3.plot(theta_peak, dQ_dtheta[idx_peak], 'ro', markersize=10,
                label=f'Peak @ {theta_peak:.1f}°')
        ax3.set_xlabel('Crank Angle [degrees]', fontsize=12, fontweight='bold')
        ax3.set_ylabel('Heat Release Rate [J/degree]', fontsize=12, fontweight='bold')
        ax3.set_title('Heat Release Rate (dQ/dθ)', fontsize=14, fontweight='bold')
        ax3.grid(True, alpha=0.3)
        ax3.legend(loc='best')
        param_text = (f'Wiebe Parameters:\n'
                     f'Start: {self.theta_start-360:.0f}° BTDC\n'
                     f'Duration: {self.duration:.0f}° CA\n'
                     f'a = {self.a:.1f}, m = {self.m:.1f}')
        ax1.text(0.02, 0.98, param_text,
                transform=ax1.transAxes, fontsize=10,
                verticalalignment='top', horizontalalignment='left',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"\n✓ Wiebe combustion plots saved to: {save_path}")
        plt.show()
    def print_info(self):
        print("\n" + "=" * 70)
        print("WIEBE COMBUSTION MODEL")
        print("=" * 70)
        print(f"\nIgnition Timing:")
        print(f"  Start of Combustion:         {self.theta_start:.1f}° CA ({self.theta_start-360:.1f}° BTDC)")
        print(f"  End of Combustion:           {self.theta_end:.1f}° CA ({self.theta_end-360:.1f}° ATDC)")
        print(f"  Combustion Duration:         {self.duration:.1f}° CA")
        print(f"\nWiebe Parameters:")
        print(f"  Efficiency parameter (a):    {self.a:.2f}")
        print(f"  Form factor (m):             {self.m:.2f}")
        theta_test = np.array([self.theta_start, 
                              self.theta_start + self.duration/2,
                              self.theta_end])
        xb_test = self.burned_mass_fraction(theta_test)
        print(f"\nBurned Mass Fraction:")
        print(f"  At start ({self.theta_start-360:.0f}° BTDC):     {xb_test[0]*100:.2f}%")
        print(f"  At mid-burn:                 {xb_test[1]*100:.2f}%")
        print(f"  At end ({self.theta_end-360:.0f}° ATDC):       {xb_test[2]*100:.2f}%")
        print("=" * 70)
if __name__ == "__main__":
    print("Creating Wiebe combustion model...")
    wiebe = WiebeCombustion(theta_start=-15, duration=50, a=5.0, m=2.0)
    wiebe.print_info()
    from thermodynamics import OttoCycle
    otto = OttoCycle()
    Q_total = otto.Qin
    print(f"\nUsing Q_total = {Q_total:.2f} J from Otto cycle")
    wiebe.plot_combustion(Q_total=Q_total, 
                         save_path='/Users/arda/Documents/ecyg/engine_cycle/wiebe_combustion.png')