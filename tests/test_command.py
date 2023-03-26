import pytest
from telewrap import shell_command


class TestCommand:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("command, expected_output",
                             [
        ("sleep 0", ""),
        ("'sleep 0'", ""),
        ("python -c \"print('hi')\"", "hi"),
        ('\'python -c "print(\'"\'"\'hi\'"\'"\')"\'', "hi"),
        ]
    )
    async def test_run_command(self, command, expected_output):
        lines = []
        await shell_command.run_command(command, lines)
        assert expected_output == "\n".join(lines)
