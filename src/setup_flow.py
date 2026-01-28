"""
Setup flow for Orange integration.

:copyright: (c) 2025 Albaintor
:license: Mozilla Public License Version 2.0, see LICENSE for more details.
"""

import asyncio
import logging
from enum import IntEnum
from urllib.parse import urlparse

from ucapi import (
    AbortDriverSetup,
    DriverSetupRequest,
    IntegrationSetupError,
    RequestUserInput,
    SetupAction,
    SetupComplete,
    SetupDriver,
    SetupError,
    UserDataResponse,
)

import config
import discover
from client import OrangeTVClient
from config import OrangeConfigDevice
from const import OPERATION_INFORMATION

_LOG = logging.getLogger(__name__)

# pylint: disable = W1405,C0103


class SetupSteps(IntEnum):
    """Enumeration of setup steps to keep track of user data responses."""

    INIT = 0
    WORKFLOW_MODE = 1
    DEVICE_CONFIGURATION_MODE = 2
    DISCOVER = 3
    DEVICE_CHOICE = 4
    RECONFIGURE = 5
    BACKUP_RESTORE = 6


_setup_step = SetupSteps.INIT
_cfg_add_device: bool = False
_reconfigured_device: OrangeConfigDevice | None = None
_user_input_discovery = RequestUserInput(
    {"en": "Setup mode", "de": "Setup Modus"},
    [
        {
            "field": {"text": {"value": ""}},
            "id": "address",
            "label": {"en": "Endpoint", "de": "Adresse", "fr": "Adresse"},
        },
        {
            "id": "info",
            "label": {"en": ""},
            "field": {
                "label": {
                    "value": {
                        "en": "Leave blank to use auto-discovery.",
                        "de": "Leer lassen, um automatische Erkennung zu verwenden.",
                        "fr": "Laissez le champ vide pour utiliser la découverte automatique.",
                    }
                }
            },
        },
    ],
)


# pylint: disable=R0911
async def driver_setup_handler(msg: SetupDriver) -> SetupAction:
    """
    Dispatch driver setup requests to corresponding handlers.

    Either start the setup process or handle the selected AVR device.

    :param msg: the setup driver request object, either DriverSetupRequest or UserDataResponse
    :return: the setup action on how to continue
    """
    global _setup_step
    global _cfg_add_device

    _LOG.debug("driver_setup_handler")

    if isinstance(msg, DriverSetupRequest):
        _setup_step = SetupSteps.INIT
        _cfg_add_device = False
        return await handle_driver_setup(msg)
    if isinstance(msg, UserDataResponse):
        _LOG.debug("Setup handler message : step %s, message : %s", _setup_step, msg)
        if _setup_step == SetupSteps.WORKFLOW_MODE:
            if msg.input_values.get("configuration_mode", "") == "normal":
                _setup_step = SetupSteps.DEVICE_CONFIGURATION_MODE
                _LOG.debug("Starting normal setup workflow")
                return _user_input_discovery
            _LOG.debug("User requested backup/restore of configuration")
            return await _handle_backup_restore_step()
        if _setup_step == SetupSteps.DEVICE_CONFIGURATION_MODE:
            if "action" in msg.input_values:
                _LOG.debug("Setup flow starts with existing configuration")
                return await handle_configuration_mode(msg)
            _LOG.debug("Setup flow configuration mode")
            return await _handle_discovery(msg)
        if _setup_step == SetupSteps.DISCOVER and "address" in msg.input_values:
            return await _handle_discovery(msg)
        if _setup_step == SetupSteps.DEVICE_CHOICE and "choice" in msg.input_values:
            return await handle_device_choice(msg)
        if _setup_step == SetupSteps.RECONFIGURE:
            return await _handle_device_reconfigure(msg)
        if _setup_step == SetupSteps.BACKUP_RESTORE:
            return await _handle_backup_restore(msg)
        _LOG.error("No or invalid user response was received: %s", msg)
    elif isinstance(msg, AbortDriverSetup):
        _LOG.info("Setup was aborted with code: %s", msg.error)
        _setup_step = SetupSteps.INIT

    # user confirmation not used in setup process
    # if isinstance(msg, UserConfirmationResponse):
    #     return handle_user_confirmation(msg)

    return SetupError()


