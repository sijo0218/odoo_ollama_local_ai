# -*- coding: utf-8 -*-
{
    'name': 'Ollama Local AI Copilot (100% Private & GDPR Compliant)',
    'version': '18.0.1.0.0',
    'category': 'Extra Tools/Productivity',
    'summary': 'Connect Odoo to local Ollama (Llama 3, DeepSeek, Mistral). 100% Private On-Premise AI for CRM, Leads & Mail. $0 API Fees.',
    'description': """
Ollama Local AI Copilot for Odoo (Self-Hosted & Private)
=========================================================
Empower your sales, support, and operations teams with powerful Generative AI
without ever sending confidential client data or contracts to third-party US cloud APIs.

Key Benefits:
-------------
* **100% GDPR Compliant & Zero-Data-Leak:** AI runs locally on your own server or office GPU via Ollama. No data leaves your network.
* **$0 Monthly API Bills:** Unlimited generations with open-weight models (DeepSeek-R1/V3, Llama 3.3, Mistral, Qwen).
* **CRM Lead Copilot:** 1-click AI Lead Summarizer, Next-Best-Action predictor, and Qualification Scoring.
* **Smart Mail Composer:** Instant AI Draft Replies based on previous chatter history, Tone Shifter (Formal, Friendly, Concise), and Grammar Polish.
* **Universal Model Support:** Connects directly to any Ollama instance via LAN or localhost.
    """,
    'author': 'Sijo Joseph S',
    'website': 'https://github.com/sijo0218',
    'license': 'OPL-1',
    'price': 149.00,
    'currency': 'EUR',
    'depends': ['base', 'mail', 'crm', 'base_setup'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'views/crm_lead_views.xml',
        'views/mail_compose_message_views.xml',
        'wizard/ai_prompt_wizard_views.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
