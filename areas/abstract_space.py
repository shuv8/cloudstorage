# from directory_manager import DirectoryManager

class DirectoryManager:
    ...


class AbstractSpace:

    def provide_main_directory(self) -> DirectoryManager:
        return DirectoryManager()
