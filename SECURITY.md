# Security Policy

**The Loom** interacts with untrusted, potentially malicious content sourced from the deep and dark web.  
This document outlines recommended security practices for safely deploying and running the project.

---

## 1. Supported Versions

As an open-source project maintained by the community, specific version support is not guaranteed.  
Users are encouraged to:

- Use the latest stable commit  
- Apply patches regularly  
- Audit dependencies and container images before deployment  

---

## 2. Security Risks

Running collectors and parsers for dark-web content introduces risks including:

- Malware embedded in scraped content  
- Malicious scripts or payloads  
- Access to illegal or harmful material  
- Operational deanonymization (if using Tor/proxies incorrectly)  
- Exposure of sensitive data if logs or storage are misconfigured  

Deploy The Loom only in a controlled and isolated environment.

---

## 3. Secure Deployment Recommendations

### Isolation
- Run The Loom in **isolated VMs**, containers, or sandboxed hosts  
- Keep scrapers separate from corporate networks  
- Use firewalls, namespaces, and seccomp profiles  

### Networking
- Route all dark-web traffic through Tor or an approved proxy  
- Block all inbound access to scraping containers  
- Use outbound allowlists where possible  

### Secrets Management
- Store API keys in `.env` files or secret managers  
- Do not commit secrets to version control  
- Rotate credentials regularly  

### Least Privilege
- Ensure containers run as **non-root**  
- Restrict file-system access to necessary directories  

---

## 4. Vulnerability Reporting

If you discover a vulnerability in The Loom:

1. Do **not** publicly post exploit details  
2. Open a GitHub **Security Advisory** or contact the maintainers privately  
3. Provide:
   - A description of the issue  
   - Steps to reproduce  
   - Impact analysis  
   - Possible fix (optional)  

We will coordinate responsible disclosure.

---

## 5. Handling Malicious Content

Since the project processes untrusted text, images, and HTML, you should:

- Disable automatic rendering in logs  
- Use strict HTML sanitization for previews  
- Avoid executing or interpreting downloaded scripts  
- Run parsing logic in restricted environments  

---

## 6. Dependency Security

- Use `pip-audit`, `npm audit`, or equivalent scanners regularly  
- Pin dependencies (`requirements.txt`, lockfiles)  
- Enable GitHub Dependabot alerts  
- Prefer verified container images  

---

## 7. Logging & Monitoring

- Enable audit logs for ingestion, enrichment, and access  
- Monitor outbound traffic for suspicious spikes  
- Track resource usage for potential compromise detection  
- Apply IDS/IPS rules where appropriate  

---

## 8. Incident Response

If you suspect a compromise:

1. Immediately isolate or shut down affected containers  
2. Rotate all associated credentials  
3. Audit logs and outbound traffic  
4. Restore from a known-good backup  
5. Patch and redeploy components  

---

## 9. Disclaimer

This project is provided **without warranty**.  
You are responsible for:

- Maintaining a secure deployment  
- Preventing misuse  
- Complying with legal and operational requirements  

---

# Summary

Running The Loom safely requires isolation, strict access control, proper secret handling, and active monitoring.  
Security is a shared responsibility — the tool does not protect itself.
