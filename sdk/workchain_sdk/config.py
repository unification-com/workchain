import json
import logging

import click

from workchain_sdk.bootnode import BootnodeKey
from workchain_sdk.composer import generate
from workchain_sdk.documentation import WorkchainDocumentation
from workchain_sdk.genesis import build_genesis
from workchain_sdk.utils import write_build_file

log = logging.getLogger(__name__)


def parse_config(config_file):
    with open(config_file, 'r') as f:
        contents = f.read()
        d = json.loads(contents)

    return d


def generate_readme(config, genesis_json, bootnode_address=None):
    doc_gen = WorkchainDocumentation(config,
                                     genesis_json['config']['chainId'],
                                     bootnode_address=bootnode_address)
    readme = doc_gen.generate()
    return readme


def generate_genesis(config):
    block_period = config['workchain']['ledger']['consensus']['period']
    validators = config['workchain']['validators']
    pre_funded_accounts = config['workchain']['coin']['prefund']

    workchain_base = config['workchain']['ledger']['base']
    workchain_consensus = config['workchain']['ledger']['consensus']['type']

    genesis_json = build_genesis(
        block_period=block_period, validators=validators,
        workchain_base=workchain_base,
        workchain_consensus=workchain_consensus,
        pre_funded_accounts=pre_funded_accounts)

    return genesis_json


def write_genesis(build_dir, genesis_json):
    write_build_file(build_dir + '/genesis.json', genesis_json)


def write_readme(build_dir, readme):
    write_build_file(build_dir + '/README.md', readme)


def write_composition(build_dir, composition):
    write_build_file(build_dir + '/docker-compose.yml', composition)


@click.group()
def main():
    pass


@main.command()
@click.argument('config_file')
@click.argument('build_dir')
def generate_workchain(config_file, build_dir):
    log.info(f'Generating environment from: {config_file}')
    config = parse_config(config_file)

    genesis_json = generate_genesis(config)
    bootnode_address = None

    if config['workchain']['bootnode']['use']:
        bootnode_key = BootnodeKey(build_dir)
        bootnode_address = bootnode_key.get_bootnode_address()
        click.echo(f'Bootnode Address: {bootnode_address}')

    readme = generate_readme(config, genesis_json, bootnode_address)

    rendered = json.dumps(genesis_json, indent=2, separators=(',', ':'))
    composition = generate()

    write_genesis(build_dir, rendered)
    write_readme(build_dir, readme)
    write_composition(build_dir, composition)

    click.echo(readme)
    click.echo(rendered)
    click.echo(composition)


if __name__ == "__main__":
    main()
