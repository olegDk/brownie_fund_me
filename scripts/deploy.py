from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_fund_me():
    account = get_account()
    print(account)
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        print(
            f"Network {network.show_active()} is testnet or mainnet fork, using deployed price aggregator"
        )
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        print(
            f"Network {network.show_active()} is in local environment, deploying mock price aggregator"
        )
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
