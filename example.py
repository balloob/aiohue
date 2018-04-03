import asyncio
from pprint import pprint
import sys

import aiohttp

from aiohue.discovery import discover_nupnp


async def main():
    async with aiohttp.ClientSession() as session:
        await run(session)


async def run(websession):
    bridges = await discover_nupnp(websession)
    bridge = bridges[0]

    print('Found bridge at', bridge.host)

    if len(sys.argv) == 1:
        await bridge.create_user('aiophue-example')
        print('Your username is', bridge.username)
        print('Pass this to the example to control the bridge')
        return

    bridge.username = sys.argv[1]

    await bridge.initialize()

    print('Name', bridge.config.name)
    print('Mac', bridge.config.mac)
    print('API version', bridge.config.apiversion)

    print()
    print('Lights:')
    for id in bridge.lights:
        light = bridge.lights[id]
        print('{}: {}'.format(light.name, 'on' if light.state['on'] else 'off'))

    print()
    print('Groups:')
    for id in bridge.groups:
        group = bridge.groups[id]
        print('{}: {}'.format(group.name, 'on' if group.action['on'] else 'off'))

    print()
    print('Scenes:')
    for id in bridge.scenes:
        scene = bridge.scenes[id]
        print(scene.name)

    print()
    print('Sensors:')
    for id in bridge.sensors:
        sensor = bridge.sensors[id]
        print(sensor.name)

asyncio.get_event_loop().run_until_complete(main())
