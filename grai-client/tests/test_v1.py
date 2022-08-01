from grai_client.testing.schema import mock_v1_edge, mock_v1_node, mock_v1_edge_and_nodes
from grai_client.endpoints.v1.client import ClientV1
from grai_client.schemas.schema import Schema
from grai_client.schemas.node import NodeV1
from grai_client.schemas.edge import EdgeV1
import pytest


client = ClientV1('localhost', '8000')
client.set_authentication_headers(username='null@grai.io', password='super_secret')


def test_get_nodes():
    nodes = client.get('node')
    assert all(isinstance(node, NodeV1) for node in nodes)


def test_get_edges():
    result = client.get('edge')
    assert all(isinstance(edge, EdgeV1) for edge in result)


def test_post_node():
    test_node = mock_v1_node()
    result = client.post(test_node)
    assert isinstance(result, NodeV1)


def test_post_edge():
    test_edge, test_nodes = mock_v1_edge_and_nodes()
    client.post(test_nodes)
    result = client.post(test_edge)
    assert isinstance(result, EdgeV1)


def test_delete_node():
    test_node = mock_v1_node()
    test_node = client.post(test_node)
    assert client.get(test_node)
    client.delete(test_node)
    result = client.get(test_node)
    assert result is None


def test_delete_edge():
    test_edge, test_nodes = mock_v1_edge_and_nodes()
    test_nodes = client.post(test_nodes)
    test_edge = client.post(test_edge)
    assert client.get(test_edge)
    client.delete(test_edge)

    result = client.get(test_edge)
    assert result is None

    client.delete(test_nodes)


def test_patch_node():
    test_node = mock_v1_node()
    test_node = client.post(test_node)

    updated_node = test_node.update({'spec': {'is_active': True}})
    server_updated_node = client.patch(updated_node)
    assert server_updated_node == updated_node

    client.delete(test_node)


def test_patch_edge():
    test_edge, test_nodes = mock_v1_edge_and_nodes()
    test_nodes = client.post(test_nodes)
    test_edge = client.post(test_edge)

    updated_edge = test_edge.update({'spec': {'is_active': True}})
    server_updated_edge = client.patch(updated_edge)
    assert server_updated_edge == updated_edge

    client.delete(test_edge)
    client.delete(test_nodes)