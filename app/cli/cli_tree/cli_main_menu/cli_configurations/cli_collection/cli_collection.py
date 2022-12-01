from app.cli.cli_components.menu import Menu
from app.cli.cli_components.selection import Selection
from app.cli.cli_tree.cli_main_menu.cli_configurations.cli_collection.information.cli_collection_information import \
    MenuCollectionInformation
from app.cli.cli_tree.cli_main_menu.cli_configurations.cli_collection.new.cli_collection_new import \
    MenuCollectionNew
from app.cli.enum.cli_options import CLIPaths
from app.configuration.dao.dao_collection import DaoCollection
from app.configuration.model.collection import Collection


class MenuCollection(Menu):
    def __init__(self, console, prompt: str = "Please select one of these command collections"):
        super().__init__(
            console=console,
            path=CLIPaths.COLLECTIONS.value
        )
        self.selection = None
        self.console = console
        self.selection_collection = None
        self.collections = {}
        self.collections.clear()
        self.prompt = prompt

    def _load_options(self):
        collections = DaoCollection().find_all_collections()
        if collections:
            for collection in collections:
                self._add_collection_to_selection(collection=collection)
        self._add_new_option()
        self._add_back_option()

    def _add_back_option(self):
        if self.collections:
            if max(self.collections) < 99:
                index = 99
            else:
                index = max(self.collections) + 1
        else:
            index = 99
        self.collections.setdefault(index, (CLIPaths.BACK, "value"))

    def _add_new_option(self):
        if self.collections:
            index = max(self.collections) + 1
        else:
            index = 1
        self.collections.setdefault(index, (MenuCollectionNew(console=self.console), "name"))

    def _add_collection_to_selection(self, collection: Collection) -> int:
        index = 1
        if self.collections:
            index = max(self.collections) + 1
        self.collections.setdefault(
            index,
            (MenuCollectionInformation(console=self.console, collection=collection), collection.name)
        )
        return index

    def _setup_collection_selection(self):
        self.selection_collection = Selection(prompt=self.prompt, console=self.console)
        self.selection_collection.register_and_show_options(self.collections)

    def start(self):
        self.reset_screen()
        self._load_options()
        self._setup_collection_selection()
        selection = self.selection_collection.start_selection()
        self.horizontal_spacer()
        self._decide_upon_selection(selected_option=selection)

    def _decide_upon_selection(self, selected_option):
        self.collections.clear()
        super()._decide_upon_selection(selected_option=selected_option)
