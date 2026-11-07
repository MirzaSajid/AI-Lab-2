"""Lab 2 - Task 3: stateful classroom agent that avoids repeated commands.

Keeps the SAME thresholds and occupancy priority as the reflex agent
(empty -> ECO; temp > 26 -> COOL; temp < 20 -> WARM; otherwise IDLE) and adds
one piece of internal state: the previous target mode. act() returns BOTH the
target mode and whether a command should be sent (True only when the target
differs from the previous mode).

Modes are simulated labels; no hardware is controlled. Thresholds are
synthetic lab assumptions. Remembering the previous mode is not learning from
data, and it does not by itself provide hysteresis (see lab2_check.py).
Run: python lab2_model.py
"""


class ClassroomAgent:
    """Reflex agent (Lab 2 manual, Section 2.4): percept -> target mode."""

    def act(self, temp, occupied):
        if not occupied:
            return "ECO"
        if temp > 26:
            return "COOL"
        if temp < 20:
            return "WARM"
        return "IDLE"


class StatefulClassroomAgent:
    """Same policy plus internal storage of the previous target mode."""

    def __init__(self):
        self.previous_mode = None  # nothing has been commanded yet
        self._policy = ClassroomAgent()

    def act(self, temp, occupied):
        target = self._policy.act(temp, occupied)
        send_command = target != self.previous_mode
        self.previous_mode = target
        return target, send_command


# Eight percepts covering: repeated percept, both exact boundaries (26 and 20),
# a mode transition, and an empty-room case.
PERCEPTS = [
    (29, True),   # 1 first cooling request
    (29, True),   # 2 repeated percept
    (26, True),   # 3 upper boundary (> 26 is false) and a transition
    (20, True),   # 4 lower boundary (< 20 is false), same mode as step 3
    (19, True),   # 5 just below the lower boundary
    (29, False),  # 6 empty room overrides a hot reading
    (29, False),  # 7 repeated empty-room percept
    (29, True),   # 8 transition from ECO back to COOL
]


def main():
    reflex = ClassroomAgent()
    agent = StatefulClassroomAgent()
    reflex_sent = 0
    stateful_sent = 0

    print("step | previous mode | percept | target | command")
    for step, percept in enumerate(PERCEPTS, 1):
        previous = agent.previous_mode
        target, send = agent.act(*percept)
        reflex.act(*percept)          # a reflex agent re-issues every step
        reflex_sent += 1
        stateful_sent += send
        print(step, previous, percept, target,
              "SEND" if send else "NO-COMMAND", sep=" | ")

    print()
    print(f"Reflex agent commands issued   : {reflex_sent} of {len(PERCEPTS)}")
    print(f"Stateful agent commands issued : {stateful_sent} of {len(PERCEPTS)}")
    print(f"Repeated commands avoided      : {reflex_sent - stateful_sent}")


if __name__ == "__main__":
    main()
