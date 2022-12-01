from dataclasses import dataclass
from ipaddress import ip_address, IPv6Address, IPv4Address
from typing import Optional

from rich.panel import Panel


@dataclass
class Host:
    ipv4_address: str
    ipv6_address: str
    fqdn: str
    manufacturer_name: str
    group_names: list[str]
    address: str
    name: Optional[str] = None

    def __init__(self, manufacturer_name: str, ipv4_address: str = None,
                 ipv6_address: str = None, fqdn: str = None, name: str = None,
                 group_names: list[str] = None):
        self.check_if_address_information_is_provided(
            ipv4_address=ipv4_address,
            ipv6_address=ipv6_address,
            fqdn=fqdn
        )
        self.ipv4_address = ipv4_address if ipv4_address else None
        self.ipv6_address = ipv6_address if ipv6_address else None
        self.fqdn = fqdn if fqdn else None

        if self.fqdn:
            self.address = self.fqdn
        elif self.ipv6_address:
            self.address = self.ipv6_address
        elif self.ipv4_address:
            self.address = self.ipv4_address

        self.manufacturer_name = manufacturer_name
        self.group_names = group_names if group_names else []

        self.name = name if name else None
        if not name:
            self.name = f"host_{self._autofill_name()}"

    @staticmethod
    def validate_ipv4_address(ipv4_address: str) -> None:
        from app.inventory.dao import DaoHost
        hosts = DaoHost().get_all_hosts()
        for host in hosts:
            if host.ipv4_address == ipv4_address:
                raise Host.InvalidName(f"Bad ípv4 address. Already in use by host '{host.name}'!")
        try:
            if not ipv4_address:
                return
            ipv4_address = ip_address(address=ipv4_address)
            if ipv4_address.is_loopback:
                raise Host.InvalidIPv4Address("Bad IPv4 address. Loopback addresses are not allowed!")
            if not isinstance(ipv4_address, IPv4Address):
                raise Host.InvalidIPv4Address(f"Bad IPv4 address. "
                                              f"´{ipv4_address}' does not appear to be an IPv4 address!")
        except ValueError as exception:
            raise Host.InvalidIPv4Address(
                "Bad IPv4 address. %s" % str(exception).replace(" or IPv6", "")
            ) from exception

    @staticmethod
    def validate_ipv6_address(ipv6_address: str) -> None:
        from app.inventory.dao import DaoHost
        hosts = DaoHost().get_all_hosts()
        for host in hosts:
            if host.ipv6_address == ipv6_address:
                raise Host.InvalidName(f"Bad ípv6 address. Already in use by host '{host.name}'!")
        try:
            if not ipv6_address:
                return
            ipv6_address = ip_address(address=ipv6_address)
            if ipv6_address.is_loopback:
                raise Host.InvalidIPv6Address("Bad IPv6 address. Loopback addresses are not allowed!")
            if not isinstance(ipv6_address, IPv6Address):
                raise Host.InvalidIPv4Address(f"Bad IPv6 address. "
                                              f"´{ipv6_address}' does not appear to be an IPv6 address!")
        except ValueError as exception:
            raise Host.InvalidIPv6Address(
                "Bad IPv6 address. %s" % str(exception).replace("IPv4 or ", "")
            ) from exception

    @staticmethod
    def validate_name(name: str) -> None:
        try:
            if name:
                int(name)
                raise Host.InvalidName("Bad name. The name must not be a number!")
        except ValueError:
            pass
        from app.inventory.dao import DaoHost
        hosts = DaoHost().get_all_hosts()
        for host in hosts:
            if host.name.upper() == name.upper():
                raise Host.InvalidName("Bad name. Already in use!")

    @staticmethod
    def validate_fqdn(fqdn: str):
        from app.inventory.dao import DaoHost
        hosts = DaoHost().get_all_hosts()
        for host in hosts:
            if host.fqdn:
                if host.fqdn.lower() == fqdn.lower():
                    raise Host.InvalidFQDN(f"Bad fqdn. Already in use by host '{host.name}'!")

    @staticmethod
    def is_valid_address_information(console, ipv4_address: str, ipv6_address: str, fqdn: str):
        try:
            Host.check_if_address_information_is_provided(
                ipv4_address=ipv4_address,
                ipv6_address=ipv6_address,
                fqdn=fqdn
            )
            return True
        except Host.NoAddressException:
            console.print(
                Panel("The entered information is invalid. Couldn't find any address information. "
                      "You must at least specify one address for adding a new host.",
                      title="Process aborted!"),
                style="red")
            return False

    @staticmethod
    def check_if_address_information_is_provided(ipv4_address: str, ipv6_address: str, fqdn: str) -> None:
        try:
            if str(ipv4_address).strip():
                return
            if str(ipv6_address).strip():
                return
            if str(fqdn).strip():
                return
        except AttributeError:
            pass
        raise Host.NoAddressException

    def _autofill_name(self):
        if self.fqdn:
            return self.fqdn
        elif self.ipv4_address:
            return self.ipv4_address
        elif self.ipv6_address:
            return self.ipv6_address

    class NoAddressException(Exception):
        pass

    class InvalidIPv4Address(Exception):
        def __init__(self, message):
            self.message = message

    class InvalidIPv6Address(Exception):
        def __init__(self, message):
            self.message = message

    class InvalidName(Exception):
        def __init__(self, message):
            self.message = message

    class InvalidFQDN(Exception):
        def __init__(self, message):
            self.message = message

    def __str__(self):
        return f"<Host> ipv4_address={self.ipv6_address}, ipv6_address={self.ipv6_address}," \
               f" fqdn={self.fqdn}, manufacturer_name={self.manufacturer_name}," \
               f" group_names={self.group_names}"

    def __hash__(self):
        return hash(str(self.name))

    def __eq__(self, other):
        if not isinstance(other, Host):
            return self.name == other
        return self.name == other.name
