""" main function of this project
"""

import ray
from modules.execution.executor_factory import ExcutorExperiment, ExecutorCreatePopulationContr, ExecutorInitialPopulation

from modules.utils.get_config import get_config
CONFIG = get_config()
DEBUGGER = CONFIG["DEBUGGER"]["DEBUGGER"]


def initial_population():
    excutor = ExecutorInitialPopulation()
    excutor.run()

def create_population_contr():
    excutor = ExecutorCreatePopulationContr()
    excutor.run()

def experiment():
    excutor = ExcutorExperiment()
    excutor.run()

def main():
    initial_population()
    # create_population_contr()
    # experiment()

if __name__=="__main__":
    main()
    # ray.shutdown()
