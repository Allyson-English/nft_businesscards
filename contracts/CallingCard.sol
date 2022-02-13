// contracts/MyNFT.sol
// SPDX-License-Identifier: MIT
pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract CallingCard is ERC721, VRFConsumerBase {
    uint256 public tokenCounter;
    bytes32 public keyhash;
    uint256 public fee;
    enum Card {
        WAVING,
        BLASTOFF,
        OTHER3
    }
    mapping(uint256 => Card) public tokenIdToCard;
    event handedOutMyCard(uint256 indexed tokenId, Card card);
    mapping(bytes32 => address) public requestIdToSender;
    event requestedCollectible(bytes32 indexed requestId, address requester);
    mapping(bytes32 => string) public requestIdToTokenURI;

    constructor(
        address _VRFCoordinator,
        address _linkToken,
        bytes32 _keyHash,
        uint256 _fee
    )
        public
        VRFConsumerBase(_VRFCoordinator, _linkToken)
        ERC721("CallingCard", "AE")
    {
        tokenCounter = 0;
        keyhash = _keyHash;
        fee = _fee;
    }

    function mintAnOpportunity() public returns (bytes32) {
        bytes32 requestId = requestRandomness(keyhash, fee);
        requestIdToSender[requestId] = msg.sender;
        emit requestedCollectible(requestId, msg.sender);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber)
        internal
        override
    {
        Card card = Card(randomNumber % 3);
        uint256 newTokenId = tokenCounter;
        tokenIdToCard[newTokenId] = card;
        emit handedOutMyCard(newTokenId, card);

        address owner = requestIdToSender[requestId];
        _safeMint(owner, newTokenId);

        tokenCounter += 1;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        // need the token URIs for the business cards
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721 is not owner or approved"
        );
        _setTokenURI(tokenId, _tokenURI);
    }

    function peepMyWebsite() public returns (string memory) {
        return "www.allysonenglish.io";
    }
}