async def handle_driver_setup(_msg: DriverSetupRequest) -> RequestUserInput | SetupError:
    """
    Start driver setup.

    Initiated by Remote Two to set up the driver.
    Ask user to enter ip-address for manual configuration, otherwise auto-discovery is used.

    :param _msg: not used, we don't have any input fields in the first setup screen.
    :return: the setup action on how to continue
    """
    global _setup_step

    # workaround for web-configurator not picking up first response
    await asyncio.sleep(1)

    reconfigure = _msg.reconfigure
    _LOG.debug("Handle driver setup, reconfigure=%s", reconfigure)
    if reconfigure:
        _setup_step = SetupSteps.DEVICE_CONFIGURATION_MODE

        # get all configured devices for the user to choose from
        dropdown_devices = []
        for device in config.devices.all():
            dropdown_devices.append({"id": device.id, "label": {"en": f"{device.name} ({device.id})"}})

        # TODO #12 externalize language texts
        # build user actions, based on available devices
        dropdown_actions = [
            {
                "id": "add",
                "label": {
                    "en": "Add a new device",
                    "de": "Neues Gerät hinzufügen",
                    "fr": "Ajouter un nouvel appareil",
                },
            },
        ]

        # add remove & reset actions if there's at least one configured device
        if dropdown_devices:
            dropdown_actions.append(
                {
                    "id": "configure",
                    "label": {
                        "en": "Configure selected device",
                        "fr": "Configurer l'appareil sélectionné",
                    },
                },
            )
            dropdown_actions.append(
                {
                    "id": "remove",
                    "label": {
                        "en": "Delete selected device",
                        "de": "Selektiertes Gerät löschen",
                        "fr": "Supprimer l'appareil sélectionné",
                    },
                },
            )
            dropdown_actions.append(
                {
                    "id": "reset",
                    "label": {
                        "en": "Reset configuration and reconfigure",
                        "de": "Konfiguration zurücksetzen und neu konfigurieren",
                        "fr": "Réinitialiser la configuration et reconfigurer",
                    },
                },
            )
        else:
            # dummy entry if no devices are available
            dropdown_devices.append({"id": "", "label": {"en": "---"}})

        dropdown_actions.append(
            {
                "id": "backup_restore",
                "label": {
                    "en": "Backup or restore devices configuration",
                    "fr": "Sauvegarder ou restaurer la configuration des appareils",
                },
            },
        )

        return RequestUserInput(
            {"en": "Configuration mode", "de": "Konfigurations-Modus"},
            [
                {
                    "field": {"dropdown": {"value": dropdown_devices[0]["id"], "items": dropdown_devices}},
                    "id": "choice",
                    "label": {
                        "en": "Configured devices",
                        "de": "Konfigurierte Geräte",
                        "fr": "Appareils configurés",
                    },
                },
                {
                    "field": {"dropdown": {"value": dropdown_actions[0]["id"], "items": dropdown_actions}},
                    "id": "action",
                    "label": {
                        "en": "Action",
                        "de": "Aktion",
                        "fr": "Appareils configurés",
                    },
                },
            ],
        )
    # Initial setup, make sure we have a clean configuration
    config.devices.clear()  # triggers device instance removal
    _setup_step = SetupSteps.WORKFLOW_MODE
    return RequestUserInput(
        {"en": "Configuration mode", "de": "Konfigurations-Modus"},
        [
            {
                "field": {
                    "dropdown": {
                        "value": "normal",
                        "items": [
                            {
                                "id": "normal",
                                "label": {
                                    "en": "Start the configuration of the integration",
                                    "fr": "Démarrer la configuration de l'intégration",
                                },
                            },
                            {
                                "id": "backup_restore",
                                "label": {
                                    "en": "Backup or restore devices configuration",
                                    "fr": "Sauvegarder ou restaurer la configuration des appareils",
                                },
                            },
                        ],
                    }
                },
                "id": "configuration_mode",
                "label": {
                    "en": "Configuration mode",
                    "fr": "Mode de configuration",
                },
            }
        ],
    )


