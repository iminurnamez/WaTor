from . import prepare,tools
from .states import simulation, graph, setupscreen, intro

def main():
    controller = tools.Control(prepare.ORIGINAL_CAPTION)
    states = {"INTRO": intro.Intro(),
                   "SETUPSCREEN": setupscreen.SetupScreen(),
                   "SIMULATION": simulation.Sim(),
                   "GRAPH": graph.StatsGraph()}
    controller.setup_states(states, "INTRO")
    controller.main()
