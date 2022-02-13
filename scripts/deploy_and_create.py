from scripts.helpful_scrits import get_account, get_contract, fund_with_link, OPENSEA_URL
from brownie import CallingCard, config, network

def deploy_and_create():
    account = get_account()
    hire_me = CallingCard.deploy(get_contract("vrf_coordinator"),
                            get_contract("link_token"),
                            config["networks"][network.show_active()]["keyhash"],
                            config["networks"][network.show_active()]["fee"],
                            {"from": account},
                            publish_source=config['networks'][network.show_active()].get('verify')
            )
    fund_with_link(hire_me.address)
    tx = hire_me.mintAnOpportunity({"from": account})
    tx.wait(1)
    print(f"Awesome, you can now hire allyson english! check out her resume at {OPENSEA_URL.format(hire_me.address, hire_me.tokenCounter())}")
    return hire_me, tx

def main():
    deploy_and_create()