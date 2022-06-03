## This dynamic loader looks for module that are inside the given 'root'
import importlib
import os


class ModuleNotFound(BaseException):
    def __init__(self, module_name: str, root_name: str):
        super().__init__("Failed to find module {0} under {1}".format(module_name, root_name))


class DynamicLoader(object):

    def __build_folder_tree(self, path: str):
        files = os.listdir(path)
        for file in files:
            if file == ".." or file == ".":
                continue
            file_path = os.path.join(path, file)
            if os.path.isfile(file_path) and file_path.endswith(".py"):
                module_name = file.removesuffix(".py")
                module_path = (self.parent_module + ((path + "/" + module_name).removeprefix(self.root))).replace("/",
                                                                                                                  ".")
                present = self.module_list.get(file)
                if present is not None:
                    raise Exception("Duplicate Module Name found under {0} ({1})".format(self.root, file))
                self.module_list[module_name] = module_path
            if os.path.isdir(file_path):
                self.__build_folder_tree(file_path)

    def __init__(self, root: str):
        self.root = root
        # map module_name to path
        self.parent_module = root.split("/")[-1]
        self.module_list: dict[str, str] = {}
        self.__build_folder_tree(root)

    def load(self, module_name: str, class_name: str):
        kmodule = self.module_list.get(module_name)
        kmodule = importlib.import_module(kmodule)
        if kmodule is None:
            raise ModuleNotFound(module_name=module_name, root_name=self.root)
        return getattr(kmodule, class_name)
