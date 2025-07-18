# Changelog

## [4.10.0](https://github.com/aronnebrivio/homeassistant-config/compare/v4.9.0...v4.10.0) (2025-07-11)


### Features

* **automations:** use button 1 to toggle work station ([e3d964c](https://github.com/aronnebrivio/homeassistant-config/commit/e3d964cce254ecb527164114a216385a05319988))
* **core:** upgrade HA to 2025.7.1 ([1b5b750](https://github.com/aronnebrivio/homeassistant-config/commit/1b5b75097f69a2d2168c7884303cc3e833d6d0ec))
* **docs:** update screenshots ([573b1ef](https://github.com/aronnebrivio/homeassistant-config/commit/573b1ef6ab6d2844f3f7c1bcbac93a14375e1bbf))
* update README.md and ui-lovelace.yaml via service ([301b12e](https://github.com/aronnebrivio/homeassistant-config/commit/301b12eefd7435f11279c2ebb5ebbcea4a5a368a))


### Bug Fixes

* remove telegram bot yaml configuration since it has been deprecated ([b180c1a](https://github.com/aronnebrivio/homeassistant-config/commit/b180c1a181ed6d17554c3cc4f3d0a3e8a2b4a05b))

## [4.9.0](https://github.com/aronnebrivio/homeassistant-config/compare/v4.8.0...v4.9.0) (2025-06-21)


### Features

* **climate:** adjust bedroom AC automation to check for opened window ([5db6c86](https://github.com/aronnebrivio/homeassistant-config/commit/5db6c86e20421195b439f84f433a541caa7fac7f))
* **custom_components:** update Adaptive Lighting via HACS ([517a220](https://github.com/aronnebrivio/homeassistant-config/commit/517a220ba96915f24d956c914bf3e24e887d84d3))
* update HA to 2025.6.1 ([34b0418](https://github.com/aronnebrivio/homeassistant-config/commit/34b04187d71d964a8e2a25d937ec241a3a145f5d))
* **z2m:** add new doors and windows sensor ([45a252d](https://github.com/aronnebrivio/homeassistant-config/commit/45a252d53ac6c0c587a435e0726ec4226e6a6323))


### Bug Fixes

* **custom_components:** use a fixed pre-release version for Generate Readme custom component ([f79d662](https://github.com/aronnebrivio/homeassistant-config/commit/f79d662b437a79daae1ed8dea6aad3e1a3e2a235))

## [4.8.0](https://github.com/aronnebrivio/homeassistant-config/compare/v4.7.0...v4.8.0) (2025-06-13)


### Features

* **automations:** review climate automations with a time trigger too ([fc27407](https://github.com/aronnebrivio/homeassistant-config/commit/fc2740750a47c28f9ee3d37f0dd245280b095e2b))
* update HA to 2025.6.0 ([19fa412](https://github.com/aronnebrivio/homeassistant-config/commit/19fa412bade5d9102415c0b5bdfc71d634f23610))
* **z2m:** use new frontend ([2de4fd5](https://github.com/aronnebrivio/homeassistant-config/commit/2de4fd5dd8e8301fbbe62785f4655c942ad92893))


### Bug Fixes

* **entities:** set kitchen AC as a cooling device ([8ca1d30](https://github.com/aronnebrivio/homeassistant-config/commit/8ca1d30620d455c9a41177c74d7a348ce22c880e))

## [4.7.0](https://github.com/aronnebrivio/homeassistant-config/compare/v4.6.0...v4.7.0) (2025-05-13)


### Features

* **dependencies:** update custom components via HACS ([f3ef44d](https://github.com/aronnebrivio/homeassistant-config/commit/f3ef44d6ab1227b58be5cd5439d9ad4fdc76ffc8))

## [4.6.0](https://github.com/aronnebrivio/homeassistant-config/compare/v4.5.0...v4.6.0) (2025-05-10)


### Features

* add Hue Dimmer Remote Switch to control livingroom lights ([c3dc08a](https://github.com/aronnebrivio/homeassistant-config/commit/c3dc08af56954dff47bd003735d859f9eaf96d64))
* **dashboard:** update dashboard yaml via service ([f312660](https://github.com/aronnebrivio/homeassistant-config/commit/f312660b69166c7d46a3da97929f4d4b98393911))
* **dependencies:** update custom components via HACS ([6973da9](https://github.com/aronnebrivio/homeassistant-config/commit/6973da9d1e91461a7c39da937be6b67a625bf0de))
* upgrade HA to 2025.5.1 ([9247271](https://github.com/aronnebrivio/homeassistant-config/commit/9247271e763ee414f832ba8152b9775c1b4620bb))


### Bug Fixes

* ignore scripts.yaml from yamllint since it's handled by HA UI ([cf9e290](https://github.com/aronnebrivio/homeassistant-config/commit/cf9e2906a86de8e36127914aaacb37e875b3dcab))

## [4.5.0](https://github.com/aronnebrivio/homeassistant-config/compare/v4.4.0...v4.5.0) (2025-03-18)


### Features

* back to RPC Shutdown to avoid depending on a Windows app to shutdown the PC ([512d9f9](https://github.com/aronnebrivio/homeassistant-config/commit/512d9f949a913240d8561c3012a8d295d6eb3c1e))
* update custom components via HACS ([9472b2c](https://github.com/aronnebrivio/homeassistant-config/commit/9472b2c6d327371eca0c4897da67fb204b87abcf))
* upgrade HA to 2025.3.3 ([25554aa](https://github.com/aronnebrivio/homeassistant-config/commit/25554aa5805c2e2f4c7dbdd746345f0930585266))
* use HA Matter Hub to locally expose entities to Alexa ([23ed1ee](https://github.com/aronnebrivio/homeassistant-config/commit/23ed1eed8ff62e864b4c07037928de62867b17f7))

## [4.4.0](https://github.com/aronnebrivio/homeassistant-config/compare/v4.3.0...v4.4.0) (2025-02-09)


### Features

* back to generic thermostat for kitchen air conditioner, since Dual Smart Thermostat does not work with same switch for heating and cooling ([159cbde](https://github.com/aronnebrivio/homeassistant-config/commit/159cbde4a443a92ad314b13e9929953cf8c761cd))
* remove Alexa shopping list related custom components ([ee9aed6](https://github.com/aronnebrivio/homeassistant-config/commit/ee9aed67ad6798d9bbd3f2cbe7ff19911a05b554))

## [4.3.0](https://github.com/aronnebrivio/homeassistant-config/compare/v4.2.0...v4.3.0) (2025-02-08)


### Features

* add alexa shopping list custom component from source ([c48e264](https://github.com/aronnebrivio/homeassistant-config/commit/c48e2648716f239611537613d7ab2b0f7768d287))
* removed scenes since were not used ([33db43b](https://github.com/aronnebrivio/homeassistant-config/commit/33db43bd86fdf125f3bdb12daf28c51ed9f6d4b2))
* **z2m:** update devices list ([b78f8e0](https://github.com/aronnebrivio/homeassistant-config/commit/b78f8e05e9b7674d1b11de3ae24565cc818f3fa0))

## [4.2.0](https://github.com/aronnebrivio/homeassistant-config/compare/v4.1.1...v4.2.0) (2025-01-26)


### Features

* upgrade custom components via HACS ([56a465b](https://github.com/aronnebrivio/homeassistant-config/commit/56a465b1f65fe11b5fb21170b27d7d0a1c9d8ce4))
* upgrade HA to 2025.1.4 ([0977e2a](https://github.com/aronnebrivio/homeassistant-config/commit/0977e2af12118bc8bf4c0e3fa7d66215b8d3ee21))

## [4.1.1](https://github.com/aronnebrivio/homeassistant-config/compare/v4.1.0...v4.1.1) (2025-01-04)


### Bug Fixes

* **adaptive_lighting:** set min color temp to 2500 to match the values supported by Tapo bulbs ([af53e57](https://github.com/aronnebrivio/homeassistant-config/commit/af53e57e04d52bb8b6dfffc4e75aea0bf4b32899))

## [4.1.0](https://github.com/aronnebrivio/homeassistant-config/compare/v4.0.0...v4.1.0) (2025-01-04)


### Features

* **entities:** testing dual_smart_thermostat custom integration ([1a352b8](https://github.com/aronnebrivio/homeassistant-config/commit/1a352b86ea6494c8a8cd5b481bef6e5bbcc2b5ba))

## [4.0.0](https://github.com/aronnebrivio/homeassistant-config/compare/v3.4.0...v4.0.0) (2025-01-04)


### ⚠ BREAKING CHANGES

* upgrade Zigbee2MQTT to 2.0.0

### Features

* **entities:** use 2 new TP-Link Tapo smart bulb for bed lights ([5b7d799](https://github.com/aronnebrivio/homeassistant-config/commit/5b7d799636911a6d6290a1c53a0f48b26ecd5a27))
* upgrade HA to 2025.1.0 ([8b741ef](https://github.com/aronnebrivio/homeassistant-config/commit/8b741ef00f949703be19b1a979d08bbed785b926))
* use Tapo Controller custom component to locally control Tapo smart bulbs ([28a9c56](https://github.com/aronnebrivio/homeassistant-config/commit/28a9c56766e2e6ecb044c88dfe34c06e1e64ba44))


### Bug Fixes

* **entities:** TEMP disable ac_mode to kitchen air conditioner to use it for heating ([b347497](https://github.com/aronnebrivio/homeassistant-config/commit/b3474979c001f28e249b3c238ad2502e4f6c32f2))


### Miscellaneous Chores

* upgrade Zigbee2MQTT to 2.0.0 ([8576f93](https://github.com/aronnebrivio/homeassistant-config/commit/8576f931e498fe1a384131ded62ee36fcb0f8d8d))

## [3.4.0](https://github.com/aronnebrivio/homeassistant-config/compare/v3.3.0...v3.4.0) (2024-12-22)


### Features

* update HA to 2024.12.5 ([cfa4778](https://github.com/aronnebrivio/homeassistant-config/commit/cfa4778f365417c27aa3db26a2a6e2eaea055b74))


### Bug Fixes

* **lovelace:** remove whitespaces between value and unit of measure ([085d019](https://github.com/aronnebrivio/homeassistant-config/commit/085d0190471e81407a449c1a455726fd0efffc83))

## [3.3.0](https://github.com/aronnebrivio/homeassistant-config/compare/v3.2.0...v3.3.0) (2024-11-24)


### Features

* upgrade HA to 2024.11.3 ([2d9f447](https://github.com/aronnebrivio/homeassistant-config/commit/2d9f44719c4aabcf746ff74b09b2a012c6bd7191))


### Bug Fixes

* **esp-home:** expose Restart button on esp32-01 ([6050a90](https://github.com/aronnebrivio/homeassistant-config/commit/6050a900cc7d7dc078ec5546b0aeb8cd727d0cd7))

## [3.2.0](https://github.com/aronnebrivio/homeassistant-config/compare/v3.1.0...v3.2.0) (2024-11-13)


### Features

* **lovelace:** more tiles instead of custom components. Reviewed stats view. ([5aeb3a9](https://github.com/aronnebrivio/homeassistant-config/commit/5aeb3a981bb0fd258ae6c95ee7d84ff42d06519b))

## [3.1.0](https://github.com/aronnebrivio/homeassistant-config/compare/v3.0.0...v3.1.0) (2024-11-12)


### Features

* **lovelace:** use better-thermostat and tile cards, add devices view ([9078551](https://github.com/aronnebrivio/homeassistant-config/commit/907855139d5832afc6d004f0e0194008310b7b9f))

## [3.0.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.43.0...v3.0.0) (2024-11-10)


### ⚠ BREAKING CHANGES

* review Lovelace dashboard using sections
* cleanup lot of unused components due to switch to single sections dashboard

### Features

* add notifications for indoor vs outdoor AQI ([f870c39](https://github.com/aronnebrivio/homeassistant-config/commit/f870c39b8741d33bebd6859928c9a2535436bcf3))
* add secret for WAQI integration ([164cab7](https://github.com/aronnebrivio/homeassistant-config/commit/164cab79d025bc3b85249b4293d0ab8323fe6a62))
* update HA to 2024.11.1 ([385860a](https://github.com/aronnebrivio/homeassistant-config/commit/385860a0900dd70ba26ce0ad011e884b2f721b83))


### Code Refactoring

* cleanup lot of unused components due to switch to single sections dashboard ([bdd0e6a](https://github.com/aronnebrivio/homeassistant-config/commit/bdd0e6a8bdf8ea3462fc8c0f0754d510c530940e))
* review Lovelace dashboard using sections ([33dfba6](https://github.com/aronnebrivio/homeassistant-config/commit/33dfba6e2c0ab2305ce984a10392e3b737ae4e2c))

## [2.43.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.42.0...v2.43.0) (2024-11-02)


### Features

* **air-quality:** add entities to measure air quality via ESPHome and calculate AQI from PM2.5 ([f786179](https://github.com/aronnebrivio/homeassistant-config/commit/f7861795ad3061081762562dec2c5092dc11a397))
* **air-quality:** review web and mobile dashboards to view air quality data ([25145a4](https://github.com/aronnebrivio/homeassistant-config/commit/25145a4a07182e8285b3099acdd7c8ed25e54332))
* **automations:** add vetrina ingresso NFC toggle and review bed lights tag ([1bf3f09](https://github.com/aronnebrivio/homeassistant-config/commit/1bf3f09eaebfe344a202232fe03bb074fe7248f9))
* update HA to 2024.10.4 ([5f7782b](https://github.com/aronnebrivio/homeassistant-config/commit/5f7782b0e7af98f3cb0766b4d8d74c4c9c232cbe))


### Bug Fixes

* remove unused include ([69b62f3](https://github.com/aronnebrivio/homeassistant-config/commit/69b62f3997ba2574c38bf3348561fe8b40baf673))

## [2.42.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.41.0...v2.42.0) (2024-10-12)


### Features

* add Sensor.Community integration for air quality sensors ([96260be](https://github.com/aronnebrivio/homeassistant-config/commit/96260be9ff4705a5a807e17efdddae2f752194b9))
* remove Cloudflared add-on ([b5aafc1](https://github.com/aronnebrivio/homeassistant-config/commit/b5aafc1299798457090dbd36ab79be90001603ad))
* remove RPC Shutdown add-on ([27871e1](https://github.com/aronnebrivio/homeassistant-config/commit/27871e1447ab13fd784f3129db83ada15c5b8d70))
* use button created by HASS.Agent instead of RPCShutdown to turn off PC ([a488ce6](https://github.com/aronnebrivio/homeassistant-config/commit/a488ce673cea34aef8a557f0fba0014e63c66439))
* use smart plug 1 for bedroom mosquitto repellent ([81a8169](https://github.com/aronnebrivio/homeassistant-config/commit/81a8169dd2a13e72499ac35fb4e2d57b5875ad80))

## [2.41.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.40.0...v2.41.0) (2024-10-12)


### Features

* include additional custom dashboards json files from .storage folder ([83a3076](https://github.com/aronnebrivio/homeassistant-config/commit/83a30766abf847124153f579420e756a65719371))
* review esp8266-01 configuration and use as Master Sword switch instead of a smat plug ([9bfa1cd](https://github.com/aronnebrivio/homeassistant-config/commit/9bfa1cd8e153729c0d2407594725210c112db3fd))


### Bug Fixes

* use Python 3.12 to execute esphome configuration check ([d0a8b3b](https://github.com/aronnebrivio/homeassistant-config/commit/d0a8b3b2e53c5bbec511dccd60dfc64365366ced))

## [2.40.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.39.0...v2.40.0) (2024-10-11)


### Features

* review CI workflow ([3e745c4](https://github.com/aronnebrivio/homeassistant-config/commit/3e745c4632590cefa260a2c5464db594a6e9868f))

## [2.39.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.38.0...v2.39.0) (2024-10-11)


### Features

* add ESPHome add-on and first test configuration ([4bcee4c](https://github.com/aronnebrivio/homeassistant-config/commit/4bcee4c1b231b8d9a274eea9e90db30436454866))
* new CPU, RAM and Storage sensor cards ([3dcc848](https://github.com/aronnebrivio/homeassistant-config/commit/3dcc8482c118e80e623a097ac0517ae5f587df74))
* update custom components via HACS ([52a2e9e](https://github.com/aronnebrivio/homeassistant-config/commit/52a2e9e16686cc3836ddf67be64941e20ef2b653))
* update HA to 2024.10.2 ([ae217f0](https://github.com/aronnebrivio/homeassistant-config/commit/ae217f09e89dc5ebd4ba5f5e5fe8ee685860e55c))
* update Wallpanel via HACS ([2d70704](https://github.com/aronnebrivio/homeassistant-config/commit/2d707047303644805e4afea888dbf0e18bd47314))
* upgrade HA to 2024.10.1 ([d40551c](https://github.com/aronnebrivio/homeassistant-config/commit/d40551c3aea2837f26be2610da52da005f4ba516))

## [2.38.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.37.0...v2.38.0) (2024-09-27)


### Features

* update README and ui-lovelace.yaml via service ([1410b89](https://github.com/aronnebrivio/homeassistant-config/commit/1410b89612dfa949c7a3713eb1b5d4c009be2918))
* upgrade HA to 2024.9.3 ([099ea15](https://github.com/aronnebrivio/homeassistant-config/commit/099ea1586c64a5281f126da4b9e953f36913cb52))

## [2.37.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.36.0...v2.37.0) (2024-09-23)


### Features

* update multiple custom components via HACS ([76f4e30](https://github.com/aronnebrivio/homeassistant-config/commit/76f4e306ccb645f98f811e3d79e0ba3a9047e311))
* update themes via HACS ([eeddcc6](https://github.com/aronnebrivio/homeassistant-config/commit/eeddcc654bfeae42d1facc251cc47da0a5ee166c))
* upgrade HA to 2024.9.2 ([09a804f](https://github.com/aronnebrivio/homeassistant-config/commit/09a804f735d5fb4b7fd2a53f24269f6d043c8c5e))

## [2.36.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.35.0...v2.36.0) (2024-08-11)


### Features

* add Spook Inverse, provided via Spook ([2d8560b](https://github.com/aronnebrivio/homeassistant-config/commit/2d8560bd42a0cd8db837a7a2d20068d1bece85d6))
* add Spook via HACS ([d62ecd9](https://github.com/aronnebrivio/homeassistant-config/commit/d62ecd97261b92f894aab0239f92745f85613dda))
* remove DuckDNS integration ([f7d8af3](https://github.com/aronnebrivio/homeassistant-config/commit/f7d8af350c6f21bcb0c22dfd927894be3476b438))
* review automations ([f2392fd](https://github.com/aronnebrivio/homeassistant-config/commit/f2392fd950d4cdbd1aa0106a4a2967d6ad002308))
* update Alexa Media Player via HACS ([cb19529](https://github.com/aronnebrivio/homeassistant-config/commit/cb19529ec3a801f357af79dae7f67d51d5e818d0))
* update Comfortable Environment Card via HACS ([eeb04a4](https://github.com/aronnebrivio/homeassistant-config/commit/eeb04a4862c762c6a3ef16cd9a267768c4750797))
* update HA to 2024.8.1 ([8ae4f5d](https://github.com/aronnebrivio/homeassistant-config/commit/8ae4f5df84ab55073bdcb4055eb945e15c9f5a43))
* update Lovelace Wallpanel via HACS ([999506d](https://github.com/aronnebrivio/homeassistant-config/commit/999506d005f865babed86e921e0015c4ff3bc659))
* update Mushrooms via HACS ([23b0aaf](https://github.com/aronnebrivio/homeassistant-config/commit/23b0aaf3983a2ba19148eabf4a14bc74bc9a4fa9))
* update Spotcast via HACS ([04668a7](https://github.com/aronnebrivio/homeassistant-config/commit/04668a78acb202a9a6dd5577482fd0d3978efc78))
* update Waste Collection Schedule via HACS ([5997c6f](https://github.com/aronnebrivio/homeassistant-config/commit/5997c6f523d52f6878c230996ed83056bc1dd4c2))


### Bug Fixes

* reset bedroom thermometer device ([6b107d4](https://github.com/aronnebrivio/homeassistant-config/commit/6b107d4d69cb75be6885f5152837a349ec8fb673))
* set kitchen air conditioner in the correct group ([9cdbc76](https://github.com/aronnebrivio/homeassistant-config/commit/9cdbc76a9b4d72958a9d8dd6fbf5167be7c19e67))

## [2.35.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.34.0...v2.35.0) (2024-05-28)


### Features

* update Adaptive Lighting via HACS ([1753f81](https://github.com/aronnebrivio/homeassistant-config/commit/1753f81161ce1580a9514ca5e5617b0bc68d2d0b))
* update Alexa Media Player via HACS ([54baabe](https://github.com/aronnebrivio/homeassistant-config/commit/54baabe694ade52365d30b3d7a1c3450a5c2e6e6))
* update Comfortable Environment Card via HACS ([13ac20c](https://github.com/aronnebrivio/homeassistant-config/commit/13ac20c7890b166777b398506348fdb79bbe81b4))
* update HA to 2024.5.5 ([f4a025b](https://github.com/aronnebrivio/homeassistant-config/commit/f4a025bd57383f376ef5757a4fae377cf5ce1d1e))
* update Lovelace Wallpanel via HACS ([6e715e5](https://github.com/aronnebrivio/homeassistant-config/commit/6e715e53c953cb31b54e5e0543a2b45f007b1471))
* update README and ui-lovelace.yaml via service ([d3122ad](https://github.com/aronnebrivio/homeassistant-config/commit/d3122ad555ecb4e28195c74eda32bd247e91474a))
* update Waste Collection Schedule via HACS ([b349fcf](https://github.com/aronnebrivio/homeassistant-config/commit/b349fcf80d38260075206d9fb43b4052f09c9257))

## [2.34.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.33.0...v2.34.0) (2024-04-25)


### Features

* update Adaptive Lighting via HACS ([19579c3](https://github.com/aronnebrivio/homeassistant-config/commit/19579c331966f94b7267fc94f3c063c69aa7da23))
* update HA to 2024.4.4 ([d60c26e](https://github.com/aronnebrivio/homeassistant-config/commit/d60c26eded0705c70bb70951044d9db6b4fbda89))
* update UI components via HACS ([30fc254](https://github.com/aronnebrivio/homeassistant-config/commit/30fc254e18cc8b5556bdb1beb46039ce66414332))
* update Waste Collection Schedule via HACS ([8bde631](https://github.com/aronnebrivio/homeassistant-config/commit/8bde63100293ebce024d0ba2ae9828b391305e35))

## [2.33.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.32.0...v2.33.0) (2024-03-15)


### Features

* update Comfortable Environment Card via HACS ([763a691](https://github.com/aronnebrivio/homeassistant-config/commit/763a691f5248ed060d4e84e14055b1e396db1c83))
* update HA to 2024.3.1 ([b24adff](https://github.com/aronnebrivio/homeassistant-config/commit/b24adffbb190a47d85ff3bd7dde477de2fb3175b))
* update Lovelace Layout Card via HACS ([33f1434](https://github.com/aronnebrivio/homeassistant-config/commit/33f1434d6613629c7594cb13983ea779e1022e1a))
* update Lovelace Mushroom via HACS ([a082d2e](https://github.com/aronnebrivio/homeassistant-config/commit/a082d2ee45498a3a13f642e549524540634c31df))
* update Lovelace Wallpanel via HACS ([f980985](https://github.com/aronnebrivio/homeassistant-config/commit/f980985e52b64bba3527c43a7145a915dcbc149b))
* update README via service ([e579290](https://github.com/aronnebrivio/homeassistant-config/commit/e57929077c19c54862d5047bb81fe994b9105596))
* update Spotcast via HACS ([5b45387](https://github.com/aronnebrivio/homeassistant-config/commit/5b453870a5f1aeb68621079e47496b0564db2946))
* update Waste Collection Schedule via HACS ([cb94e53](https://github.com/aronnebrivio/homeassistant-config/commit/cb94e5357829ee9656faca4db86a72110191b138))


### Bug Fixes

* set thermometer icon for home temperature sensor ([2e347e3](https://github.com/aronnebrivio/homeassistant-config/commit/2e347e3b37253f9ecf4378025648e0db3b395aca))

## [2.32.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.31.0...v2.32.0) (2024-02-17)


### Features

* remove ddeprecated beat attribute to datetime sensor ([c0eb632](https://github.com/aronnebrivio/homeassistant-config/commit/c0eb63256bc69a23a1d96fceae5768d62b4dca01))
* update Alexa Media Player via HACS ([c7166ff](https://github.com/aronnebrivio/homeassistant-config/commit/c7166ffb49c3a4f3f7b2e239bbc2f009a6478e84))
* update Comfortable Environment Card via HACS ([5d5fab0](https://github.com/aronnebrivio/homeassistant-config/commit/5d5fab068d848f54e18c18df04cc2bcd12856881))
* update HA to 2024.2.2 ([25b6480](https://github.com/aronnebrivio/homeassistant-config/commit/25b6480d164a7c74af7554641e98b01944e450fc))
* update HACS via HACS ([082751e](https://github.com/aronnebrivio/homeassistant-config/commit/082751e3cdd4f83e4665936a47b9e38cb7f03b4b))
* update Lovelace Mushroom via HACS ([86bc26c](https://github.com/aronnebrivio/homeassistant-config/commit/86bc26cdbf07f37df9d46a15cc97f0e5e7610a12))
* update Lovelace Wallpanel via HACS ([e529685](https://github.com/aronnebrivio/homeassistant-config/commit/e529685c8514720d352a11ed54981806f5c584e8))
* update Mini Graph Card via HACS ([cb87fb8](https://github.com/aronnebrivio/homeassistant-config/commit/cb87fb8fce88313c68dccc9e2960dacf705a0ecb))
* update Waste Collection Schedule via HACS ([32f8f13](https://github.com/aronnebrivio/homeassistant-config/commit/32f8f13eca7ad47ec28b631287dda60180dc42d1))

## [2.31.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.30.0...v2.31.0) (2024-01-13)


### Features

* update Alexa Media Player via HACS ([6da13b8](https://github.com/aronnebrivio/homeassistant-config/commit/6da13b8e044bb839e3191e76713f4edc97792925))
* update Comfortable Environment Card via HACS ([ee990f5](https://github.com/aronnebrivio/homeassistant-config/commit/ee990f55bdf8f8dc048198659d870bceb1d45fdc))
* update HA to 2024.1.3 ([b0a7d16](https://github.com/aronnebrivio/homeassistant-config/commit/b0a7d164cd3a9d18ba98d541dda3870105201c48))
* update Lovelace Mushroom via HACS ([6b76419](https://github.com/aronnebrivio/homeassistant-config/commit/6b764195097b07bbd1b3d5d9f2105d8a062b26cc))
* update Lovelace Wallpanel via HACS ([289b3cd](https://github.com/aronnebrivio/homeassistant-config/commit/289b3cd7d2b563c212f5514480a616c9843bcd21))
* update README and ui-lovelace.yaml via service ([6db28d9](https://github.com/aronnebrivio/homeassistant-config/commit/6db28d9bf8cd2586bcd24ccda8cc2266d2078f1e))
* update Thermal Comfort via HACS ([20bb41d](https://github.com/aronnebrivio/homeassistant-config/commit/20bb41da1cf1b5288cd56d34c1b2e7c97a057c6c))

## [2.30.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.29.0...v2.30.0) (2023-12-28)


### Features

* add Comfortable Environment Card via HACS ([fa5c6b9](https://github.com/aronnebrivio/homeassistant-config/commit/fa5c6b9efa39ce5b30cc79a7b268446f6aaf949b))
* update HA to 2023.12.4 ([4048c3e](https://github.com/aronnebrivio/homeassistant-config/commit/4048c3e778433b01a9d935290b4742d744db7997))
* update Lovelace Wallpanel via HACS ([f053a9b](https://github.com/aronnebrivio/homeassistant-config/commit/f053a9b007b1076b1ea330dbc6c7b743c0dce810))
* update README and ui-lovelace.yaml via service ([146b6fe](https://github.com/aronnebrivio/homeassistant-config/commit/146b6fec478fb7427bac8d3b7695061675ef658f))

## [2.29.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.28.0...v2.29.0) (2023-12-19)


### Features

* add temperature and humidity sensors for bathroom and kitchen ([d1cbc4d](https://github.com/aronnebrivio/homeassistant-config/commit/d1cbc4d50229774fa41f236d62bcbc639968c37c))
* add Thermal Comfort via HACS ([7557a22](https://github.com/aronnebrivio/homeassistant-config/commit/7557a22d9fbcb90700f1aa5bf34ada32c4820757))
* include kitchen and bathroom temperature and humidity to calculate hom mean values ([2426347](https://github.com/aronnebrivio/homeassistant-config/commit/242634762cc9576d4b841edb3d7334946eea90ce))
* remove home absolute humidity custom template sensor since the value is now provided by Thermal Comfort integration ([603f577](https://github.com/aronnebrivio/homeassistant-config/commit/603f577ae986556c349df8bf0482d306277c3bcb))
* update Adaptive Lighting via HACS ([a7f8fe2](https://github.com/aronnebrivio/homeassistant-config/commit/a7f8fe2fa2e6ba3d3d52f0c2192b2c0b17127868))
* update Alexa Media via HACS ([75027a4](https://github.com/aronnebrivio/homeassistant-config/commit/75027a41351013575e7a81a030a542fdc03ef109))
* update HA to 2023.12.3 ([f3bd8b8](https://github.com/aronnebrivio/homeassistant-config/commit/f3bd8b8c12bcd3836798e4e80f32821c744a7ae4))
* update README.md and ui-lovelace.yaml via service ([1908c27](https://github.com/aronnebrivio/homeassistant-config/commit/1908c271b00e765d4bf3833f9349478f1b607ca2))
* update SmartIR via HACS ([7e80c4c](https://github.com/aronnebrivio/homeassistant-config/commit/7e80c4cd97c721dd837493d1f4a3625c7c897a9c))
* use new temperature sensor for kitchen air conditioner ([c7c07f8](https://github.com/aronnebrivio/homeassistant-config/commit/c7c07f8eba1f84c1417764ec91015b951e3d4756))

## [2.28.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.27.0...v2.28.0) (2023-12-06)


### Features

* remove ping sensor from YAML since deprecated and replaced by Ping integration ([86dd469](https://github.com/aronnebrivio/homeassistant-config/commit/86dd4690eb9a20c929a48d1a557b4eb4ff6866b2))
* update Alexa Media via HACS ([535fc83](https://github.com/aronnebrivio/homeassistant-config/commit/535fc83882d927903f2f68e0e1373573d1f86842))
* update HA to 2023.12.0 ([49a94d7](https://github.com/aronnebrivio/homeassistant-config/commit/49a94d71664f353af8909981dc42c3c4d3de6e96))
* update Waste Collection Schedule via HACS ([10c3e75](https://github.com/aronnebrivio/homeassistant-config/commit/10c3e75035ffabe0cdec948904d325e64148bfc8))

## [2.27.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.26.0...v2.27.0) (2023-11-27)


### Features

* add Christmas Time date sensor ([d68b335](https://github.com/aronnebrivio/homeassistant-config/commit/d68b335f796acdeee385c8505b3402fd64a95f13))
* add Christmas Tree switch ([eb7711f](https://github.com/aronnebrivio/homeassistant-config/commit/eb7711f5bd870868ebf36fee01d775b5ad69ec87))
* add new smart plug to Zigbee2MQTT ([38039cc](https://github.com/aronnebrivio/homeassistant-config/commit/38039ccd7b6d7e24d25a7012a14540824d079e2f))
* update Lovelace Wallpanel via HACS ([0363e9b](https://github.com/aronnebrivio/homeassistant-config/commit/0363e9be3921cd1dc51fa748f1df3494f1de4968))
* update README and ui-lovelace.yaml via service ([23badf9](https://github.com/aronnebrivio/homeassistant-config/commit/23badf97a8c5a6110fd4f71297b4c97118904c63))

## [2.26.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.25.0...v2.26.0) (2023-11-25)


### Features

* update HA to 2023.11.3 ([dbb2904](https://github.com/aronnebrivio/homeassistant-config/commit/dbb2904f65eac41e051e1b240961d9df022d1bc3))
* update Lovelace Wallpanel via HACS ([d272a61](https://github.com/aronnebrivio/homeassistant-config/commit/d272a61fa5400b1eaf53b8429ee66afbbaa1a6cf))

## [2.25.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.24.1...v2.25.0) (2023-11-16)


### Features

* add mold indicator sensor ([7f14aca](https://github.com/aronnebrivio/homeassistant-config/commit/7f14aca51416ef70c1e107da01a9b9d7a1cfa20b))
* update README.md and ui-lovelace.yaml via service ([6f8b7f6](https://github.com/aronnebrivio/homeassistant-config/commit/6f8b7f681f54ea0eeb283054907aafaf779f473a))


### Bug Fixes

* make notifications for HA updates working again ([e12c564](https://github.com/aronnebrivio/homeassistant-config/commit/e12c5647e4589d96705ea90ac36b9082cff597ea))

## [2.24.1](https://github.com/aronnebrivio/homeassistant-config/compare/v2.24.0...v2.24.1) (2023-11-15)


### Bug Fixes

* make Home Assistant read template entities correctly ([1186cae](https://github.com/aronnebrivio/homeassistant-config/commit/1186cae9b5bc0e04f9ce123d57c88714ab68254b))

## [2.24.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.23.0...v2.24.0) (2023-11-14)


### Features

* add all new files to configuration ([1746801](https://github.com/aronnebrivio/homeassistant-config/commit/17468011146692808fa44d55db335cd4ff99b92f))
* add entities to retrieve external temperature and humidity from Met.no ([1bdda52](https://github.com/aronnebrivio/homeassistant-config/commit/1bdda52e64b4b87df38fdaee8e5bb9bcafc55cd6))
* add Jinja macro to calculate absolute humidity ([80a3aab](https://github.com/aronnebrivio/homeassistant-config/commit/80a3aab6e4fe1a1fb27beaf43cb830c53b2d7526))
* add template to calculate internal and external absolute humidity and provide it as sensor ([3e49689](https://github.com/aronnebrivio/homeassistant-config/commit/3e49689e8c1e94a37174ede618917bc8aea4e247))
* update Alexa Media Player via HACS ([13572d4](https://github.com/aronnebrivio/homeassistant-config/commit/13572d41944f6f2d05ead753164d990ffca5746a))
* update Garbage Collection Card via HACS ([260a1d7](https://github.com/aronnebrivio/homeassistant-config/commit/260a1d76bd48be147ca72cccc158e4339e44a80f))
* update HA to 2023.11.2 ([879b0ab](https://github.com/aronnebrivio/homeassistant-config/commit/879b0abd655a3641f76017bbb5b6b2c5bdc94200))
* update Lovelace Wallpanel via HACS ([030b9ba](https://github.com/aronnebrivio/homeassistant-config/commit/030b9baf42aa0a9a6698409549dae8da630f79f1))
* update README and ui-lovelace.yaml via service ([3734b0d](https://github.com/aronnebrivio/homeassistant-config/commit/3734b0da16c7d1fcde108655f9576282a8002c90))


### Bug Fixes

* CRLF to LF to pass YAML lint ([e7fbd08](https://github.com/aronnebrivio/homeassistant-config/commit/e7fbd08bb76a5a45abf3bb31a302e587a2149aec))

## [2.23.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.22.0...v2.23.0) (2023-11-03)


### Features

* update HA version to 2023.11.0 ([4d95730](https://github.com/aronnebrivio/homeassistant-config/commit/4d957305d7d7cdc91b10e0860bc4353b6965bfc8))
* update Lovelace Mushroom via HACS ([a0da721](https://github.com/aronnebrivio/homeassistant-config/commit/a0da721b8e0ce3a7d0502f3a967f52b269c00e8c))
* update Lovelace Wallpanel via HACS ([119c078](https://github.com/aronnebrivio/homeassistant-config/commit/119c0787e4829b8da331d953da789f9624a1e026))

## [2.22.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.21.0...v2.22.0) (2023-10-29)


### Features

* **smartir:** add heat codes for Air Nova from 20C to 30C ([beaeffa](https://github.com/aronnebrivio/homeassistant-config/commit/beaeffa85b9bf581471f8a173ffedc9e60f3240b))

## [2.21.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.20.0...v2.21.0) (2023-10-26)


### Features

* update HA version to 2023.10.5 ([3a51d30](https://github.com/aronnebrivio/homeassistant-config/commit/3a51d30e885df59d67c24cb896c60e4e5e697d3e))

## [2.20.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.19.0...v2.20.0) (2023-10-18)


### Features

* revert DuckDNS removal, keep both DuckDNS and Cloudflare Tunnel ([b9f8f80](https://github.com/aronnebrivio/homeassistant-config/commit/b9f8f80e886dd5710946afc7aacf26b9cbc99868))
* switch from DuckDNS to Cloudflare ([1c6075a](https://github.com/aronnebrivio/homeassistant-config/commit/1c6075a4b8ac2c9c56964529cabe774315f89645))
* update Waster Collection Schedule via HACS ([74ea7c2](https://github.com/aronnebrivio/homeassistant-config/commit/74ea7c2b32123fe007cbcc4415e5dd2eb0bc1bb1))

## [2.19.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.18.0...v2.19.0) (2023-10-14)


### Features

* update Alexa Media Player via HACS ([b98ce97](https://github.com/aronnebrivio/homeassistant-config/commit/b98ce9714c66812be1039e964d1a1f10f8c6be28))
* update HA version to 2023.10.3 ([b894b93](https://github.com/aronnebrivio/homeassistant-config/commit/b894b938bb72cbd5d30d197b31499522295583d1))

## [2.18.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.17.0...v2.18.0) (2023-10-07)


### Features

* update Alexa Media Player via HACS ([0d87461](https://github.com/aronnebrivio/homeassistant-config/commit/0d87461d1666e9d769d8a2d7cddc3a494b3955af))
* update HA version to 2023.10.1 ([1f7d356](https://github.com/aronnebrivio/homeassistant-config/commit/1f7d3567fdbee2fd3f0783fd51bddad19d610ca7))
* update Hacs via Hacs ([559da59](https://github.com/aronnebrivio/homeassistant-config/commit/559da59fa9bec9fabd5a29f1c69d5b27e74b7330))
* update SmartIR via HACS ([3faa8ad](https://github.com/aronnebrivio/homeassistant-config/commit/3faa8ad25b409a22465ba17c3845a01e8035acc5))

## [2.17.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.16.0...v2.17.0) (2023-09-18)


### Features

* update alexa media player via HACS ([375d9e1](https://github.com/aronnebrivio/homeassistant-config/commit/375d9e1937f3f04522a553cdcf7cd040d4bae7c1))
* update lovelace wallpanel via HACS ([a3afca3](https://github.com/aronnebrivio/homeassistant-config/commit/a3afca3f07ac01a0914998cd2d122203308b19b6))

## [2.16.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.15.0...v2.16.0) (2023-09-15)


### Features

* update alexa media player via HACS ([b21a89f](https://github.com/aronnebrivio/homeassistant-config/commit/b21a89fb0a8b0e2cd11525f12a0ad180b862613a))
* update README via service ([fb408f4](https://github.com/aronnebrivio/homeassistant-config/commit/fb408f40e4cdf690a4634b8b2c15c110f8819b41))

## [2.15.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.14.0...v2.15.0) (2023-09-13)


### Features

* update HA version to 2023.9.2 ([7ddb465](https://github.com/aronnebrivio/homeassistant-config/commit/7ddb465cfa54496112a94a371d69fc79b6feb5db))

## [2.14.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.13.0...v2.14.0) (2023-09-12)


### Features

* update HA version to 2023.9.1 ([664eb3d](https://github.com/aronnebrivio/homeassistant-config/commit/664eb3d25e611240663581de46d25e88bbe702e6))
* update spotcast via HACS ([7e61710](https://github.com/aronnebrivio/homeassistant-config/commit/7e61710a3b113c8c17448b7acb93ce14396e9cdd))

## [2.13.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.12.0...v2.13.0) (2023-09-07)


### Features

* update HA version to 2023.9.0 ([1290f17](https://github.com/aronnebrivio/homeassistant-config/commit/1290f171540a8d3b059634d9134449f7457ff437))
* update lovelace-mushroom via HACS ([0b0d92e](https://github.com/aronnebrivio/homeassistant-config/commit/0b0d92e38fcf7a12090460fd346fa88f14f5d698))

## [2.12.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.11.0...v2.12.0) (2023-09-01)


### Features

* update Waster Collection Schedule via HACS ([cbd543e](https://github.com/aronnebrivio/homeassistant-config/commit/cbd543edc79f7891f204961e6851d8b10aec973c))

## [2.11.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.10.0...v2.11.0) (2023-08-29)


### Features

* add Todoist Shopping List custom integration ([2a678f2](https://github.com/aronnebrivio/homeassistant-config/commit/2a678f2debc6642603525a6030ae33d2639c6f88))
* remote pyscript and manual script to sync shopping list with Todoist ([fae5445](https://github.com/aronnebrivio/homeassistant-config/commit/fae54450ba1e13d1592bce7aaaefc3a08f7bfe98))
* remove old automation to sync shopping list with Todoist ([2249692](https://github.com/aronnebrivio/homeassistant-config/commit/224969244e5c7f550f2b46fbfad8ecbfca238cd5))

## [2.10.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.9.0...v2.10.0) (2023-08-27)


### Features

* configure Garbage Collection calendar, integration and sensors ([9c0480a](https://github.com/aronnebrivio/homeassistant-config/commit/9c0480aa09a9ef5d77346e9ef3c0a8d1876c3d29))
* review Garbage Collection Tomorrow automation with new binary sensor ([954f0d9](https://github.com/aronnebrivio/homeassistant-config/commit/954f0d9906f844777ab3cb17787743a802766cc7))
* update README and ui-lovelace.yaml via service ([240d711](https://github.com/aronnebrivio/homeassistant-config/commit/240d711c88f49ccb8b0097fb3dee44ab25ea0b5d))
* update readme template and Lovelace screenshots ([22e9070](https://github.com/aronnebrivio/homeassistant-config/commit/22e907006f020d480f7d6b164ef2e3065a552ffd))

## [2.9.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.8.0...v2.9.0) (2023-08-25)


### Features

* add Waste Collection Schedule via HACS ([2e8df65](https://github.com/aronnebrivio/homeassistant-config/commit/2e8df6596991741688700b6c81f57636b7138304))
* bump HA_VERSION to 2023.8.2 ([6e13f34](https://github.com/aronnebrivio/homeassistant-config/commit/6e13f34ed9cb3c98de98a835fc41ffc768d4b160))
* update adaptive lighting via HACS ([242ea45](https://github.com/aronnebrivio/homeassistant-config/commit/242ea45bc1b3072c3e053d56d161101221389dc0))
* update HA version to 2023.8.4 ([6623cb5](https://github.com/aronnebrivio/homeassistant-config/commit/6623cb5a41109baf274b41828f35a1659c5d7e28))
* update readme ([9be04b2](https://github.com/aronnebrivio/homeassistant-config/commit/9be04b2dc0dc86b2632e3bd634a7b4fe793a88fc))

## [2.8.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.7.0...v2.8.0) (2023-08-06)


### Features

* add and enable Generate Readme component ([e352a83](https://github.com/aronnebrivio/homeassistant-config/commit/e352a837c2a4284f16c353e1f746578749c84f8a))
* add autogenerated readme and ui-lovelace.yaml ([da2f922](https://github.com/aronnebrivio/homeassistant-config/commit/da2f9229de49c14b38a395034721ec12fc6c7003))
* remove old lovelace YAML configuration ([7c6df54](https://github.com/aronnebrivio/homeassistant-config/commit/7c6df54f7b70e3943ee675da8d6c426583f2ae9d))
* update Generate Readme template ([df6c6cb](https://github.com/aronnebrivio/homeassistant-config/commit/df6c6cbc53534f165cff62ca67da5e9814b3a7c6))


### Bug Fixes

* exclude ui-lovelace.yaml from linting since it's autogenerated ([0f15d32](https://github.com/aronnebrivio/homeassistant-config/commit/0f15d32e38e9ba5b73491cac25397bfddf63eafa))
* resolve YAMLLint warning ([f25d53a](https://github.com/aronnebrivio/homeassistant-config/commit/f25d53ae1c2dbccbcefa6483f07b6fabecd632ea))

## [2.7.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.6.1...v2.7.0) (2023-08-06)


### Features

* update Adaptive Lighting via HACS ([5769e25](https://github.com/aronnebrivio/homeassistant-config/commit/5769e25af87a2dc6c78711bbe0f57ab8cfb4ec4c))
* update HA version to 2023.8.1 ([a28804b](https://github.com/aronnebrivio/homeassistant-config/commit/a28804bba239e11ccc4a4ae045036a96a5277f6e))

## [2.6.1](https://github.com/aronnebrivio/homeassistant-config/compare/v2.6.0...v2.6.1) (2023-07-30)


### Bug Fixes

* update Pyscript via HACS, fix test against HA dev and beta ([87e5366](https://github.com/aronnebrivio/homeassistant-config/commit/87e53663d3c7363d3bf9cfc7def1c538c9302c8c))

## [2.6.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.5.0...v2.6.0) (2023-07-30)


### Features

* update AC SmartIR codes to support up to 25°C ([8b39ab7](https://github.com/aronnebrivio/homeassistant-config/commit/8b39ab7335faae4e56de64351fcced115c1a8224))
* update climate automations for bedroom v2 ([285d4af](https://github.com/aronnebrivio/homeassistant-config/commit/285d4afe70ebf2a5360387d70787d6d447e99add))

## [2.5.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.4.0...v2.5.0) (2023-07-27)


### Features

* update climate automations for bedroom ([a07308f](https://github.com/aronnebrivio/homeassistant-config/commit/a07308f3b46d4a37a4b32e26f899b0938cd75c69))

## [2.4.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.3.0...v2.4.0) (2023-07-21)


### Features

* update adaptive lighting via HACS ([dee02bf](https://github.com/aronnebrivio/homeassistant-config/commit/dee02bf10c76509e78748454deb515bae34b9ece))
* update HA version to 2023.7.3 ([f0ae58c](https://github.com/aronnebrivio/homeassistant-config/commit/f0ae58c7b7eafbfee01bed8a33b4c8fc26d42165))
* update Mushrooms via HACS ([545e80f](https://github.com/aronnebrivio/homeassistant-config/commit/545e80fdc56e0fbab844b13e4a904a7bdaa1e986))

## [2.3.0](https://github.com/aronnebrivio/homeassistant-config/compare/v2.2.0...v2.3.0) (2023-07-18)


### Features

* add release-please github action ([b78f6b1](https://github.com/aronnebrivio/homeassistant-config/commit/b78f6b1b388a716bc298f8f40d9f2c8ca2ba2197))
* update HA version to 2023.7.2 ([790991e](https://github.com/aronnebrivio/homeassistant-config/commit/790991e5bfd9d356910f108403b15083efb95da8))
* update lovelace-mushroom via HACS ([800deaa](https://github.com/aronnebrivio/homeassistant-config/commit/800deaa38f99961c673ba0119a89d7e40280270a))


### Bug Fixes

* review climate IR commands to make 15C works ([4b5ea71](https://github.com/aronnebrivio/homeassistant-config/commit/4b5ea71aa7cfa50dff4b812f541e0c38ffe29cd9))
