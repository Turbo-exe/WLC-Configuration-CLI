from enum import Enum


class CLIOptions(Enum):
    BACK = "(back)"

    CLOSE = "(close)"
    MODIFY = "(modify)"
    REMOVE = "(remove)"
    NEW = "(new)"
    RENAME = "(rename)"

    MAIN_MENU = "Main Menu"

    NODES = "Nodes"
    CONFIGURATIONS = "Configurations"
    EXECUTION = "Execution"

    OVERVIEW = "Overview"
    MANUFACTURERS = "Manufacturers"
    GROUPS = "Groups"
    HOSTS = "Hosts"

    COMMANDS = "Commands"
    COLLECTIONS = "Collection"
    VARIABLES = "Variables"

    INFORMATION = "Information"


class CLIPaths(Enum):
    BACK = CLIOptions.BACK.value

    CLOSE = CLIOptions.CLOSE.value,

    MAIN_MENU = (CLIOptions.MAIN_MENU.value,)

    # NODES

    NODES = MAIN_MENU + (CLIOptions.NODES.value,)

    OVERVIEW = NODES + (CLIOptions.OVERVIEW.value,)

    MANUFACTURER = NODES + (CLIOptions.MANUFACTURERS.value,)
    MANUFACTURER_INFORMATION = MANUFACTURER + (CLIOptions.INFORMATION.value,)
    MANUFACTURER_NEW = MANUFACTURER + (CLIOptions.NEW.value,)
    MANUFACTURER_RENAME = MANUFACTURER_INFORMATION + (CLIOptions.RENAME.value,)
    MANUFACTURER_REMOVE = MANUFACTURER_INFORMATION + (CLIOptions.REMOVE.value,)

    GROUPS = NODES + (CLIOptions.GROUPS.value,)
    GROUPS_INFORMATION = GROUPS + (CLIOptions.INFORMATION.value,)
    GROUPS_NEW = GROUPS + (CLIOptions.NEW.value, )
    GROUPS_MODIFY = GROUPS + (CLIOptions.MODIFY.value,)
    GROUPS_REMOVE = GROUPS + (CLIOptions.REMOVE.value, )

    HOST = NODES + (CLIOptions.HOSTS.value,)
    HOST_INFORMATION = HOST + (CLIOptions.INFORMATION.value,)
    HOST_NEW = HOST_INFORMATION + (CLIOptions.NEW.value,)
    HOST_MODIFY = HOST_INFORMATION + (CLIOptions.MODIFY.value,)
    HOST_REMOVE = HOST_INFORMATION + (CLIOptions.REMOVE.value,)

    # CONFIGURATIONS

    CONFIGURATIONS = MAIN_MENU + (CLIOptions.CONFIGURATIONS.value,)

    COMMANDS = CONFIGURATIONS + (CLIOptions.COMMANDS.value,)
    COMMANDS_NEW = COMMANDS + (CLIOptions.NEW.value,)
    COMMANDS_INFORMATION = COMMANDS + (CLIOptions.INFORMATION.value,)
    COMMANDS_MODIFY = COMMANDS + (CLIOptions.MODIFY.value,)
    COMMANDS_REMOVE = COMMANDS + (CLIOptions.REMOVE.value,)

    COLLECTIONS = CONFIGURATIONS + (CLIOptions.COLLECTIONS.value,)
    COLLECTIONS_NEW = COLLECTIONS + (CLIOptions.NEW.value,)
    COLLECTIONS_INFORMATION = COLLECTIONS + (CLIOptions.INFORMATION.value,)
    COLLECTIONS_MODIFY = COLLECTIONS + (CLIOptions.MODIFY.value,)
    COLLECTIONS_REMOVE = COLLECTIONS + (CLIOptions.REMOVE.value,)

    VARIABLES = CONFIGURATIONS + (CLIOptions.VARIABLES.value,)
    VARIABLES_NEW = VARIABLES + (CLIOptions.NEW.value,)
    VARIABLES_MODIFY = VARIABLES + (CLIOptions.MODIFY.value,)
    VARIABLES_REMOVE = VARIABLES + (CLIOptions.REMOVE.value,)

    # EXECUTION

    EXECUTION = MAIN_MENU + (CLIOptions.EXECUTION.value,)
