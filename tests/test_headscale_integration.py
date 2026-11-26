import os

import pytest
import uuid
from dotenv import load_dotenv

from cluster_builder.infrastructure.headscale import (
    HeadscaleClient,
    HeadscaleConfig,
    HeadscaleNotFoundError,
)

load_dotenv(".env", override=True)

BASE_URL = os.getenv("HEADSCALE_BASE_URL")
API_KEY = os.getenv("HEADSCALE_API_KEY")

pytestmark = pytest.mark.skipif(
    not BASE_URL or not API_KEY,
    reason="Set HEADSCALE_BASE_URL and HEADSCALE_API_KEY to run live tests",
)


@pytest.fixture
def headscale_client():
    return HeadscaleClient(
        HeadscaleConfig(
            base_url=BASE_URL,
            api_key=API_KEY,
        )
    )


def test_live_list_users(headscale_client):
    users = headscale_client.list_users()

    assert isinstance(users, list)
    assert all(isinstance(user, dict) for user in users)

    print(f"\nLive Headscale server returned {len(users)} users")


def test_live_list_nodes(headscale_client):
    nodes = headscale_client.list_nodes()

    assert isinstance(nodes, list)
    assert all(isinstance(node, dict) for node in nodes)

    print(f"\nLive Headscale server returned {len(nodes)} nodes")


def test_live_create_user(headscale_client):
    username = f"integration-test-{uuid.uuid4().hex[:8]}"

    response = headscale_client.create_user(username)

    assert isinstance(response, dict)
    assert "user" in response

    user = response["user"]

    assert user.get("id") is not None
    assert user.get("name") == username

    print(f"\nCreated temporary Headscale user:")
    print(f"ID: {user['id']}")
    print(f"Name: {user['name']}")


def test_live_create_preauth_key(headscale_client):

    username = f"integration-test-{uuid.uuid4().hex[:8]}"

    response = headscale_client.create_user(username)
    user = response["user"]

    user_id = user["id"]

    key_response = headscale_client.create_preauth_key(
        user=user_id,
        reusable=False,
        ephemeral=False,
    )

    assert isinstance(key_response, dict)

    print(f"\nCreated pre-auth key for user ID: {user_id}")
    print("Pre-auth key creation succeeded")



def test_live_delete_user(headscale_client):

    username = f"integration-test-{uuid.uuid4().hex[:8]}"

    response = headscale_client.create_user(username)
    user_id = response["user"]["id"]

    delete_response = headscale_client.delete_user(user_id)

    print(f"\nDeleted temporary user ID: {user_id}")

    users = headscale_client.list_users()
    remaining_ids = [str(user["id"]) for user in users]

    assert str(user_id) not in remaining_ids


def test_live_delete_nonexistent_node(headscale_client):
    nonexistent_node_id = "999999999"

    with pytest.raises(HeadscaleNotFoundError):
        headscale_client.delete_node(nonexistent_node_id)

    print("\nCorrectly handled deletion of a nonexistent node")
