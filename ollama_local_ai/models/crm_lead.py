# -*- coding: utf-8 -*-
import re
from odoo import api, fields, models
from odoo.exceptions import UserError
from .ollama_client import OllamaClient, get_config_param


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    ai_summary = fields.Html(
        string="AI Lead Summary & Analysis",
        readonly=True,
        help="Synthesized deal intelligence generated locally via Ollama.",
    )
    ai_next_action = fields.Text(
        string="AI Recommended Next Step",
        readonly=True,
        help="Strategic next action recommended by local AI based on conversation history.",
    )
    ai_qualification_score = fields.Integer(
        string="AI Deal Health (0-100)",
        readonly=True,
        help="Predicted deal viability based on client engagement and budget parameters.",
    )

    def action_generate_ai_summary(self):
        """Analyzes lead details and chatter history to produce a structured intelligence brief."""
        self.ensure_one()
        if not get_config_param(self.env, 'ollama_local_ai.enabled', True, 'bool'):
            raise UserError("Ollama Local AI is currently disabled. Please enable it in General Settings.")

        endpoint = get_config_param(self.env, 'ollama_local_ai.endpoint', 'http://localhost:11434')
        model = get_config_param(self.env, 'ollama_local_ai.model', 'llama3')
        temperature = get_config_param(self.env, 'ollama_local_ai.temperature', 0.5, 'float')

        # Extract recent conversation history from chatter
        recent_messages = []
        for msg in self.message_ids.filtered(lambda m: m.message_type in ('comment', 'email') and m.body)[:5]:
            clean_body = re.sub('<[^<]+?>', '', msg.body or '').strip()
            if clean_body:
                author = msg.author_id.name if msg.author_id else "Client"
                recent_messages.append(f"{author}: {clean_body[:300]}")

        conversation_context = "\n".join(recent_messages) if recent_messages else "No prior communication recorded."
        clean_desc = re.sub('<[^<]+?>', '', self.description or '').strip() if self.description else "No description provided."

        prompt = f"""
You are an expert enterprise sales advisor. Analyze the following CRM opportunity and generate a structured executive brief in clean HTML (using <h4>, <p>, <ul>, <li> tags, no markdown codeblocks):

Opportunity Name: {self.name}
Customer: {self.partner_id.name or self.contact_name or 'Unknown'}
Expected Revenue: {self.expected_revenue} {self.company_currency.symbol or ''}
Probability: {self.probability}%
Stage: {self.stage_id.name or 'New'}
Lead Description: {clean_desc}

Recent Communications:
{conversation_context}

Provide:
1. Executive Overview
2. Client Needs & Key Pain Points
3. Win Strategy & Value Proposition
4. Potential Deal Blockers
"""
        system_prompt = "You are a professional B2B CRM sales strategist. Answer in structured HTML only without enclosing codeblocks."

        try:
            ai_response = OllamaClient.generate(
                endpoint_url=endpoint,
                model=model,
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=temperature,
            )
            # Remove any stray ```html tags if present
            ai_response = re.sub(r'^```html\s*', '', ai_response, flags=re.MULTILINE)
            ai_response = re.sub(r'```$', '', ai_response, flags=re.MULTILINE).strip()

            self.write({
                'ai_summary': ai_response,
            })
            return True
        except Exception as e:
            raise UserError(f"Ollama Generation Failed: {str(e)}")

    def action_predict_ai_next_step(self):
        """Generates a concrete, tactical next step for the sales representative."""
        self.ensure_one()
        if not get_config_param(self.env, 'ollama_local_ai.enabled', True, 'bool'):
            raise UserError("Ollama Local AI is currently disabled.")

        endpoint = get_config_param(self.env, 'ollama_local_ai.endpoint', 'http://localhost:11434')
        model = get_config_param(self.env, 'ollama_local_ai.model', 'llama3')

        clean_desc = re.sub('<[^<]+?>', '', self.description or '').strip() if self.description else ""

        prompt = f"""
Lead: {self.name}
Customer: {self.partner_id.name or 'Unknown'}
Stage: {self.stage_id.name}
Notes: {clean_desc}

In 2 concise sentences, state the single highest-impact action the sales rep should take today to move this deal forward.
"""
        try:
            next_action = OllamaClient.generate(
                endpoint_url=endpoint,
                model=model,
                prompt=prompt,
                temperature=0.3,
            )
            self.write({'ai_next_action': next_action.strip()})
            return True
        except Exception as e:
            raise UserError(f"Ollama Next Step Prediction Failed: {str(e)}")
