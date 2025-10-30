"""Reusable narrative elements for rebuilding CyberLearn lessons."""

from __future__ import annotations

DOMAIN_LIBRARY = {
    "active_directory": {
        "tools": [
            {
                "name": "BloodHound",
                "description": (
                    "BloodHound maps Active Directory relationships with graph analytics, allowing defenders to surface abuse paths "
                    "that traverse tier zero assets, service accounts, and delegated privileges."
                ),
                "usage": (
                    "Analysts run Cypher queries such as `MATCH p=shortestPath((u:User)-[*1..]->(g:Group)` to enumerate escalation "
                    "chains and validate remediation steps before production rollout."
                ),
            },
            {
                "name": "Azure AD Connect Health",
                "description": (
                    "The monitoring service captures synchronization health, authentication failures, and suspicious device joins "
                    "across hybrid deployments that blend on-premises AD with Azure AD."
                ),
                "usage": (
                    "Incident responders export health telemetry with PowerShell cmdlets like `Get-AzureADConnectHealthADDSConnectorStatus` "
                    "to baseline replication latency and uncover malicious configuration drift."
                ),
            },
            {
                "name": "Mimikatz",
                "description": (
                    "Credential extraction tooling like Mimikatz demonstrates how attackers capture Kerberos tickets, PRTs, and "
                    "cached passwords from improperly hardened domain controllers."
                ),
                "usage": (
                    "Blue teams replicate techniques with constrained admin workstations and monitor for Event ID 4624 anomalies when "
                    "Mimikatz modules execute against LSASS or DPAPI secrets."
                ),
            },
            {
                "name": "AzureHound",
                "description": (
                    "AzureHound extends BloodHound collection into Azure AD, ingesting role assignments, applications, service "
                    "principals, and conditional access policies for unified graph analysis."
                ),
                "usage": (
                    "Detection engineers schedule AzureHound collectors via Azure Functions to continuously review cloud-only attack "
                    "paths and integrate alerts into Microsoft Sentinel workbooks."
                ),
            },
            {
                "name": "Defender for Identity",
                "description": (
                    "Microsoft Defender for Identity inspects domain controller traffic to flag unusual Kerberos pre-auth, DCSync "
                    "behavior, and lateral movement heuristics."
                ),
                "usage": (
                    "Threat hunters pivot through Defender for Identity timelines to correlate anomalous authentication sequences with "
                    "device context derived from Defender for Endpoint."
                ),
            },
        ],
        "telemetry": [
            {
                "name": "Azure AD sign-in logs",
                "description": (
                    "The logs surface conditional access evaluations, device compliance decisions, IP reputation, and token types "
                    "for every interactive and non-interactive sign-in."
                ),
                "analysis": (
                    "Correlation across sign-in logs, Azure AD audit logs, and Microsoft 365 Unified Audit Log entries reveals "
                    "suspicious user agent spoofing or impossible travel patterns indicative of token replay."
                ),
            },
            {
                "name": "Azure AD audit logs",
                "description": (
                    "Audit logs capture configuration drift, service principal secret rotations, privileged role assignments, and "
                    "application consent operations."
                ),
                "analysis": (
                    "Security engineers stream audit events to Log Analytics workspaces to create KQL detections for suspicious "
                    "additions to the Global Administrator role or service principal credential updates."
                ),
            },
            {
                "name": "Defender for Cloud Apps",
                "description": (
                    "Microsoft Defender for Cloud Apps integrates OAuth app governance, session controls, and anomaly detection to "
                    "surface risky third-party integrations."
                ),
                "analysis": (
                    "Investigators review the App governance risk workbook to identify multi-tenant applications pulling excessive "
                    "Graph permissions shortly before suspicious mailbox rule creation."
                ),
            },
            {
                "name": "Azure AD Connect health logs",
                "description": (
                    "Synchronization health metrics detail password hash sync status, PTA agent health, and unexpected object "
                    "deletions flowing between forests."
                ),
                "analysis": (
                    "When attackers tamper with staging servers, engineers compare health logs to AD replication metadata to verify "
                    "unauthorized connector modifications."
                ),
            },
        ],
        "attacks": [
            {
                "name": "Pass-the-PRT",
                "description": (
                    "Adversaries steal Primary Refresh Tokens from compromised Windows 10 devices to mint new access tokens and bypass "
                    "MFA-enforced conditional access."
                ),
                "detection": (
                    "Look for anomalous `grant_type=refresh_token` requests where the device ID differs from the registered "
                    "Intune identifier and the session originates from unfamiliar ASN ranges."
                ),
            },
            {
                "name": "Golden SAML",
                "description": (
                    "Golden SAML attacks compromise AD FS token-signing certificates, enabling forged SAML assertions to cloud "
                    "services without touching Azure AD directly."
                ),
                "detection": (
                    "Instrument AD FS with auditing of Event ID 307 and monitor for unusual token issuance volume that lacks "
                    "corresponding AD authentication logs."
                ),
            },
            {
                "name": "Azure AD Connect staging takeover",
                "description": (
                    "Attackers gain administrative access to staging servers, modify sync rules, and inject credentials into on-prem "
                    "AD with stealthy attribute flows."
                ),
                "detection": (
                    "Compare exported sync rule configurations with baseline backups and alert on unexpected rule precedence "
                    "changes or injected transformation scripts."
                ),
            },
            {
                "name": "Illicit consent grant",
                "description": (
                    "Consent phishing lures administrators into authorizing rogue multi-tenant applications that harvest mailbox "
                    "contents and Graph data silently."
                ),
                "detection": (
                    "Use Azure AD Identity Protection policies to require admin consent workflows and alert on OAuth apps requesting "
                    "high-impact permissions."
                ),
            },
        ],
        "incidents": [
            {
                "name": "SolarWinds 2020",
                "description": (
                    "The Nobelium intrusion demonstrated how forged SAML tokens granted persistent access to Microsoft 365 tenants "
                    "while operators blended into legitimate federated identity traffic."
                ),
                "lesson": (
                    "Organizations hardened AD FS, rotated signing certificates, and implemented certificate lifecycle monitoring "
                    "paired with workload identity governance after the breach."
                ),
            },
            {
                "name": "Password spray campaigns against O365 tenants",
                "description": (
                    "Nation-state actors rotated through common passwords while staying under account lockout thresholds across "
                    "thousands of Azure AD tenants."
                ),
                "lesson": (
                    "Defenders enforced smart lockout, deployed Conditional Access with compliant devices, and reviewed sign-in "
                    "risk detection to block commodity sprays."
                ),
            },
            {
                "name": "LAPS credential theft in hybrid environments",
                "description": (
                    "Attackers abused misconfigured Local Administrator Password Solution deployments to retrieve cleartext local "
                    "admin passwords from Azure AD synced attributes."
                ),
                "lesson": (
                    "Security teams hardened ACLs, enabled encrypted attribute sync, and audited who could read ms-Mcs-AdmPwd "
                    "values through Graph Explorer."
                ),
            },
        ],
        "pitfalls": [
            "Many hybrid identity teams leave emergency break-glass accounts exempt from Conditional Access indefinitely, creating golden tickets for adversaries who discover legacy credentials.",
            "Administrators frequently rely on default synchronization rules and fail to review transformation scripts, allowing malicious attribute flows to persist unnoticed for months.",
            "Overlooking Intune device compliance drift means Primary Refresh Tokens keep refreshing from non-compliant machines long after the initial compromise.",
            "Organizations trust perimeter IP allow lists even though attackers routinely proxy through residential IP ranges that bypass geographic filters.",
        ],
        "troubleshooting": [
            "Baseline Conditional Access policies in a lower environment, then replay risky sign-in patterns with test accounts to confirm enforcement logic works as designed.",
            "Export Azure AD audit logs to a SIEM and pivot on correlation IDs to stitch together user, device, and application context during complex hybrid incidents.",
            "When authentication anomalies appear, capture Fiddler traces and compare JWT token claims to expected resource audiences and tenant IDs.",
            "Create PowerShell scripts that query MS Graph beta endpoints for service principal credential states to quickly identify stale secrets or certificates.",
        ],
        "memory_hooks": [
            {
                "mnemonic": "TOKEN",
                "story": (
                    "Remember TOKEN: Track refresh tokens, Observe Conditional Access, Keep AD Connect hardened, Examine app consents, Neutralize illicit grants."
                ),
                "visual": (
                    "Visualize a security analyst guarding a vault labeled TOKEN while ropes connect on-prem servers to Azure clouds."
                ),
            },
            {
                "mnemonic": "SYNC",
                "story": (
                    "SYNC stands for Secure connectors, Yield telemetry, Nullify drift, and Control privilege escalations across hybrid edges."
                ),
                "visual": (
                    "Imagine gears labeled S, Y, N, C keeping cloud and on-premises directories aligned while sensors pulse telemetry lights."
                ),
            },
        ],
        "reflection_prompts": [
            "Which hybrid identity signals in your environment currently lack centralized monitoring, and how would an attacker abuse that blind spot?",
            "How can you validate that break-glass accounts truly follow least privilege and emergency rotation policies?",
            "Where should Conditional Access policies be simulated before production rollout to prevent business outages while still enforcing zero trust principles?",
        ],
        "encouragement": [
            "Hybrid identity defense is a marathon, not a sprint. Every improvement you make to Conditional Access or sync hygiene directly protects users from token theft campaigns.",
            "You are translating dense authentication theory into actionable detections that stop real intrusions. Celebrate the depth of expertise you are building."
        ],
        "next_steps": [
            "Review Microsoft’s Azure AD attack matrix and map each technique to existing detections and gaps in your SOC runbooks.",
            "Automate export of Azure AD sign-in logs into a notebook environment to experiment with anomaly detection on refresh token patterns.",
            "Pilot privileged identity management (PIM) for service principals to limit long-lived application secrets."
        ],
        "commands": [
            {
                "snippet": (
                    "Get-AzureADAuditDirectoryLogs -Filter \"activityDisplayName eq 'Add app role assignment to service principal'\""
                ),
                "context": (
                    "This PowerShell command retrieves Azure AD audit events when administrators grant new permissions to service principals, highlighting potential illicit consent grants."
                ),
            },
            {
                "snippet": "Invoke-ADFSSecurityAssessment.ps1 -SkipAutoUpdate -ExportCSV .\adfs_findings.csv",
                "context": (
                    "Running the AD FS security assessment script surfaces weak TLS settings, outdated certificates, and missing auditing critical for preventing Golden SAML attacks."
                ),
            },
            {
                "snippet": "Get-MsolDevice -All | Where-Object { $_.ComplianceStatus -ne 'Compliant' }",
                "context": (
                    "Querying device compliance status via MSOnline modules quickly reveals laptops that are still refreshing tokens despite falling out of policy."
                ),
            },
            {
                "snippet": "MATCH p=shortestPath((n:User {name:'svc_sql'})-[*1..]->(m:Group {name:'Domain Admins'})) RETURN p",
                "context": (
                    "This BloodHound Cypher query demonstrates how a compromised service account could pivot into the Domain Admins group, illustrating graph-powered detections."
                ),
            },
        ],
        "case_studies": [
            {
                "scenario": "Nobelium’s cloud pivot",
                "details": (
                    "After compromising on-premises SolarWinds Orion servers, Nobelium actors accessed AD FS token signing certificates, forged tokens, and quietly exfiltrated data from Microsoft 365 mailboxes over months."
                ),
                "response": (
                    "Responders isolated Orion servers, rebuilt AD FS infrastructure, rotated certificates, and audited every privileged consent to cut off persistence."
                ),
            },
            {
                "scenario": "Pass-the-PRT in a manufacturing tenant",
                "details": (
                    "Attackers reused a stolen Primary Refresh Token from an unmanaged kiosk device to access SharePoint Online engineering plans, bypassing MFA entirely."
                ),
                "response": (
                    "The SOC forced token revocation, required compliant devices, and enforced device-based Conditional Access policies before re-enabling external collaboration."
                ),
            },
        ],
    },
    "ai_security": {
        "tools": [
            {
                "name": "TensorFlow Privacy",
                "description": (
                    "TensorFlow Privacy enables differential privacy training routines that inject calibrated noise into gradients to reduce exposure of sensitive training examples."
                ),
                "usage": (
                    "Security engineers instrument privacy budgets and clipping norms, then monitor model utility metrics to maintain accuracy while preventing membership inference leaks."
                ),
            },
            {
                "name": "Microsoft Counterfit",
                "description": (
                    "Counterfit automates adversarial robustness testing by orchestrating evasion, poisoning, and model extraction attacks against machine learning endpoints."
                ),
                "usage": (
                    "Teams integrate Counterfit into CI pipelines, replaying attacks like Fast Gradient Sign Method and TextFooler to validate that mitigations block real adversarial perturbations."
                ),
            },
            {
                "name": "IBM Adversarial Robustness Toolbox",
                "description": (
                    "The toolkit provides wrappers for TensorFlow, PyTorch, and scikit-learn models, bundling dozens of attack algorithms alongside defenses like feature squeezing."
                ),
                "usage": (
                    "ML security specialists script experiments to evaluate how logits shift under Carlini-Wagner or boundary attacks while logging precision and recall changes."
                ),
            },
            {
                "name": "OpenAI Evals",
                "description": (
                    "OpenAI Evals automates scenario-based evaluations to test prompt injection resilience, jailbreak detection, and safety classifier performance for large language models."
                ),
                "usage": (
                    "Trust and safety teams compose evaluation suites mixing malicious instructions, data exfiltration prompts, and red-team transcripts to benchmark mitigation effectiveness."
                ),
            },
        ],
        "telemetry": [
            {
                "name": "Model inference logs",
                "description": (
                    "Inference logs record prompts, response latencies, token usage, and user identifiers across interactive ML workloads."
                ),
                "analysis": (
                    "Streaming logs into SIEM platforms enables detectors that flag prompt injection attempts, suspicious data exfiltration patterns, or spikes in refusal overrides."
                ),
            },
            {
                "name": "Training pipeline audit trails",
                "description": (
                    "Machine learning pipelines emit metadata about dataset versions, feature engineering notebooks, hyperparameters, and container images."
                ),
                "analysis": (
                    "Auditors track lineage to ensure only approved datasets feed the pipeline and to detect poisoning attacks where adversaries manipulate upstream features."
                ),
            },
            {
                "name": "GPU utilization metrics",
                "description": (
                    "GPU monitoring surfaces resource spikes, kernel panics, and unusual memory pressure that often accompany cryptomining or rogue model training workloads."
                ),
                "analysis": (
                    "Operations teams correlate GPU anomalies with scheduler logs to quarantine compromised Kubernetes nodes before lateral movement spreads."
                ),
            },
        ],
        "attacks": [
            {
                "name": "Prompt injection",
                "description": (
                    "Attackers craft inputs that redirect model behavior, override safety policies, or exfiltrate system prompts embedded within LLM-powered applications."
                ),
                "detection": (
                    "Monitor for tokens associated with jailbreak instructions, deploy output filtering, and validate downstream actions with rule-based guardrails."
                ),
            },
            {
                "name": "Data poisoning",
                "description": (
                    "Malicious contributions to training datasets skew model outputs, degrade accuracy, or implant backdoors triggered by specific inputs."
                ),
                "detection": (
                    "Use robust statistics, dataset sanitization, and cross-validation to spot label distribution shifts or anomalous feature vectors."
                ),
            },
            {
                "name": "Model inversion",
                "description": (
                    "Inversion attacks reconstruct training data records by repeatedly querying exposed model endpoints."
                ),
                "detection": (
                    "Throttle requests, apply differential privacy, and track repeated queries targeting sensitive attribute combinations."
                ),
            },
            {
                "name": "Model extraction",
                "description": (
                    "Adversaries approximate proprietary models by harvesting prediction APIs and training surrogate models."
                ),
                "detection": (
                    "Rate-limit unknown clients, watermark outputs, and compare query fingerprints against baseline customer behavior."
                ),
            },
        ],
        "incidents": [
            {
                "name": "GPT-4 jailbreak red-teaming",
                "description": (
                    "External researchers combined prompt injection with retrieval plugins to draw out system prompts and bypass safety classifiers."
                ),
                "lesson": (
                    "Vendors responded by layering content filters, adding memory scrubbers, and codifying allowed tool usage scopes."
                ),
            },
            {
                "name": "Tesla autopilot adversarial examples",
                "description": (
                    "Researchers placed stickers on road signs that caused vision models to misclassify speed limits, leading to dangerous acceleration."
                ),
                "lesson": (
                    "Manufacturers incorporated redundancy, map validation, and adversarial training to harden perception pipelines."
                ),
            },
            {
                "name": "Microsoft Tay chatbot",
                "description": (
                    "Coordinated trolling campaigns poisoned the chatbot’s language model, forcing Microsoft to shut it down within 24 hours of launch."
                ),
                "lesson": (
                    "The incident highlighted the need for aggressive content filtering, moderation tooling, and human-in-the-loop oversight."
                ),
            },
        ],
        "pitfalls": [
            "Teams release generative AI prototypes without red teaming for prompt injection, leaving workflows open to data exfiltration or malicious tool invocation.",
            "Security reviews often stop at API authentication and ignore dataset lineage, creating blind spots for poisoning attacks within MLOps pipelines.",
            "Organizations frequently log only aggregated model metrics, preventing investigators from reconstructing the exact prompts and responses involved in an incident.",
        ],
        "troubleshooting": [
            "Capture full inference traces including prompts, temperature, and system responses when an LLM misbehaves so engineers can replay the scenario in a sandbox.",
            "Run reproducibility checks by rebuilding models from declared datasets and hyperparameters to ensure release artifacts match governance records.",
            "Inject known adversarial examples into canary deployments to confirm monitoring detects and blocks malicious behavior before production exposure.",
        ],
        "memory_hooks": [
            {
                "mnemonic": "MODEL",
                "story": (
                    "MODEL reminds you to Monitor prompts, Observe datasets, Defend endpoints, Evaluate resilience, and Limit exposure."
                ),
                "visual": (
                    "Picture a model card shielded by five concentric rings labeled Monitor, Observe, Defend, Evaluate, Limit."
                ),
            },
            {
                "mnemonic": "GUARD",
                "story": (
                    "GUARD captures Gather telemetry, Understand threat models, Assess mitigations, Review incidents, and Deploy red teaming."
                ),
                "visual": (
                    "Imagine a neural network wearing armor plates stamped with each GUARD verb to reinforce defense in depth."
                ),
            },
        ],
        "reflection_prompts": [
            "Which parts of your ML pipeline currently lack differential privacy or robust statistics, and how would you mitigate targeted poisoning?",
            "What human approval checkpoints exist before high-impact model predictions trigger automated actions in your organization?",
            "How will you evaluate third-party model providers for secure development, deployment, and monitoring practices?",
        ],
        "encouragement": [
            "Every experiment you run to stress test a model makes downstream users safer. You are defining what trustworthy AI operations look like.",
            "Stay curious about attack research. Rapid iteration keeps you ahead of adversaries and builds a culture of resilient machine learning."
        ],
        "next_steps": [
            "Publish a model card that documents training data sources, evaluation metrics, and known limitations for your flagship model.",
            "Integrate automated adversarial testing into CI/CD so every release shows evidence of robustness checks.",
            "Coordinate with legal and ethics teams to define escalation paths when models produce harmful or biased outputs."
        ],
        "commands": [
            {
                "snippet": "counterfit run --config configs/prompt_injection.yaml",
                "context": (
                    "Executes a Counterfit prompt-injection test plan that replays malicious instructions against an LLM endpoint to validate guardrail effectiveness."
                ),
            },
            {
                "snippet": "python -m tensorflow_privacy.privacy.optimizers.dp_optimizer_keras_example --noise_multiplier=1.1 --l2_norm_clip=1.5",
                "context": (
                    "Runs a TensorFlow Privacy training script with differential privacy parameters tuned to balance epsilon budgets and accuracy."
                ),
            },
            {
                "snippet": "kubectl logs deployment/model-serving -c inference --since=1h",
                "context": (
                    "Pulls inference logs from a Kubernetes deployment so analysts can inspect prompts and responses during an ongoing incident."
                ),
            },
            {
                "snippet": "az monitor metrics list --resource /subscriptions/... --metric GPUUtilizationPercent",
                "context": (
                    "Queries Azure Monitor for GPU utilization to detect unexpected spikes that may indicate rogue training jobs or cryptomining."
                ),
            },
        ],
        "case_studies": [
            {
                "scenario": "Financial chatbot prompt injection",
                "details": (
                    "Attackers embedded malicious instructions inside uploaded PDF statements, causing a chatbot to summarize and exfiltrate confidential account details."
                ),
                "response": (
                    "The bank added document sanitization, contextual output filters, and human approval checkpoints for high-risk intents."
                ),
            },
            {
                "scenario": "Healthcare model inversion",
                "details": (
                    "An adversary repeatedly queried a medical diagnosis API to reconstruct sensitive patient imaging data from prediction confidence scores."
                ),
                "response": (
                    "Engineers applied differential privacy noise, rate limiting, and monitoring to prevent future reconstructions while retraining on sanitized datasets."
                ),
            },
        ],
    },
    "blue_team": {
        "tools": [
            {
                "name": "Microsoft Sentinel",
                "description": (
                    "Sentinel correlates telemetry from Azure, Microsoft 365, and third-party data sources to power hunting,"
                    " alerting, and automated incident response workflows."
                ),
                "usage": (
                    "SOC analysts build KQL workbooks, fusion detections, and playbooks that orchestrate Logic Apps for rapid"
                    " containment."
                ),
            },
            {
                "name": "Splunk Enterprise Security",
                "description": (
                    "Splunk ES provides risk-based alerting, adaptive response actions, and data models for common security"
                    " domains."
                ),
                "usage": (
                    "Blue teams create correlation searches that combine endpoint, firewall, and identity data, then trigger"
                    " Phantom playbooks to isolate hosts."
                ),
            },
            {
                "name": "ELK Stack",
                "description": (
                    "Elastic, Logstash, and Kibana deliver scalable log ingestion, transformation, and visualization for custom"
                    " detection engineering."
                ),
                "usage": (
                    "Detection engineers leverage Elasticsearch query DSL to craft behavioral analytics and integrate machine"
                    " learning jobs for anomaly scoring."
                ),
            },
            {
                "name": "Sigma",
                "description": (
                    "Sigma offers a generic signature format that can be translated into SIEM-specific queries across Splunk,"
                    " Sentinel, Elastic, and more."
                ),
                "usage": (
                    "Teams maintain version-controlled Sigma repositories, run `sigmac` to compile queries, and push updates"
                    " via CI pipelines."
                ),
            },
        ],
        "telemetry": [
            {
                "name": "Windows Event Forwarding",
                "description": (
                    "WEF aggregates endpoint security logs, PowerShell transcript data, and Sysmon telemetry into a central"
                    " collector."
                ),
                "analysis": (
                    "SOC operators baseline event frequency, create detection rules for Event IDs 4104, 4688, and 4720, and"
                    " correlate suspicious process chains."
                ),
            },
            {
                "name": "EDR telemetry",
                "description": (
                    "Endpoint detection and response platforms capture process trees, network connections, memory indicators,"
                    " and malicious activity scores."
                ),
                "analysis": (
                    "Incident responders pivot from detections into timeline views, compare parent-child process context, and"
                    " quarantine endpoints via API."
                ),
            },
            {
                "name": "Network flow records",
                "description": (
                    "NetFlow, IPFIX, and Zeek telemetry expose lateral movement, beaconing, and data exfiltration attempts across"
                    " enterprise networks."
                ),
                "analysis": (
                    "Blue teams enrich flows with asset metadata, apply threat intelligence for command-and-control detection,"
                    " and escalate suspicious sessions for packet capture."
                ),
            },
        ],
        "attacks": [
            {
                "name": "Credential dumping",
                "description": (
                    "Attackers harvest credentials from LSASS memory, SAM databases, or browser stores to escalate privilege."
                ),
                "detection": (
                    "Monitor for Event ID 10 Sysmon process access, unexpected `lsass.exe` handle requests, and memory dump"
                    " artifacts."
                ),
            },
            {
                "name": "Command and control beaconing",
                "description": (
                    "Persistent backdoors communicate with remote infrastructure, using low-and-slow beacons to avoid detection."
                ),
                "detection": (
                    "Apply statistical models to network flow intervals, inspect JA3/JA3S TLS fingerprints, and correlate DNS"
                    " tunneling patterns."
                ),
            },
            {
                "name": "Living-off-the-land",
                "description": (
                    "Adversaries abuse native binaries such as PowerShell, certutil, and mshta to evade traditional security"
                    " controls."
                ),
                "detection": (
                    "Baseline script block logging, alert on suspicious encoded commands, and review LOLBAS catalog updates."
                ),
            },
        ],
        "incidents": [
            {
                "name": "NotPetya response",
                "description": (
                    "Enterprises worldwide rebuilt networks after destructive wiper malware masqueraded as ransomware."
                ),
                "lesson": (
                    "Effective blue teams executed isolation playbooks, redeployed golden images, and validated segmentation"
                    " to prevent reinfection."
                ),
            },
            {
                "name": "Colonial Pipeline",
                "description": (
                    "A DarkSide ransomware affiliate disrupted fuel distribution, forcing shutdown of pipeline operations."
                ),
                "lesson": (
                    "SOC teams emphasized identity security, EDR coverage, and incident command structures for critical"
                    " infrastructure."
                ),
            },
            {
                "name": "Capital One insider threat",
                "description": (
                    "A misconfigured firewall allowed data exfiltration by an attacker leveraging AWS metadata service flaws."
                ),
                "lesson": (
                    "Blue teams integrated cloud telemetry, anomaly detection, and zero-trust segmentation to reduce future"
                    " exposure."
                ),
            },
        ],
        "pitfalls": [
            "Alert fatigue causes analysts to miss subtle anomalies hidden among thousands of commodity detections.",
            "Playbooks often assume on-premises environments and neglect SaaS and cloud telemetry sources.",
            "Lack of asset inventory makes it difficult to prioritize triage when multiple high severity alerts trigger"
            " simultaneously.",
        ],
        "troubleshooting": [
            "Validate detection fidelity in a lab before production rollout by replaying attack datasets and measuring signal"
            " to noise ratios.",
            "Establish chatops channels and runbooks for escalations so cross-functional stakeholders can coordinate quickly.",
            "Instrument ticketing systems with structured fields to capture MITRE ATT&CK techniques, response actions, and"
            " lessons learned for later analysis.",
        ],
        "memory_hooks": [
            {
                "mnemonic": "SHIELD",
                "story": (
                    "SHIELD represents Scope telemetry, Hunt continuously, Integrate automation, Establish communication,"
                    " Learn from incidents, and Document outcomes."
                ),
                "visual": (
                    "Picture a SOC command center with a shield formed by dashboards, playbooks, and collaboration tools"
                    " guarding the enterprise."
                ),
            },
            {
                "mnemonic": "PACE",
                "story": (
                    "PACE stands for Preventive controls, Active monitoring, Containment readiness, and Evidence preservation."
                ),
                "visual": (
                    "Imagine a relay race where each runner hands off detections, triage, containment, and recovery flawlessly."
                ),
            },
        ],
        "reflection_prompts": [
            "How does your SOC measure detection coverage across the MITRE ATT&CK matrix, and where are the gaps?",
            "Which response playbooks require cross-team rehearsals with legal, communications, or OT stakeholders?",
            "How can automation reduce manual toil without hiding critical investigative context?",
        ],
        "encouragement": [
            "Every alert you investigate protects customers and colleagues. Your diligence turns raw telemetry into real risk"
            " reduction.",
            "Analysts who document lessons learned improve the entire organization’s resilience. Your curiosity drives"
            " continual improvement."
        ],
        "next_steps": [
            "Run a purple team exercise to validate SOC detections against real adversary tradecraft.",
            "Automate enrichment for priority alerts using threat intelligence, asset criticality, and vulnerability data.",
            "Develop metrics dashboards that show mean time to detect, respond, and remediate across incident categories."
        ],
        "commands": [
            {
                "snippet": "Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-Sysmon/Operational'; ID=4104} | Select-Object TimeCreated,Message",
                "context": (
                    "Extracts PowerShell Script Block logging events so analysts can hunt for encoded or obfuscated commands."
                ),
            },
            {
                "snippet": (
                    "es_query='process_name:cmd.exe AND child_process_name:powershell.exe'; "
                    "curl -XPOST http://localhost:9200/soc-events/_search "
                    "-H 'Content-Type: application/json' "
                    "-d \"{\\\"query\\\":{\\\"query_string\\\":{\\\"query\\\":\\\"${es_query}\\\"}}}\""
                ),
                "context": (
                    "Queries Elastic for suspicious process spawn patterns linking command shells and PowerShell."
                ),
            },
            {
                "snippet": "sourcetype=firewall action=blocked | stats count by src_ip, dest_ip, dest_port | sort -count",
                "context": (
                    "Splunk search highlighting repeated blocked connections that may indicate command-and-control testing."
                ),
            },
        ],
        "case_studies": [
            {
                "scenario": "Ransomware rapid response",
                "details": (
                    "A regional hospital detected anomalous SMB traffic, isolated affected segments within minutes, and prevented"
                    " encryption of electronic medical records."
                ),
                "response": (
                    "Runbooks guided containment, backups restored critical systems, and post-incident reviews improved detection"
                    " rules."
                ),
            },
            {
                "scenario": "BEC disruption",
                "details": (
                    "Blue team analysts spotted suspicious mailbox forwarding rules and stopped a business email compromise"
                    " targeting accounts payable."
                ),
                "response": (
                    "They reset credentials, enabled MFA, implemented DMARC enforcement, and coached finance teams on verification"
                    " steps."
                ),
            },
        ],
    },
    "cloud": {
        "tools": [
            {
                "name": "AWS Config",
                "description": (
                    "AWS Config continuously evaluates infrastructure state against compliance rules, flagging drift and"
                    " insecure configurations across regions."
                ),
                "usage": (
                    "Cloud security teams author custom rules in Lambda, integrate findings with Security Hub, and trigger"
                    " remediation via Systems Manager automation documents."
                ),
            },
            {
                "name": "Azure Policy",
                "description": (
                    "Azure Policy enforces resource governance, requiring tags, approved SKUs, and network restrictions"
                    " across subscriptions."
                ),
                "usage": (
                    "Engineers deploy policy initiatives, remediate non-compliant resources with managed identities, and"
                    " track compliance posture in Azure Security Center."
                ),
            },
            {
                "name": "GCP Security Command Center",
                "description": (
                    "SCC aggregates findings from services such as Web Security Scanner, Event Threat Detection, and"
                    " Container Analysis."
                ),
                "usage": (
                    "Operators prioritize findings, connect Chronicle SOAR playbooks, and collaborate with developers to"
                    " patch vulnerable workloads."
                ),
            },
            {
                "name": "Terraform Cloud",
                "description": (
                    "Terraform Cloud centralizes infrastructure as code with policy as code (Sentinel) to prevent risky"
                    " deployments."
                ),
                "usage": (
                    "Security teams add Sentinel policies enforcing encryption, version pinning, and explicit approvals before"
                    " apply stages proceed."
                ),
            },
        ],
        "telemetry": [
            {
                "name": "AWS CloudTrail",
                "description": (
                    "CloudTrail records API calls, IAM activity, and resource changes across AWS accounts."
                ),
                "analysis": (
                    "Analysts stream logs to S3 and Athena, query unusual AssumeRole sequences, and detect credential"
                    " abuse via GuardDuty."
                ),
            },
            {
                "name": "Azure Activity Logs",
                "description": (
                    "Activity logs capture administrative operations, service health events, and policy evaluations in"
                    " Azure."
                ),
                "analysis": (
                    "Security analysts send logs to Log Analytics, join with Azure AD sign-ins, and detect suspicious service"
                    " principal creations."
                ),
            },
            {
                "name": "GCP Audit Logs",
                "description": (
                    "Admin, data access, and system event logs provide visibility into Google Cloud resource activity."
                ),
                "analysis": (
                    "Teams export logs to BigQuery, craft scheduled queries to identify public storage buckets, and alert"
                    " on IAM policy tampering."
                ),
            },
            {
                "name": "VPC Flow Logs",
                "description": (
                    "Flow logs capture accepted and rejected traffic metadata across cloud networks."
                ),
                "analysis": (
                    "Engineers examine sudden egress spikes, flag communication with TOR exit nodes, and verify segmentation"
                    " boundaries."
                ),
            },
        ],
        "attacks": [
            {
                "name": "IAM privilege escalation",
                "description": (
                    "Misconfigured IAM policies allow attackers to escalate privileges via PassRole, AttachRolePolicy, or"
                    " lambda:UpdateFunctionCode."
                ),
                "detection": (
                    "Alert on policy changes granting `iam:*` permissions, monitor CloudTrail for suspicious `AssumeRole`"
                    " into admin roles, and require MFA."
                ),
            },
            {
                "name": "Public storage exposure",
                "description": (
                    "Misconfigured S3 buckets, Azure Blob containers, or GCS buckets leak sensitive data."
                ),
                "detection": (
                    "Use Config, Azure Storage analytics, or SCC findings to identify public ACLs and enforce encryption."
                ),
            },
            {
                "name": "Serverless abuse",
                "description": (
                    "Attackers exploit over-permissioned Lambda, Functions, or Cloud Functions to pivot deeper into"
                    " environments."
                ),
                "detection": (
                    "Monitor invocation patterns, restrict environment variables, and inspect build artifacts for secrets."
                ),
            },
            {
                "name": "Container escape",
                "description": (
                    "Compromised containers leverage kernel exploits or metadata service access to control hosts."
                ),
                "detection": (
                    "Deploy eBPF sensors, enable GKE workload identity, and restrict IMDSv2 tokens in AWS."
                ),
            },
        ],
        "incidents": [
            {
                "name": "Code Spaces breach",
                "description": (
                    "Attackers deleted AWS resources after compromising console credentials lacking multi-factor"
                    " authentication."
                ),
                "lesson": (
                    "The incident highlighted the need for IAM least privilege, MFA everywhere, and disaster recovery"
                    " automation."
                ),
            },
            {
                "name": "Tesla Kubernetes console compromise",
                "description": (
                    "Unauthenticated Kubernetes consoles exposed AWS credentials, enabling cryptomining workloads."
                ),
                "lesson": (
                    "Defenders enforced RBAC, restricted metadata access, and improved container image scanning pipelines."
                ),
            },
            {
                "name": "Accenture LockBit incident",
                "description": (
                    "Ransomware affiliates targeted cloud-hosted systems and exfiltrated data through remote access services."
                ),
                "lesson": (
                    "Cloud SOC teams revalidated remote access controls, hardened privileged identities, and improved"
                    " segmentation."
                ),
            },
        ],
        "pitfalls": [
            "Shadow IT cloud accounts bypass centralized monitoring and quickly drift from security baselines.",
            "Teams neglect to rotate access keys and service principals, allowing long-lived credentials to accumulate risk.",
            "Infrastructure as code templates are rarely security-reviewed, replicating misconfigurations at scale.",
        ],
        "troubleshooting": [
            "Continuously compare deployed resources with infrastructure as code repositories to detect manual drift.",
            "Use AWS Config timelines, Azure Resource Graph, or gcloud asset inventory snapshots to reconstruct incident"
            " timelines.",
            "Automate cross-account log aggregation so investigators can pivot between production, staging, and security"
            " tooling quickly.",
        ],
        "memory_hooks": [
            {
                "mnemonic": "CLOUD",
                "story": (
                    "CLOUD reminds you to Catalog accounts, Lock identities, Observe telemetry, Use automation, and Defend"
                    " workloads."
                ),
                "visual": (
                    "Envision a layered cloud skyline where each layer is labeled Catalog, Lock, Observe, Use, Defend."
                ),
            },
            {
                "mnemonic": "STACK",
                "story": (
                    "STACK stands for Secure storage, Tighten IAM, Automate policy, Check network paths, and Keep IaC"
                    " reviewed."
                ),
                "visual": (
                    "Picture cloud resources stacked like blocks with security engineers reinforcing each layer."
                ),
            },
        ],
        "reflection_prompts": [
            "How many cloud accounts can you audit within an hour, and what automation would shorten that time?",
            "Where do you enforce preventive controls versus detective alerts for misconfigurations?",
            "How do you validate that developers follow secure defaults when launching new services?",
        ],
        "encouragement": [
            "Cloud environments evolve daily. Your efforts to codify guardrails keep innovation safe for every team",
            " shipping to production.",
            "You are building cross-cloud expertise that translates into resilient architectures customers can trust."
        ],
        "next_steps": [
            "Enable organization-wide guardrails such as AWS Service Control Policies or Azure Blueprints.",
            "Integrate CIS benchmark scans into CI pipelines for Terraform, ARM, or Cloud Deployment Manager templates.",
            "Establish game days simulating misconfigurations to test alerting and response."
        ],
        "commands": [
            {
                "snippet": "aws iam generate-service-last-accessed-details --arn arn:aws:iam::123456789012:role/SecurityAudit",
                "context": (
                    "Generates IAM last accessed reports to find over-permissioned roles requiring review."
                ),
            },
            {
                "snippet": "az policy assignment list --include-descendants",
                "context": (
                    "Enumerates Azure Policy assignments across management groups and subscriptions to verify coverage."
                ),
            },
            {
                "snippet": "gcloud storage buckets list --format='value(name,iamConfiguration.uniformBucketLevelAccess)'",
                "context": (
                    "Identifies GCS buckets lacking uniform bucket-level access controls."
                ),
            },
            {
                "snippet": "terraform fmt && terraform validate && terraform plan",
                "context": (
                    "Validates infrastructure as code changes before apply, enabling pre-deployment security reviews."
                ),
            },
        ],
        "case_studies": [
            {
                "scenario": "Over-permissioned CI/CD role",
                "details": (
                    "A CI pipeline role allowed `iam:PassRole` and `sts:AssumeRole` into production, enabling attackers to"
                    " escalate after stealing credentials."
                ),
                "response": (
                    "Security engineers refactored IAM policies, enforced least privilege, and added GuardDuty custom"
                    " detections."
                ),
            },
            {
                "scenario": "Public data lake exposure",
                "details": (
                    "Data scientists accidentally opened an analytics bucket to the internet, exposing sensitive telemetry."
                ),
                "response": (
                    "Incident responders revoked public access, rotated keys, and implemented SCPs blocking public S3"
                    " policies."
                ),
            },
        ],
    },
    "dfir": {
        "tools": [
            {
                "name": "Volatility 3",
                "description": (
                    "Volatility parses memory images to extract processes, network connections, DLLs, and registry hives"
                    " for incident response."
                ),
                "usage": (
                    "Forensic analysts build custom plugins, analyze userland injections, and compare baseline memory"
                    " profiles to detect anomalies."
                ),
            },
            {
                "name": "Plaso / log2timeline",
                "description": (
                    "Plaso processes diverse log sources to create unified forensic timelines for Windows, Linux, and"
                    " macOS systems."
                ),
                "usage": (
                    "Responders feed artifacts into Plaso, query super timelines, and correlate execution, file access,"
                    " and network events."
                ),
            },
            {
                "name": "Velociraptor",
                "description": (
                    "Velociraptor collects forensic artifacts at scale with VQL queries across endpoints."
                ),
                "usage": (
                    "Incident handlers deploy hunts, collect targeted registry keys, Master File Table entries, and process"
                    " creation logs, then stream results for analysis."
                ),
            },
            {
                "name": "Kape",
                "description": (
                    "Kroll Artifact Parser and Extractor automates artifact collection and parsing on compromised systems."
                ),
                "usage": (
                    "DFIR teams orchestrate targeted triage packages, extract browser data, jump lists, and SRUM artifacts"
                    " to accelerate investigations."
                ),
            },
        ],
        "telemetry": [
            {
                "name": "Windows event logs",
                "description": (
                    "Security, System, and Application logs reveal credential abuse, persistence, and lateral movement"
                    " indicators."
                ),
                "analysis": (
                    "Investigators parse EVTX files, highlight Event IDs 4624, 4688, 7045, and map activity to MITRE"
                    " ATT&CK techniques."
                ),
            },
            {
                "name": "NTFS metadata",
                "description": (
                    "Master File Table entries, USN journal records, and $LogFile entries provide file system activity"
                    " timelines."
                ),
                "analysis": (
                    "Analysts reconstruct file creation and deletion, recover timestamps, and detect timestomping attempts."
                ),
            },
            {
                "name": "Prefetch and Shimcache",
                "description": (
                    "Application execution artifacts highlight first-run timestamps and execution frequency."
                ),
                "analysis": (
                    "Responders compare prefetch metadata with malware dropper timelines to confirm execution sequences."
                ),
            },
            {
                "name": "Network packet captures",
                "description": (
                    "PCAPs capture command-and-control communications, data exfiltration, and lateral movement protocols."
                ),
                "analysis": (
                    "DFIR teams carve HTTP payloads, reconstruct TLS sessions, and extract IOCs for containment actions."
                ),
            },
        ],
        "attacks": [
            {
                "name": "Ransomware triage",
                "description": (
                    "Responders must identify initial access vectors, enumerate encrypted hosts, and preserve artifacts"
                    " before cleanup."
                ),
                "detection": (
                    "Analyze ransom notes, examine scheduled tasks or services, and trace command history for staging"
                    " scripts."
                ),
            },
            {
                "name": "Advanced persistent threat foothold",
                "description": (
                    "APT actors deploy stealthy implants, modify registry run keys, and abuse legitimate tools for persistence."
                ),
                "detection": (
                    "Hunt for anomalous WMI persistence, unusual DLL search order hijacking, and network beacons in memory"
                    " dumps."
                ),
            },
            {
                "name": "Insider data theft",
                "description": (
                    "Insiders copy intellectual property to removable media or cloud storage, often after-hours."
                ),
                "detection": (
                    "Review USB device history, shellbags, and browser cache records; correlate with VPN and proxy logs."
                ),
            },
        ],
        "incidents": [
            {
                "name": "Sony Pictures attack",
                "description": (
                    "Destructive wiper malware disabled systems, leaked data, and disrupted operations."
                ),
                "lesson": (
                    "DFIR teams validated backups, reconstructed wiper execution paths, and hardened network segmentation."
                ),
            },
            {
                "name": "Target POS breach",
                "description": (
                    "Attackers installed memory scraping malware on point-of-sale systems to steal card data."
                ),
                "lesson": (
                    "Investigators examined memory images, network traffic, and vendor remote access to remediate."
                ),
            },
            {
                "name": "Trisis/Triconex incident",
                "description": (
                    "Malware targeted industrial safety systems, manipulating controllers and forcing shutdowns."
                ),
                "lesson": (
                    "Responders collected engineering workstation forensics, reviewed ICS network captures, and coordinated"
                    " with OT teams."
                ),
            },
        ],
        "pitfalls": [
            "Failing to capture volatile memory before powering down systems destroys critical evidence.",
            "Not documenting chain of custody makes findings inadmissible and undermines trust with legal teams.",
            "Relying solely on antivirus detections overlooks manual artifacts like command history or registry changes.",
        ],
        "troubleshooting": [
            "Validate hash values immediately after evidence acquisition to ensure integrity during transfer.",
            "Use a forensic workstation isolated from production networks to avoid contaminating evidence.",
            "Cross-reference multiple artifact families (logs, registry, memory) to confirm hypotheses and reduce false"
            " positives.",
        ],
        "memory_hooks": [
            {
                "mnemonic": "ACQUIRE",
                "story": (
                    "ACQUIRE: Assess scope, Capture evidence, Quickly image memory, Understand timelines, Investigate artifacts,"
                    " Report findings, Escalate remediation."
                ),
                "visual": (
                    "Visualize a forensic toolkit labeled ACQUIRE with compartments for memory, disk, logs, and reports."
                ),
            },
            {
                "mnemonic": "TRACE",
                "story": (
                    "TRACE reminds you to Timeline, Reconstruct actions, Analyze malware, Confirm persistence, and Escalate to"
                    " stakeholders."
                ),
                "visual": (
                    "Imagine a detective following footprints labeled Timeline, Reconstruct, Analyze, Confirm, Escalate."
                ),
            },
        ],
        "reflection_prompts": [
            "How quickly can your team deploy memory capture across hundreds of endpoints?",
            "Which artifacts would confirm or refute the suspected initial access vector?",
            "Do you have legal-approved procedures for cross-border evidence handling?",
        ],
        "encouragement": [
            "Every artifact you recover tells part of the story. Your meticulous work restores business operations and"
            " protects victims.",
            "DFIR professionals transform chaos into clarity. Celebrate each timeline you rebuild."
        ],
        "next_steps": [
            "Establish a forensic readiness kit with write blockers, imaging tools, and triage scripts.",
            "Automate log preservation policies so critical evidence is retained beyond default retention.",
            "Schedule tabletop exercises focusing on evidence collection, legal approvals, and communications."
        ],
        "commands": [
            {
                "snippet": "vol -f memory.raw windows.pslist",
                "context": (
                    "Lists running processes from a Windows memory image, establishing baseline activity."
                ),
            },
            {
                "snippet": "log2timeline.py --storage-file timeline.plaso evidence/",
                "context": (
                    "Generates a Plaso storage file combining logs for timeline analysis."
                ),
            },
            {
                "snippet": "velociraptor query 'SELECT * FROM info()' --format json",
                "context": (
                    "Executes a VQL query across endpoints to gather system metadata."
                ),
            },
            {
                "snippet": "bulk_extractor -o artifacts/ usb_image.dd",
                "context": (
                    "Extracts artifacts such as email addresses and credit card numbers from disk images."
                ),
            },
        ],
        "case_studies": [
            {
                "scenario": "Credential theft investigation",
                "details": (
                    "An attacker harvested credentials via Mimikatz; responders analyzed LSASS memory dumps and event logs"
                    " to map lateral movement."
                ),
                "response": (
                    "They reset compromised accounts, deployed LSASS protection, and tuned EDR rules."
                ),
            },
            {
                "scenario": "Industrial control malware",
                "details": (
                    "Malicious code modified PLC logic; DFIR teams captured engineering workstation images and compared"
                    " ladder logic."
                ),
                "response": (
                    "They restored validated logic, segmented networks, and implemented strict access auditing."
                ),
            },
        ],
    },
    "fundamentals": {
        "tools": [
            {
                "name": "NIST Cybersecurity Framework",
                "description": (
                    "The CSF organizes security programs around identify, protect, detect, respond, and recover functions."
                ),
                "usage": (
                    "Security leaders map existing controls, highlight gaps, and prioritize improvements aligned with"
                    " business objectives."
                ),
            },
            {
                "name": "CIS Critical Security Controls",
                "description": (
                    "The CIS Controls provide prioritized safeguards for enterprise defenders, from asset inventory to"
                    " incident response."
                ),
                "usage": (
                    "Teams assess maturity, align initiatives, and measure progress through implementation groups."
                ),
            },
            {
                "name": "ISO/IEC 27001",
                "description": (
                    "ISO 27001 defines requirements for information security management systems (ISMS) and risk treatment."
                ),
                "usage": (
                    "Organizations document policies, conduct risk assessments, implement controls, and undergo audits"
                    " for certification."
                ),
            },
            {
                "name": "Risk register platforms",
                "description": (
                    "Tools such as ServiceNow GRC or RiskWatch track risks, mitigation plans, and residual exposure."
                ),
                "usage": (
                    "Security teams quantify likelihood and impact, assign owners, and align remediation timelines with"
                    " business priorities."
                ),
            },
        ],
        "telemetry": [
            {
                "name": "Vulnerability scans",
                "description": (
                    "Regular scans identify missing patches, misconfigurations, and insecure services across the enterprise."
                ),
                "analysis": (
                    "Risk teams prioritize remediation based on CVSS scores, asset criticality, and exploit availability."
                ),
            },
            {
                "name": "Configuration baselines",
                "description": (
                    "Benchmarks such as CIS hardening guides ensure systems adhere to secure configurations."
                ),
                "analysis": (
                    "GRC analysts review deviation reports and coordinate with system owners to close gaps."
                ),
            },
            {
                "name": "Policy exception logs",
                "description": (
                    "Exception tracking reveals where business needs override security standards."
                ),
                "analysis": (
                    "Security leaders revisit exception aging, ensure compensating controls, and sunset outdated waivers."
                ),
            },
            {
                "name": "Awareness training metrics",
                "description": (
                    "Phishing simulation results, training completion, and survey feedback measure human risk."
                ),
                "analysis": (
                    "Program managers identify departments needing targeted coaching and adjust curriculum accordingly."
                ),
            },
        ],
        "attacks": [
            {
                "name": "Phishing campaigns",
                "description": (
                    "Phishing remains a top initial access vector exploiting users through email, SMS, or collaboration"
                    " platforms."
                ),
                "detection": (
                    "Monitor secure email gateway logs, DMARC reports, and user-reported messages to spot active campaigns."
                ),
            },
            {
                "name": "Misconfiguration exploitation",
                "description": (
                    "Unpatched systems and default settings offer easy footholds for attackers."
                ),
                "detection": (
                    "Continuous configuration assessments and vulnerability management prevent opportunistic breaches."
                ),
            },
            {
                "name": "Insider threats",
                "description": (
                    "Disgruntled employees or contractors may steal data or sabotage systems."
                ),
                "detection": (
                    "Use behavioral analytics, access reviews, and segregation of duties to mitigate insider risk."
                ),
            },
        ],
        "incidents": [
            {
                "name": "Equifax 2017",
                "description": (
                    "A missed Apache Struts patch allowed attackers to steal data from over 140 million individuals."
                ),
                "lesson": (
                    "Robust patch management, asset inventory, and segmentation are foundational security practices."
                ),
            },
            {
                "name": "Marriott Starwood breach",
                "description": (
                    "Attackers persisted in reservation systems for years, exfiltrating customer records."
                ),
                "lesson": (
                    "Due diligence during mergers, network segmentation, and monitoring are core defensive fundamentals."
                ),
            },
            {
                "name": "Office 365 credential phishing",
                "description": (
                    "Business email compromise actors used phishing to access cloud mailboxes and redirect payments."
                ),
                "lesson": (
                    "Fundamental controls like MFA, user training, and payment verification prevented losses."
                ),
            },
        ],
        "pitfalls": [
            "Treating compliance checklists as the end goal rather than building layered defenses.",
            "Failing to engage executives results in underfunded programs lacking business alignment.",
            "Policies written in jargon confuse staff and hinder adoption."
        ],
        "troubleshooting": [
            "Hold regular risk committee meetings with clear metrics so leaders understand priorities.",
            "Pilot security training with small groups to refine messaging before enterprise rollout.",
            "Map controls to business processes to uncover ownership gaps and double coverage."
        ],
        "memory_hooks": [
            {
                "mnemonic": "FOUND",
                "story": (
                    "FOUND stands for Frameworks, Operations, Users, Network, and Data—core pillars of any program."
                ),
                "visual": (
                    "Imagine a building foundation labeled with each FOUND pillar supporting the organization."
                ),
            },
            {
                "mnemonic": "RISK",
                "story": (
                    "RISK reminds you to Recognize assets, Identify threats, Score exposure, and Keep stakeholders informed."
                ),
                "visual": (
                    "Visualize a risk heatmap overlayed on business units guiding resource allocation."
                ),
            },
        ],
        "reflection_prompts": [
            "Which business units lack clear security ownership, and how will you engage them?",
            "Where are your largest blind spots in asset inventory and data classification?",
            "How do you measure the effectiveness of your awareness training and policies?",
        ],
        "encouragement": [
            "By mastering fundamentals, you build the scaffolding that supports every advanced security initiative.",
            "Your work translating frameworks into action earns trust across the organization."
        ],
        "next_steps": [
            "Refresh your risk register with current threats, mitigations, and business impacts.",
            "Align security roadmaps with corporate objectives and budget cycles.",
            "Establish metrics dashboards showing policy adoption, patch cadence, and incident trends."
        ],
        "commands": [
            {
                "snippet": "nessus -q --policy 'CIS Windows Server' --targets targets.txt",
                "context": (
                    "Runs a vulnerability scan aligned to CIS benchmarks for prioritized remediation."
                ),
            },
            {
                "snippet": "powershell -Command \"Get-ADComputer -Filter * -Property LastLogonDate | Export-Csv devices.csv\"",
                "context": (
                    "Generates an asset inventory list for governance and patch planning."
                ),
            },
            {
                "snippet": "python risk_register.py --update --owner finance",
                "context": (
                    "Updates a risk register entry and notifies the assigned business owner."
                ),
            },
        ],
        "case_studies": [
            {
                "scenario": "Policy modernization",
                "details": (
                    "A company rewrote outdated policies into plain language, paired with training, reducing phishing"
                    " click rates by 40%."
                ),
                "response": (
                    "They established quarterly reviews, champion networks, and continuous measurement."
                ),
            },
            {
                "scenario": "Framework adoption",
                "details": (
                    "A startup mapped existing controls to NIST CSF, revealing gaps in incident response planning."
                ),
                "response": (
                    "Leadership funded runbook creation, tabletop exercises, and monitoring investments."
                ),
            },
        ],
    },
    "iot_security": {
        "tools": [
            {
                "name": "Cisco Cyber Vision",
                "description": (
                    "Cyber Vision inventories industrial assets, monitors network behavior, and detects anomalies across"
                    " OT environments."
                ),
                "usage": (
                    "Engineers integrate with Firepower firewalls, configure segmentation policies, and alert on new device"
                    " fingerprints."
                ),
            },
            {
                "name": "Nozomi Networks Guardian",
                "description": (
                    "Guardian provides deep packet inspection for ICS protocols and builds asset maps for OT networks."
                ),
                "usage": (
                    "Analysts baseline PLC communications, detect unauthorized logic changes, and orchestrate incident"
                    " response with OT staff."
                ),
            },
            {
                "name": "AWS IoT Device Defender",
                "description": (
                    "Device Defender audits IoT configurations, monitors metrics, and applies mitigation actions."
                ),
                "usage": (
                    "Teams set anomaly detection models for device metrics, enforce secure TLS configurations, and automate"
                    " quarantine."
                ),
            },
            {
                "name": "Shodan and Censys",
                "description": (
                    "Search engines discover exposed IoT devices, revealing misconfigurations and outdated firmware."
                ),
                "usage": (
                    "Security researchers inventory external attack surface and prioritize remediation of exposed interfaces."
                ),
            },
        ],
        "telemetry": [
            {
                "name": "ICS protocol captures",
                "description": (
                    "Modbus, DNP3, PROFINET, and OPC UA traffic reveals device interactions and command patterns."
                ),
                "analysis": (
                    "Operators baseline normal coils/register accesses, detect unauthorized write commands, and enforce"
                    " whitelists."
                ),
            },
            {
                "name": "Device inventory databases",
                "description": (
                    "Asset repositories track firmware versions, vendors, and communication paths."
                ),
                "analysis": (
                    "Security teams identify unsupported devices, patch gaps, and plan network segmentation."
                ),
            },
            {
                "name": "Physical access logs",
                "description": (
                    "Badge readers and maintenance records correlate physical presence with configuration changes."
                ),
                "analysis": (
                    "Investigators review logs to validate authorized maintenance and detect insider threats."
                ),
            },
            {
                "name": "IoT cloud telemetry",
                "description": (
                    "Device twins, MQTT topics, and metrics from IoT hubs expose operational status."
                ),
                "analysis": (
                    "Security teams monitor for unusual publish/subscribe patterns, certificate expirations, and latency"
                    " spikes indicating compromise."
                ),
            },
        ],
        "attacks": [
            {
                "name": "Firmware tampering",
                "description": (
                    "Attackers modify firmware to embed backdoors or disable safety checks."
                ),
                "detection": (
                    "Implement code signing, monitor for unexpected firmware hashes, and maintain golden images."
                ),
            },
            {
                "name": "Botnet recruitment",
                "description": (
                    "IoT botnets such as Mirai exploit weak credentials to launch DDoS attacks."
                ),
                "detection": (
                    "Alert on outbound scanning, default credential usage, and unusual DNS queries."
                ),
            },
            {
                "name": "Lateral movement into OT networks",
                "description": (
                    "Compromised IT systems pivot into OT segments via poorly secured remote access."
                ),
                "detection": (
                    "Enforce segmentation, monitor jump hosts, and inspect protocol usage crossing network zones."
                ),
            },
        ],
        "incidents": [
            {
                "name": "Stuxnet",
                "description": (
                    "The worm targeted Iranian centrifuges, manipulating PLC logic to cause physical damage."
                ),
                "lesson": (
                    "Defense-in-depth, code signing, and monitoring of engineering workstations are critical for OT security."
                ),
            },
            {
                "name": "Mirai botnet",
                "description": (
                    "Mirai infected IoT devices, launching massive DDoS attacks against Dyn DNS providers."
                ),
                "lesson": (
                    "Strong authentication, patch management, and network filtering prevent large-scale botnets."
                ),
            },
            {
                "name": "TRITON malware",
                "description": (
                    "TRITON targeted safety instrumented systems, attempting to manipulate emergency shutdown controllers."
                ),
                "lesson": (
                    "Segmentation between safety systems and engineering networks, plus strict change management, are"
                    " essential."
                ),
            },
        ],
        "pitfalls": [
            "Legacy OT devices lack security agents, requiring compensating controls like network monitoring.",
            "Unmanaged remote access by vendors bypasses enterprise security policies.",
            "Firmware updates often require downtime, so teams postpone them indefinitely."
        ],
        "troubleshooting": [
            "Establish maintenance windows and test environments to validate firmware patches before deployment.",
            "Coordinate with OT engineers to understand process constraints and design security controls that respect"
            " safety requirements.",
            "Document vendor access procedures and monitor sessions in real time to detect anomalies."
        ],
        "memory_hooks": [
            {
                "mnemonic": "DEVICE",
                "story": (
                    "DEVICE stands for Discover assets, Enforce segmentation, Verify firmware, Integrate monitoring,"
                    " Collaborate with engineers, and Educate staff."
                ),
                "visual": (
                    "Imagine a factory floor where each production line displays the DEVICE steps on digital signage."
                ),
            },
            {
                "mnemonic": "SAFE",
                "story": (
                    "SAFE reminds defenders to Segment networks, Authenticate access, Fortify firmware, and Evaluate"
                    " physical security."
                ),
                "visual": (
                    "Picture a safety helmet emblazoned with the SAFE acronym shielding robotic arms."
                ),
            },
        ],
        "reflection_prompts": [
            "Which OT assets still run unsupported firmware, and what is the remediation plan?",
            "How do you monitor vendor remote access for both network and physical maintenance?",
            "What procedures exist to validate changes to PLC logic or IoT cloud policies?",
        ],
        "encouragement": [
            "Securing IoT and OT environments protects not just data but physical processes and safety. Your diligence"
            " safeguards communities.",
            "Every improvement to inventory, segmentation, and monitoring reduces the blast radius of attacks."
        ],
        "next_steps": [
            "Perform a zero-trust segmentation review of IT/OT boundaries.",
            "Develop firmware management roadmaps with vendors and operations teams.",
            "Integrate IoT telemetry into SOC dashboards and incident response playbooks."
        ],
        "commands": [
            {
                "snippet": "tshark -r ics_capture.pcap -Y 'modbus.func_code == 5'",
                "context": (
                    "Filters Modbus write single coil commands to identify unauthorized control attempts."
                ),
            },
            {
                "snippet": "aws iot list-things --query 'things[].thingName'",
                "context": (
                    "Lists IoT devices registered in AWS IoT Core for inventory checks."
                ),
            },
            {
                "snippet": "gcloud iot devices list --registry=plant-registry --region=us-central1",
                "context": (
                    "Enumerates GCP IoT Core devices to verify enrollment and status."
                ),
            },
        ],
        "case_studies": [
            {
                "scenario": "Smart building compromise",
                "details": (
                    "Attackers exploited default credentials on HVAC controllers, adjusting temperatures and impacting"
                    " critical labs."
                ),
                "response": (
                    "Security teams enforced credential rotation, implemented network segmentation, and deployed"
                    " monitoring sensors."
                ),
            },
            {
                "scenario": "Manufacturing downtime",
                "details": (
                    "A ransomware attack on IT systems threatened OT operations; segmentation prevented direct impact"
                    " but highlighted monitoring gaps."
                ),
                "response": (
                    "The company accelerated OT visibility projects, integrated anomaly detection, and rehearsed joint"
                    " incident response drills."
                ),
            },
        ],
    },
    "linux": {
        "tools": [
            {
                "name": "auditd",
                "description": (
                    "Linux Audit daemon records system calls, file access, and security-relevant events for compliance and"
                    " forensics."
                ),
                "usage": (
                    "Security engineers define rules for privileged commands, monitor configuration changes, and forward logs"
                    " to SIEM platforms."
                ),
            },
            {
                "name": "SELinux",
                "description": (
                    "Security-Enhanced Linux enforces mandatory access controls using policies that confine processes and"
                    " files."
                ),
                "usage": (
                    "Administrators tune policies, analyze AVC denials, and leverage permissive mode before enforcing"
                    " contexts."
                ),
            },
            {
                "name": "Falco",
                "description": (
                    "Falco monitors kernel system calls to detect anomalous behavior on Linux hosts and containers."
                ),
                "usage": (
                    "Teams craft Falco rules to flag suspicious process execution, privilege escalation, and data exfiltration"
                    " attempts."
                ),
            },
            {
                "name": "OSQuery",
                "description": (
                    "OSQuery exposes the operating system as a relational database for security analytics."
                ),
                "usage": (
                    "Security teams schedule queries to monitor package versions, user accounts, and loaded kernel modules."
                ),
            },
        ],
        "telemetry": [
            {
                "name": "Syslog",
                "description": (
                    "Syslog consolidates authentication logs, kernel messages, and application events."
                ),
                "analysis": (
                    "Analysts inspect `/var/log/secure`, `/var/log/auth.log`, and journald entries for brute force or"
                    " privilege escalation."
                ),
            },
            {
                "name": "Process accounting",
                "description": (
                    "acct/pacct files track command execution history with CPU usage and UID/GID context."
                ),
                "analysis": (
                    "Incident responders review unusual commands, long-running scripts, and user activity timelines."
                ),
            },
            {
                "name": "Kernel security modules",
                "description": (
                    "SELinux, AppArmor, and seccomp generate audit logs when policies block unauthorized actions."
                ),
                "analysis": (
                    "Engineers analyze denials to adjust policies and detect exploitation attempts."
                ),
            },
            {
                "name": "Package manager logs",
                "description": (
                    "APT, YUM, and zypper logs reveal installation and update history."
                ),
                "analysis": (
                    "Security teams verify critical updates, detect unauthorized package sources, and audit supply chain"
                    " risks."
                ),
            },
        ],
        "attacks": [
            {
                "name": "Rootkit deployment",
                "description": (
                    "Kernel rootkits hide processes, files, and network connections to maintain stealthy persistence."
                ),
                "detection": (
                    "Monitor kernel module loads, verify signatures, and compare `/proc` data against trusted baselines."
                ),
            },
            {
                "name": "Container escape",
                "description": (
                    "Attackers exploit container runtime vulnerabilities to access the host."
                ),
                "detection": (
                    "Enforce namespace isolation, monitor syscalls with Falco, and restrict privileged containers."
                ),
            },
            {
                "name": "Credential harvesting",
                "description": (
                    "Malicious actors extract SSH keys, `/etc/shadow` hashes, or cached credentials."
                ),
                "detection": (
                    "Audit file access, enforce MFA, and monitor for unusual SSH agent forwarding."
                ),
            },
        ],
        "incidents": [
            {
                "name": "Dirty COW exploitation",
                "description": (
                    "CVE-2016-5195 allowed local privilege escalation via copy-on-write vulnerabilities."
                ),
                "lesson": (
                    "Rapid patching and kernel hardening mitigated high-impact Linux vulnerabilities."
                ),
            },
            {
                "name": "CDN cryptomining incident",
                "description": (
                    "A compromised CDN injected scripts that installed Linux cryptominers on web servers."
                ),
                "lesson": (
                    "Integrity monitoring and outbound traffic analysis helped detect and remove miners quickly."
                ),
            },
            {
                "name": "Docker API exposure",
                "description": (
                    "Exposed Docker APIs allowed attackers to run malicious containers with host privileges."
                ),
                "lesson": (
                    "Securing APIs, enforcing TLS, and limiting socket access prevented future abuse."
                ),
            },
        ],
        "pitfalls": [
            "Running containers or services as root increases impact of compromises.",
            "Ignoring baseline comparisons allows subtle file tampering to persist undetected.",
            "Leaving default SSH configurations enables password authentication and weak ciphers."
        ],
        "troubleshooting": [
            "Regularly run integrity checks with tools like AIDE or Tripwire to detect unauthorized changes.",
            "Collect strace or perf traces when diagnosing suspicious performance or system calls.",
            "Leverage systemd cgroups and resource controls to contain runaway processes."
        ],
        "memory_hooks": [
            {
                "mnemonic": "HARDEN",
                "story": (
                    "HARDEN stands for Harden SSH, Audit processes, Restrict services, Detect anomalies, Enforce patches,"
                    " and Normalize logging."
                ),
                "visual": (
                    "Imagine a penguin wearing armor labeled with each HARDEN step."
                ),
            },
            {
                "mnemonic": "PATCH",
                "story": (
                    "PATCH reminds you to Protect packages, Authenticate users, Tune kernel parameters, Control access,"
                    " and Harden containers."
                ),
                "visual": (
                    "Visualize patch cables connecting to shielded servers marked with the PATCH acronym."
                ),
            },
        ],
        "reflection_prompts": [
            "Which servers still allow password-based SSH, and when will you migrate to key-based authentication?",
            "How do you baseline package versions and configuration files across fleets?",
            "What runtime detection do you have for container escapes or kernel exploits?",
        ],
        "encouragement": [
            "Mastering Linux security empowers you to protect massive fleets and critical infrastructure.",
            "Every hardening change reduces attacker options and builds resilience."
        ],
        "next_steps": [
            "Implement centralized logging with journalbeat or rsyslog forwarding.",
            "Deploy MFA for sudo and SSH access using solutions like Duo or PAM modules.",
            "Containerize critical services with least-privilege configurations and regular image scanning."
        ],
        "commands": [
            {
                "snippet": "ausearch -k privileged-actions",
                "context": (
                    "Searches audit logs for events tagged with a privileged actions key."
                ),
            },
            {
                "snippet": "semanage boolean -l | grep httpd",
                "context": (
                    "Displays SELinux booleans affecting Apache to ensure policies match intended behavior."
                ),
            },
            {
                "snippet": "osqueryi 'SELECT user, host, time FROM last_logins ORDER BY time DESC LIMIT 10;'",
                "context": (
                    "Lists recent logins for threat hunting and anomaly detection."
                ),
            },
            {
                "snippet": "falco -r rules.yaml --pidfile=/var/run/falco.pid",
                "context": (
                    "Runs Falco with custom rules to monitor kernel events in real time."
                ),
            },
        ],
        "case_studies": [
            {
                "scenario": "Privilege escalation detection",
                "details": (
                    "Falco alerted on unexpected `chmod 777` operations inside a container, revealing compromised credentials."
                ),
                "response": (
                    "The team rotated secrets, locked down volumes, and added regression tests for container images."
                ),
            },
            {
                "scenario": "Kernel exploit response",
                "details": (
                    "After Dirty Pipe disclosures, administrators rapidly patched kernels, monitored for exploitation"
                    " attempts, and validated patch deployment."
                ),
                "response": (
                    "They implemented automated patch pipelines and runtime mitigations like seccomp profiles."
                ),
            },
        ],
    },
    "malware": {
        "tools": [
            {
                "name": "Ghidra",
                "description": (
                    "Ghidra provides a powerful reverse engineering framework for disassembling and decompiling binaries."
                ),
                "usage": (
                    "Malware analysts use Ghidra to reconstruct control flow, analyze obfuscation, and script bulk analysis"
                    " with Python."
                ),
            },
            {
                "name": "IDA Pro",
                "description": (
                    "IDA Pro offers interactive disassembly with plugin support for unpacking and debugging malware."
                ),
                "usage": (
                    "Researchers integrate Hex-Rays decompiler, apply signatures, and annotate functions to accelerate"
                    " triage."
                ),
            },
            {
                "name": "Cuckoo Sandbox",
                "description": (
                    "Cuckoo automates malware detonation in isolated environments, capturing behavior, network traffic,"
                    " and artifacts."
                ),
                "usage": (
                    "Teams enrich samples, collect dropped files, and generate YARA rules based on observed behaviors."
                ),
            },
            {
                "name": "YARA",
                "description": (
                    "YARA rules describe malware patterns for detection across files and memory."
                ),
                "usage": (
                    "Detection engineers craft rules leveraging strings, PE metadata, and module imports; they test rules"
                    " against benign datasets to avoid false positives."
                ),
            },
        ],
        "telemetry": [
            {
                "name": "Dynamic analysis reports",
                "description": (
                    "Sandbox logs provide process creation, network indicators, and API call traces."
                ),
                "analysis": (
                    "Analysts identify persistence mechanisms, command-and-control domains, and encryption routines."
                ),
            },
            {
                "name": "Static file metadata",
                "description": (
                    "PE headers, imports, and resources reveal compiler timestamps, packer usage, and targeted platforms."
                ),
                "analysis": (
                    "Reverse engineers correlate metadata with known families, track versioning, and support attribution."
                ),
            },
            {
                "name": "Memory forensic artifacts",
                "description": (
                    "Memory dumps capture decrypted payloads, injected code, and network sockets."
                ),
                "analysis": (
                    "DFIR teams extract reflective DLLs, map injected threads, and recover configuration data."
                ),
            },
            {
                "name": "Threat intelligence feeds",
                "description": (
                    "TI feeds aggregate indicators, malware hashes, and TTP reports from vendors and communities."
                ),
                "analysis": (
                    "SOC teams operationalize indicators, enrich detections, and track adversary campaigns."
                ),
            },
        ],
        "attacks": [
            {
                "name": "Ransomware",
                "description": (
                    "Ransomware encrypts data and demands payment, often exfiltrating information for double extortion."
                ),
                "detection": (
                    "Monitor for rapid file modifications, suspicious SMB traffic, and shadow copy deletions."
                ),
            },
            {
                "name": "Loader and downloader chains",
                "description": (
                    "Malware often arrives via small loaders that fetch payloads from remote infrastructure."
                ),
                "detection": (
                    "Inspect command-and-control URLs, analyze PowerShell stagers, and block suspicious domain generation"
                    " algorithms."
                ),
            },
            {
                "name": "Fileless malware",
                "description": (
                    "Adversaries leverage scripts, WMI, and memory-only payloads to evade disk-based detection."
                ),
                "detection": (
                    "Instrument PowerShell logging, AMSI, and memory scanning to catch in-memory threats."
                ),
            },
        ],
        "incidents": [
            {
                "name": "WannaCry",
                "description": (
                    "The 2017 ransomware worm exploited SMB vulnerabilities, encrypting systems worldwide."
                ),
                "lesson": (
                    "Patching, network segmentation, and SMB hardening are critical defenses."
                ),
            },
            {
                "name": "NotPetya",
                "description": (
                    "NotPetya masqueraded as ransomware but delivered destructive wiper payloads."
                ),
                "lesson": (
                    "Incident response plans must include destructive malware scenarios and offline backups."
                ),
            },
            {
                "name": "Emotet resurgence",
                "description": (
                    "Emotet botnet returned with modular loaders distributing ransomware affiliates."
                ),
                "lesson": (
                    "Continuous monitoring, email hardening, and collaborative takedowns reduce botnet impact."
                ),
            },
        ],
        "pitfalls": [
            "Relying solely on static signatures misses obfuscated or polymorphic variants.",
            "Skipping behavior analysis obscures persistence and lateral movement capabilities.",
            "Ignoring malware configuration data prevents effective takedowns and blocking."
        ],
        "troubleshooting": [
            "Unpack samples in stages, documenting each layer of decryption or packing.",
            "Capture full network traffic during detonations to extract indicators.",
            "Use version-controlled YARA repositories with automated testing to prevent false positives."
        ],
        "memory_hooks": [
            {
                "mnemonic": "TRACE",
                "story": (
                    "TRACE stands for Triaging behavior, Reversing code, Assessing configuration, Crafting detections,"
                    " and Educating responders."
                ),
                "visual": (
                    "Picture a magnifying glass tracing malware execution stages labeled with TRACE steps."
                ),
            },
            {
                "mnemonic": "DECODE",
                "story": (
                    "DECODE reminds analysts to Detonate safely, Extract artifacts, Classify family, Observe command"
                    " channels, Document indicators, and Educate stakeholders."
                ),
                "visual": (
                    "Imagine a codebook unlocking layers of malicious logic with each DECODE word."
                ),
            },
        ],
        "reflection_prompts": [
            "Do you maintain isolated analysis environments that mimic customer networks?",
            "How do you share newly discovered indicators with detection engineering teams?",
            "What automation can accelerate unpacking and classification of malware families?",
        ],
        "encouragement": [
            "Your persistence transforms malicious code into actionable intelligence protecting countless users.",
            "Every sample you analyze strengthens global defenses and informs better detections."
        ],
        "next_steps": [
            "Automate sandbox detonation pipelines with enrichment and reporting.",
            "Collaborate with threat intel teams to map malware families to adversary groups.",
            "Contribute YARA rules and reverse engineering notes to shared knowledge bases."
        ],
        "commands": [
            {
                "snippet": "python3 flare-qdb.py sample.exe",
                "context": (
                    "Uses FireEye's FLARE QDB to query PE metadata and unpacking notes."
                ),
            },
            {
                "snippet": "cuckoo submit sample.exe",
                "context": (
                    "Submits a sample to Cuckoo Sandbox for automated detonation."
                ),
            },
            {
                "snippet": "yarac rules/index.yar malware.bin",
                "context": (
                    "Tests YARA rules against a sample to validate detection coverage."
                ),
            },
            {
                "snippet": "vol -f mem.dmp windows.malfind",
                "context": (
                    "Identifies injected code regions in memory for further analysis."
                ),
            },
        ],
        "case_studies": [
            {
                "scenario": "Ransomware affiliate pivot",
                "details": (
                    "Dynamic analysis revealed a loader dropping Conti ransomware; defenders blocked infrastructure and"
                    " updated detections."
                ),
                "response": (
                    "They shared indicators with ISAC partners and executed restoration playbooks."
                ),
            },
            {
                "scenario": "Fileless intrusion",
                "details": (
                    "Memory forensics uncovered PowerShell-based malware leveraging reflective DLL injection."
                ),
                "response": (
                    "Analysts extracted script content, created AMSI signatures, and deployed hunting queries."
                ),
            },
        ],
    },
    "osint": {
        "tools": [
            {
                "name": "Maltego",
                "description": (
                    "Maltego visualizes relationships across domains, emails, social media, and infrastructure using"
                    " transform plugins."
                ),
                "usage": (
                    "OSINT analysts chain transforms to map attacker infrastructure, corporate relationships, and leaked"
                    " credentials."
                ),
            },
            {
                "name": "SpiderFoot",
                "description": (
                    "SpiderFoot automates reconnaissance across hundreds of data sources, gathering threat intelligence"
                    " artifacts."
                ),
                "usage": (
                    "Investigators configure modules to collect WHOIS, DNS, breach data, and dark web mentions, then review"
                    " risk scores."
                ),
            },
            {
                "name": "Recon-ng",
                "description": (
                    "Recon-ng provides a modular framework for reconnaissance with API integrations and reporting."
                ),
                "usage": (
                    "Researchers build workspaces, add modules for certificates, GitHub, and Shodan, and export findings"
                    " to share with defenders."
                ),
            },
            {
                "name": "IntelTechniques tools",
                "description": (
                    "IntelTechniques offers curated search utilities for people, social media, and public records."
                ),
                "usage": (
                    "Analysts cross-reference names with social platforms, property records, and breach data to build"
                    " profiles."
                ),
            },
        ],
        "telemetry": [
            {
                "name": "DNS and certificate transparency",
                "description": (
                    "DNS history and certificate logs reveal subdomains, infrastructure changes, and new deployments."
                ),
                "analysis": (
                    "OSINT practitioners track attacker infrastructure, monitor brand abuse, and feed detections."
                ),
            },
            {
                "name": "Social media activity",
                "description": (
                    "Public posts on Twitter, LinkedIn, and GitHub surface employee details and attacker chatter."
                ),
                "analysis": (
                    "Analysts assess social engineering exposure and identify adversary recruitment or bragging."
                ),
            },
            {
                "name": "Breach repositories",
                "description": (
                    "Collections such as Have I Been Pwned reveal compromised credentials and personal data."
                ),
                "analysis": (
                    "Security teams notify affected users, enforce password resets, and monitor for targeted phishing."
                ),
            },
            {
                "name": "Geospatial imagery",
                "description": (
                    "Satellite and street-level imagery help analyze physical locations, infrastructure, and logistic routes."
                ),
                "analysis": (
                    "Investigators verify facility layouts, supply chain nodes, and conflict zones."
                ),
            },
        ],
        "attacks": [
            {
                "name": "Doxxing",
                "description": (
                    "Threat actors compile public and breached data to expose individuals."
                ),
                "detection": (
                    "Monitor breach forums, social media, and paste sites for leaked information to coordinate takedowns."
                ),
            },
            {
                "name": "Infrastructure pivoting",
                "description": (
                    "Adversaries leverage OSINT to identify vulnerable third parties or supply chain targets."
                ),
                "detection": (
                    "Track certificate transparency, domain registrations, and Git repositories for signs of staging."
                ),
            },
            {
                "name": "Social engineering",
                "description": (
                    "Attackers study employee profiles to craft convincing phishing or voice scams."
                ),
                "detection": (
                    "Educate staff about oversharing and monitor for targeted spear-phishing attempts."
                ),
            },
        ],
        "incidents": [
            {
                "name": "2014 Sony phishing",
                "description": (
                    "Attackers used public data to spear-phish executives, leading to catastrophic breaches."
                ),
                "lesson": (
                    "Regular OSINT reviews and awareness reduce social engineering success."
                ),
            },
            {
                "name": "APT infrastructure discovery",
                "description": (
                    "Researchers used OSINT to map Fancy Bear domains and certificates, informing global defenses."
                ),
                "lesson": (
                    "Open-source investigations empower defenders to preempt attacker campaigns."
                ),
            },
            {
                "name": "Deepfake scams",
                "description": (
                    "Executives were targeted with AI-generated audio leveraging publicly available voice samples."
                ),
                "lesson": (
                    "Monitoring for brand impersonation and training staff on verification prevents fraud."
                ),
            },
        ],
        "pitfalls": [
            "Failing to validate data sources introduces bias and misinformation into investigations.",
            "Neglecting privacy and legal considerations risks violating regulations.",
            "Working alone without peer review increases the chance of misattribution."
        ],
        "troubleshooting": [
            "Document every data source, time, and method to maintain chain of custody.",
            "Use VPNs and sock puppets to avoid tipping off targets during reconnaissance.",
            "Correlate findings across multiple sources before drawing conclusions."
        ],
        "memory_hooks": [
            {
                "mnemonic": "VERIFY",
                "story": (
                    "VERIFY stands for Vet sources, Establish context, Review legality, Identify bias, Formalize notes,"
                    " and Yield actionable intel."
                ),
                "visual": (
                    "Imagine a detective stamping documents with a VERIFY seal after cross-checking evidence."
                ),
            },
            {
                "mnemonic": "MAP",
                "story": (
                    "MAP captures Monitor, Analyze, and Publish—core OSINT workflow stages."
                ),
                "visual": (
                    "Picture a world map overlayed with data points connected by analysis lines."
                ),
            },
        ],
        "reflection_prompts": [
            "How do you ensure your OSINT process respects privacy laws and organizational policies?",
            "What automation can free analysts to focus on deeper correlation?",
            "Which stakeholders need regular OSINT reporting and how do they act on it?",
        ],
        "encouragement": [
            "Your ability to extract insight from public data gives defenders a head start against adversaries.",
            "Ethical OSINT work protects people and supports informed decision making."
        ],
        "next_steps": [
            "Build playbooks for brand monitoring, executive protection, and vulnerability discovery.",
            "Automate data ingestion pipelines with tagging and relevance scoring.",
            "Partner with legal and communications teams to respond to findings effectively."
        ],
        "commands": [
            {
                "snippet": "python spiderfoot-cli.py -s example.com -m sfp_dns,sfp_sslcert",
                "context": (
                    "Launches SpiderFoot modules to collect DNS and certificate data for a target domain."
                ),
            },
            {
                "snippet": "recon-ng --workspace company --module recon/domains-hosts/brute_hosts --options WORDLIST=top1m.txt",
                "context": (
                    "Uses Recon-ng to brute-force subdomains associated with an organization."
                ),
            },
            {
                "snippet": "maltego --transform seedToIP example.com",
                "context": (
                    "Executes a Maltego transform to pivot from a domain to related IP addresses."
                ),
            },
        ],
        "case_studies": [
            {
                "scenario": "Executive protection",
                "details": (
                    "OSINT analysts discovered exposed travel itineraries on social media, enabling security teams to"
                    " adjust plans."
                ),
                "response": (
                    "They implemented awareness training and set up ongoing monitoring feeds."
                ),
            },
            {
                "scenario": "Brand impersonation takedown",
                "details": (
                    "Monitoring detected fake customer support accounts scamming victims."
                ),
                "response": (
                    "The organization coordinated with social platforms to remove accounts and published safety guidance."
                ),
            },
        ],
    },
    "pentest": {
        "tools": [
            {
                "name": "Burp Suite Professional",
                "description": (
                    "Burp Suite enables comprehensive web application testing with intercepting proxies, scanners, and"
                    " extensibility."
                ),
                "usage": (
                    "Penetration testers chain intruder, repeater, and extender modules to identify injection, auth"
                    " flaws, and logic bugs."
                ),
            },
            {
                "name": "Nmap",
                "description": (
                    "Nmap discovers hosts, services, and vulnerabilities using port scanning and NSE scripts."
                ),
                "usage": (
                    "Testers run targeted scans, leverage NSE for CVE detection, and baseline network exposure."
                ),
            },
            {
                "name": "Metasploit Framework",
                "description": (
                    "Metasploit packages exploits, payloads, and post-exploitation modules for controlled testing."
                ),
                "usage": (
                    "Operators customize modules, stage payloads, and document exploitation steps responsibly."
                ),
            },
            {
                "name": "ffuf",
                "description": (
                    "ffuf performs fast web fuzzing to enumerate directories, parameters, and hostnames."
                ),
                "usage": (
                    "Penetration testers brute-force endpoints, discover hidden APIs, and locate misconfigurations."
                ),
            },
        ],
        "telemetry": [
            {
                "name": "Scan logs",
                "description": (
                    "Penetration tests produce detailed logs of targets, requests, and responses."
                ),
                "analysis": (
                    "Security teams review findings, reproduce issues, and prioritize remediation."
                ),
            },
            {
                "name": "Exploit reports",
                "description": (
                    "Reports capture proof-of-concept exploits, screenshots, and impacted business processes."
                ),
                "analysis": (
                    "Stakeholders evaluate risk, assign owners, and track remediation commitments."
                ),
            },
            {
                "name": "Test scope documentation",
                "description": (
                    "Scopes define authorized systems, time windows, and rules of engagement."
                ),
                "analysis": (
                    "Program managers ensure testing stays within bounds and inform operations teams."
                ),
            },
        ],
        "attacks": [
            {
                "name": "Injection flaws",
                "description": (
                    "SQLi, command injection, and template injection grant attackers unauthorized control."
                ),
                "detection": (
                    "Use parameterized queries, input validation, and WAF rules; testers validate remediation."
                ),
            },
            {
                "name": "Authentication bypass",
                "description": (
                    "Weak session management and logic errors allow attackers to impersonate users."
                ),
                "detection": (
                    "Penetration tests identify missing MFA, session fixation, or token misconfigurations."
                ),
            },
            {
                "name": "Misconfigured cloud APIs",
                "description": (
                    "Overly permissive IAM policies or exposed endpoints leak data."
                ),
                "detection": (
                    "Testers enumerate APIs, review IAM roles, and craft privilege escalation scenarios."
                ),
            },
        ],
        "incidents": [
            {
                "name": "OWASP Top 10 breaches",
                "description": (
                    "Real-world breaches like TalkTalk and Heartland stemmed from injection and auth flaws."
                ),
                "lesson": (
                    "Routine pentesting and secure coding training address common vulnerabilities."
                ),
            },
            {
                "name": "Cloud bucket exposures",
                "description": (
                    "Multiple organizations leaked sensitive data via publicly accessible storage."
                ),
                "lesson": (
                    "Attack surface reviews, automation, and continuous pentesting prevent recurrence."
                ),
            },
            {
                "name": "SSRF exploitation",
                "description": (
                    "Capital One breach exploited SSRF against AWS metadata service."
                ),
                "lesson": (
                    "Penetration tests must include SSRF cases, metadata protections, and firewall controls."
                ),
            },
        ],
        "pitfalls": [
            "Scope creep undermines trust; testers must respect boundaries and coordinate with stakeholders.",
            "Poor communication leads to downtime or missed remediation opportunities.",
            "Failure to retest keeps vulnerabilities open."
        ],
        "troubleshooting": [
            "Maintain clear communication channels with operations teams before, during, and after testing.",
            "Use version-controlled notes and scripts to reproduce issues reliably.",
            "Schedule retests and verification to confirm fixes."
        ],
        "memory_hooks": [
            {
                "mnemonic": "PLAN",
                "story": (
                    "PLAN stands for Prepare scope, Launch tests, Analyze findings, and Notify stakeholders."
                ),
                "visual": (
                    "Visualize a checklist moving through each PLAN stage with approvals at every step."
                ),
            },
            {
                "mnemonic": "SAFE",
                "story": (
                    "In pentesting, SAFE means Scope, Attack, Fix, Evaluate to maintain professional ethics."
                ),
                "visual": (
                    "Picture a lock icon guiding testers through each SAFE phase responsibly."
                ),
            },
        ],
        "reflection_prompts": [
            "Does your organization align pentest frequency with asset criticality?",
            "How do you ensure findings feed into developer training and secure SDLC improvements?",
            "Which automation can support continuous testing without overwhelming teams?",
        ],
        "encouragement": [
            "Professional testers uncover weaknesses before adversaries do, directly reducing risk.",
            "Your ability to communicate findings respectfully builds lasting partnerships with development teams."
        ],
        "next_steps": [
            "Create a centralized vulnerability management backlog with SLAs tied to pentest findings.",
            "Integrate authenticated testing into CI/CD for high-risk applications.",
            "Host purple team sessions to align offensive and defensive insights."
        ],
        "commands": [
            {
                "snippet": "nmap -sC -sV -oA scans/internal 10.0.0.0/24",
                "context": (
                    "Runs a service/version detection scan against an internal subnet."
                ),
            },
            {
                "snippet": "burpsuite --project-file api_test.burp --config-file ci-config.json",
                "context": (
                    "Launches Burp Suite with saved project and configuration for repeatable testing."
                ),
            },
            {
                "snippet": "msfconsole -q -x \"use exploit/multi/http/struts_dmi_exec; set RHOSTS target; run\"",
                "context": (
                    "Executes a Metasploit module demonstrating Struts vulnerability exploitation in a controlled lab."
                ),
            },
            {
                "snippet": "ffuf -w wordlists/api.txt -u https://app.example.com/FUZZ",
                "context": (
                    "Fuzzes API endpoints to discover hidden routes and functionality."
                ),
            },
        ],
        "case_studies": [
            {
                "scenario": "API assessment",
                "details": (
                    "Testing discovered IDOR vulnerabilities allowing access to other customer records."
                ),
                "response": (
                    "Developers implemented object-level authorization, regression tests, and improved logging."
                ),
            },
            {
                "scenario": "Cloud privilege escalation",
                "details": (
                    "Pentesters leveraged misconfigured IAM policies to pivot into production environments."
                ),
                "response": (
                    "Security teams tightened IAM roles, enabled CloudTrail monitoring, and enforced MFA."
                ),
            },
        ],
    },
    "red_team": {
        "tools": [
            {
                "name": "Cobalt Strike",
                "description": (
                    "Cobalt Strike provides beacon payloads, team servers, and post-exploitation tooling for adversary"
                    " emulation."
                ),
                "usage": (
                    "Red teams customize profiles, use malleable C2, and coordinate operations while blue teams practice"
                    " detection."
                ),
            },
            {
                "name": "Sliver",
                "description": (
                    "Sliver is an open-source adversary emulation framework supporting multiplatform implants."
                ),
                "usage": (
                    "Operators run staged payloads, experiment with C2 channels, and integrate with CI pipelines for"
                    " automated exercises."
                ),
            },
            {
                "name": "Mythic",
                "description": (
                    "Mythic orchestrates multiple agents, communication profiles, and payload types with community"
                    " plugins."
                ),
                "usage": (
                    "Teams design campaigns, mix HTTP, WebSocket, and SMB channels, and share artifacts with defenders."
                ),
            },
            {
                "name": "Atomic Red Team",
                "description": (
                    "Atomic Red Team provides small, testable scripts aligned to MITRE ATT&CK techniques."
                ),
                "usage": (
                    "Security teams execute atomic tests to validate detections and build repeatable purple team"
                    " exercises."
                ),
            },
        ],
        "telemetry": [
            {
                "name": "Engagement logs",
                "description": (
                    "Command-and-control servers and operator consoles capture actions taken during engagements."
                ),
                "analysis": (
                    "Post-engagement reviews correlate actions with blue team detections and refine tradecraft."
                ),
            },
            {
                "name": "Detection alerts",
                "description": (
                    "Alerts triggered during exercises reveal detection coverage and response workflows."
                ),
                "analysis": (
                    "Red and blue teams collaborate to evaluate alert fidelity and response speed."
                ),
            },
            {
                "name": "Lessons learned reports",
                "description": (
                    "After-action reports document strengths, gaps, and recommended improvements."
                ),
                "analysis": (
                    "Leadership prioritizes remediation and invests in controls or training."
                ),
            },
        ],
        "attacks": [
            {
                "name": "Initial access techniques",
                "description": (
                    "Spear-phishing, drive-by downloads, and external exploitation simulate real adversary entry."
                ),
                "detection": (
                    "Use safe payloads with legal approvals, monitor for defensive detection, and iterate on phishing"
                    " templates."
                ),
            },
            {
                "name": "Lateral movement",
                "description": (
                    "Red teams pivot using pass-the-hash, RDP, or WMI to access internal systems."
                ),
                "detection": (
                    "Track authentication logs, detect unusual service creation, and review network segmentation."
                ),
            },
            {
                "name": "Data exfiltration",
                "description": (
                    "Simulated exfiltration tests DLP controls and monitoring."
                ),
                "detection": (
                    "Monitor outbound traffic, inspect unusual protocols, and enforce encryption policies."
                ),
            },
        ],
        "incidents": [
            {
                "name": "APT simulation exercises",
                "description": (
                    "Organizations mimic adversary campaigns like APT29 to validate defenses."
                ),
                "lesson": (
                    "Collaborative planning ensures exercises drive measurable detection and response improvements."
                ),
            },
            {
                "name": "Purple team optimization",
                "description": (
                    "Joint exercises aligned detection content with attacker behaviors, reducing mean time to detect."
                ),
                "lesson": (
                    "Iterative testing and knowledge sharing build trust between offensive and defensive teams."
                ),
            },
            {
                "name": "Assumed breach drills",
                "description": (
                    "Simulated insider threats highlighted identity and segmentation weaknesses."
                ),
                "lesson": (
                    "Organizations improved privileged access management and lateral movement detections."
                ),
            },
        ],
        "pitfalls": [
            "Red team activities without clear objectives waste resources and strain relationships.",
            "Poor documentation limits learning for defenders.",
            "Using production-impacting payloads violates trust and may cause outages."
        ],
        "troubleshooting": [
            "Establish rules of engagement signed by legal and leadership before operations.",
            "Maintain communication channels for kill-switch coordination if issues arise.",
            "Capture detailed timelines to debrief effectively and tie findings to MITRE ATT&CK."
        ],
        "memory_hooks": [
            {
                "mnemonic": "ALIGN",
                "story": (
                    "ALIGN stands for Agree on scope, Link to threats, Integrate defenders, Generate insights, and"
                    " Normalize lessons."
                ),
                "visual": (
                    "Picture offensive and defensive teams aligning puzzle pieces labeled with each ALIGN step."
                ),
            },
            {
                "mnemonic": "PACE",
                "story": (
                    "PACE here means Plan, Attack, Communicate, Evaluate to maintain disciplined operations."
                ),
                "visual": (
                    "Imagine mission control screens guiding each PACE stage with alerts for coordination."
                ),
            },
        ],
        "reflection_prompts": [
            "Do your red team objectives map to priority threats and business risks?",
            "How do you ensure lessons learned feed into detection engineering and tabletop exercises?",
            "What safeguards exist to prevent collateral damage during operations?",
        ],
        "encouragement": [
            "Thoughtful red team campaigns sharpen the entire security organization.",
            "Your collaboration with blue teams builds a shared understanding of adversary tradecraft."
        ],
        "next_steps": [
            "Schedule joint planning sessions with detection engineers to define success metrics.",
            "Automate infrastructure provisioning for repeatable adversary simulations.",
            "Publish engagement reports highlighting detection successes and growth areas."
        ],
        "commands": [
            {
                "snippet": "csconsole -script load_profile.cna",
                "context": (
                    "Loads a Cobalt Strike aggressor script to customize beacon profiles."
                ),
            },
            {
                "snippet": "sliver server",
                "context": (
                    "Starts a Sliver C2 server ready for implant callbacks."
                ),
            },
            {
                "snippet": "mythic-cli payload generate apfell --callback http://teamserver/callback",
                "context": (
                    "Generates a Mythic payload using the Apfell agent for macOS targets."
                ),
            },
            {
                "snippet": "Invoke-AtomicTest T1059.001 -ShowDetailsBrief",
                "context": (
                    "Executes an Atomic Red Team PowerShell test to validate script block logging detections."
                ),
            },
        ],
        "case_studies": [
            {
                "scenario": "Credential theft emulation",
                "details": (
                    "Red teamers simulated Mimikatz usage; defenders improved LSASS protections and alerting."
                ),
                "response": (
                    "Outcome metrics demonstrated reduced dwell time during subsequent exercises."
                ),
            },
            {
                "scenario": "Data exfiltration rehearsal",
                "details": (
                    "Simulated exfiltration over HTTPS bypassed legacy DLP; insights drove new detection signatures."
                ),
                "response": (
                    "Security operations deployed TLS inspection and anomaly detection tuned to exercise data."
                ),
            },
        ],
    },
    "system": {
        "tools": [
            {
                "name": "WinDbg",
                "description": (
                    "WinDbg provides kernel and user-mode debugging for Windows internals analysis."
                ),
                "usage": (
                    "Engineers inspect kernel structures, analyze crashes, and debug drivers to understand system behavior."
                ),
            },
            {
                "name": "Sysinternals Suite",
                "description": (
                    "Utilities like Process Explorer, Procmon, and Autoruns reveal deep OS telemetry."
                ),
                "usage": (
                    "System experts trace handles, registry activity, and startup persistence to diagnose anomalies."
                ),
            },
            {
                "name": "LLDB",
                "description": (
                    "LLDB offers debugging for macOS and iOS kernel and user-space components."
                ),
                "usage": (
                    "Researchers step through Mach kernel code, inspect threads, and evaluate security mitigations."
                ),
            },
            {
                "name": "eBPF tooling",
                "description": (
                    "bcc and bpftrace instruments Linux kernel events for performance and security observability."
                ),
                "usage": (
                    "System engineers craft scripts to monitor syscalls, context switches, and network activity without"
                    " kernel recompiles."
                ),
            },
        ],
        "telemetry": [
            {
                "name": "Kernel crash dumps",
                "description": (
                    "Crash dumps reveal call stacks, memory contents, and bugcheck parameters after system failures."
                ),
                "analysis": (
                    "Experts use WinDbg or LLDB to identify faulty drivers, kernel exploits, or hardware issues."
                ),
            },
            {
                "name": "Event tracing for Windows (ETW)",
                "description": (
                    "ETW captures granular OS events for performance, security, and diagnostics."
                ),
                "analysis": (
                    "Engineers subscribe to providers like Kernel-Process or Threat-Intelligence to monitor low-level"
                    " activity."
                ),
            },
            {
                "name": "Kernel logs",
                "description": (
                    "Linux dmesg, macOS unified logs, and hypervisor logs expose driver loading and hardware events."
                ),
                "analysis": (
                    "System teams detect unsigned driver installs, virtualization escapes, and hardware faults."
                ),
            },
            {
                "name": "Performance counters",
                "description": (
                    "Perf counters track CPU, memory, and I/O behavior at granular intervals."
                ),
                "analysis": (
                    "Performance engineers identify bottlenecks, tune scheduling, and detect abnormal workloads."
                ),
            },
        ],
        "attacks": [
            {
                "name": "Kernel exploit chains",
                "description": (
                    "Exploits targeting kernel vulnerabilities grant root or SYSTEM access."
                ),
                "detection": (
                    "Monitor driver loads, enforce virtualization-based security, and patch promptly."
                ),
            },
            {
                "name": "Firmware persistence",
                "description": (
                    "Adversaries implant code in BIOS/UEFI or device firmware to survive reinstalls."
                ),
                "detection": (
                    "Use firmware scanning, measured boot, and secure boot attestation to detect tampering."
                ),
            },
            {
                "name": "Hypervisor escapes",
                "description": (
                    "Malicious code breaks virtualization boundaries to control hosts."
                ),
                "detection": (
                    "Apply timely hypervisor patches, monitor unusual VM operations, and restrict device passthrough."
                ),
            },
        ],
        "incidents": [
            {
                "name": "Stuxnet kernel drivers",
                "description": (
                    "Signed rootkits manipulated Windows kernel to hide PLC sabotage."
                ),
                "lesson": (
                    "Driver signing enforcement and integrity monitoring are essential."
                ),
            },
            {
                "name": "Thunderstrike firmware attack",
                "description": (
                    "Thunderbolt option ROM exploits replaced Mac firmware with malicious code."
                ),
                "lesson": (
                    "Physical security, firmware updates, and secure boot protect against hardware attacks."
                ),
            },
            {
                "name": "Cloud hypervisor breakout",
                "description": (
                    "Cloud providers mitigated vulnerabilities like Venom (CVE-2015-3456) affecting virtualized"
                    " environments."
                ),
                "lesson": (
                    "Micro-segmentation, patch cadence, and hardware isolation reduce impact."
                ),
            },
        ],
        "pitfalls": [
            "Ignoring hardware and firmware layers leaves blind spots for advanced persistence.",
            "Insufficient logging of kernel events hampers investigations.",
            "Running outdated drivers introduces stability and security risks."
        ],
        "troubleshooting": [
            "Maintain lab environments mirroring production kernels for patch testing.",
            "Collect crash dumps and logs immediately after incidents to preserve context.",
            "Collaborate with hardware vendors for firmware updates and telemetry access."
        ],
        "memory_hooks": [
            {
                "mnemonic": "CORE",
                "story": (
                    "CORE stands for Code integrity, OS telemetry, Resilient firmware, and Exploit mitigation."
                ),
                "visual": (
                    "Imagine a server core surrounded by shields labeled with CORE components."
                ),
            },
            {
                "mnemonic": "HYPER",
                "story": (
                    "HYPER captures Harden hosts, Yield logs, Patch hypervisors, Evaluate firmware, and Respond quickly."
                ),
                "visual": (
                    "Picture a hypervisor diagram with layers colored for each HYPER action."
                ),
            },
        ],
        "reflection_prompts": [
            "How do you validate firmware integrity across fleets?",
            "Which kernel or driver events are you currently blind to?",
            "What change management ensures stability when updating low-level components?",
        ],
        "encouragement": [
            "System-level expertise safeguards the foundation of every application and service.",
            "Your ability to bridge hardware, OS, and security disciplines unlocks resilient architectures."
        ],
        "next_steps": [
            "Implement device health attestation to monitor boot integrity.",
            "Deploy kernel-mode telemetry collectors integrated with security analytics.",
            "Establish firmware update cycles with verification checklists."
        ],
        "commands": [
            {
                "snippet": "windbg -z C:\\dumps\\memory.dmp -c \"!analyze -v; q\"",
                "context": (
                    "Automates WinDbg analysis of crash dumps before exiting."
                ),
            },
            {
                "snippet": "logman start kernel_trace -p Microsoft-Windows-Kernel-Process 0x10 0x5 -ets",
                "context": (
                    "Starts an ETW session capturing process events for kernel diagnostics."
                ),
            },
            {
                "snippet": "sudo bpftrace -e 'tracepoint:syscalls:sys_enter_execve { printf(\"%s\n\", str(args->filename)); }'",
                "context": (
                    "Prints executed binaries via eBPF to monitor Linux execve calls."
                ),
            },
            {
                "snippet": "system_profiler SPHardwareDataType",
                "context": (
                    "Retrieves macOS hardware and firmware information for baseline comparisons."
                ),
            },
        ],
        "case_studies": [
            {
                "scenario": "Driver vulnerability response",
                "details": (
                    "A vulnerable VPN driver allowed privilege escalation; engineers analyzed crash dumps and deployed"
                    " patched drivers."
                ),
                "response": (
                    "They implemented driver allow lists and improved update telemetry."
                ),
            },
            {
                "scenario": "Firmware attestation rollout",
                "details": (
                    "An enterprise deployed measured boot with TPM reporting to detect unauthorized firmware changes."
                ),
                "response": (
                    "Security operations integrated attestation results with SIEM dashboards and incident workflows."
                ),
            },
        ],
    },
    "threat_hunting": {
        "tools": [
            {
                "name": "Elastic SIEM",
                "description": (
                    "Elastic provides scalable log ingestion, detections, and Kibana visualizations for hunting."
                ),
                "usage": (
                    "Hunters craft Kibana queries, build detection rules, and pivot across indices to investigate"
                    " hypotheses."
                ),
            },
            {
                "name": "Microsoft Sentinel",
                "description": (
                    "Sentinel combines analytics, automation, and notebooks for advanced hunting."
                ),
                "usage": (
                    "Teams write KQL queries, leverage notebooks for enrichment, and automate responses via Logic Apps."
                ),
            },
            {
                "name": "Sigma",
                "description": (
                    "Sigma rules offer a detection language convertible to multiple SIEM platforms."
                ),
                "usage": (
                    "Hunters author Sigma rules, convert them to native queries, and maintain version control."
                ),
            },
            {
                "name": "Jupyter Notebooks",
                "description": (
                    "Notebooks integrate Python, pandas, and visualizations to analyze hunt datasets."
                ),
                "usage": (
                    "Threat hunters explore telemetry, build baselines, and automate hypotheses."
                ),
            },
        ],
        "telemetry": [
            {
                "name": "Endpoint detection telemetry",
                "description": (
                    "EDR data captures process trees, command lines, and file modifications."
                ),
                "analysis": (
                    "Hunters identify anomalous parent-child relationships, lateral movement, and persistence artifacts."
                ),
            },
            {
                "name": "Authentication logs",
                "description": (
                    "Azure AD, Okta, and Active Directory logs reveal login activity and anomalies."
                ),
                "analysis": (
                    "Analysts detect impossible travel, brute force, and suspicious service account use."
                ),
            },
            {
                "name": "Network telemetry",
                "description": (
                    "NetFlow, Zeek, and proxy logs surface beaconing, data exfiltration, and lateral movement."
                ),
                "analysis": (
                    "Hunters baseline communication patterns and flag anomalies with machine learning or heuristics."
                ),
            },
            {
                "name": "Cloud audit logs",
                "description": (
                    "AWS CloudTrail, Azure Activity logs, and GCP audit logs show control plane actions."
                ),
                "analysis": (
                    "Threat hunters monitor for privilege escalations, rogue users, and suspicious automation."
                ),
            },
        ],
        "attacks": [
            {
                "name": "Credential abuse",
                "description": (
                    "Attackers reuse stolen credentials across services."
                ),
                "detection": (
                    "Hunt for atypical logon times, impossible travel, and unusual MFA prompts."
                ),
            },
            {
                "name": "Beaconing",
                "description": (
                    "Command-and-control beacons exhibit regular intervals and unusual destinations."
                ),
                "detection": (
                    "Apply statistical analysis, frequency domain transforms, and enrichment to identify C2."
                ),
            },
            {
                "name": "Living off the land",
                "description": (
                    "Adversaries leverage native tools like PowerShell and WMI."
                ),
                "detection": (
                    "Hunt for unusual command lines, script block logging, and encoded payloads."
                ),
            },
        ],
        "incidents": [
            {
                "name": "SolarWinds hunting",
                "description": (
                    "Teams worldwide hunted for SUNBURST indicators using network, endpoint, and identity telemetry."
                ),
                "lesson": (
                    "Hunting programs must rapidly incorporate threat intelligence to identify stealthy campaigns."
                ),
            },
            {
                "name": "MFA fatigue attacks",
                "description": (
                    "Adversaries spammed push notifications to trick users into approving logins."
                ),
                "lesson": (
                    "Hunting for repeated MFA prompts and user reports led to blocking malicious sessions."
                ),
            },
            {
                "name": "Ransomware lateral movement",
                "description": (
                    "Hunting uncovered credential dumping and remote execution before encryption triggered."
                ),
                "lesson": (
                    "Proactive hunts reduce dwell time and enable containment before impact."
                ),
            },
        ],
        "pitfalls": [
            "Hunting without hypotheses leads to aimless data mining.",
            "Lack of documentation prevents sharing insights and improving detections.",
            "Ignoring feedback loops with detection engineering wastes discoveries."
        ],
        "troubleshooting": [
            "Establish hypothesis-driven hunts with defined success criteria.",
            "Use hunt notebooks or templates to capture methodology, queries, and outcomes.",
            "Brief SOC and detection teams regularly to convert hunt findings into detections."
        ],
        "memory_hooks": [
            {
                "mnemonic": "HUNT",
                "story": (
                    "HUNT stands for Hypothesize, Understand data, Narrow signals, and Transfer outcomes."
                ),
                "visual": (
                    "Imagine a hunter following a trail with signposts labeled H, U, N, T."
                ),
            },
            {
                "mnemonic": "LOOP",
                "story": (
                    "LOOP means Learn from intel, Observe telemetry, Operationalize detections, and Promote feedback."
                ),
                "visual": (
                    "Picture a feedback loop diagram connecting intel, hunts, detections, and SOC processes."
                ),
            },
        ],
        "reflection_prompts": [
            "Which telemetry sources remain siloed from your hunting team?",
            "How do you prioritize hunts based on threat intelligence and risk?",
            "What metrics demonstrate hunt effectiveness to leadership?",
        ],
        "encouragement": [
            "Every hunt sharpens organizational awareness and uncovers blind spots before adversaries exploit them.",
            "Your curiosity and persistence transform data into actionable intelligence."
        ],
        "next_steps": [
            "Build a hunt backlog aligned to MITRE ATT&CK techniques and recent intel.",
            "Automate hunt result tracking and detection follow-up in shared dashboards.",
            "Host regular retrospectives to evaluate hypothesis quality and outcomes."
        ],
        "commands": [
            {
                "snippet": "Search ProcessCreate | where CommandLine contains 'rundll32' | take 50",
                "context": (
                    "Sentinel KQL query identifying suspicious rundll32 usage."
                ),
            },
            {
                "snippet": "es | where event.module == 'endpoint' and process.args : 'Invoke-WebRequest'",
                "context": (
                    "Elastic query hunting for PowerShell download cradle usage."
                ),
            },
            {
                "snippet": "zeek-cut id.orig_h id.resp_h resp_p < conn.log | sort | uniq -c | sort -nr | head",
                "context": (
                    "Zeek command summarizing frequent network connections for beacon analysis."
                ),
            },
            {
                "snippet": "jupyter nbconvert --to html hunt_notebook.ipynb",
                "context": (
                    "Exports hunt notebooks for sharing with stakeholders."
                ),
            },
        ],
        "case_studies": [
            {
                "scenario": "OAuth token theft hunt",
                "details": (
                    "Hunters correlated Azure AD logs with MailItemsAccessed events to detect OAuth abuse."
                ),
                "response": (
                    "They revoked tokens, tightened consent policies, and delivered new detections."
                ),
            },
            {
                "scenario": "Beacon detection sprint",
                "details": (
                    "A focused hunt identified low-and-slow beacons; defenders blocked infrastructure and patched"
                    " initial access vectors."
                ),
                "response": (
                    "Results informed new analytics and prioritized security monitoring investments."
                ),
            },
        ],
    },
    "web3_security": {
        "tools": [
            {
                "name": "Slither",
                "description": (
                    "Slither performs static analysis of Solidity smart contracts to flag vulnerabilities."
                ),
                "usage": (
                    "Security auditors integrate Slither into CI to catch reentrancy, access control, and arithmetic"
                    " issues."
                ),
            },
            {
                "name": "Foundry",
                "description": (
                    "Foundry provides fast smart contract development, fuzzing, and testing toolchains."
                ),
                "usage": (
                    "Engineers write invariant tests, fuzz inputs, and simulate upgrades to validate contract logic."
                ),
            },
            {
                "name": "MythX / Mythril",
                "description": (
                    "MythX/Mythril analyze smart contracts using symbolic execution and security checks."
                ),
                "usage": (
                    "Auditors run Mythril to detect integer overflow, unchecked calls, and dangerous patterns."
                ),
            },
            {
                "name": "Tenderly",
                "description": (
                    "Tenderly monitors DeFi contracts, simulates transactions, and provides debugging."
                ),
                "usage": (
                    "Security teams simulate exploit scenarios, monitor on-chain metrics, and trigger alerts."
                ),
            },
        ],
        "telemetry": [
            {
                "name": "On-chain transaction data",
                "description": (
                    "Blockchain explorers expose transaction traces, contract calls, and state changes."
                ),
                "analysis": (
                    "Analysts inspect transaction graphs to spot exploit patterns, flash loans, and fund flows."
                ),
            },
            {
                "name": "Event logs",
                "description": (
                    "Smart contracts emit events capturing transfers, swaps, and administrative actions."
                ),
                "analysis": (
                    "Security engineers monitor events for abnormal withdrawals or parameter changes."
                ),
            },
            {
                "name": "Governance proposals",
                "description": (
                    "DAO proposals and voting records reveal governance attack surfaces."
                ),
                "analysis": (
                    "Analysts review proposals for malicious payloads or vote-buying tactics."
                ),
            },
            {
                "name": "Off-chain infrastructure logs",
                "description": (
                    "Bridges, oracles, and APIs produce logs that highlight tampering or outages."
                ),
                "analysis": (
                    "Web3 defenders correlate off-chain logs with on-chain events to detect coordinated attacks."
                ),
            },
        ],
        "attacks": [
            {
                "name": "Reentrancy",
                "description": (
                    "Reentrancy allows attackers to repeatedly call functions before state updates."
                ),
                "detection": (
                    "Use reentrancy guards, checks-effects-interactions pattern, and audit call flows."
                ),
            },
            {
                "name": "Price oracle manipulation",
                "description": (
                    "Attackers manipulate oracle prices to drain lending pools or trigger liquidations."
                ),
                "detection": (
                    "Monitor price deviations, enforce time-weighted oracles, and detect flash loan spikes."
                ),
            },
            {
                "name": "Bridge exploits",
                "description": (
                    "Cross-chain bridges are prime targets for logic flaws and key compromise."
                ),
                "detection": (
                    "Audit bridge contracts, enforce multi-sig validations, and monitor large withdrawals."
                ),
            },
        ],
        "incidents": [
            {
                "name": "DAO hack",
                "description": (
                    "The 2016 DAO exploit drained millions of Ether via recursive calls."
                ),
                "lesson": (
                    "Prompted the Ethereum hard fork and established secure development practices."
                ),
            },
            {
                "name": "Poly Network breach",
                "description": (
                    "Cross-chain bridge flaws allowed attackers to steal $600M before funds were returned."
                ),
                "lesson": (
                    "Highlighted the importance of multi-sig governance, auditing, and emergency response playbooks."
                ),
            },
            {
                "name": "Wormhole exploit",
                "description": (
                    "A signature verification bug let attackers mint wrapped assets without collateral."
                ),
                "lesson": (
                    "Teams must validate elliptic curve checks and implement layered security."
                ),
            },
        ],
        "pitfalls": [
            "Smart contracts are immutable once deployed; unpatched flaws persist on-chain.",
            "Decentralized governance introduces social attack vectors.",
            "Complex composability increases systemic risk across protocols."
        ],
        "troubleshooting": [
            "Implement upgradeable proxies with rigorous access controls and timelocks.",
            "Design emergency pause mechanisms (circuit breakers) for critical contracts.",
            "Conduct war games simulating bridge, oracle, and governance attacks."
        ],
        "memory_hooks": [
            {
                "mnemonic": "CHAIN",
                "story": (
                    "CHAIN stands for Code review, Harden oracles, Audit bridges, Implement governance security, and"
                    " Notify community."
                ),
                "visual": (
                    "Imagine a blockchain chain with each link labeled by CHAIN steps."
                ),
            },
            {
                "mnemonic": "VAULT",
                "story": (
                    "VAULT reminds defenders to Verify contracts, Audit dependencies, Use monitoring, Limit privileges,"
                    " and Test recovery."
                ),
                "visual": (
                    "Picture a digital vault protecting crypto assets with VAULT etched above the door."
                ),
            },
        ],
        "reflection_prompts": [
            "What controls protect your protocol if an oracle or bridge is compromised?",
            "How quickly can you pause or upgrade contracts during an incident?",
            "Do you monitor governance proposals for malicious payloads?",
        ],
        "encouragement": [
            "Web3 security protects user funds and trust in decentralized ecosystems.",
            "Your diligence in audits and monitoring prevents multimillion-dollar losses."
        ],
        "next_steps": [
            "Set up continuous integration pipelines running Slither, Foundry, and Mythril checks.",
            "Deploy on-chain monitoring dashboards tracking TVL, token transfers, and governance changes.",
            "Establish bug bounty programs and rapid response channels with the community."
        ],
        "commands": [
            {
                "snippet": "slither contracts/ --triage",
                "context": (
                    "Runs Slither analysis and prioritizes findings for review."
                ),
            },
            {
                "snippet": "forge test --fork-url https://mainnet.infura.io/v3/KEY",
                "context": (
                    "Executes Foundry tests against a forked mainnet state to validate interactions."
                ),
            },
            {
                "snippet": "myth analyze contracts/Vault.sol --solv 0.8.19",
                "context": (
                    "Runs Mythril symbolic analysis on a target Solidity contract."
                ),
            },
            {
                "snippet": "tenderly devnet spawn --project project-id",
                "context": (
                    "Creates a Tenderly devnet to simulate exploit scenarios safely."
                ),
            },
        ],
        "case_studies": [
            {
                "scenario": "Flash loan exploitation",
                "details": (
                    "Attackers used flash loans to manipulate prices and drain liquidity pools."
                ),
                "response": (
                    "Protocols added price checks, circuit breakers, and diversified oracle feeds."
                ),
            },
            {
                "scenario": "Governance takeover",
                "details": (
                    "A DAO attacker amassed voting power to pass malicious proposals."
                ),
                "response": (
                    "Community enacted quorum changes, delegated voting safeguards, and multi-sig oversight."
                ),
            },
        ],
    },
}
