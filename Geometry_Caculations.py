import numpy as np

# Constants for engine in general
m = 270 # mass of propellant (kg) 
r = 0.3 # Radius of tank (m)
m_NO2 = 270*3.5/4.5
m_IPA = 270/4.5
density_NO2 = 975.2
density_IPA = 788.25
NO2_Volume = m_NO2/density_NO2
IPA_Volume = m_IPA/density_IPA
Ullage_fraction = 0.1
Total_OxFuel_Volume = (NO2_Volume + IPA_Volume)*(1 + Ullage_fraction)


# Constants for pressurisation calculation
propellant_pressure = 25e5
pressurant_initial_pressure = 50e5
R = 2079
Rn = 189
T_0 = 298

def get_pressurant_details():
    # We're making the assumption that we're using Helium and that the expansion is isothermal
    # Using PV = constant
    V_0 = Total_OxFuel_Volume*propellant_pressure/(pressurant_initial_pressure - propellant_pressure)
    m_pressurant = (pressurant_initial_pressure*V_0)/(R*T_0)
    return [V_0, m_pressurant]

# Length Calculations
pressurant_volume, m_He = get_pressurant_details()
total_volume = (pressurant_volume + Total_OxFuel_Volume)*1.15 # 1.15 is a fudge factor for increase in volume due to connectors and etc
Area_cylinder = (np.pi*(r**2))
Length = total_volume/Area_cylinder
IPA_Length = IPA_Volume/Area_cylinder
NO2_Length = NO2_Volume/Area_cylinder
pressurant_length = pressurant_volume/Area_cylinder
total_pressfuel_mass = m_NO2 + m_IPA + m_He
White_Giant_length = 0.9
White_Giant_mass = 3
Total_Length = Length + White_Giant_length

#COM Calculations
White_Giant_COM = White_Giant_length/2
IPA_COM = White_Giant_length + IPA_Length/2
NO2_COM = White_Giant_length + IPA_Length + NO2_Length/2
pressurant_COM = White_Giant_length + IPA_Length + NO2_Length + pressurant_length/2
COM  = (White_Giant_COM*White_Giant_mass + IPA_COM*m_IPA + NO2_COM*m_NO2 + pressurant_COM*m_He)/(total_pressfuel_mass + White_Giant_mass)

print(f"Length is {Total_Length} m.")
print(f"Lengths IPA : {IPA_Length}, NO2: {NO2_Length}, Pressurant: {pressurant_length}")
print(f"Masses IPA: {m_IPA}, NO2: {m_NO2}, Pressurant: {m_He}")
print(f"Center of mass is {COM} m from the bottom of the rocket")
print(f"This is  {COM/Total_Length} of the way up the rocket.")

## Carbon Fibre Parameters
density_CF = 1750 # kg/m3
Yield_strength_CF = 2500e6 # in Pa
E_CF = 183e9

# Modelling Parameters
Thrust = 10e3 # in N
Bending_Force_Fins = 80e3 # in N

#Assuming encastre at joining
#Analyse Axial load
t = 0.002 # Tank Thickness
CrossArea = 2*np.pi*r*t
I = np.pi*(r**3)*t

#Stress and deflection Calculation
Axial_stress = Thrust/(CrossArea)
Bending_Moment = Bending_Force_Fins*Total_Length
Bending_stress = Bending_Moment*r/I
deflection = Bending_Force_Fins*(Total_Length**3)/(3*E_CF*I)

#Approximate Mass Calculation
tank_mass = (CrossArea*(Total_Length) + Area_cylinder*4*t)*density_CF # Assuming 4 plates separate the tanks from one another and that their thickness is the same
total_mass = total_pressfuel_mass + White_Giant_mass + tank_mass

print(f"Thickness: {t}m")
print(f"Axial stress: {Axial_stress} Pa")
print(f"Bending_stress: {Bending_stress} Pa")
print(f"Yield Strength: {Yield_strength_CF} Pa")
print(f"Is Yield Strength greater than Axial and Bending Stress: {Yield_strength_CF> Axial_stress and Yield_strength_CF > Bending_stress}")
print(f"Deflection: {deflection} m")
print(f"Approximate tank mass: {tank_mass} kg")
print(f"Approximate Panthera mass: {total_mass} kg")