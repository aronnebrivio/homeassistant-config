"""Grocy services."""
from __future__ import annotations

import asyncio
import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import entity_component

from pygrocy import TransactionType, EntityType

# pylint: disable=relative-beyond-top-level
from .const import DOMAIN

SERVICE_PRODUCT_ID = "product_id"
SERVICE_AMOUNT = "amount"
SERVICE_PRICE = "price"
SERVICE_SPOILED = "spoiled"
SERVICE_SUBPRODUCT_SUBSTITUTION = "allow_subproduct_substitution"
SERVICE_TRANSACTION_TYPE = "transaction_type"
SERVICE_CHORE_ID = "chore_id"
SERVICE_DONE_BY = "done_by"
SERVICE_TASK_ID = "task_id"
SERVICE_ENTITY_TYPE = "entity_type"
SERVICE_DATA = "data"

SERVICE_ADD_PRODUCT = "add_product_to_stock"
SERVICE_CONSUME_PRODUCT = "consume_product_from_stock"
SERVICE_EXECUTE_CHORE = "execute_chore"
SERVICE_COMPLETE_TASK = "complete_task"
SERVICE_ADD_GENERIC = "add_generic"

SERVICE_ADD_PRODUCT_SCHEMA = vol.All(
    vol.Schema(
        {
            vol.Required(SERVICE_PRODUCT_ID): vol.Coerce(int),
            vol.Required(SERVICE_AMOUNT): vol.Coerce(float),
            vol.Optional(SERVICE_PRICE): str,
        }
    )
)

SERVICE_CONSUME_PRODUCT_SCHEMA = vol.All(
    vol.Schema(
        {
            vol.Required(SERVICE_PRODUCT_ID): vol.Coerce(int),
            vol.Required(SERVICE_AMOUNT): vol.Coerce(float),
            vol.Optional(SERVICE_SPOILED): bool,
            vol.Optional(SERVICE_SUBPRODUCT_SUBSTITUTION): bool,
            vol.Optional(SERVICE_TRANSACTION_TYPE): str,
        }
    )
)

SERVICE_EXECUTE_CHORE_SCHEMA = vol.All(
    vol.Schema(
        {
            vol.Required(SERVICE_CHORE_ID): vol.Coerce(int),
            vol.Optional(SERVICE_DONE_BY): vol.Coerce(int),
        }
    )
)

SERVICE_COMPLETE_TASK_SCHEMA = vol.All(
    vol.Schema(
        {
            vol.Required(SERVICE_TASK_ID): vol.Coerce(int),
        }
    )
)

SERVICE_ADD_GENERIC_SCHEMA = vol.All(
    vol.Schema(
        {
            vol.Required(SERVICE_ENTITY_TYPE): str,
            vol.Required(SERVICE_DATA): object,
        }
    )
)

SERVICES_WITH_ACCOMPANYING_SCHEMA: list[tuple[str, vol.Schema]] = [
    (SERVICE_ADD_PRODUCT, SERVICE_ADD_PRODUCT_SCHEMA),
    (SERVICE_CONSUME_PRODUCT, SERVICE_CONSUME_PRODUCT_SCHEMA),
    (SERVICE_EXECUTE_CHORE, SERVICE_EXECUTE_CHORE_SCHEMA),
    (SERVICE_COMPLETE_TASK, SERVICE_COMPLETE_TASK_SCHEMA),
    (SERVICE_ADD_GENERIC, SERVICE_ADD_GENERIC_SCHEMA),
]


async def async_setup_services(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Set up services for Grocy integration."""
    coordinator = hass.data[DOMAIN]
    if hass.services.async_services().get(DOMAIN):
        return

    async def async_call_grocy_service(service_call: ServiceCall) -> None:
        """Call correct Grocy service."""
        service = service_call.service
        service_data = service_call.data

        if service == SERVICE_ADD_PRODUCT:
            await async_add_product_service(hass, coordinator, service_data)

        elif service == SERVICE_CONSUME_PRODUCT:
            await async_consume_product_service(hass, coordinator, service_data)

        elif service == SERVICE_EXECUTE_CHORE:
            await async_execute_chore_service(hass, coordinator, service_data)

        elif service == SERVICE_COMPLETE_TASK:
            await async_complete_task_service(hass, coordinator, service_data)

        elif service == SERVICE_ADD_GENERIC:
            await async_add_generic_service(hass, coordinator, service_data)

    for service, schema in SERVICES_WITH_ACCOMPANYING_SCHEMA:
        hass.services.async_register(DOMAIN, service, async_call_grocy_service, schema)


async def async_unload_services(hass: HomeAssistant) -> None:
    """Unload Grocy services."""
    if not hass.services.async_services().get(DOMAIN):
        return

    for service, _ in SERVICES_WITH_ACCOMPANYING_SCHEMA:
        hass.services.async_remove(DOMAIN, service)


async def async_add_product_service(hass, coordinator, data):
    """Add a product in Grocy."""
    product_id = data[SERVICE_PRODUCT_ID]
    amount = data[SERVICE_AMOUNT]
    price = data.get(SERVICE_PRICE, "")

    def wrapper():
        coordinator.api.add_product(product_id, amount, price)

    await hass.async_add_executor_job(wrapper)


async def async_consume_product_service(hass, coordinator, data):
    """Consume a product in Grocy."""
    product_id = data[SERVICE_PRODUCT_ID]
    amount = data[SERVICE_AMOUNT]
    spoiled = data.get(SERVICE_SPOILED, False)
    allow_subproduct_substitution = data.get(SERVICE_SUBPRODUCT_SUBSTITUTION, False)

    transaction_type_raw = data.get(SERVICE_TRANSACTION_TYPE, None)
    transaction_type = TransactionType.CONSUME

    if transaction_type_raw is not None:
        transaction_type = TransactionType[transaction_type_raw]

    def wrapper():
        coordinator.api.consume_product(
            product_id,
            amount,
            spoiled=spoiled,
            transaction_type=transaction_type,
            allow_subproduct_substitution=allow_subproduct_substitution,
        )

    await hass.async_add_executor_job(wrapper)


async def async_execute_chore_service(hass, coordinator, data):
    """Execute a chore in Grocy."""
    chore_id = data[SERVICE_CHORE_ID]
    done_by = data.get(SERVICE_DONE_BY, "")

    def wrapper():
        coordinator.api.execute_chore(chore_id, done_by)

    await hass.async_add_executor_job(wrapper)

    asyncio.run_coroutine_threadsafe(
        entity_component.async_update_entity(hass, "sensor.grocy_chores"), hass.loop
    )


async def async_complete_task_service(hass, coordinator, data):
    """Complete a task in Grocy."""
    task_id = data[SERVICE_TASK_ID]

    def wrapper():
        coordinator.api.complete_task(task_id)

    await hass.async_add_executor_job(wrapper)

    asyncio.run_coroutine_threadsafe(
        entity_component.async_update_entity(hass, "sensor.grocy_tasks"), hass.loop
    )


async def async_add_generic_service(hass, coordinator, data):
    """Add a generic entity in Grocy."""
    entity_type_raw = data.get(SERVICE_ENTITY_TYPE, None)
    entity_type = EntityType.TASKS

    if entity_type_raw is not None:
        entity_type = EntityType(entity_type_raw)

    data = data[SERVICE_DATA]

    def wrapper():
        coordinator.api.add_generic(entity_type, data)

    await hass.async_add_executor_job(wrapper)
