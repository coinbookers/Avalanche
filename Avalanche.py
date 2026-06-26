from dataclasses import dataclass
from datetime import datetime
import json
import uuid


@dataclass
class NetworkConfig:
    name: str
    chain_id: int
    rpc_url: str


class MetadataBuilder:

    def __init__(self):
        self.labels = {
            "network": "avalanche",
            "asset": "avax"
        }

    def build(self):
        return {
            "id": str(uuid.uuid4()),
            "created": datetime.utcnow().isoformat(),
            "labels": self.labels
        }


class ContractInteraction:

    def __init__(
        self,
        contract_address,
        sender
    ):
        self.contract_address = contract_address
        self.sender = sender
        self.metadata = MetadataBuilder()

    def create_request(self):

        payload = self.metadata.build()

        return {
            "from": self.sender,
            "to": self.contract_address,
            "value": 0,
            "data": json.dumps(payload)
        }


class Validator:

    @staticmethod
    def validate(request):

        required = [
            "from",
            "to",
            "value",
            "data"
        ]

        for field in required:
            if field not in request:
                raise ValueError(
                    f"Missing field: {field}"
                )

        return True


class Reporter:

    @staticmethod
    def display(request):

        print("=" * 50)
        print("Interaction Preview")
        print("=" * 50)

        print(
            json.dumps(
                request,
                indent=2
            )
        )

        print("=" * 50)


def load_configuration():

    return NetworkConfig(
        name="avalanche",
        chain_id=43114,
        rpc_url="https://example-rpc.invalid"
    )


def main():

    config = load_configuration()

    interaction = ContractInteraction(
        contract_address=(
            "0x1234567890123456789012345678901234567890"
        ),
        sender=(
            "0xABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCD"
        )
    )

    request = interaction.create_request()

    Validator.validate(request)

    Reporter.display(request)

    print("Network:", config.name)
    print("Asset:", "avax")
    print("Chain ID:", config.chain_id)


if __name__ == "__main__":
    main()
