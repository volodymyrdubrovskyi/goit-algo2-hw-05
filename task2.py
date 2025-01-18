import timeit
from hyperloglog import HyperLogLog

# Читання даних із файлу
def load_log_file(file_path):
    """Читає лог-файл з кодуванням utf-8 та повертає список записів."""
    with open(file_path, 'r', encoding='utf-8') as file:
        log_entries = file.readlines()
    return log_entries

# Метод для точного підрахунку унікальних записів
def count_unique_exact(entries):
    """Реалізує точний підрахунок унікальних записів за допомогою структури set."""
    unique_entries = set(entries)
    return len(unique_entries)

# Метод для наближеного підрахунку унікальних записів
def count_unique_approx(entries):
    """Реалізує наближений підрахунок унікальних записів за допомогою HyperLogLog."""
    hll = HyperLogLog(0.01)
    for entry in entries:
        hll.add(entry)
    return len(hll)

# Порівняння методів за часом виконання
def compare_methods(file_path):
    """Порівнює час виконання точного та наближеного методів підрахунку унікальних записів."""
    log_entries = load_log_file(file_path)
    exact_unique = count_unique_exact(log_entries)
    approx_unique = count_unique_approx(log_entries)

    exact_time = timeit.timeit(lambda: count_unique_exact(log_entries), number=10)
    approx_time = timeit.timeit(lambda: count_unique_approx(log_entries), number=10)

    print("Результати порівняння:")
    print("                       Точний підрахунок   HyperLogLog")
    print(f"Унікальні елементи            {exact_unique:.0f}            {approx_unique:.0f}")
    print(f"Час виконання (сек.)          {exact_time:.2f}              {approx_time:.2f}")
    
    return exact_unique, approx_unique, exact_time, approx_time

# Викличемо функцію для завантаження та проведення порівняння
file_path = 'lms-stage-access.log'
compare_methods(file_path)
