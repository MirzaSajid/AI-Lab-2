# Lab 2 - Intelligent Agents & the PEAS Framework

**Student:** Sajid Hussain (BSAIM-046) | **Course:** CAI601400 - Artificial Intelligence | **Lab:** 2 (CLO1)

A smart-classroom energy agent (temperature + occupancy -> ECO / COOL / WARM / IDLE),
first as a reflex agent, then as a stateful agent that avoids repeating identical
commands. The report also gives PEAS specifications and environment classifications
for a delivery robot and an LLM-based student-support agent.

ECO / COOL / WARM / IDLE are **simulated mode labels; no hardware is controlled**.
All thresholds are **synthetic lab assumptions**.

## Setup
Python 3.8+ (tested on 3.12). Standard library only. No virtual environment needed.

```bash
python --version
```

## Run
```bash
python lab2_percepts.py   # reflex agent, 6-percept trace (manual Section 2.5)
python lab2_model.py      # stateful agent: previous mode + command/no-command trace
python lab2_check.py      # 16 automated checks, noisy-sensor edge case, hysteresis idea
```
`lab2_check.py` imports `lab2_model.py`, so keep them in the same folder. Its exit
code is 0 when all checks pass.

## Files
| File | Purpose |
|---|---|
| `lab2_percepts.py` | Reflex agent and percept trace (manual Section 2.5) |
| `lab2_model.py` | Stateful agent returning (target, send_command) |
| `lab2_check.py` | Checks, boundary tests, noisy 26 C edge case, hysteresis extension |
| `outputs/*.txt` | Captured outputs of the three scripts |
| `Lab2_Report.docx` | Full report: PEAS, classifications, traces, analysis, reflection |

## Reproducing the outputs
```bash
python lab2_percepts.py > outputs/percepts_output.txt
python lab2_model.py    > outputs/model_output.txt
python lab2_check.py    > outputs/check_output.txt
```

## Sources
`lab2_percepts.py` and the reflex policy are taken from the Lab 2 manual
(Sections 2.4-2.5). `lab2_model.py` and `lab2_check.py` are my own extensions.
Factual sources are listed in the References section of `Lab2_Report.docx`.
No credentials, private data or virtual environments are included.
