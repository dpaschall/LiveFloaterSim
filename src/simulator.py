import os
import numpy as np
import pickle
import sympy as sp
from scipy.integrate import solve_ivp

# Paths
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
results_dir = os.path.join(base_dir, 'results')

# Load expressions
theta_dd, phi_dd, psi_dd = pickle.load(open(os.path.join(results_dir, 'eom_exprs.pkl'), 'rb'))

# lambdify
t = sp.symbols('t', real=True)
θ,ϕ,ψ = sp.symbols('theta phi psi', real=True)
θd,ϕd,ψd = sp.symbols('theta_dot phi_dot psi_dot', real=True)
I_s,mB_s,omega_s,gamma_s = sp.symbols('I mB omega gamma', positive=True, real=True)
f_th = sp.lambdify((t,θ,ϕ,ψ,θd,ϕd,ψd,I_s,mB_s,omega_s,gamma_s), theta_dd, 'numpy')
f_ph = sp.lambdify((t,θ,ϕ,ψ,θd,ϕd,ψd,I_s,mB_s,omega_s,gamma_s), phi_dd, 'numpy')
f_ps = sp.lambdify((t,θ,ϕ,ψ,θd,ϕd,ψd,I_s,mB_s,omega_s,gamma_s), psi_dd, 'numpy')

# Load config & IC
import json
config = json.load(open(os.path.join(base_dir, 'config.json')))
ic = np.load(os.path.join(base_dir, 'initial_conditions.npz'))
theta0, phi0, psi0 = ic['theta0'], ic['phi0'], ic['psi0']
omega0 = ic['omega_body0']

# EOM
def eom(tt, yy):
    th,ph,ps, th_d,ph_d,ps_d = yy
    return [
        th_d, ph_d, ps_d,
        f_th(tt, th,ph,ps, th_d,ph_d,ps_d,
             config['I'], config['mB'], config['omega'], config['gamma']),
        f_ph(tt, th,ph,ps, th_d,ph_d,ps_d,
             config['I'], config['mB'], config['omega'], config['gamma']),
        f_ps(tt, th,ph,ps, th_d,ph_d,ps_d,
             config['I'], config['mB'], config['omega'], config['gamma'])
    ]

# simulate
t_eval = np.linspace(0,1,20)
y0 = [theta0, phi0, psi0, 0.0, omega0, -omega0]
sol = solve_ivp(eom, [0,1], y0, t_eval=t_eval)

# save sim and axis
np.savetxt(os.path.join(results_dir,'sim_output.csv'),
           sol.y.T, delimiter=',', header='theta,phi,psi,theta_dot,phi_dot,psi_dot', comments='')
axis_vecs = []
for th,ph,ps in zip(sol.y[0], sol.y[1], sol.y[2]):
    Rz_phi = np.array([[np.cos(ph), -np.sin(ph),0],
                       [np.sin(ph),  np.cos(ph),0],
                       [0,0,1]])
    Rx_th = np.array([[1,0,0],
                      [0,np.cos(th),-np.sin(th)],
                      [0,np.sin(th), np.cos(th)]])
    Rz_ps = np.array([[np.cos(ps), -np.sin(ps),0],
                      [np.sin(ps),  np.cos(ps),0],
                      [0,0,1]])
    R = Rz_phi @ Rx_th @ Rz_ps
    axis_vecs.append(R @ np.array([0,0,1]))
axis_vecs = np.array(axis_vecs)
np.savez(os.path.join(results_dir,'axis_vecs.npz'), axis=axis_vecs)
