"""Lab 2 - automated checks, edge case and proposed improvement.

1. Checks that the stateful agent keeps the reflex agent's thresholds and
   occupancy priority, handles both exact boundaries, and suppresses repeats.
2. Edge case: a noisy temperature sequence around 26 C. Remembering the last
   mode does NOT stop chattering, because every reading flips the target.
3. Proposed improvement (EXTENSION, not required): a hysteresis band. The
   25 C release point is a synthetic lab assumption.

Exit code 0 if every check passes, 1 otherwise.
Run: python lab2_check.py
"""
import sys

from lab2_model import ClassroomAgent, StatefulClassroomAgent


class HysteresisAgent:
    """Stateful agent with a deadband: once cooling, keep cooling until
    temp <= COOL_OFF. Empty-room priority and the 20 C warm rule are kept."""

    COOL_ON = 26
    COOL_OFF = 25   # synthetic assumption
    WARM_ON = 20

    def __init__(self):
        self.previous_mode = None

    def act(self, temp, occupied):
        if not occupied:
            target = "ECO"
        elif self.previous_mode == "COOL" and temp > self.COOL_OFF:
            target = "COOL"
        elif temp > self.COOL_ON:
            target = "COOL"
        elif temp < self.WARM_ON:
            target = "WARM"
        else:
            target = "IDLE"
        send = target != self.previous_mode
        self.previous_mode = target
        return target, send


results = []


def check(name, condition):
    results.append(condition)
    print(f"{'PASS' if condition else 'FAIL'} | {name}")


def commands(agent, temps, occupied=True):
    modes, sends = [], 0
    for t in temps:
        mode, send = agent.act(t, occupied)
        modes.append(mode)
        sends += send
    return modes, sends


def main():
    print("== Part 1: correctness checks ==")
    reflex = ClassroomAgent()
    check("exact boundary 26 C occupied -> IDLE", reflex.act(26, True) == "IDLE")
    check("exact boundary 20 C occupied -> IDLE", reflex.act(20, True) == "IDLE")
    check("26.1 C occupied -> COOL", reflex.act(26.1, True) == "COOL")
    check("19.9 C occupied -> WARM", reflex.act(19.9, True) == "WARM")
    check("empty room beats hot reading -> ECO", reflex.act(35, False) == "ECO")
    check("empty room beats cold reading -> ECO", reflex.act(5, False) == "ECO")

    s = StatefulClassroomAgent()
    check("first percept always sends a command", s.act(29, True) == ("COOL", True))
    check("identical repeated percept sends no command", s.act(29, True) == ("COOL", False))
    check("mode transition sends a command", s.act(24, True) == ("IDLE", True))
    check("transition to empty room sends ECO", s.act(24, False) == ("ECO", True))

    same = True
    for occupied in (True, False):
        stateful = StatefulClassroomAgent()
        for tenth in range(-100, 451):          # -10.0 .. 45.0 C
            t = tenth / 10
            if stateful.act(t, occupied)[0] != reflex.act(t, occupied):
                same = False
    check("stateful targets equal reflex targets (sweep -10..45 C)", same)

    print()
    print("== Part 2: edge case - noisy readings around 26 C ==")
    noisy = [26.5, 25.5, 26.5, 25.5, 26.5]
    print("temperature sequence:", noisy)
    modes, sent = commands(StatefulClassroomAgent(), noisy)
    print("stateful modes      :", modes)
    print(f"stateful commands   : {sent} of {len(noisy)}")
    check("stateful agent still chatters (command every step)", sent == len(noisy))

    print()
    print("== Part 3: proposed improvement - hysteresis band (extension) ==")
    modes, sent = commands(HysteresisAgent(), noisy)
    print("hysteresis modes    :", modes)
    print(f"hysteresis commands : {sent} of {len(noisy)}")
    check("hysteresis agent sends one command for the noisy sequence", sent == 1)
    h = HysteresisAgent()
    check("hysteresis: cold start at 27 C still COOLs", h.act(27, True) == ("COOL", True))
    check("hysteresis: empty room still ECO", h.act(27, False) == ("ECO", True))
    check("hysteresis: releases cooling at 25 C", HysteresisAgent().act(25, True)[0] == "IDLE")

    passed = sum(results)
    print()
    print(f"{passed}/{len(results)} checks passed")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
