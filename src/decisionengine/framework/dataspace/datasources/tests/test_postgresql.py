from decisionengine.framework.dataspace.datasources.postgresql import (
    generate_insert_query,
)


def test_generate_insert_query():
    table_name = "header"
    keys = ["generation_id", "create_time", "creator"]
    expected_query = (
        "INSERT INTO header (generation_id,create_time,creator) VALUES (%s,%s,%s)"
    )

    result_query = generate_insert_query(table_name, keys).strip()

    assert result_query == expected_query
