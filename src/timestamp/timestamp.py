import time
import struct
import math
from datetime import datetime, timezone
from typing import Tuple


class Timestamp:
    def __init__(self):
        self.seconds: int = 0
        self.nanoseconds: int = 0
        self.isotimestamp: str = ""
        self._update()

    def _update(self):
        now = time.time()
        self.seconds = int(now)
        self.nanoseconds = int((now - self.seconds) * 1_000_000_000)
        dt = datetime.fromtimestamp(self.seconds, tz=timezone.utc)
        self.isotimestamp = dt.strftime("%Y-%m-%dT%H:%M:%S")

    def to_unix_ms(self) -> int:
        return self.seconds * 1000 + self.nanoseconds // 1_000_000

    def to_iso8601(self) -> str:
        return f"{self.isotimestamp}.{self.nanoseconds:09d}Z"

    def __repr__(self):
        return self.to_iso8601()


class EncryptedNode:
    def __init__(self, node_id: str = "", mac: str = ""):
        self.node_id: bytes = node_id.encode("utf-8")[:16].ljust(16, b"\x00")
        self.mac_address: bytes = self._parse_mac(mac)
        self.radius: float = 1.0
        self.diameter: float = self.radius * 2.0
        self.volume: float = (4.0 / 3.0) * math.pi * (self.radius**3)
        self.timestamp: int = int(time.time())
        self.encrypted: bool = False

    def _parse_mac(self, mac: str) -> bytes:
        if not mac:
            return bytes(6)
        parts = mac.split(":")
        return bytes(int(p, 16) for p in parts[:6]).ljust(6, b"\x00")

    def set_radius(self, r: float):
        self.radius = r
        self.diameter = r * 2.0
        self.volume = (4.0 / 3.0) * math.pi * (r**3)

    def encrypt(self):
        self.node_id = bytes(b ^ 0xFF for b in self.node_id)
        self.mac_address = bytes(b ^ 0xFF for b in self.mac_address)
        self.encrypted = True

    def decrypt(self):
        self.node_id = bytes(b ^ 0xFF for b in self.node_id)
        self.mac_address = bytes(b ^ 0xFF for b in self.mac_address)
        self.encrypted = False

    def get_radius_bits(self) -> int:
        return struct.unpack(">Q", struct.pack(">d", self.radius))[0]

    def get_diameter_bits(self) -> int:
        return struct.unpack(">Q", struct.pack(">d", self.diameter))[0]

    def get_volume_bits(self) -> int:
        return struct.unpack(">Q", struct.pack(">d", self.volume))[0]

    def __repr__(self):
        return (
            f"EncryptedNode(id={self.node_id!r}, mac={self.mac_address.hex()}, "
            f"radius={self.radius:.17g}, diameter={self.diameter:.17g}, "
            f"volume={self.volume:.17g}, encrypted={self.encrypted})"
        )


if __name__ == "__main__":
    import math

    ts = Timestamp()
    print(f"Timestamp: {ts}")
    print(f"Unix ms: {ts.to_unix_ms()}")

    node = EncryptedNode("C2E4B97AF8951B", "e4:b9:7a:f8:95:1b")
    print(f"\n{node}")
    print(f"Radius bits: {node.get_radius_bits():016x}")
    print(f"Diameter bits: {node.get_diameter_bits():016x}")
    print(f"Volume bits: {node.get_volume_bits():016x}")

    node.set_radius(42.0)
    print(f"\nAfter set_radius(42.0):")
    print(f"Radius: {node.radius:.17g} (64-bit float)")
    print(f"Diameter: {node.diameter:.17g}")
    print(f"Volume: {node.volume:.17g}")

    node.encrypt()
    print(f"\nEncrypted: {node.encrypted}")
    node.decrypt()
    print(f"Decrypted: {node.encrypted}")
