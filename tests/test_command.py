from typing import Final
import unittest

from midea_beautiful.command import (
    DeviceCapabilitiesCommand,
    DeviceCapabilitiesCommandMore,
    midea_command_reset_sequence,
)
from midea_beautiful.lan import LanDevice
from midea_beautiful.midea import (
    APPLIANCE_TYPE_AIRCON,
    APPLIANCE_TYPE_DEHUMIDIFIER,
    DEFAULT_APPKEY,
)

APP_KEY: Final = DEFAULT_APPKEY


class TestCommand(unittest.TestCase):
    def test_device_capabilities_command(self) -> None:
        dc = DeviceCapabilitiesCommand()
        self.assertEqual("aa0ea100000000000303b501118ef6", dc.finalize().hex())

    def test_device_capabilities_command_more(self) -> None:
        dc = DeviceCapabilitiesCommandMore()
        self.assertEqual("aa0ea100000000000303b501011381", dc.finalize().hex())

    def test_dehumidifier_status(self) -> None:
        midea_command_reset_sequence()
        device = LanDevice(id="12345", appliance_type=APPLIANCE_TYPE_DEHUMIDIFIER)
        cmd = device.state.refresh_command()
        self.assertEqual(
            "aa20a100000000000003418100ff03ff000000000000000000000000000001294f",
            cmd.finalize().hex(),
        )

    def test_dehumidifier_set(self) -> None:
        midea_command_reset_sequence()
        device = LanDevice(id="12345", appliance_type=APPLIANCE_TYPE_DEHUMIDIFIER)
        cmd = device.state.apply_command()
        self.assertEqual(
            "aa20a100000000000302480000280000003200000000000000000000000001395e",
            cmd.finalize().hex(),
        )

    def test_dehumidifier_set_fan_speed(self) -> None:
        midea_command_reset_sequence()
        device = LanDevice(id="12345", appliance_type=APPLIANCE_TYPE_DEHUMIDIFIER)
        setattr(device.state, "fan_speed", 60)
        cmd = device.state.apply_command()
        self.assertEqual(
            "aa20a1000000000003024800003c0000003200000000000000000000000001dea5",
            cmd.finalize().hex(),
        )

    def test_dehumidifier_set_mode(self) -> None:
        midea_command_reset_sequence()
        device = LanDevice(id="12345", appliance_type=APPLIANCE_TYPE_DEHUMIDIFIER)
        setattr(device.state, "mode", 3)
        cmd = device.state.apply_command()
        self.assertEqual(
            "aa20a1000000000003024800032800000032000000000000000000000000014b49",
            cmd.finalize().hex(),
        )

    def test_dehumidifier_set_target_humidity(self) -> None:
        midea_command_reset_sequence()
        device = LanDevice(id="12345", appliance_type=APPLIANCE_TYPE_DEHUMIDIFIER)
        setattr(device.state, "target_humidity", 45)
        cmd = device.state.apply_command()
        self.assertEqual(
            "aa20a100000000000302480000280000002d000000000000000000000000017626",
            cmd.finalize().hex(),
        )

    def test_ac_status(self) -> None:
        midea_command_reset_sequence()
        device = LanDevice(id="12345", appliance_type=APPLIANCE_TYPE_AIRCON)
        cmd = device.state.refresh_command().finalize().hex()
        self.assertEqual(
            "aa20ac00000000000003418100ff03ff00020000000000000000000000000171fa",
            cmd,
        )

        midea_command_reset_sequence(2)
        device = LanDevice(id="12345", appliance_type=APPLIANCE_TYPE_AIRCON)
        cmd = device.state.refresh_command().finalize().hex()
        self.assertEqual(
            "aa20ac00000000000003418100ff03ff000200000000000000000000000003cd9c",
            cmd,
        )

    def test_aircon_set_fan(self) -> None:
        midea_command_reset_sequence()
        device = LanDevice(id="12345", appliance_type=APPLIANCE_TYPE_AIRCON)
        setattr(device.state, "beep_prompt", True)
        setattr(device.state, "fan_speed", 48)
        cmd = device.state.apply_command().finalize()
        self.assertEqual(
            "aa23ac0000000000000240400030000000000000100000000000000000000100000078f6",
            cmd.hex(),
        )

    def test_aircon_set_mode(self) -> None:
        midea_command_reset_sequence()
        device = LanDevice(id="12345", appliance_type=APPLIANCE_TYPE_AIRCON)
        setattr(device.state, "beep_prompt", True)
        setattr(device.state, "fan_speed", 48)
        setattr(device.state, "mode", 2)
        cmd = device.state.apply_command().finalize()
        self.assertEqual(
            "aa23ac00000000000002404040300000000000001000000000000000000001000000ce60",
            cmd.hex(),
        )

    def test_aircon_set_turbo(self) -> None:
        midea_command_reset_sequence()
        device = LanDevice(id="12345", appliance_type=APPLIANCE_TYPE_AIRCON)
        setattr(device.state, "beep_prompt", True)
        setattr(device.state, "turbo", True)
        setattr(device.state, "fan_speed", 40)

        cmd = device.state.apply_command().finalize()
        self.assertEqual(
            "aa23ac000000000000024040002800000000000012000000000000000000010000000173",
            cmd.hex(),
        )

    def test_aircon_set_temperature(self) -> None:
        midea_command_reset_sequence()
        device = LanDevice(id="12345", appliance_type=APPLIANCE_TYPE_AIRCON)
        setattr(device.state, "beep_prompt", True)
        setattr(device.state, "turbo", True)
        setattr(device.state, "fan_speed", 45)
        setattr(device.state, "target_temperature", 20.5)

        cmd = device.state.apply_command().finalize()
        self.assertEqual(
            "aa23ac000000000000024040142d0000000000001200000000000000000001000000a7b4",
            cmd.hex(),
        )
