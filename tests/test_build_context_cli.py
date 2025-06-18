import os
import subprocess
from pathlib import Path


def test_build_context_cli_runs(tmp_path):
    # Create dummy config
    config_path = tmp_path / ".gptcontext-config.yml"
    config_path.write_text("MAX_TOTAL_TOKENS: 5000\n")

    # Create dummy message template
    template_path = tmp_path / "message_sample.txt"
    template_path.write_text("Message:\n<context starts>\n${context}\n<context ends>")

    # Add a dummy file to scan
    (tmp_path / "hello.py").write_text("print('hello world')\n")

    # Inject PYTHONPATH
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1] / "src")

    result = subprocess.run(
        [
            "python",
            "-m",
            "gptcontext",
            "--base", str(tmp_path),
            "--generate-message",
            "--config-file", config_path.name,
            "--output-dir", str(tmp_path),
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        env=env,
    )

    assert result.returncode in {0, 2}, result.stderr

    # Updated output assertions
    assert (tmp_path / ".gptcontext.txt").exists()
    assert (tmp_path / ".gptcontext_message.txt").exists()
