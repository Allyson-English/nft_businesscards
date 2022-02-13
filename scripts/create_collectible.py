from brownie import CallingCard
from scripts.helpful_scrits import fund_with_link, get_account
from web3 import Web3


def main():

    account = get_account()
    callingCard = CallingCard[-1]
    fund_with_link(callingCard, amount = Web3.toWei(0.1, "ether"))
    hand_out_card = callingCard.mintAnOpportunity({'from': account})
    hand_out_card.wait(1)
    print("Handed out your card!")
    return hand_out_card