async def handle_configuration_mode(msg: UserDataResponse) -> RequestUserInput | SetupComplete | SetupError:
    """
    Process user data response in a setup process.

    If ``address`` field is set by the user: try connecting to device and retrieve model information.
    Otherwise, start Android TV discovery and present the found devices to the user to choose from.

    :param msg: response data from the requested user data
    :return: the setup action on how to continue
    """
    global _setup_step
    global _cfg_add_device
    global _reconfigured_device

    action = msg.input_values["action"]

    _LOG.debug("Handle configuration mode")

    # workaround for web-configurator not picking up first response
    await asyncio.sleep(1)

    match action:
        case "add":
            _cfg_add_device = True
        case "remove":
            choice = msg.input_values["choice"]
            if not config.devices.remove(choice):
                _LOG.warning("Could not remove device from configuration: %s", choice)
                return SetupError(error_type=IntegrationSetupError.OTHER)
            config.devices.store()
            return SetupComplete()
        case "configure":
            # Reconfigure device if the identifier has changed
            choice = msg.input_values["choice"]
            selected_device = config.devices.get(choice)
            if not selected_device:
                _LOG.warning("Can not configure device from configuration: %s", choice)
                return SetupError(error_type=IntegrationSetupError.OTHER)

            _setup_step = SetupSteps.RECONFIGURE
            _reconfigured_device = selected_device

            return RequestUserInput(
                {
                    "en": "Configure your Orange decoder",
                    "fr": "Configurez votre décodeur Orange",
                },
                [
                    {
                        "field": {"text": {"value": _reconfigured_device.address}},
                        "id": "address",
                        "label": {"en": "IP address", "de": "IP-Adresse", "fr": "Adresse IP"},
                    },
                    {
                        "id": "port",
                        "label": {
                            "en": "Port number",
                            "fr": "Numéro de port",
                        },
                        "field": {
                            "number": {
                                "value": _reconfigured_device.port,
                                "min": 1,
                                "max": 65535,
                                "steps": 1,
                                "decimals": 0,
                            }
                        },
                    },
                    {
                        "field": {
                            "dropdown": {
                                "value": _reconfigured_device.country,
                                "items": [
                                    {
                                        "id": "france",
                                        "label": {
                                            "en": "France",
                                            "de": "Frankreich",
                                            "fr": "France",
                                        },
                                    },
                                    {
                                        "id": "france",
                                        "label": {
                                            "en": "Poland",
                                            "de": "Polen",
                                            "fr": "Pologne",
                                        },
                                    },
                                ],
                            }
                        },
                        "id": "country",
                        "label": {
                            "en": "Choose your country",
                            "de": "Wähle deinen Land",
                            "fr": "Choisissez votre pays",
                        },
                    },
                    {
                        "id": "always_on",
                        "label": {
                            "en": "Keep connection alive (faster initialization, but consumes more battery)",
                            "fr": "Conserver la connexion active (lancement plus rapide, mais consomme plus de "
                            "batterie)",
                        },
                        "field": {"checkbox": {"value": _reconfigured_device.always_on}},
                    },
                    {
                        "id": "log_client",
                        "label": {
                            "en": "Log client messages for analysis",
                            "fr": "Tracer les messages du client pour analyse",
                        },
                        "field": {"checkbox": {"value": _reconfigured_device.log_client}},
                    },
                ],
            )
        case "reset":
            config.devices.clear()  # triggers device instance removal
        case "backup_restore":
            return await _handle_backup_restore_step()
        case _:
            _LOG.error("Invalid configuration action: %s", action)
            return SetupError(error_type=IntegrationSetupError.OTHER)

    _setup_step = SetupSteps.DISCOVER
    return _user_input_discovery


