import numpy as np
BORE = 76.5
STROKE = 75.6
CONNECTING_ROD_LENGTH = 144.0
COMPRESSION_RATIO = 10.5
NUM_CYLINDERS = 4
CRANK_RADIUS = STROKE / 2.0
ROD_RATIO = CONNECTING_ROD_LENGTH / CRANK_RADIUS
BORE_M = BORE / 1000.0
STROKE_M = STROKE / 1000.0
CONNECTING_ROD_LENGTH_M = CONNECTING_ROD_LENGTH / 1000.0
CRANK_RADIUS_M = CRANK_RADIUS / 1000.0
DISPLACEMENT_VOLUME = (np.pi / 4) * (BORE ** 2) * STROKE / 1000.0
TOTAL_DISPLACEMENT = DISPLACEMENT_VOLUME * NUM_CYLINDERS
CLEARANCE_VOLUME = DISPLACEMENT_VOLUME / (COMPRESSION_RATIO - 1.0)
MAX_VOLUME = DISPLACEMENT_VOLUME + CLEARANCE_VOLUME
MIN_VOLUME = CLEARANCE_VOLUME
ENGINE_SPEED = 3000
OMEGA = ENGINE_SPEED * 2 * np.pi / 60.0
T_AMBIENT = 298.15
P_AMBIENT = 101325
R_AIR = 287.0
GAMMA_AIR = 1.4
CV_AIR = R_AIR / (GAMMA_AIR - 1.0)
CP_AIR = GAMMA_AIR * CV_AIR
R_PRODUCTS = 287.0
GAMMA_PRODUCTS = 1.3
CV_PRODUCTS = R_PRODUCTS / (GAMMA_PRODUCTS - 1.0)
CP_PRODUCTS = GAMMA_PRODUCTS * CV_PRODUCTS
LHV_FUEL = 44.0
AFR_STOICH = 14.7
EQUIVALENCE_RATIO = 1.0
AFR_ACTUAL = AFR_STOICH / EQUIVALENCE_RATIO
DELTA_THETA = 1.0
THETA_ARRAY = np.arange(0, 720 + DELTA_THETA, DELTA_THETA)
N_STEPS = len(THETA_ARRAY)
def print_parameters():
    print("=" * 70)
    print("VW 1.4 MPI ENGINE PARAMETERS")
    print("=" * 70)
    print("\nGEOMETRIC PARAMETERS:")
    print(f"  Bore (D):                    {BORE:.2f} mm")
    print(f"  Stroke (S):                  {STROKE:.2f} mm")
    print(f"  Connecting Rod Length (L):   {CONNECTING_ROD_LENGTH:.2f} mm")
    print(f"  Crank Radius (r):            {CRANK_RADIUS:.2f} mm")
    print(f"  Rod Ratio (L/r):             {ROD_RATIO:.3f}")
    print(f"  Compression Ratio:           {COMPRESSION_RATIO:.1f}:1")
    print(f"  Number of Cylinders:         {NUM_CYLINDERS}")
    print("\nVOLUMES:")
    print(f"  Displacement (per cyl):      {DISPLACEMENT_VOLUME:.2f} cm³")
    print(f"  Total Displacement:          {TOTAL_DISPLACEMENT:.2f} cm³ ({TOTAL_DISPLACEMENT/1000:.3f} L)")
    print(f"  Clearance Volume (per cyl):  {CLEARANCE_VOLUME:.2f} cm³")
    print(f"  Max Volume (BDC):            {MAX_VOLUME:.2f} cm³")
    print(f"  Min Volume (TDC):            {MIN_VOLUME:.2f} cm³")
    print(f"  Verification (Vmax/Vmin):    {MAX_VOLUME/MIN_VOLUME:.2f} (should be {COMPRESSION_RATIO:.1f})")
    print("\nOPERATING CONDITIONS:")
    print(f"  Engine Speed:                {ENGINE_SPEED} RPM")
    print(f"  Angular Velocity:            {OMEGA:.2f} rad/s")
    print(f"  Ambient Temperature:         {T_AMBIENT:.2f} K ({T_AMBIENT-273.15:.1f}°C)")
    print(f"  Ambient Pressure:            {P_AMBIENT/1000:.2f} kPa")
    print("\nGAS PROPERTIES:")
    print(f"  R (air):                     {R_AIR:.1f} J/(kg·K)")
    print(f"  γ (air):                     {GAMMA_AIR:.2f}")
    print(f"  Cp (air):                    {CP_AIR:.1f} J/(kg·K)")
    print(f"  Cv (air):                    {CV_AIR:.1f} J/(kg·K)")
    print(f"  γ (products):                {GAMMA_PRODUCTS:.2f}")
    print("\nFUEL PROPERTIES:")
    print(f"  LHV (gasoline):              {LHV_FUEL:.1f} MJ/kg")
    print(f"  Stoichiometric AFR:          {AFR_STOICH:.1f}")
    print(f"  Equivalence Ratio:           {EQUIVALENCE_RATIO:.2f}")
    print("\nSIMULATION PARAMETERS:")
    print(f"  Crank Angle Resolution:      {DELTA_THETA:.1f}°")
    print(f"  Number of Steps:             {N_STEPS}")
    print("=" * 70)
if __name__ == "__main__":
    print_parameters()