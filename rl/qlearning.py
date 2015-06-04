from sim import Sim
from configs import config
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Q-learning  exercise")
    parser.add_argument("-e","--episodes", help = "Number of episodes to be executed"       , dest = "episodes"      , default = config.episodes)
    parser.add_argument("-s","--steps"   , help = "Maximum numbef of steps for each episode", dest = "steps"         , default = config.maxsteps)
    parser.add_argument("-stop-success"  , help = "Stops if end is reached"                 , dest = "stop_success"  , action = "store_true")
    parser.add_argument("-stop-best"     , help = "Stops if best path is found"             , dest = "stop_best"     , action = "store_true")
    parser.add_argument("-p", "-policy"  , help = "Defined policy from " + str(config.valid_policies), dest = "policy"        , default = config.policy)
    parser.add_argument("-episilon"      , help = "Episilon for e-greedy policy"            , dest = "episilon"      , default = config.episilon)
    args = parser.parse_args()
    config.maxsteps = int(args.steps)
    config.stop_best = args.stop_best
    config.stop_success = args.stop_success
    if args.policy not in config.valid_policies:
        print "Invalid policy"
        sys.exit(0)
    config.policy = args.policy
    config.episodes = int(args.episodes)
    config.episilon = float(args.episilon)
    sim = Sim()
    sim.runEpisode(config.episodes)


