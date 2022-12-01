from app.cli.cli_components.menu import Menu
from app.cli.cli_components.selection import Selection
from app.cli.cli_tree.cli_main_menu.cli_nodes.cli_host.information.cli_host_information import MenuHostInformation
from app.cli.cli_tree.cli_main_menu.cli_nodes.cli_host.new.cli_host_new import MenuHostNew
from app.cli.enum.cli_options import CLIPaths
from app.inventory.dao import DaoHost
from app.inventory.model.host import Host


class MenuHost(Menu):
    def __init__(self, console, prompt="Please select a WLC (host)"):
        super().__init__(
            console=console,
            path=CLIPaths.HOST.value
        )
        self.selection_host = None
        self.hosts = {}
        self.hosts.clear()
        self.prompt = prompt

    def _load_options(self):
        hosts = DaoHost().get_all_hosts()
        if hosts:
            for host in hosts:
                self._add_host_selection(host=host)
        self._add_new_option()
        self._add_back_option()

    def _add_back_option(self):
        if self.hosts:
            if max(self.hosts) < 99:
                index = 99
            else:
                index = max(self.hosts) + 1
        else:
            index = 99
        self.hosts.setdefault(index, (CLIPaths.BACK, "value"))

    def _add_new_option(self):
        if self.hosts:
            index = max(self.hosts) + 1
        else:
            index = 1
        self.hosts.setdefault(index, (MenuHostNew(console=self.console), "name"))

    def _add_host_selection(self, host: Host) -> int:
        index = 1
        if self.hosts:
            index = max(self.hosts) + 1
        self.hosts.setdefault(
            index,
            (MenuHostInformation(console=self.console, host=host), host.name)
        )
        return index

    def _setup_host_selection(self):
        self.selection_host = Selection(prompt=self.prompt, console=self.console)
        self.selection_host.register_and_show_options(self.hosts)

    def start(self):
        self.reset_screen()
        self._load_options()
        self._setup_host_selection()
        selection = self.selection_host.start_selection()
        self.horizontal_spacer()
        self._decide_upon_selection(selected_option=selection)

    def _decide_upon_selection(self, selected_option):
        self.hosts.clear()
        super()._decide_upon_selection(selected_option=selected_option)
