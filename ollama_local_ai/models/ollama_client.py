# -*- coding: utf-8 -*-
import json
import logging
import urllib.request
import urllib.error

_logger = logging.getLogger(__name__)


def get_config_param(env, key, default='', param_type='str'):
    """Universal configuration getter compatible with Odoo 17/18/19 and Odoo 20+."""
    ICP = env['ir.config_parameter'].sudo()
    if hasattr(ICP, 'get_str'):
        if param_type == 'bool':
            return ICP.get_bool(key, default=bool(default))
        elif param_type == 'int':
            return ICP.get_int(key, default=int(default or 0))
        return ICP.get_str(key, default=str(default or ''))
    elif hasattr(ICP, 'get_param'):
        val = ICP.get_param(key, default)
        if param_type == 'bool':
            return val in ('True', 'true', '1', True)
        elif param_type == 'int':
            try:
                return int(val or 0)
            except (ValueError, TypeError):
                return int(default or 0)
        return val if val is not None else default
    return default


class OllamaClient:
    """Lightweight, zero-dependency HTTP client for self-hosted Ollama AI instances."""

    @classmethod
    def test_connection(cls, endpoint_url="http://localhost:11434"):
        """Validates connection to Ollama and returns list of installed models."""
        url = f"{endpoint_url.rstrip('/')}/api/tags"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Odoo-Ollama-Copilot'})
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    models = [m.get('name') for m in data.get('models', [])]
                    model_str = ", ".join(models) if models else "No models installed yet (run 'ollama pull llama3')"
                    return True, f"Connected to Ollama successfully! Found models: {model_str}", models
                return False, f"Unexpected response from Ollama: HTTP {response.status}", []
        except urllib.error.URLError as e:
            return False, f"Could not reach Ollama at {endpoint_url}: {e.reason}", []
        except Exception as e:
            return False, f"Ollama connection error: {str(e)}", []

    @classmethod
    def generate(cls, endpoint_url, model, prompt, system_prompt=None, temperature=0.7):
        """Sends a generation request to Ollama and returns the output string."""
        url = f"{endpoint_url.rstrip('/')}/api/generate"
        payload = {
            'model': model,
            'prompt': prompt,
            'stream': False,
            'options': {
                'temperature': float(temperature),
            }
        }
        if system_prompt:
            payload['system'] = system_prompt

        json_data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            url,
            data=json_data,
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'Odoo-Ollama-Copilot',
            }
        )

        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                if response.status == 200:
                    result = json.loads(response.read().decode('utf-8'))
                    return result.get('response', '').strip()
                raise RuntimeError(f"Ollama returned HTTP status {response.status}")
        except urllib.error.HTTPError as e:
            err_body = e.read().decode('utf-8')
            raise RuntimeError(f"Ollama API Error [{e.code}]: {err_body}")
        except urllib.error.URLError as e:
            raise RuntimeError(f"Failed to connect to Ollama at {endpoint_url}: {e.reason}")
