import numpy as np
import sys
import ase
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution, force_temperature
from ase.md.verlet import VelocityVerlet
from ase import units


from qmlearn.io.model import db2qmmodel
from qmlearn.api.api4ase import QMLCalculator

from ase.build import molecule
from sklearn.kernel_ridge import KernelRidge

models={'gamma2cum': KernelRidge(alpha=0.0,kernel='rbf'),
        'delta_gamma': KernelRidge(alpha=0.0,kernel='rbf')}

if __name__ == "__main__":
    #
    np.random.seed(8888)
    T = 300
    #
    dbfile = sys.argv[1]
    atoms = molecule('H2O')
    qmmodel = db2qmmodel(dbfile, names = '*', mmodels=models, target='delta_gamma', method='delta_gamma',purify_gamma=False)
    qmmodel2 = db2qmmodel(dbfile, names = '*', mmodels=models, target='gamma2cum', method='gamma2cum',purify_gamma=False)
    #
    atoms.calc = QMLCalculator(qmmodel = qmmodel, qmmodel2 = qmmodel2, method = 'gamma2cum', properties=('energy'))
    # atoms.calc = QMLCalculator(qmmodel = qmmodel.refqmmol, method = 'engine2', properties=('energy'))
    MaxwellBoltzmannDistribution(atoms, temperature_K = T, force_temp=True)
    p = atoms.get_momenta()
    c = p.sum(axis = 0)
    p -= c/len(atoms)
    atoms.set_momenta(p)
    force_temperature(atoms, T)

    dyn = VelocityVerlet(atoms, timestep=0.5*units.fs, trajectory='md_nve.traj', logfile='md_nve.log')
    dyn.run(20000)