async def _handle_discovery(msg: UserDataResponse) -> RequestUserInput | SetupError:
    """
    Process user data response in a setup process.

    If ``address`` field is set by the user: try connecting to device and retrieve model information.
    Otherwise, start discovery and present the found devices to the user to choose from.

    :param msg: response data from the requested user data
    :return: the setup action on how to continue
    """
    # pylint: disable=W1405,W0718
    global _setup_step

    dropdown_items = []
    _LOG.debug("Handle driver setup with discovery")

    address = msg.input_values["address"]
    device = None
    if address:
        _LOG.debug("Starting manual driver setup for %s", address)
        try:
            # simple connection check
            result = urlparse("//" + address)
            port = 8080
            if result.port:
                port = result.port
            device = OrangeTVClient(
                OrangeConfigDevice(
                    id="Orange", name="Orange", address=result.hostname, country="france", always_on=False, port=port
                )
            )
            await device.connect()
            data = await device.rq_livebox(OPERATION_INFORMATION)
            friendly_name = data["result"]["data"]["friendlyName"]
            dropdown_items.append({"id": address, "label": {"en": f"{friendly_name} [{address}]"}})
            await device.disconnect()
            device = None
        except Exception as ex:
            _LOG.error("Cannot connect to manually entered address %s: %s", address, ex)
            return SetupError(error_type=IntegrationSetupError.CONNECTION_REFUSED)
    else:
        _LOG.debug("Starting auto-discovery driver setup")
        devices = await discover.async_identify_orangetv_devices()
        for device in devices:
            avr_data = {
                "id": device.get("host"),
                "label": {"en": f"{device.get('friendlyName')} [{device.get('host')}]"},
            }
            dropdown_items.append(avr_data)

    if not dropdown_items:
        _LOG.warning("No OrangeTV found")
        return SetupError(error_type=IntegrationSetupError.NOT_FOUND)

    _setup_step = SetupSteps.DEVICE_CHOICE
    return RequestUserInput(
        {
            "en": "Please choose your Orange TV STB",
            "de": "Bitte Orange TV STB auswählen",
            "fr": "Sélectionnez votre décodeur Orange",
        },
        [
            {
                "field": {"dropdown": {"value": dropdown_items[0]["id"], "items": dropdown_items}},
                "id": "choice",
                "label": {
                    "en": "Choose your Orange STB",
                    "de": "Wähle deinen Orange STB",
                    "fr": "Choisissez votre décodeur Orange",
                },
            },
            {
                "id": "port",
                "label": {
                    "en": "Port number",
                    "fr": "Numéro de port",
                },
                "field": {"number": {"value": 8080, "min": 1, "max": 65535, "steps": 1, "decimals": 0}},
            },
            {
                "field": {
                    "dropdown": {
                        "value": "france",
                        "items": [
                            {
                                "id": "france",
                                "label": {
                                    "en": "France",
                                    "de": "Frankreich",
                                    "fr": "France",
                                },
                            },
                            {
                                "id": "france",
                                "label": {
                                    "en": "Poland",
                                    "de": "Polen",
                                    "fr": "Pologne",
                                },
                            },
                        ],
                    }
                },
                "id": "country",
                "label": {
                    "en": "Choose your country",
                    "de": "Wähle deinen Land",
                    "fr": "Choisissez votre pays",
                },
            },
            {
                "id": "always_on",
                "label": {
                    "en": "Keep connection alive (faster initialization, but consumes more battery)",
                    "fr": "Conserver la connexion active (lancement plus rapide, mais consomme plus de batterie)",
                },
                "field": {"checkbox": {"value": False}},
            },
            {
                "id": "log_client",
                "label": {
                    "en": "Log client messages for analysis",
                    "fr": "Tracer les messages du client pour analyse",
                },
                "field": {"checkbox": {"value": False}},
            },
        ],
    )


