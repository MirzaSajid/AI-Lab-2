"""Lab 2 - Section 2.5: reflex classroom agent, percept and action trace.

ECO / COOL / WARM / IDLE are simulated operating-mode labels; no hardware is
controlled. temp is in degrees Celsius, occupied is a Boolean. An empty room
has priority over temperature. At exactly 20 C or 26 C an occupied room is IDLE
because the comparisons use < and >.
Source: Lab 2 manual, Section 2.5 (CAI601400 AI Lab Manual).
Run: python lab2_percepts.py
"""


class ClassroomAgent:
    def act(self, temp, occupied):
        if not occupied:
            return "ECO"
        if temp > 26:
            return "COOL"
        if temp < 20:
            return "WARM"
        return "IDLE"


agent = ClassroomAgent()
percepts = [(29, True), (29, True), (20, True),
            (26, True), (19, True), (29, False)]
for step, percept in enumerate(percepts, 1):
    print(step, percept, "target mode", agent.act(*percept))
