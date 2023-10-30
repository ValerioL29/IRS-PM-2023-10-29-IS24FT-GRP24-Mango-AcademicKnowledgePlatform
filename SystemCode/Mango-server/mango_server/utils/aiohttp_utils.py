import aiohttp

from mango_server.utils.logging_utils import logger


async def post_request_with_body(
        request_url: str,
        request_body: dict,
        request_params: dict | None = None,
        request_header: dict | None = None
) -> dict:
    logger.debug(f"Sending request to: {request_url}.")
    logger.debug(f"With body data: {request_body}")
    async with aiohttp.ClientSession() as session:
        logger.debug("Session initialized.")
        async with session.post(
                url=request_url, params=request_params,
                data=request_body, headers=request_header
        ) as response:
            logger.debug("Request sent successfully. Wait for response...")
            rsp_data = await response.json()
            logger.debug("Response received. Preparing return value...")
            ret = {
                "status": response.status,
                "content-type": response.headers['content-type'],
                "response": rsp_data,
                "body": request_body
            }
    logger.debug(f"Done preparation. Return value: {ret}")
    return rsp_data


async def put_request_with_body(
        request_url: str,
        request_body: dict
) -> dict:
    logger.debug(f"Sending request to: {request_url}.")
    logger.debug(f"With body data: {request_body}")
    async with aiohttp.ClientSession() as session:
        logger.debug("Session initialized.")
        async with session.put(url=request_url, json=request_body) as response:
            logger.debug("Request sent successfully. Wait for response...")
            logger.debug("Response received. Preparing return value...")
            ret = {
                "status": response.status,
                "content-type": response.headers['content-type'],
                "body": request_body
            }
    logger.debug(f"Done preparation. Return value: {ret}")
    return ret


async def get_request_with_query(
        request_url: str,
        request_query: dict | None = None,
        request_header: dict | None = None
) -> dict:
    logger.debug(f"Sending request to: {request_url}.")
    async with aiohttp.ClientSession() as session:
        logger.debug("Session initialized.")
        async with session.get(
                url=request_url, params=request_query, headers=request_header) as response:
            logger.debug("Request sent successfully. Wait for response...")
            rsp_data = await response.json()
            logger.debug("Response received. Preparing return value...")
            ret = {
                "status": response.status,
                "content-type": response.headers['content-type'],
                "response": rsp_data,
            }
    logger.debug(f"Done preparation. Return value: {ret}")
    return rsp_data


async def patch_request_with_path_and_body(
        request_url: str,
        request_body: dict
) -> dict:
    logger.debug(f"Sending request to: {request_url}.")
    async with aiohttp.ClientSession() as session:
        logger.debug("Session initialized.")
        async with session.patch(url=request_url, data=request_body) as response:
            logger.debug("Request sent successfully. Wait for response...")
            rsp_data = await response.json()
            logger.debug("Response received. Preparing return value...")
            ret = {
                "status": response.status,
                "content-type": response.headers['content-type'],
                "response": rsp_data,
            }
    logger.debug(f"Done preparation. Return value: {ret}")
    return ret


async def delete_request_with_path(
        request_url: str,
) -> dict:
    logger.debug(f"Sending request to: {request_url}.")
    async with aiohttp.ClientSession() as session:
        logger.debug("Session initialized.")
        async with session.delete(url=request_url) as response:
            logger.debug("Request sent successfully. Wait for response...")
            logger.debug("Response received. Preparing return value...")
            ret = {
                "status": response.status,
                "content-type": response.headers['content-type']
            }
    logger.debug(f"Done preparation. Return value: {ret}")
    return ret
