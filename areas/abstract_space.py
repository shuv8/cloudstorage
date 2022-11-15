class AbstractSpace:

    def provide_main_directory(self) -> DirectoryManager:
        return DirectoryManager()
