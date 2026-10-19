# Ollama Local AI Copilot for Odoo

**100% Private, On-Premise AI for CRM, Leads & Mail (Zero Cloud API Bills & Full GDPR Compliance)**

[![Odoo Version](https://img.shields.io/badge/Odoo-17.0%20%7C%2018.0%20%7C%2019.0%20%7C%2020.0-purple.svg)](https://apps.odoo.com)
[![License: OPL-1](https://img.shields.io/badge/License-OPL--1-blue.svg)](https://www.odoo.com/documentation/user/17.0/legal/licenses/licenses.html#odoo-proprietary-license-v1-0)
[![Privacy: 100% On-Premise](https://img.shields.io/badge/Privacy-100%25%20Local-green.svg)](https://ollama.com)

---

## Overview

Unlike standard cloud AI plugins that send confidential customer records, invoices, and sales pitches to third-party US cloud providers (violating GDPR and client NDAs), **Ollama Local AI Copilot** runs 100% on your own server or office GPU via [Ollama](https://ollama.com).

* **Zero Data Leaves Your Network:** Complete peace of mind for EU, healthcare, and enterprise legal compliance.
* **$0 Monthly Token Bills:** Unlimited generation with open-weight models (**Llama 3.3, DeepSeek-R1, Mistral, Qwen 2.5**).
* **CRM Lead Intelligence:** 1-click executive deal briefs, risk analysis, and next-best-action prediction.
* **Smart Mail Composer:** Instant AI draft replies and tone shifting directly inside the Odoo email wizard.

---

## Quickstart

1. **Install and Run Ollama:**
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ollama pull llama3
   ollama serve
   ```

2. **Add to Odoo Addons:**
   Clone or copy `ollama_local_ai` to your Odoo `addons_path`.

3. **Install in Odoo:**
   Update your Apps list and install **`ollama_local_ai`**.

4. **Verify in Settings:**
   * Go to **Settings -> General Settings -> Local AI**.
   * Enter your Ollama URL (default: `http://localhost:11434` or your LAN server IP).
   * Click **Test Ollama Connection** to verify installed models.

---

## Author & Support

* **Author:** Sijo Joseph S
* **GitHub:** [sijo0218](https://github.com/sijo0218)
* **Email:** `sijo0218@gmail.com`
