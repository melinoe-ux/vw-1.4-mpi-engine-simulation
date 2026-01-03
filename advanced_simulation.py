import numpy as np
import matplotlib.pyplot as plt
from engine_parameters import *
from geometry import cylinder_volume
from combustion import WiebeCombustion
from heat_transfer import WoschniHeatTransfer
from thermodynamics import OttoCycle
class AdvancedSimulation:
    def __init__(self, use_wiebe=True, use_heat_transfer=True,
                 theta_ignition=-15, combustion_duration=50):
        self.use_wiebe = use_wiebe
        self.use_heat_transfer = use_heat_transfer
        otto = OttoCycle()
        self.Qin = otto.Qin
        self.m = otto.m
        if use_wiebe:
            self.combustion = WiebeCombustion(theta_start=theta_ignition,
                                             duration=combustion_duration)
        if use_heat_transfer:
            self.heat_transfer = WoschniHeatTransfer(T_wall=400, C=130)
        self.theta = THETA_ARRAY
        self.n_steps = len(self.theta)
        self.P = np.zeros(self.n_steps)
        self.T = np.zeros(self.n_steps)
        self.V = np.zeros(self.n_steps)
        self._run_simulation()
    def _run_simulation(self):
        self.V = cylinder_volume(self.theta)
        P_intake = P_AMBIENT
        T_intake = T_AMBIENT
        idx_intake = (self.theta >= 0) & (self.theta <= 180)
        self.P[idx_intake] = P_intake
        self.T[idx_intake] = T_intake
        V_BDC = cylinder_volume(180)
        P_BDC = P_intake
        T_BDC = T_intake
        for i in range(self.n_steps):
            if self.theta[i] <= 180:
                continue
            elif self.theta[i] > 540:
                break
            if self.theta[i] <= 360:
                self.P[i] = P_BDC * (V_BDC / self.V[i]) ** GAMMA_AIR
                self.T[i] = T_BDC * (V_BDC / self.V[i]) ** (GAMMA_AIR - 1)
            else:
                P_prev = self.P[i-1]
                T_prev = self.T[i-1]
                V_prev = self.V[i-1]
                V_curr = self.V[i]
                dV = V_curr - V_prev
                if self.use_wiebe:
                    dQ_combustion = self.combustion.heat_release_rate(
                        self.theta[i], self.Qin) * DELTA_THETA
                else:
                    if abs(self.theta[i] - 360) < DELTA_THETA:
                        dQ_combustion = self.Qin
                    else:
                        dQ_combustion = 0
                if self.use_heat_transfer:
                    dQ_loss = self.heat_transfer.heat_loss_rate(
                        self.theta[i], P_prev, T_prev) * DELTA_THETA
                else:
                    dQ_loss = 0
                dQ_net = dQ_combustion - dQ_loss
                dT = (dQ_net - P_prev * dV) / (self.m * CV_AIR)
                T_curr = T_prev + dT
                P_curr = (self.m * R_AIR * T_curr) / V_curr
                self.P[i] = P_curr
                self.T[i] = T_curr
        if not self.use_wiebe:
            idx_tdc = np.argmin(np.abs(self.theta - 360))
            T_before = self.T[idx_tdc]
            T_after = T_before + self.Qin / (self.m * CV_AIR)
            self.T[idx_tdc] = T_after
            self.P[idx_tdc] = (self.m * R_AIR * T_after) / self.V[idx_tdc]
        idx_exhaust = (self.theta > 540) & (self.theta <= 720)
        self.P[idx_exhaust] = P_intake
        T_EVO = self.T[np.argmin(np.abs(self.theta - 540))]
        self.T[idx_exhaust] = T_EVO
        self._calculate_performance()
    def _calculate_performance(self):
        idx_comp = (self.theta >= 180) & (self.theta <= 360)
        idx_exp = (self.theta >= 360) & (self.theta <= 540)
        W_comp = np.trapezoid(self.P[idx_comp], self.V[idx_comp])
        W_exp = np.trapezoid(self.P[idx_exp], self.V[idx_exp])
        self.W_indicated = W_exp + W_comp
        V_d = (MAX_VOLUME - MIN_VOLUME) / 1e6
        self.IMEP = self.W_indicated / V_d
        self.IMEP_bar = self.IMEP / 1e5
        self.P_indicated = self.W_indicated * ENGINE_SPEED / (2 * 60)
        self.P_indicated_kW = self.P_indicated / 1000
        self.P_total = self.P_indicated * NUM_CYLINDERS
        self.P_total_kW = self.P_total / 1000
        self.eta_indicated = self.W_indicated / self.Qin
    def print_results(self):
        print("\n" + "=" * 70)
        print("ADVANCED SIMULATION RESULTS")
        print("=" * 70)
        print(f"\nConfiguration:")
        print(f"  Wiebe Combustion:            {'Enabled' if self.use_wiebe else 'Disabled'}")
        print(f"  Heat Transfer:               {'Enabled' if self.use_heat_transfer else 'Disabled'}")
        if self.use_wiebe:
            print(f"  Ignition Timing:             {self.combustion.theta_start-360:.0f}° BTDC")
            print(f"  Combustion Duration:         {self.combustion.duration:.0f}° CA")
        print(f"\nPeak Values:")
        print(f"  Peak Pressure:               {np.max(self.P)/1e5:.2f} bar @ {self.theta[np.argmax(self.P)]:.1f}°")
        print(f"  Peak Temperature:            {np.max(self.T):.2f} K")
        print(f"\nPerformance:")
        print(f"  Indicated Work:              {self.W_indicated:.2f} J")
        print(f"  IMEP:                        {self.IMEP_bar:.2f} bar")
        print(f"  Total Power:                 {self.P_total_kW:.2f} kW ({self.P_total_kW*1.341:.2f} hp)")
        print(f"  Indicated Efficiency:        {self.eta_indicated*100:.2f}%")
        print("=" * 70)
if __name__ == "__main__":
    from simulation import CrankAngleSimulation
    from plots import plot_comparison, print_performance_summary
    print("=" * 70)
    print("VW 1.4 MPI ENGINE CYCLE SIMULATION")
    print("Complete Analysis with All Models")
    print("=" * 70)
    print("\n[1/3] Running ideal simulation...")
    sim_ideal = CrankAngleSimulation()
    print("\n[2/3] Running advanced simulation (Wiebe + Heat Transfer)...")
    sim_advanced = AdvancedSimulation(use_wiebe=True, use_heat_transfer=True)
    print("\n[3/3] Generating results...")
    sim_advanced.print_results()
    print_performance_summary(sim_ideal, sim_advanced)
    plot_comparison(sim_ideal, sim_advanced,
                   save_path='/Users/arda/Documents/ecyg/engine_cycle/final_comparison.png')
    print("\n" + "=" * 70)
    print("SIMULATION COMPLETE!")
    print("=" * 70)
    print("\nGenerated files:")
    print("  - geometry_plots.png")
    print("  - otto_pv_diagram.png")
    print("  - crank_angle_simulation.png")
    print("  - wiebe_combustion.png")
    print("  - final_comparison.png")
    print("=" * 70)