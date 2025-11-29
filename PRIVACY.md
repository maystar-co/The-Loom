# Privacy Policy

**The Loom** processes data collected from open, deep, and dark web sources for legitimate cybersecurity, research, and defensive purposes.

This document describes how data is handled within the project.  
By using this software, you acknowledge that *you* are responsible for ensuring compliance with all applicable privacy regulations, including GDPR, CCPA, and local data protection laws.

---

## 1. Nature of Collected Data

Depending on your configuration, The Loom may collect and process:

- Publicly available posts, messages, or forum content  
- Data shared on deep/dark web marketplaces or paste sites  
- Email addresses, usernames, IP addresses, domains  
- Mentions of your organization’s assets or employees  
- Indicators of compromise (IOCs)  
- Metadata from observed content (timestamps, URLs, source identifiers)  

The Loom does **not** inherently collect personal data unless such information is already present in scraped sources.

---

## 2. Sensitive and Personal Data

Dark web sources may contain highly sensitive or illegally obtained personal data such as:

- Stolen credentials  
- Payment information  
- Identity documents  
- Personal contact information  
- Medical or financial data  

Handling and storing such data may be subject to strict legal requirements.  
**You are fully responsible** for complying with applicable privacy and retention laws.

The maintainers do **not** receive, store, or process any data on your behalf.

---

## 3. Data Storage

You choose where and how data is stored. Typical deployments may store:

- Raw scraped content  
- Normalized threat-intelligence events  
- IOC enrichment results  
- Correlation metadata  

**Ensure your storage backend (database, S3/GCS bucket, SIEM, etc.) is secure.**

Encryption at rest and access control are strongly recommended.

---

## 4. Data Retention & Deletion

You determine your own retention policies.

Best practices include:

- Short-term retention for raw scraped data (e.g., 7–30 days)  
- Longer retention for enriched threat metadata (e.g., 90–365 days)  
- Deleting or anonymizing personal data when legally required  
- Keeping audit logs of collection and deletion operations  

No built-in retention policy is enforced by default.

---

## 5. Data Sharing

The Loom **does not share data** automatically.

Sharing responsibility lies with the user or organization operating the tool.

If you choose to export, share, or publish collected intelligence, ensure:

- Sensitive data is redacted where required  
- Personal data is anonymized  
- Legal and organizational rules permit such sharing  

---

## 6. User Responsibility & Compliance

You are responsible for:

- Determining lawful bases for data collection  
- Securing consent where required (if applicable)  
- Managing requests for deletion or access  
- Setting retention limits  
- Implementing technical safeguards  

Use of this software does not grant immunity or legal clearance.

---

## 7. No Telemetry / No Phone-Home

The Loom does **not**:

- Collect usage analytics  
- Transmit data to the maintainers  
- Include telemetry, fingerprinting, or tracking mechanisms  

All data stays within your environment.

---

## 8. Changes to This Policy

As an open-source project, updates may be made by contributors through version control.  
You are responsible for monitoring changes and determining if updates affect your compliance posture.

---

# Summary

You control all data processing.  
You control retention, deletion, and compliance.  
You are fully responsible for protecting any sensitive information collected using The Loom.