async def handle_device_choice(msg: UserDataResponse) -> SetupComplete | SetupError:
    """
    Process user data response in a setup process.

    Driver setup callback to provide requested user data during the setup process.

    :param msg: response data from the requested user data
    :return: the setup action on how to continue: SetupComplete if a valid AVR device was chosen.
    """
    # pylint: disable=W1405,W0718
    host = msg.input_values["choice"]
    result = urlparse("//" + host)
    host = result.hostname
    port = 8080
    if result.port:
        port = result.port
    else:
        try:
            port = int(msg.input_values.get("port", 8080))
        except ValueError:
            return SetupError(error_type=IntegrationSetupError.OTHER)
    country = msg.input_values.get("country", "france")
    always_on = msg.input_values.get("always_on") == "true"
    log_client = msg.input_values.get("log_client") == "true"
    _LOG.debug("Chosen Orange: %s. Trying to connect and retrieve device information...", host)
    try:
        # simple connection check
        device = OrangeTVClient(
            OrangeConfigDevice(
                id="Orange",
                name="Orange",
                address=host,
                country=country,
                always_on=always_on,
                port=port,
                log_client=True,
            )
        )
        await device.connect()
        data = await device.rq_livebox(OPERATION_INFORMATION)
        _LOG.debug("Got data from device %s", data)
        friendly_name = data["result"]["data"]["friendlyName"]
        identifier = data["result"]["data"]["macAddress"]
        await device.disconnect()
    except Exception as ex:
        _LOG.error("Cannot connect to %s: %s", host, ex)
        return SetupError(error_type=IntegrationSetupError.CONNECTION_REFUSED)

    assert device
    assert identifier

    unique_id = identifier

    if unique_id is None:
        _LOG.error("Could not get mac address of host %s: required to create a unique device", host)
        return SetupError(error_type=IntegrationSetupError.OTHER)

    config.devices.add(
        OrangeConfigDevice(
            id=unique_id,
            name=friendly_name,
            address=host,
            country=country,
            always_on=always_on,
            port=port,
            log_client=log_client,
        )
    )  # triggers OrangeAVR instance creation
    config.devices.store()

    # AVR device connection will be triggered with subscribe_entities request

    await asyncio.sleep(1)

    _LOG.info("Setup successfully completed for %s (%s)", friendly_name, unique_id)
    return SetupComplete()


async def _handle_backup_restore_step() -> RequestUserInput:
    global _setup_step

    _setup_step = SetupSteps.BACKUP_RESTORE
    current_config = config.devices.export()

    _LOG.debug("Handle backup/restore step")

    return RequestUserInput(
        {
            "en": "Backup or restore devices configuration (all existing devices will be removed)",
            "fr": "Sauvegarder ou restaurer la configuration des appareils (tous les appareils existants seront "
            "supprimés)",
        },
        [
            {
                "field": {
                    "textarea": {
                        "value": current_config,
                    }
                },
                "id": "config",
                "label": {
                    "en": "Devices configuration",
                    "fr": "Configuration des appareils",
                },
            },
        ],
    )


async def _handle_device_reconfigure(msg: UserDataResponse) -> SetupComplete | SetupError:
    """
    Process reconfiguration of a registered Android TV device.

    :param msg: response data from the requested user data
    :return: the setup action on how to continue: SetupComplete after updating configuration
    """
    # flake8: noqa:F824
    # pylint: disable=W0602
    global _reconfigured_device

    if _reconfigured_device is None:
        return SetupError()

    address = msg.input_values.get("address", "")
    port = 8080
    try:
        port = int(msg.input_values.get("port", 8080))
    except ValueError:
        return SetupError(error_type=IntegrationSetupError.OTHER)
    country = msg.input_values.get("country", "france")
    always_on = msg.input_values.get("always_on") == "true"
    log_client = msg.input_values.get("log_client") == "true"

    _LOG.debug("User has changed configuration")
    _reconfigured_device.address = address
    _reconfigured_device.port = port
    _reconfigured_device.country = country
    _reconfigured_device.always_on = always_on
    _reconfigured_device.log_client = log_client

    config.devices.add_or_update(_reconfigured_device)  # triggers ATV instance update
    await asyncio.sleep(1)
    _LOG.info("Setup successfully completed for %s", _reconfigured_device.name)

    return SetupComplete()


async def _handle_backup_restore(msg: UserDataResponse) -> SetupComplete | SetupError:
    """
    Process import of configuration

    :param msg: response data from the requested user data
    :return: the setup action on how to continue: SetupComplete after updating configuration
    """
    # flake8: noqa:F824
    # pylint: disable=W0602
    global _reconfigured_device

    _LOG.debug("Handle backup/restore")
    updated_config = msg.input_values["config"]
    _LOG.info("Replacing configuration with : %s", updated_config)
    if not config.devices.import_config(updated_config):
        _LOG.error("Setup error : unable to import updated configuration %s", updated_config)
        return SetupError(error_type=IntegrationSetupError.OTHER)
    _LOG.debug("Configuration imported successfully")

    await asyncio.sleep(1)
    return SetupComplete()
