# -*- coding: utf-8 -*-
import re
from odoo import api, fields, models
from odoo.exceptions import UserError
from ..models.ollama_client import OllamaClient, get_config_param


class AiPromptWizard(models.TransientModel):
    _name = 'ai.prompt.wizard'
    _description = 'Interactive Local AI Assistant'

    prompt = fields.Text(
        string="Your Prompt / Question",
        required=True,
        
    )
    response = fields.Html(
        string="Local AI Response",
        readonly=True,
    )
    model = fields.Char(
        string="Model",
        default=lambda self: get_config_param(self.env, 'ollama_local_ai.model', 'llama3'),
    )

    def action_generate(self):
        """Generates response via local Ollama instance."""
        self.ensure_one()
        endpoint = get_config_param(self.env, 'ollama_local_ai.endpoint', 'http://localhost:11434')
        try:
            res = OllamaClient.generate(
                endpoint_url=endpoint,
                model=self.model or 'llama3',
                prompt=self.prompt,
                temperature=0.7,
            )
            # Format text into basic paragraphs for display
            paragraphs = res.split('\n\n')
            formatted_html = "".join([f"<p>{p.replace('\n', '<br/>')}</p>" for p in paragraphs if p.strip()])
            self.response = formatted_html

            return {
                'type': 'ir.actions.act_window',
                'res_model': 'ai.prompt.wizard',
                'res_id': self.id,
                'view_mode': 'form',
                'target': 'new',
            }
        except Exception as e:
            raise UserError(f"Ollama Request Failed: {str(e)}")
