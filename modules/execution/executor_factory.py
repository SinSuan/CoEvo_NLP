from modules.execution.blocks.preparers import PreparerCreatePopulationContr, PreparerExperiment, PreparerExperiment2, PreparerExperiment3, PreparerExperiment4, PreparerInitialPopulation

def run(self):
    """ run the experiment
    """
    print(f"{self.num_experiment=}")
    for idx_experiment in range(self.num_experiment):
        # framework = self.prepare(idx_experiment)
        # framework.run()
        print(f"{idx_experiment=}")
        ttl_framework = self.prepare(idx_experiment)
        for framework in ttl_framework:
            try:
                framework.run()
            except Exception as e:
                print("in executor_factory.py/run")
                print(f"error in {framework.folder_experiment=}")
                raise e

class ExcutorExperiment(PreparerExperiment):
    run = run

class ExcutorExperiment2(PreparerExperiment2):
    run = run


class ExcutorExperiment3(PreparerExperiment3):
    run = run

class ExcutorExperiment4(PreparerExperiment4):
    run = run


class ExecutorCreatePopulationContr(PreparerCreatePopulationContr):
    run = run

class ExecutorInitialPopulation(PreparerInitialPopulation):
    run = run
