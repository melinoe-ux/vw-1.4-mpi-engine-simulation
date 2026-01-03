import numpy as np
from engine_parameters import *
class WoschniHeatTransfer:
    def __init__(self, T_wall=400, C=130):
        self.T_wall = T_wall
        self.C = C
        self.D = BORE_M
        self.S = STROKE_M
        self.C_m = 2 * self.S * ENGINE_SPEED / 60.0
    def characteristic_velocity(self, theta, P, V, P_motored=None):
        w = 2.28 * self.C_m
        return w
    def heat_transfer_coefficient(self, P, T, w=None):
        if w is None:
            w = 2.28 * self.C_m
        P_bar = P / 1e5
        h = self.C * (self.D ** (-0.2)) * (P_bar ** 0.8) * \
            (T ** (-0.55)) * (w ** 0.8)
        return h
    def instantaneous_area(self, theta):
        from geometry import piston_position
        x = piston_position(theta)
        A_head = np.pi * (self.D ** 2) / 4.0
        A_piston = np.pi * (self.D ** 2) / 4.0
        A_cylinder = np.pi * self.D * x
        A_total = A_head + A_piston + A_cylinder
        return A_total
    def heat_loss_rate(self, theta, P, T, omega=None):
        if omega is None:
            omega = OMEGA
        h = self.heat_transfer_coefficient(P, T)
        A = self.instantaneous_area(theta)
        dQ_dt = h * A * (T - self.T_wall)
        dtheta_dt = omega * (180.0 / np.pi)
        dQ_dtheta = dQ_dt / dtheta_dt
        return dQ_dtheta
    def print_info(self):
        print("\n" + "=" * 70)
        print("WOSCHNI HEAT TRANSFER MODEL")
        print("=" * 70)
        print(f"\nWall Temperature:            {self.T_wall:.1f} K ({self.T_wall-273.15:.1f}°C)")
        print(f"Woschni Constant (C):        {self.C:.1f}")
        print(f"Bore Diameter:               {self.D*1000:.2f} mm")
        print(f"Mean Piston Speed:           {self.C_m:.2f} m/s")
        print(f"Characteristic Velocity:     {2.28*self.C_m:.2f} m/s")
        print("=" * 70)
if __name__ == "__main__":
    print("Creating Woschni heat transfer model...")
    ht = WoschniHeatTransfer(T_wall=400, C=130)
    ht.print_info()
    print("\nExample Heat Transfer Calculation:")
    print("-" * 70)
    P_peak = 166.63e5
    T_peak = 4669.67
    theta_peak = 360
    h = ht.heat_transfer_coefficient(P_peak, T_peak)
    A = ht.instantaneous_area(theta_peak)
    dQ_dtheta = ht.heat_loss_rate(theta_peak, P_peak, T_peak)
    print(f"At peak pressure (θ = {theta_peak}°):")
    print(f"  Pressure:                    {P_peak/1e5:.2f} bar")
    print(f"  Temperature:                 {T_peak:.2f} K")
    print(f"  Heat transfer coefficient:   {h:.2f} W/(m²·K)")
    print(f"  Heat transfer area:          {A*1e4:.2f} cm²")
    print(f"  Heat loss rate:              {dQ_dtheta:.4f} J/degree")
    print("-" * 70)