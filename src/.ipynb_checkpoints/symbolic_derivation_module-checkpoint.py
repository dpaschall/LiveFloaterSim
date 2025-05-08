import sympy as sp
import os
import pickle

def run_symbolic_derivation(params, output_dir):
    sp.init_printing()
    t = sp.symbols('t', real=True)
    I, mB, omega, gamma = sp.symbols('I mB omega gamma', positive=True, real=True)
    theta, phi, psi = sp.symbols('theta phi psi', cls=sp.Function)
    th = theta(t); ph = phi(t); ps = psi(t)
    th_d = sp.diff(th, t); ph_d = sp.diff(ph, t); ps_d = sp.diff(ps, t)

    # Kinetic + potential
    T_rot = (I/2)*(th_d**2 + (ph_d*sp.sin(th))**2 + (ps_d + ph_d*sp.cos(th))**2)
    B_lab = sp.Matrix([
        mB*sp.cos(omega*t)*sp.cos(gamma),
        mB*sp.sin(omega*t)*sp.cos(gamma),
        mB*sp.sin(gamma)
    ])
    Rz_phi = sp.Matrix([[sp.cos(ph), -sp.sin(ph), 0],
                        [sp.sin(ph),  sp.cos(ph), 0],
                        [0,           0,          1]])
    Rx_th  = sp.Matrix([[1,0,0],
                        [0,sp.cos(th),-sp.sin(th)],
                        [0,sp.sin(th), sp.cos(th)]])
    Rz_ps  = sp.Matrix([[sp.cos(ps), -sp.sin(ps), 0],
                        [sp.sin(ps),  sp.cos(ps), 0],
                        [0,           0,          1]])
    R = Rz_phi @ Rx_th @ Rz_ps
    m_body = sp.Matrix([0,0,1])
    m_lab = R @ m_body
    U = -m_lab.dot(B_lab)
    L = T_rot - U

    coords = [th, ph, ps]
    derivs = [th_d, ph_d, ps_d]
    EL = [sp.simplify(sp.diff(sp.diff(L, qd), t) - sp.diff(L, q)) for q, qd in zip(coords, derivs)]

    th_dd = sp.diff(th, t, 2)
    ph_dd = sp.diff(ph, t, 2)
    ps_dd = sp.diff(ps, t, 2)
    theta_dd = sp.simplify(-(EL[0] - I*th_dd)/I)
    phi_dd = sp.solve(EL[1].subs(th_dd, theta_dd), ph_dd)[0]
    psi_dd = sp.solve(EL[2].subs({th_dd: theta_dd, ph_dd: phi_dd}), ps_dd)[0]
    phi_dd = phi_dd.subs(ps_dd, psi_dd)

    subs_map = {th:sp.symbols('theta'), ph:sp.symbols('phi'), ps:sp.symbols('psi'),
                th_d:sp.symbols('theta_dot'), ph_d:sp.symbols('phi_dot'), ps_d:sp.symbols('psi_dot')}
    theta_dd = theta_dd.xreplace(subs_map)
    phi_dd = phi_dd.xreplace(subs_map)
    psi_dd = psi_dd.xreplace(subs_map)

    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, 'eom_exprs.pkl'), 'wb') as f:
        pickle.dump((theta_dd, phi_dd, psi_dd), f)
    return theta_dd, phi_dd, psi_dd
