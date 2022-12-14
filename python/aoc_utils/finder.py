from dataclasses import dataclass
from importlib import util
from pathlib import Path
from types import ModuleType
from typing import List


@dataclass
class Day:
    day_number: int
    module: ModuleType
    solution_input: str | None
    example_input: str
    example_answers: List[str]


def get_days() -> List[Day]:
    days: List[Day] = []
    project_path = Path(__file__).resolve().parent.parent
    solutions_path = project_path / "solutions"
    examples_path = project_path / "examples"
    inputs = project_path / "inputs"
    for py_file in solutions_path.glob("*.py"):
        day_number = py_file.name[-5:-3]
        if not day_number.isnumeric():
            continue
        spec = util.spec_from_file_location("", py_file)
        if not spec:
            raise Exception(f"Unable to load module {py_file}")
        module = util.module_from_spec(spec)
        if not spec.loader:
            raise Exception(f"Unable to load module {py_file}")
        spec.loader.exec_module(module)

        example_input = (examples_path / f"{day_number}.txt").read_text()
        answers_text = (examples_path / f"{day_number}_answer.txt").read_text()
        example_answers = answers_text.splitlines()
        if len(example_answers) > 2:
            example_answers = answers_text.split("\n\n")
        solution_input = None
        solution_path = inputs / f"{day_number}.txt"
        if solution_path.exists():
            solution_input = solution_path.read_text()

        days.append(
            Day(int(day_number), module, solution_input, example_input, example_answers)
        )
    return sorted(days, key=lambda x: x.day_number)
