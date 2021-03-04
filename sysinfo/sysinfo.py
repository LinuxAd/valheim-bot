import psutil


class Info:
    def __init__(self, cpu: str, mem: float, per: float):
        self.cpu = cpu
        self.mem = mem
        self.per = per


class System:

    @staticmethod
    def get_cpu_load() -> str:
        return psutil.cpu_percent()

    @staticmethod
    def get_cpu_load_detailed() -> str:
        return psutil.cpu_times_percent()

    @staticmethod
    def get_stuff():
        return psutil.cpu_stats()

    @classmethod
    def get_memory(cls) -> float:
        mem = psutil.virtual_memory()
        return cls.__to_gb(mem.available)

    @staticmethod
    def get_part_usage(mount: str) -> float:
        disk = psutil.disk_usage(mount)
        return round(disk.percent, 1)

    @staticmethod
    def __to_gb(num: float) -> float:
        return round(num / 1024 / 1024 / 1024, 1)
