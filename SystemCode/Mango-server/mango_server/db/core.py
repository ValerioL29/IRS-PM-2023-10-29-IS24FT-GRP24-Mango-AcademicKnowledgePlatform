import duckdb

from contextlib import contextmanager

from mango_server.config import paper_detail_fields


@contextmanager
def connect_duckdb(path_to_db: str, read_only_or_not: bool = True):
    conn = None
    try:
        conn = duckdb.connect(path_to_db, read_only=read_only_or_not)

        yield conn
    except Exception:
        raise RuntimeError("Connection is not established. Please check the path to the database.")
    finally:
        conn.close()


def post_process_result(
    raw_ret: list[tuple],
    fields_list: list[str] | None = None
):
    # Default fields_list is paper_detail_fields
    if not fields_list:
        fields_list = paper_detail_fields

    ret = [
        {
            field: row[idx]
            for idx, field in enumerate(fields_list)
        }
        for row in raw_ret
    ]
    return ret


def get_within_predicate(column_name: str, name_list: list[str]):
    return f"{column_name} in ({','.join(name_list)})"


async def get_records_with_list_in(
        value_list: list[str],
        column_name: str,
        table_name: str = "paper_details",
        fields_list: list[str] | None = None,
        db_path: str = "stores/mango.duckdb"
):
    # Default fields_list is paper_detail_fields
    if not fields_list:
        fields_list = paper_detail_fields

    with connect_duckdb(db_path, read_only_or_not=True) as cursor:
        # SQL Preprocess
        paper_ids = map(lambda x: f"'{str(x)}'", value_list)
        # noinspection PyTypeChecker
        predicate = get_within_predicate(column_name, paper_ids)
        fields = ",".join(fields_list)
        # Fetch records from DuckDB
        raw_sql = f"SELECT {fields} FROM {table_name} WHERE {predicate}"
        raw_ret = cursor.sql(raw_sql).fetchall()
        # Post Process
        ret = post_process_result(raw_ret, fields_list)

        return ret


async def get_records_with_ids(
        paper_ids: list[str],
        id_type: str = "paperId",
        table_name: str = "paper_details",
        fields_list: list[str] | None = None,
        db_path: str = "stores/mango.duckdb"
):
    return await get_records_with_list_in(
        value_list=paper_ids,
        column_name=id_type,
        table_name=table_name,
        fields_list=fields_list,
        db_path=db_path
    )


async def get_paper_details_with_titles(
        titles: list[str],
):
    return await get_records_with_list_in(
        value_list=titles,
        column_name="title",
    )


async def get_paper_details(
        paper_ids: list[str],
        id_type: str = "paperId",
        db_path: str = "stores/mango.duckdb"
):
    return await get_records_with_ids(
        paper_ids=paper_ids,
        id_type=id_type,
        table_name="paper_details",
        fields_list=paper_detail_fields,
        db_path=db_path
    )


async def get_paper_detail_with_id(
        paper_id: str,
        id_type: str = "paperId",
        table_name: str = "paper_details",
        fields_list: list[str] | None = None,
        db_path: str = "stores/mango.duckdb"
):
    # Default fields_list is paper_detail_fields
    if not fields_list:
        fields_list = paper_detail_fields

    with connect_duckdb(db_path, read_only_or_not=True) as cursor:
        # SQL Preprocess
        predicate = f"{id_type} = '{paper_id}'"
        fields = ",".join(fields_list)
        # Fetch records from DuckDB
        raw_sql = f"SELECT {fields} FROM {table_name} WHERE {predicate}"
        raw_ret = cursor.sql(raw_sql).fetchone()
        # Post Process
        ret = {
            field: raw_ret[idx]
            for idx, field in enumerate(fields_list)
        }

        return ret
