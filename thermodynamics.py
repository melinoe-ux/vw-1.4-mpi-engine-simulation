import numpy as np
import matplotlib.pyplot as plt
from engine_parameters import *
class OttoCycle:
    def __init__(self, T1=None, P1=None, Qin=None, gamma=None):
        self.r = COMPRESSION_RATIO
        self.gamma = gamma if gamma is not None else GAMMA_AIR
        self.T1 = T1 if T1 is not None else T_AMBIENT
        self.P1 = P1 if P1 is not None else P_AMBIENT
        V1 = MAX_VOLUME / 1e6
        self.m = (self.P1 * V1) / (R_AIR * self.T1)
        if Qin is None:
            m_fuel = self.m / (AFR_STOICH + 1)
            self.Qin = m_fuel * LHV_FUEL * 1e6
        else:
            self.Qin = Qin
        self._calculate_states()
    def _calculate_states(self):
        self.T1_state = self.T1
        self.P1_state = self.P1
        self.V1 = MAX_VOLUME / 1e6
        self.T2 = self.T1 * (self.r ** (self.gamma - 1))
        self.P2 = self.P1 * (self.r ** self.gamma)
        self.V2 = MIN_VOLUME / 1e6
        Cv = CV_AIR
        self.T3 = self.T2 + self.Qin / (self.m * Cv)
        self.P3 = self.P2 * (self.T3 / self.T2)
        self.V3 = self.V2
        self.T4 = self.T3 / (self.r ** (self.gamma - 1))
        self.P4 = self.P3 / (self.r ** self.gamma)
        self.V4 = self.V1
        self._calculate_performance()
    def _calculate_performance(self):
        Cv = CV_AIR
        self.Q_in = self.m * Cv * (self.T3 - self.T2)
        self.Q_out = self.m * Cv * (self.T4 - self.T1)
        self.W_net = self.Q_in - self.Q_out
        self.eta_thermal = self.W_net / self.Q_in
        self.eta_theoretical = 1 - (1 / (self.r ** (self.gamma - 1)))
        V_d = (self.V1 - self.V2)
        self.MEP = self.W_net / V_d
        self.MEP_bar = self.MEP / 1e5
    def get_states(self):
        return {
            'State 1 (BDC, intake)': {
                'P': self.P1_state / 1e5,
                'V': self.V1 * 1e6,
                'T': self.T1_state
            },
            'State 2 (TDC, compressed)': {
                'P': self.P2 / 1e5,
                'V': self.V2 * 1e6,
                'T': self.T2
            },
            'State 3 (TDC, combusted)': {
                'P': self.P3 / 1e5,
                'V': self.V3 * 1e6,
                'T': self.T3
            },
            'State 4 (BDC, expanded)': {
                'P': self.P4 / 1e5,
                'V': self.V4 * 1e6,
                'T': self.T4
            }
        }
    def print_results(self):
        print("\n" + "=" * 70)
        print("IDEAL OTTO CYCLE ANALYSIS")
        print("=" * 70)
        print(f"\nCycle Parameters:")
        print(f"  Compression Ratio:           {self.r:.2f}")
        print(f"  Specific Heat Ratio (γ):     {self.gamma:.3f}")
        print(f"  Air Mass:                    {self.m*1000:.4f} g")
        print(f"  Heat Input:                  {self.Q_in:.2f} J")
        print(f"\nCycle States:")
        states = self.get_states()
        for state_name, values in states.items():
            print(f"\n  {state_name}:")
            print(f"    Pressure:    {values['P']:8.2f} bar")
            print(f"    Volume:      {values['V']:8.2f} cm³")
            print(f"    Temperature: {values['T']:8.2f} K ({values['T']-273.15:.1f}°C)")
        print(f"\nPerformance:")
        print(f"  Heat Input (Qin):            {self.Q_in:.2f} J")
        print(f"  Heat Rejected (Qout):        {self.Q_out:.2f} J")
        print(f"  Net Work:                    {self.W_net:.2f} J")
        print(f"  Thermal Efficiency:          {self.eta_thermal*100:.2f}%")
        print(f"  Theoretical Efficiency:      {self.eta_theoretical*100:.2f}%")
        print(f"  MEP:                         {self.MEP_bar:.2f} bar")
        print("=" * 70)
    def plot_pv_diagram(self, save_path=None):
        n_points = 100
        V_12 = np.linspace(self.V1, self.V2, n_points)
        P_12 = self.P1 * (self.V1 / V_12) ** self.gamma
        V_23 = np.array([self.V2, self.V3])
        P_23 = np.array([self.P2, self.P3])
        V_34 = np.linspace(self.V3, self.V4, n_points)
        P_34 = self.P3 * (self.V3 / V_34) ** self.gamma
        V_41 = np.array([self.V4, self.V1])
        P_41 = np.array([self.P4, self.P1_state])
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.plot(V_12 * 1e6, P_12 / 1e5, 'b-', linewidth=2.5, label='1→2 Compression')
        ax.plot(V_23 * 1e6, P_23 / 1e5, 'r-', linewidth=2.5, label='2→3 Heat Addition')
        ax.plot(V_34 * 1e6, P_34 / 1e5, 'g-', linewidth=2.5, label='3→4 Expansion')
        ax.plot(V_41 * 1e6, P_41 / 1e5, 'orange', linewidth=2.5, label='4→1 Heat Rejection')
        states_V = [self.V1, self.V2, self.V3, self.V4]
        states_P = [self.P1_state, self.P2, self.P3, self.P4]
        state_labels = ['1', '2', '3', '4']
        for i, (V, P, label) in enumerate(zip(states_V, states_P, state_labels)):
            ax.plot(V * 1e6, P / 1e5, 'ko', markersize=10)
            offset_x = 5 if i in [0, 3] else -15
            offset_y = 2 if i in [2] else -3
            ax.annotate(label, xy=(V * 1e6, P / 1e5), 
                       xytext=(offset_x, offset_y), textcoords='offset points',
                       fontsize=14, fontweight='bold',
                       bbox=dict(boxstyle='circle', facecolor='white', edgecolor='black'))
        ax.set_xlabel('Volume [cm³]', fontsize=12, fontweight='bold')
        ax.set_ylabel('Pressure [bar]', fontsize=12, fontweight='bold')
        ax.set_title(f'Ideal Otto Cycle P-V Diagram (r={self.r:.1f}, η={self.eta_thermal*100:.1f}%)',
                    fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best', fontsize=10)
        ax.text(0.98, 0.02, 
               f'Thermal Efficiency: {self.eta_thermal*100:.2f}%\nMEP: {self.MEP_bar:.2f} bar\nWork: {self.W_net:.1f} J',
               transform=ax.transAxes, fontsize=10,
               verticalalignment='bottom', horizontalalignment='right',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"\n✓ P-V diagram saved to: {save_path}")
        plt.show()
def verify_otto_cycle():
    print("\n" + "=" * 70)
    print("OTTO CYCLE VERIFICATION")
    print("=" * 70)
    otto = OttoCycle()
    eta_formula = 1 - (1 / (COMPRESSION_RATIO ** (GAMMA_AIR - 1)))
    print(f"\nTheoretical Efficiency Check:")
    print(f"  From formula η = 1 - 1/r^(γ-1):  {eta_formula*100:.3f}%")
    print(f"  From cycle calculation:          {otto.eta_theoretical*100:.3f}%")
    print(f"  Error:                           {abs(eta_formula - otto.eta_theoretical)*100:.5f}%")
    r_calc = otto.V1 / otto.V2
    print(f"\nCompression Ratio Check:")
    print(f"  Expected:                        {COMPRESSION_RATIO:.3f}")
    print(f"  Calculated (V1/V2):              {r_calc:.3f}")
    print(f"  Error:                           {abs(COMPRESSION_RATIO - r_calc):.5f}")
    ratio_P = otto.P2 / otto.P1_state
    ratio_expected = COMPRESSION_RATIO ** GAMMA_AIR
    print(f"\nIsentropic Compression Check (P2/P1 = r^γ):")
    print(f"  Expected:                        {ratio_expected:.3f}")
    print(f"  Calculated:                      {ratio_P:.3f}")
    print(f"  Error:                           {abs(ratio_expected - ratio_P):.5f}")
    print("=" * 70)
    return otto
if __name__ == "__main__":
    print_parameters()
    otto = verify_otto_cycle()
    otto.print_results()
    otto.plot_pv_diagram(save_path='/Users/arda/Documents/ecyg/engine_cycle/otto_pv_diagram.png')