import numpy as np

from libs.elements.SimParams import SimParams


def test_from_dict_and_to_dict():
    sim_params = SimParams(boundaries=np.array([[-5.0, -5.0, -3.0], [5.0, 5.0, 3.0]]),
                           t0=0.1,
                           t1=2.0,
                           samples=21,
                           maxh_global=3.0,
                           tol=1e-3,
                           maxit=1000)
    for key, value in SimParams.template().from_dict(sim_params.to_dict()).__dict__.items():
        if not np.allclose(value, sim_params.__dict__[key]):
            assert False

    assert True
