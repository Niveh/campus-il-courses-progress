
class Employee:
    def __init__(self, name, age, salary) -> None:
        self._name = name
        self._age = age
        self._salary = salary

    def get_name(self):
        return self._name


class EmployeeManager:
    def __init__(self) -> None:
        self._employee_list = []
        self.eml_index = -1

    def add_employee(self, new_empl):
        self._employee_list.append(new_empl)

    def __iter__(self):
        return self

    def __next__(self):
        if self.eml_index >= len(self._employee_list) - 1:
            raise StopIteration()

        self.eml_index += 1
        return self._employee_list[self.eml_index].get_name()


hr_manager = EmployeeManager()
hr_manager.add_employee(Employee("Lia Levi", 30, 20000))
hr_manager.add_employee(Employee("Yosef Cohen", 32, 4800))
hr_manager.add_employee(Employee("Oded Haim", 47, 5100))

for emp_name in hr_manager:
    print(emp_name)
