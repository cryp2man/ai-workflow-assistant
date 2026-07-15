import pytest

from src.engine.execution_engine import UnsafeUrlError, validate_http_step_url


class TestValidateHttpStepUrl:
    async def test_public_ip_allowed(self) -> None:
        await validate_http_step_url("http://8.8.8.8/status")

    async def test_rejects_non_http_scheme(self) -> None:
        with pytest.raises(UnsafeUrlError):
            await validate_http_step_url("ftp://example.com/file")

    async def test_rejects_file_scheme(self) -> None:
        with pytest.raises(UnsafeUrlError):
            await validate_http_step_url("file:///etc/passwd")

    async def test_rejects_missing_hostname(self) -> None:
        with pytest.raises(UnsafeUrlError):
            await validate_http_step_url("http://")

    async def test_rejects_loopback(self) -> None:
        with pytest.raises(UnsafeUrlError):
            await validate_http_step_url("http://127.0.0.1:8000/api/v1/health")

    async def test_rejects_localhost_hostname(self) -> None:
        with pytest.raises(UnsafeUrlError):
            await validate_http_step_url("http://localhost:5432/")

    async def test_rejects_private_network(self) -> None:
        with pytest.raises(UnsafeUrlError):
            await validate_http_step_url("http://192.168.1.1/admin")

    async def test_rejects_cloud_metadata_endpoint(self) -> None:
        with pytest.raises(UnsafeUrlError):
            await validate_http_step_url("http://169.254.169.254/latest/meta-data/")
