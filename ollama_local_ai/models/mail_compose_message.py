# -*- coding: utf-8 -*-
import re
from odoo import api, fields, models
from odoo.exceptions import UserError
from .ollama_client import OllamaClient, get_config_param


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    ai_tone = fields.Selection([
        ('professional', 'Professional & Formal'),
        ('friendly', 'Warm & Personable'),
        ('persuasive', 'Persuasive Sales Closer'),
        ('concise', 'Concise & Direct'),
    ], string="AI Tone", default='professional')

    ai_prompt_guidance = fields.Char(
        string="Custom AI Instructions",
        
    )

    def action_ai_generate_draft(self):
        """Generates or refines an email draft using the local Ollama LLM."""
        self.ensure_one()
        if not get_config_param(self.env, 'ollama_local_ai.enabled', True, 'bool'):
            raise UserError("Ollama Local AI is currently disabled in Settings.")

        endpoint = get_config_param(self.env, 'ollama_local_ai.endpoint', 'http://localhost:11434')
        model = get_config_param(self.env, 'ollama_local_ai.model', 'llama3')
        temperature = get_config_param(self.env, 'ollama_local_ai.temperature', 0.6, 'float')

        # Retrieve context from related document (CRM lead, sales order, ticket)
        doc_context = ""
        if self.model and self.res_ids:
            try:
                res_id = self.res_ids[0] if isinstance(self.res_ids, list) else int(self.res_ids)
                record = self.env[self.model].browse(res_id)
                if record.exists():
                    doc_context = f"Document Type: {self.model}, Name: {record.display_name}"
            except Exception:
                pass

        current_body = re.sub('<[^<]+?>', '', self.body or '').strip()

        tone_instructions = {
            'professional': 'Write in a polished, formal, and authoritative corporate tone.',
            'friendly': 'Write in an approachable, warm, and conversational tone.',
            'persuasive': 'Write with compelling urgency and clear calls-to-action emphasizing ROI.',
            'concise': 'Write in bullet points with minimal fluff, getting straight to the point.',
        }.get(self.ai_tone, 'Write professionally.')

        prompt = f"""
You are an expert executive email assistant. Draft an email reply in HTML format (<p>, <br>, <ul>, <li> tags, no code fences):

Context: {doc_context}
Current Draft / Context: {current_body if current_body else 'Drafting a new message'}
User Guidance: {self.ai_prompt_guidance or 'Write an appropriate response based on context'}
Tone: {tone_instructions}

Return only the clean HTML email body starting with a professional greeting and closing with a sign-off placeholder.
"""
        try:
            ai_draft = OllamaClient.generate(
                endpoint_url=endpoint,
                model=model,
                prompt=prompt,
                system_prompt="You are an enterprise email copywriter. Output HTML body directly.",
                temperature=temperature,
            )
            clean_html = re.sub(r'^```html\s*', '', ai_draft, flags=re.MULTILINE)
            clean_html = re.sub(r'```$', '', clean_html, flags=re.MULTILINE).strip()

            self.body = clean_html
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'mail.compose.message',
                'res_id': self.id,
                'view_mode': 'form',
                'target': 'new',
            }
        except Exception as e:
            raise UserError(f"Ollama Draft Generation Failed: {str(e)}")
