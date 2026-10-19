# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError
from .ollama_client import OllamaClient


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    ollama_enabled = fields.Boolean(
        string="Enable Ollama Local AI Copilot",
        config_parameter='ollama_local_ai.enabled',
        default=True,
        help="When enabled, AI features become available in CRM Leads and Mail Composer.",
    )
    ollama_endpoint = fields.Char(
        string="Ollama Server URL",
        config_parameter='ollama_local_ai.endpoint',
        default='http://localhost:11434',
        help="Address of your local or private LAN Ollama server (e.g. http://localhost:11434 or http://192.168.1.50:11434).",
    )
    ollama_model = fields.Char(
        string="Default AI Model",
        config_parameter='ollama_local_ai.model',
        default='llama3',
        help="The model tag installed in your Ollama instance (e.g. llama3, deepseek-r1, mistral, qwen2.5).",
    )
    ollama_temperature = fields.Float(
        string="Temperature (Creativity)",
        config_parameter='ollama_local_ai.temperature',
        default=0.7,
        help="Higher values (0.8) are more creative; lower values (0.2) are more deterministic.",
    )

    def action_test_ollama_connection(self):
        """Tests connectivity to the Ollama server and lists installed models."""
        self.ensure_one()
        endpoint = self.ollama_endpoint or 'http://localhost:11434'
        success, message, models = OllamaClient.test_connection(endpoint)

        if not success:
            raise UserError(f"Could not connect to Ollama Server!\n\n{message}\n\nPlease ensure Ollama is running ('ollama serve').")

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Ollama Connection Verified',
                'message': message,
                'type': 'success',
                'sticky': False,
            }
        }
