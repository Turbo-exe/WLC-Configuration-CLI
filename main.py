import time
from os import getcwd
from os.path import exists, join
from sys import stdout, stdin

from rich.console import Console

from app.cli.cli_components.multiselection import MultiSelection
from app.cli.main_cli import CLI
from app.configuration.Database import Database, _check_if_db_exists, _create_database
from app.inventory.model.host import Host
from signal import signal, SIGINT

if __name__ == '__main__':
    if not _check_if_db_exists(path=Database.PATH):
        _create_database()
        print("Created database. Restart to start the software!")
        exit()
    CLI()

    # from netmiko import ConnectHandler
    # from getpass import getpass
    #
    # with ConnectHandler(host = 'dlw02tm98l.test.sub',
    #                     port = 22,
    #                     username = 'admin',
    #                     password = 'go4Wireless',
    #                     device_type = 'cisco_wlc_ssh') as ch:
    #     # ch.send_command("configure terminal")
    #     if not ch.check_enable_mode():
    #         ch.enable()
    #
    #     print("configure terminal")
    #     ch.send_command_timing("configure terminal", last_read=0)
    #     print("banner exec %")
    #     ch.send_command_timing("banner exec %", last_read=0)
    #     print("Test banner")
    #     ch.send_command_timing("Test banner", last_read=0)
    #     print("%")
    #     ch.send_command_timing("%", last_read=0)

        # ch.send_config_set("banner exec %")
        # ch.send_command("banner exec %")
        # ch.send_multiline(commands=["banner exec %", "Test banner 123", "%"])

    # from netmiko import ConnectHandler
    #
    # # Just pick an 'invalid' device_type
    # cisco1 = {
    #     "device_type": "invalid",
    #     "host": "cisco1.lasthop.io",
    #     "username": "pyclass",
    #     "password": "invalid"
    # }
    #
    # net_connect = ConnectHandler(**cisco1)
    # net_connect.disconnect()

    # import paramiko
    # import getpass
    
    # getLogger('paramiko.client').addHandler(NullHandler())
    
    # host = "dlw02tm98l.test.sub"
    # username = "a502060"
    # password = getpass.getpass(f"Password for {username}: ")
    # client = paramiko.client.SSHClient()
    # client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # client.connect(host, username=username, password=password)
    # stdin, stdout, stderr = client.exec_command("configure terminal")
    # stdin.write("ap dot11 5ghz shutdown")
    # stdin.channel.shutdown_write()
    
    # stdin, stdout, stderr = client.exec_command("configure terminal")
    
    # print(stdout.read().decode())
    
    # stdin.close()
    # stdout.close()
    # stderr.close()
    
    # client.close()


    # loop = True
    # while loop:
    #     selected_manufacturer = CliManufacturer().selection
    #     if selected_manufacturer[1] != "(configure manufacturers)":
    #         loop = False
    # rprint("Selection", selected_manufacturer)

    # console.log("Test")
    # inspect(Pipeline)
    # Panel.fit("[bold yellow]Hi, I'm a Panel", border_style="red")
    # for _ in track(range(20), description='[green]Processing data'):
    #     sleep(0.2)
    # error_console = Console(stderr=True, style="bold red")
    # error_console.log("Alarm!")
