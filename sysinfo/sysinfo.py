import psutil


class Info:
    def __init__(self):
        self.cpu = System.get_cpu_load()
        self.mem = System.get_memory()
        self.mem_per = System.get_memory_percent()
        self.root = System.get_part_usage("/")
        self.steam = System.get_part_usage("/home/steam")


class System:

    @staticmethod
    def get_cpu_load() -> float:
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
    def get_memory_percent() -> float:
        mem = psutil.virtual_memory()
        return mem.percent

    @staticmethod
    def get_part_usage(mount: str) -> float:
        disk = psutil.disk_usage(mount)
        return round(disk.percent, 1)

    @staticmethod
    def __to_gb(num: float) -> float:
        return round(num / 1024 / 1024 / 1024, 1)
