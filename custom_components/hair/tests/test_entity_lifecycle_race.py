"""Regression tests for the entity hass-None race.

When HAIR adds an entity via ``async_add_entities`` and a device-update
fires before HA finishes the platform registration, the entity's
``hass`` attribute is still ``None``.  Real HA's
``_async_verify_state_writable`` then raises:

    RuntimeError: Attribute hass is None for <entity unknown.unknown=unknown>

This breaks user setup flows that promote a remote with multiple
commands (each command-add fires ``async_update_entities`` against an
entity whose registration hasn't drained).  Reported from a Seeed XIAO
IR Mate user 2026-06-07.

These tests assert each entity platform's ``update_device`` method is
defensive against the race: when ``self.hass is None``, the method
skips ``async_write_ha_state`` instead of calling it (which would
raise in production).
"""
from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from custom_components.hair.climate import HAIRClimateEntity
from custom_components.hair.const import (
    CommandCategory,
    CommandSource,
    DeviceType,
)
from custom_components.hair.cover import HAIRCoverEntity
from custom_components.hair.fan import HAIRFanEntity
from custom_components.hair.light import HAIRLightEntity
from custom_components.hair.media_player import HAIRMediaPlayerEntity
from custom_components.hair.models import EntityConfig, IRCommand, IRDevice
from custom_components.hair.remote import HAIRRemoteEntity
from custom_components.hair.switch import HAIRSwitchEntity


def _device(device_type: DeviceType, device_id: str = "dev-1") -> IRDevice:
    return IRDevice(
        id=device_id,
        name="Test Device",
        device_type=device_type,
        manufacturer="TestCo",
        model="X100",
        emitter_entity_ids=["infrared.test"],
        commands=[
            IRCommand(
                id="cmd-1",
                name="Power",
                category=CommandCategory.POWER,
                source=CommandSource.CAPTURED,
                protocol="NEC",
                code="0x1234",
            )
        ],
        entity_config=EntityConfig(),
    )


def _manager() -> MagicMock:
    mgr = MagicMock()
    return mgr


def _raise_if_no_hass(entity):
    """Stub async_write_ha_state to mirror HA's _async_verify_state_writable.

    Real HA raises:
        RuntimeError: Attribute hass is None for <entity unknown.unknown=unknown>
    when async_write_ha_state runs before async_add_entities has registered
    the entity with its platform.  We simulate that here so the test fails
    loudly if update_device drops through to async_write_ha_state on a
    hass-None entity.
    """
    def _verify():
        if getattr(entity, "hass", None) is None:
            raise RuntimeError(
                "Attribute hass is None for <entity unknown.unknown=unknown>"
            )

    entity.async_write_ha_state = MagicMock(side_effect=_verify)


# ---------------------------------------------------------------------------
# Platform-by-platform race reproduction
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    ("entity_cls", "device_type"),
    [
        (HAIRFanEntity, DeviceType.FAN),
        (HAIRMediaPlayerEntity, DeviceType.MEDIA_PLAYER),
        (HAIRClimateEntity, DeviceType.AC),
        (HAIRLightEntity, DeviceType.LIGHT),
        (HAIRSwitchEntity, DeviceType.SWITCH),
        (HAIRCoverEntity, DeviceType.SCREEN),
        (HAIRRemoteEntity, DeviceType.OTHER),
    ],
)
def test_update_device_does_not_raise_when_hass_is_none(entity_cls, device_type):
    """Reproduces the production race.

    An entity is instantiated and put into the platform's local dict,
    but ``async_add_entities`` has not finished registering it yet.
    A device update fires before registration drains.

    Before the fix: ``update_device`` calls ``async_write_ha_state`` which
    raises ``RuntimeError: Attribute hass is None for <entity
    unknown.unknown=unknown>``.

    After the fix: ``update_device`` notices ``self.hass is None`` and
    skips the state write.  No exception.
    """
    device = _device(device_type)
    entity = entity_cls(device, _manager())
    # In real HA, Entity has ``hass: HomeAssistant = None`` as a class
    # attribute pre-registration.  Our test stubs omit that, so set it
    # explicitly here to mirror production.
    entity.hass = None
    _raise_if_no_hass(entity)

    new_device = _device(device_type)
    new_device.name = "Renamed Device"

    # The race: update_device fires against an entity that has not yet
    # been added to its platform.
    entity.update_device(new_device)

    # The defensive guard must prevent the state write that would raise.
    entity.async_write_ha_state.assert_not_called()


@pytest.mark.parametrize(
    ("entity_cls", "device_type"),
    [
        (HAIRFanEntity, DeviceType.FAN),
        (HAIRMediaPlayerEntity, DeviceType.MEDIA_PLAYER),
        (HAIRClimateEntity, DeviceType.AC),
        (HAIRLightEntity, DeviceType.LIGHT),
        (HAIRSwitchEntity, DeviceType.SWITCH),
        (HAIRCoverEntity, DeviceType.SCREEN),
        (HAIRRemoteEntity, DeviceType.OTHER),
    ],
)
def test_update_device_writes_state_when_hass_is_set(entity_cls, device_type):
    """The happy path: once HA has registered the entity, update_device
    must continue to call ``async_write_ha_state`` so the new device
    attributes propagate to the state machine."""
    device = _device(device_type)
    entity = entity_cls(device, _manager())
    entity.hass = MagicMock()  # simulate post-registration entity
    _raise_if_no_hass(entity)  # will allow the call now that hass is set

    new_device = _device(device_type)
    new_device.name = "Renamed Device"

    entity.update_device(new_device)

    entity.async_write_ha_state.assert_called_once()
