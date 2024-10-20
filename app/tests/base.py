from http import HTTPStatus

from httpx import AsyncClient, Response


class EndpointTestCase:

    async def _do_request_and_check_response(
        self,
        async_client: AsyncClient,
        method: str,
        path: str,
        exp_status: HTTPStatus,
        **kvargs,
    ) -> Response:
        async with async_client as client:
            response = await client.request(method, path, **kvargs)

        assert response.status_code == exp_status
        return response
