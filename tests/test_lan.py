import binascii
from datetime import datetime
from typing import Final
import unittest

from midea_beautiful.crypto import Security
from midea_beautiful.lan import LanDevice
from midea_beautiful.midea import (
    APPLIANCE_TYPE_AIRCON,
    APPLIANCE_TYPE_DEHUMIDIFIER,
    DEFAULT_APPKEY,
)

APP_KEY: Final = DEFAULT_APPKEY


BROADCAST_PAYLOAD: Final = (
    "020100c02c190000"
    "3030303030305030303030303030513131323334353637383941424330303030"
    "0b6e65745f61315f394142430000000001000000040000000000"
    "a1"
    "00000000000000"
    "123456789abc069fcd0300080103010000000000000000000000000000000000000000"
)


class TestLanDevice(unittest.TestCase):
    def test_lan_packet_header_ac(self) -> None:
        expected_header = binascii.unhexlify("5a5a01116800200000000000")

        device = LanDevice(id=str(0x12345), appliance_type=APPLIANCE_TYPE_AIRCON)
        cmd = device.state.refresh_command()
        now = datetime.now()
        res = device._lan_packet(cmd)
        self.assertEqual(expected_header, res[: len(expected_header)])
        if now.minute < 59:
            self.assertEqual(now.hour, res[15])
            if now.hour < 23:
                self.assertEqual(now.day, res[16])
                self.assertEqual(now.month, res[17])
                self.assertEqual(now.year % 100, res[18])
                self.assertEqual(int(now.year / 100), res[19])

        self.assertEqual(0x45, res[20])
        self.assertEqual(0x23, res[21])
        self.assertEqual(0x01, res[22])
        self.assertEqual(0x00, res[23])

    def test_lan_packet_header_dehumidifier(self) -> None:
        expected_header = binascii.unhexlify("5a5a01116800200000000000")

        device = LanDevice(id=str(0x12345), appliance_type=APPLIANCE_TYPE_DEHUMIDIFIER)
        cmd = device.state.refresh_command()
        now = datetime.now()
        res = device._lan_packet(cmd)
        self.assertEqual(expected_header, res[: len(expected_header)])
        if now.minute < 59:
            self.assertEqual(now.hour, res[15])
            if now.hour < 23:
                self.assertEqual(now.day, res[16])
                self.assertEqual(now.month, res[17])
                self.assertEqual(now.year % 100, res[18])
                self.assertEqual(int(now.year / 100), res[19])

        self.assertEqual(0x45, res[20])
        self.assertEqual(0x23, res[21])
        self.assertEqual(0x01, res[22])
        self.assertEqual(0x00, res[23])

    def test_appliance_from_broadcast(self):
        msg = (
            "837000b8200f04035a5a0111a8007a80000000000000000000000000010203040506"
            "0000000000000000000000000000"
            "c136771d628d08f90ca694ad1a5893b77c7ea4ac6fed1dc7e2670058df2f44675638"
            "d33cddd5727c581d84b87f54b944bbc7440daf21c3fa9cab7b342b84ac6a630967cd"
            "7d9364d23d4d7a91591e277d90b13be000894715b606127e07c2fecff31443d17c3a"
            "ac03a7656614ae1dca44"
            "8c53d543ede4d8d26c2008f541b804dc5b24fc8c2735ead584edc8dda92b243d"
        )
        response = binascii.unhexlify(msg)
        token = "TOKEN"
        key = "KEY"
        appliance = LanDevice(data=response, token=token, key=key)
        self.assertEqual("12:34:56:78:9a:bc", appliance.mac)
        self.assertEqual("000000P0000000Q1123456789ABC0000", appliance.sn)
        self.assertEqual("net_a1_9ABC", appliance.ssid)
        self.assertEqual("0xa1", appliance.type)

    def test_appliance_from_broadcast_dehumidifier(self):
        payload = bytearray(binascii.unhexlify(BROADCAST_PAYLOAD))
        encrypted = Security().aes_encrypt(payload)
        msg = (
            f"837000b8200f04035a5a0111a8007a80000000000000000000000000010203040506"
            f"0000000000000000000000000000"
            f"{encrypted.hex()}"
            f"8c53d543ede4d8d26c2008f541b804dc5b24fc8c2735ead584edc8dda92b243d"
        )
        response = binascii.unhexlify(msg)
        token = "TOKEN"
        key = "KEY"
        appliance = LanDevice(data=response, token=token, key=key)
        self.assertEqual("12:34:56:78:9a:bc", appliance.mac)
        self.assertEqual("000000P0000000Q1123456789ABC0000", appliance.sn)
        self.assertEqual("net_a1_9ABC", appliance.ssid)
        self.assertEqual("0xa1", appliance.type)

    def test_appliance_from_broadcast_ac(self):
        payload = bytearray(binascii.unhexlify(BROADCAST_PAYLOAD))
        payload[46] = 0x63  # Letter c
        payload[66] = int(APPLIANCE_TYPE_AIRCON, base=16)
        encrypted = Security().aes_encrypt(payload)
        msg = (
            f"837000b8200f04035a5a0111a8007a80000000000000000000000000010203040506"
            f"0000000000000000000000000000"
            f"{encrypted.hex()}"
            f"8c53d543ede4d8d26c2008f541b804dc5b24fc8c2735ead584edc8dda92b243d"
        )
        response = binascii.unhexlify(msg)
        token = "TOKEN"
        key = "KEY"
        appliance = LanDevice(data=response, token=token, key=key)
        self.assertEqual("12:34:56:78:9a:bc", appliance.mac)
        self.assertEqual("000000P0000000Q1123456789ABC0000", appliance.sn)
        self.assertEqual("net_ac_9ABC", appliance.ssid)
        self.assertEqual("0xac", appliance.type)
        self.assertEqual("Air conditioner", appliance.state.model)
