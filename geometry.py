import numpy as np
import matplotlib.pyplot as plt
from engine_parameters import *
def piston_position(theta_deg):
    theta_rad = np.deg2rad(theta_deg)
    r = CRANK_RADIUS_M
    L = CONNECTING_ROD_LENGTH_M
    cos_theta = np.cos(theta_rad)
    sin_theta = np.sin(theta_rad)
    s = r * cos_theta + np.sqrt(L**2 - (r * sin_theta)**2)
    x = (L + r) - s
    return x
def cylinder_volume(theta_deg):
    x = piston_position(theta_deg)
    Vc = CLEARANCE_VOLUME / 1e6
    A = np.pi * (BORE_M ** 2) / 4.0
    V = Vc + A * x
    return V
def cylinder_volume_cm3(theta_deg):
    return cylinder_volume(theta_deg) * 1e6
def verify_geometry():
    print("\n" + "=" * 70)
    print("GEOMETRY VERIFICATION")
    print("=" * 70)
    V_TDC = cylinder_volume_cm3(0)
    print(f"\nVolume at TDC (θ=0°):        {V_TDC:.2f} cm³")
    print(f"Expected (clearance vol):    {CLEARANCE_VOLUME:.2f} cm³")
    print(f"Error:                       {abs(V_TDC - CLEARANCE_VOLUME):.4f} cm³")
    V_BDC = cylinder_volume_cm3(180)
    print(f"\nVolume at BDC (θ=180°):      {V_BDC:.2f} cm³")
    print(f"Expected (max volume):       {MAX_VOLUME:.2f} cm³")
    print(f"Error:                       {abs(V_BDC - MAX_VOLUME):.4f} cm³")
    V_displacement = V_BDC - V_TDC
    print(f"\nDisplacement (BDC - TDC):    {V_displacement:.2f} cm³")
    print(f"Expected:                    {DISPLACEMENT_VOLUME:.2f} cm³")
    print(f"Error:                       {abs(V_displacement - DISPLACEMENT_VOLUME):.4f} cm³")
    r_calculated = V_BDC / V_TDC
    print(f"\nCompression ratio (Vmax/Vmin): {r_calculated:.3f}")
    print(f"Expected:                      {COMPRESSION_RATIO:.3f}")
    print(f"Error:                         {abs(r_calculated - COMPRESSION_RATIO):.4f}")
    x_TDC = piston_position(0) * 1000
    x_BDC = piston_position(180) * 1000
    piston_travel = x_BDC - x_TDC
    print(f"\nPiston position at TDC:      {x_TDC:.3f} mm")
    print(f"Piston position at BDC:      {x_BDC:.3f} mm")
    print(f"Piston travel:               {piston_travel:.3f} mm")
    print(f"Expected (stroke):           {STROKE:.3f} mm")
    print(f"Error:                       {abs(piston_travel - STROKE):.4f} mm")
    print("=" * 70)
    tolerance = 0.1
    checks = [
        abs(V_TDC - CLEARANCE_VOLUME) < tolerance,
        abs(V_BDC - MAX_VOLUME) < tolerance,
        abs(V_displacement - DISPLACEMENT_VOLUME) < tolerance,
        abs(r_calculated - COMPRESSION_RATIO) < 0.01,
        abs(piston_travel - STROKE) < tolerance
    ]
    if all(checks):
        print("\n✓ All geometry checks PASSED!")
    else:
        print("\n✗ Some geometry checks FAILED!")
    return all(checks)
def plot_geometry():
    theta = THETA_ARRAY
    x_pos = piston_position(theta) * 1000
    V = cylinder_volume_cm3(theta)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    ax1.plot(theta, x_pos, 'b-', linewidth=2, label='Piston Position')
    ax1.axhline(y=piston_position(0)*1000, color='r', linestyle='--', 
                alpha=0.5, label='TDC')
    ax1.axhline(y=piston_position(180)*1000, color='g', linestyle='--', 
                alpha=0.5, label='BDC')
    ax1.axvline(x=0, color='gray', linestyle=':', alpha=0.3)
    ax1.axvline(x=180, color='gray', linestyle=':', alpha=0.3)
    ax1.axvline(x=360, color='gray', linestyle=':', alpha=0.3)
    ax1.axvline(x=540, color='gray', linestyle=':', alpha=0.3)
    ax1.axvline(x=720, color='gray', linestyle=':', alpha=0.3)
    ax1.set_xlabel('Crank Angle [degrees]', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Piston Position from TDC [mm]', fontsize=12, fontweight='bold')
    ax1.set_title('VW 1.4 MPI - Piston Position vs. Crank Angle', 
                  fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='best')
    ax1.set_xlim([0, 720])
    ax1.text(90, piston_position(0)*1000 + STROKE/2, f'Stroke = {STROKE:.1f} mm',
             ha='center', va='center', fontsize=10, 
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    ax2.plot(theta, V, 'r-', linewidth=2, label='Cylinder Volume')
    ax2.axhline(y=CLEARANCE_VOLUME, color='b', linestyle='--', 
                alpha=0.5, label=f'Vc = {CLEARANCE_VOLUME:.1f} cm³')
    ax2.axhline(y=MAX_VOLUME, color='g', linestyle='--', 
                alpha=0.5, label=f'Vmax = {MAX_VOLUME:.1f} cm³')
    ax2.axvline(x=0, color='gray', linestyle=':', alpha=0.3)
    ax2.axvline(x=180, color='gray', linestyle=':', alpha=0.3)
    ax2.axvline(x=360, color='gray', linestyle=':', alpha=0.3)
    ax2.axvline(x=540, color='gray', linestyle=':', alpha=0.3)
    ax2.axvline(x=720, color='gray', linestyle=':', alpha=0.3)
    ax2.set_xlabel('Crank Angle [degrees]', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Cylinder Volume [cm³]', fontsize=12, fontweight='bold')
    ax2.set_title('VW 1.4 MPI - Cylinder Volume V(θ)', 
                  fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc='best')
    ax2.set_xlim([0, 720])
    strokes = [
        (90, 'Intake\n(0-180°)'),
        (270, 'Compression\n(180-360°)'),
        (450, 'Power\n(360-540°)'),
        (630, 'Exhaust\n(540-720°)')
    ]
    for angle, label in strokes:
        ax2.text(angle, MAX_VOLUME * 1.05, label, ha='center', va='bottom',
                fontsize=9, style='italic', color='darkblue')
    plt.tight_layout()
    plt.savefig('/Users/arda/Documents/ecyg/engine_cycle/geometry_plots.png', 
                dpi=150, bbox_inches='tight')
    print("\n✓ Geometry plots saved to: engine_cycle/geometry_plots.png")
    plt.show()
if __name__ == "__main__":
    print_parameters()
    verify_geometry()
    plot_geometry()