import json, uuid, textwrap, re
from pathlib import Path

OUT = Path('/home/node/.openclaw/workspace/cyberlearn/content')
OUT.mkdir(parents=True, exist_ok=True)

LESSONS = [
    {
        'order_index': 652,
        'domain': 'iot_security',
        'title': 'IoT Security Fundamentals',
        'difficulty': 1,
        'subtitle': 'How connected devices work, fail, and get defended',
        'slug': 'iot_security_fundamentals',
        'estimated_time': 45,
        'concepts': ['asset inventory', 'default credentials', 'firmware', 'network segmentation', 'device lifecycle', 'telemetry'],
        'prereq_hint': 'basic networking and endpoint security',
        'analogy': 'a smart office full of tiny computers that never got the same attention as laptops',
        'opening_points': ['why IoT devices are common attack paths', 'what makes IoT different from normal IT', 'basic defense habits that remove cheap attacker wins'],
        'deep_sections': ['device anatomy', 'common weakness patterns', 'defensive baselines'],
        'case_study': ('In 2016, the Mirai botnet abused default usernames and passwords on cameras and DVRs, then used those devices to launch massive DDoS attacks against Dyn. Large parts of the internet went sideways because small neglected devices were easy to hijack.'),
        'exercise_cmds': ['nmap -sV -O 192.168.1.0/24', 'curl -I http://192.168.1.50', 'openssl s_client -connect 192.168.1.60:443'],
        'video': 'https://www.youtube.com/watch?v=8kbxMdlBM4Q — Intro-level overview of why IoT devices create unique security risk and why inventory matters.',
        'next_title': 'Smart Home Security 101',
        'advanced_topics': ['firmware reverse engineering', 'wireless protocol analysis', 'hardware trust and supply chain validation'],
        'tags': ['IoT', 'Beginner', 'Blue Team', 'Asset Management']
    },
    {
        'order_index': 653,
        'domain': 'iot_security',
        'title': 'Smart Home Security 101',
        'difficulty': 1,
        'subtitle': 'Protecting cameras, speakers, locks, hubs, and home automations',
        'slug': 'smart_home_security_101',
        'estimated_time': 40,
        'concepts': ['home network zoning', 'vendor cloud risk', 'strong admin passwords', 'firmware updates', 'privacy settings', 'voice assistant abuse'],
        'prereq_hint': 'basic home networking and consumer devices',
        'analogy': 'giving house keys to dozens of gadgets, apps, and cloud dashboards',
        'opening_points': ['how convenience creates exposure', 'which devices are highest risk at home', 'how to harden a smart home without becoming a full-time sysadmin'],
        'deep_sections': ['high-risk smart home categories', 'cloud and app trust boundaries', 'simple hardening checklist'],
        'case_study': ('Consumer camera breaches have repeatedly shown that reused passwords, weak account recovery, and exposed RTSP feeds turn convenience products into stalking and privacy nightmares. Rings, baby monitors, and generic IP cameras have all been abused when account security was weak.'),
        'exercise_cmds': ['ip addr', 'nmap -sn 192.168.1.0/24', 'ping -c 3 192.168.1.1'],
        'video': 'https://www.youtube.com/watch?v=d0r9e4D6P0Q — Practical home-focused security advice for connected devices and voice assistants.',
        'next_title': 'Firmware Reverse Engineering for IoT',
        'advanced_topics': ['traffic inspection for smart devices', 'firmware extraction', 'local-only automation design'],
        'tags': ['IoT', 'Beginner', 'Home Lab', 'Privacy']
    },
    {
        'order_index': 662,
        'domain': 'iot_security',
        'title': 'Firmware Reverse Engineering for IoT',
        'difficulty': 3,
        'subtitle': 'Pulling apart embedded firmware to find secrets, bugs, and unsafe design',
        'slug': 'firmware_reverse_engineering_for_iot',
        'estimated_time': 60,
        'concepts': ['firmware images', 'filesystem extraction', 'binwalk', 'emulation', 'hardcoded secrets', 'patch diffing'],
        'prereq_hint': 'Linux CLI, basic reversing, and familiarity with filesystems',
        'analogy': 'opening up a sealed toy and reading the tiny rulebook hidden inside the plastic shell',
        'opening_points': ['why firmware is where vendors hide critical truth', 'how analysts extract filesystems and configs', 'where credentials and vulnerabilities usually show up'],
        'deep_sections': ['acquisition and unpacking', 'static analysis paths', 'emulation and validation'],
        'case_study': ('Researchers have repeatedly found hardcoded credentials, private keys, and old BusyBox components inside camera and router firmware. One common pattern: vendors patch the web UI but leave the backend CGI handler vulnerable inside the image.'),
        'exercise_cmds': ['binwalk -e firmware.bin', 'strings firmware.bin | head -50', 'grep -R "password\|token\|secret" _firmware.bin.extracted -n'],
        'video': 'https://www.youtube.com/watch?v=SpP8fKq5J1k — Walkthrough of extracting and inspecting embedded firmware with binwalk and strings.',
        'next_title': 'IoT Network Protocol Security',
        'advanced_topics': ['UART/JTAG access', 'QEMU emulation', 'diffing patched and unpatched images'],
        'tags': ['IoT', 'Advanced', 'Reverse Engineering', 'Firmware']
    },
    {
        'order_index': 663,
        'domain': 'iot_security',
        'title': 'IoT Network Protocol Security',
        'difficulty': 2,
        'subtitle': 'Securing MQTT, CoAP, BLE, Zigbee, and other chatty machine protocols',
        'slug': 'iot_network_protocol_security',
        'estimated_time': 50,
        'concepts': ['MQTT', 'CoAP', 'BLE', 'Zigbee', 'authentication gaps', 'encrypted transport'],
        'prereq_hint': 'basic packet analysis and IoT fundamentals',
        'analogy': 'a neighborhood where devices whisper short messages all day, and anyone nearby may listen if the windows are open',
        'opening_points': ['why lightweight protocols trade safety for simplicity', 'what weak auth looks like in machine traffic', 'how defenders monitor and isolate fragile protocols'],
        'deep_sections': ['protocol design tradeoffs', 'attack surfaces by protocol', 'secure deployment patterns'],
        'case_study': ('MQTT brokers exposed to the internet have been found with anonymous access enabled, allowing strangers to read telemetry, publish malicious commands, or enumerate device topics. In industrial and home settings alike, weak broker settings have created both safety and privacy issues.'),
        'exercise_cmds': ['mosquitto_sub -h 127.0.0.1 -t "#" -v', 'tcpdump -i any port 1883 -nn', 'tshark -r capture.pcap -Y mqtt'],
        'video': 'https://www.youtube.com/watch?v=EIxdz-2rhLs — Good overview of MQTT and why transport security and topic authorization matter.',
        'next_title': 'Industrial IoT (IIoT) and SCADA Security',
        'advanced_topics': ['broker ACL design', 'wireless packet capture', 'protocol fuzzing'],
        'tags': ['IoT', 'Intermediate', 'Network Security', 'Protocols']
    },
    {
        'order_index': 664,
        'domain': 'iot_security',
        'title': 'Industrial IoT (IIoT) and SCADA Security',
        'difficulty': 3,
        'subtitle': 'Defending connected industrial control systems where outages hit the real world',
        'slug': 'industrial_iiot_and_scada_security',
        'estimated_time': 60,
        'concepts': ['OT vs IT', 'PLC', 'safety systems', 'segmentation', 'protocol monitoring', 'engineering workstation trust'],
        'prereq_hint': 'network defense, basic ICS awareness, and incident response concepts',
        'analogy': 'running a factory where the computers are not just handling email — they are opening valves, moving motors, and keeping humans safe',
        'opening_points': ['why industrial environments punish mistakes harder than corporate IT', 'how legacy uptime needs collide with modern threats', 'what safe defensive controls look like in OT'],
        'deep_sections': ['OT architecture', 'common attack paths', 'safe hardening and monitoring'],
        'case_study': ('The 2017 Triton/Trisis attack targeted Schneider Electric safety systems in a petrochemical environment. That matters because the adversary was not just after data. They went after the last line of protection designed to stop dangerous physical conditions.'),
        'exercise_cmds': ['tcpdump -i eth0 host 10.20.30.40 -nn', 'nmap -sT -Pn --top-ports 20 10.20.30.40', 'zeek -r ot_capture.pcap'],
        'video': 'https://www.youtube.com/watch?v=Jb4X2GQ8Gz0 — Explains OT/ICS architecture and why industrial monitoring must be deliberate and safe.',
        'next_title': 'Hardware Supply Chain Security',
        'advanced_topics': ['ICS threat hunting', 'safety instrumented systems', 'secure remote vendor access'],
        'tags': ['IoT', 'Advanced', 'OT', 'SCADA']
    },
    {
        'order_index': 677,
        'domain': 'iot_security',
        'title': 'Hardware Supply Chain Security',
        'difficulty': 3,
        'subtitle': 'Trust, tamper risk, and verification from factory to field device',
        'slug': 'hardware_supply_chain_security',
        'estimated_time': 55,
        'concepts': ['bill of materials', 'secure boot', 'device provenance', 'counterfeit components', 'update signing', 'tamper detection'],
        'prereq_hint': 'embedded systems basics and product security lifecycle concepts',
        'analogy': 'building a safe out of parts bought from dozens of strangers and hoping none of them slipped in a fake lock',
        'opening_points': ['why trust starts before software ships', 'how counterfeit or altered hardware breaks security promises', 'what verification steps reduce unseen risk'],
        'deep_sections': ['supply chain stages', 'hardware root of trust', 'verification and response'],
        'case_study': ('Supply chain risk in hardware has shown up through counterfeit chips, exposed debug interfaces left on production boards, and update systems that trust unsigned images. The exact vendor changes, but the mistake is the same: trust was assumed instead of verified.'),
        'exercise_cmds': ['sha256sum firmware_v1.bin firmware_v2.bin', 'openssl dgst -sha256 -verify pubkey.pem -signature update.sig firmware.bin', 'lsusb -v'],
        'video': 'https://www.youtube.com/watch?v=4mk1v5N8x8c — Good primer on roots of trust, secure boot, and verification in embedded supply chains.',
        'next_title': 'AI Security 101',
        'advanced_topics': ['TPM/secure element design', 'hardware attestation', 'factory provisioning controls'],
        'tags': ['IoT', 'Advanced', 'Supply Chain', 'Hardware Security']
    },
    {
        'order_index': 647,
        'domain': 'ai_security',
        'title': 'LLM Prompt Injection Attacks',
        'difficulty': 2,
        'subtitle': 'How natural-language instructions become attack payloads against AI systems',
        'slug': 'llm_prompt_injection_attacks',
        'estimated_time': 45,
        'concepts': ['system prompt trust', 'indirect injection', 'tool misuse', 'data exfiltration', 'instruction hierarchy', 'guardrails'],
        'prereq_hint': 'basic understanding of LLM apps and web security logic flaws',
        'analogy': 'tricking a very obedient intern by hiding bad instructions inside a document they were told to summarize',
        'opening_points': ['what prompt injection is and is not', 'why models struggle to separate data from instructions', 'how to build systems that fail safer'],
        'deep_sections': ['attack mechanics', 'real app failure modes', 'layered mitigations'],
        'case_study': ('Researchers and red teamers have shown over and over that AI assistants connected to email, documents, and tools can be manipulated by hidden text in a web page, PDF, or issue ticket. The model reads attacker content and may follow the attacker instead of the developer.'),
        'exercise_cmds': ['grep -R "ignore previous instructions" prompts/ -n', 'python3 sanitize_input.py sample.txt', 'jq . tool_policy.json'],
        'video': 'https://www.youtube.com/watch?v=6vV6B0KxY3Q — Clear explanation of prompt injection and indirect prompt injection in tool-using LLM systems.',
        'next_title': 'AI Model Poisoning and Backdoors',
        'advanced_topics': ['policy separation', 'model context isolation', 'tool-call allowlists'],
        'tags': ['AI Security', 'Intermediate', 'Application Security', 'LLM']
    },
    {
        'order_index': 648,
        'domain': 'ai_security',
        'title': 'AI Model Poisoning and Backdoors',
        'difficulty': 3,
        'subtitle': 'When training data or fine-tuning quietly rewires model behavior',
        'slug': 'ai_model_poisoning_and_backdoors',
        'estimated_time': 60,
        'concepts': ['training data poisoning', 'backdoor triggers', 'fine-tuning risk', 'dataset provenance', 'evaluation drift', 'supply chain ML'],
        'prereq_hint': 'machine learning pipeline basics and AI Security 101 concepts',
        'analogy': 'teaching a guard dog with mostly good lessons but slipping in one secret command that makes it sit down for the wrong person',
        'opening_points': ['how poisoned data changes future behavior', 'what backdoor triggers look like', 'how defenders test and gate model updates'],
        'deep_sections': ['poisoning paths', 'triggered behavior', 'pipeline defenses'],
        'case_study': ('Academic work has shown that tiny amounts of poisoned data can implant hidden triggers in image and language models. The model acts normal in most tests, then fails in a very specific way when the trigger appears. That is what makes backdoors nasty.'),
        'exercise_cmds': ['python3 hash_dataset.py data/train.csv', 'python3 scan_labels.py data/train.csv', 'python3 eval_model.py --suite backdoor_checks.json'],
        'video': 'https://www.youtube.com/watch?v=0bV0bV7Y2A4 — Intro to data poisoning, hidden triggers, and why evaluation beyond accuracy matters.',
        'next_title': 'Adversarial Machine Learning',
        'advanced_topics': ['influence functions', 'data lineage', 'secure MLOps approvals'],
        'tags': ['AI Security', 'Advanced', 'ML Security', 'Data Integrity']
    },
    {
        'order_index': 649,
        'domain': 'ai_security',
        'title': 'Adversarial Machine Learning',
        'difficulty': 3,
        'subtitle': 'Inputs crafted to fool models without looking obviously malicious to humans',
        'slug': 'adversarial_machine_learning',
        'estimated_time': 60,
        'concepts': ['evasion attacks', 'perturbations', 'robustness', 'transferability', 'confidence calibration', 'defensive evaluation'],
        'prereq_hint': 'ML classification basics and model poisoning concepts',
        'analogy': 'painting tiny marks on a stop sign so a self-driving system thinks it is a speed limit sign while humans still see STOP',
        'opening_points': ['why model perception differs from human perception', 'how evasion attacks exploit decision boundaries', 'what robust evaluation actually checks'],
        'deep_sections': ['attack generation', 'cross-model transfer', 'defenses and their limits'],
        'case_study': ('Work in computer vision showed that carefully crafted perturbations can make models misclassify high-confidence inputs. Later studies expanded this to audio, malware classifiers, and even physical attacks where stickers or patches changed outcomes in the real world.'),
        'exercise_cmds': ['python3 run_fgsm.py --model demo.pt --image sample.png', 'python3 compare_scores.py clean.json adv.json', 'python3 evaluate_robustness.py --eps 0.03'],
        'video': 'https://www.youtube.com/watch?v=JXnM8D8mJxA — Solid visual explanation of adversarial examples and why robustness is hard.',
        'next_title': 'Firmware Reverse Engineering for IoT',
        'advanced_topics': ['certified robustness', 'ensemble defenses', 'threat-model driven evaluation'],
        'tags': ['AI Security', 'Advanced', 'ML Security', 'Adversarial ML']
    },
    {
        'order_index': 650,
        'domain': 'ai_security',
        'title': 'AI Security 101',
        'difficulty': 1,
        'subtitle': 'The attack surface of models, data, prompts, and AI-powered apps',
        'slug': 'ai_security_101',
        'estimated_time': 40,
        'concepts': ['model attack surface', 'prompt attacks', 'training data risk', 'tool access', 'output validation', 'governance basics'],
        'prereq_hint': 'general security mindset and basic familiarity with AI assistants',
        'analogy': 'hiring a brilliant intern who learns fast, talks fast, and can still do something dumb if your instructions and permissions are messy',
        'opening_points': ['what AI security covers', 'how AI apps differ from classic software', 'why access control and validation still matter'],
        'deep_sections': ['AI stack attack surfaces', 'common failure patterns', 'starter defense playbook'],
        'case_study': ('Across 2023-2026, organizations rushed AI assistants into support, coding, search, and workflow automation. The repeated lesson was simple: models do not remove security basics. They create new ways to violate them when context, tools, and data are poorly separated.'),
        'exercise_cmds': ['cat ai_app_architecture.md', 'jq . permissions.json', 'python3 validate_output.py sample_response.json'],
        'video': 'https://www.youtube.com/watch?v=Jw1dM0Y4z2A — Beginner-friendly overview of AI system risks and practical controls.',
        'next_title': 'LLM Prompt Injection Attacks',
        'advanced_topics': ['agentic tool control', 'model red teaming', 'secure AI deployment reviews'],
        'tags': ['AI Security', 'Beginner', 'Governance', 'Secure Design']
    },
]

JIM = [
    'teach_like_im_10','memory_hooks','connect_to_what_i_know','active_learning','meta_learning',
    'minimum_effective_dose','reframe_limiting_beliefs','gamify_it','learning_sprint','multiple_memory_pathways'
]

def md(text):
    return textwrap.dedent(text).strip()


def block(type_, text):
    return {'type': type_, 'content': {'text': md(text)}}

for lesson in LESSONS:
    title = lesson['title']
    domain = lesson['domain']
    concepts = lesson['concepts']
    concept_line = ', '.join(concepts)
    q = []
    for i in range(4):
        q.append({
            'question_id': str(uuid.uuid4()),
            'question': [
                f"You are reviewing a project that includes {title.lower()}. Which first move gives the best security value before you chase edge-case threats?",
                f"A team says their controls for {title.lower()} are 'good enough' because the system works. Which response is most correct?",
                f"During an incident tied to {title.lower()}, what evidence would most help you separate a design flaw from a one-off operator mistake?",
                f"Which statement best captures the core defensive lesson from this lesson on {title.lower()}?"
            ][i],
            'options': [
                [
                    'Build an inventory, map trust boundaries, and remove the easiest attacker wins first',
                    'Wait for a breach so you know where to focus',
                    'Buy a new tool before understanding the environment',
                    'Assume vendor defaults are secure because the product is commercial'
                ],
                [
                    'Functionality alone is not proof of security; you must test abuse paths and privilege boundaries',
                    'If users are happy, security review can wait until the next major release',
                    'A hidden system prompt or closed firmware means attackers cannot study it',
                    'Security risk disappears when traffic is internal only'
                ],
                [
                    'Configuration history, logs, firmware or model version changes, and access records around the event',
                    'Only the vendor marketing sheet',
                    'A screenshot of the dashboard from any random day',
                    'An unverified rumor from chat'
                ],
                [
                    'Trust must be earned with validation, least privilege, visibility, and safe defaults',
                    'Complexity is the best security control',
                    'Attackers only target the biggest systems',
                    'One perfect setting removes the need for monitoring'
                ]
            ][i],
            'correct_answer': 0,
            'difficulty': lesson['difficulty'],
            'type': 'multiple_choice',
            'explanation': [
                f"The right first move is inventory plus trust-boundary mapping because you cannot defend what you have not identified. In this lesson, {title} is framed as a system problem, not a magic-tool problem. Waiting for a breach is reckless, buying tools before understanding the environment wastes time, and trusting vendor defaults is how cheap compromises happen.",
                'Security review is about abuse, not just intended function. Systems fail when defenders confuse “it works” with “it is safe.” Internal traffic can be hostile, hidden internals can still be reverse engineered or manipulated, and user happiness says nothing about privilege design.',
                'Good incident response needs evidence that ties behavior to version, config, and access context. Logs, version history, and change records help you prove whether the issue came from architecture, drift, or an operator action. The other choices are noise, not evidence.',
                f"This lesson keeps hammering the same point: blind trust is stupid. Good defense means validation, least privilege, visibility, and safe defaults. Complexity is not protection, attackers love neglected systems, and monitoring still matters even with strong preventive controls."
            ][i]
        })

    opening = f'''
    ## Introduction to {title}

    {title} matters because it sits where convenience and risk collide. Think of it like {lesson['analogy']}. The device or model is useful, fast, and often ignored until something breaks. Attackers love that. They do not need cinematic zero-days when they can win with weak defaults, missing validation, or blind trust.

    Start with the big idea: security here is less about one magic trick and more about asking boring, powerful questions. What is connected? Who can talk to it? What does it trust? What happens when it gets strange input? Who notices when it goes sideways?

    Let's break it down:
    1. Find the parts that matter most.
    2. Remove the cheap attacker wins.
    3. Add visibility so surprises are short-lived.

    **Why you should care:** {lesson['opening_points'][0]}. This lesson also shows {lesson['opening_points'][1]} and {lesson['opening_points'][2]}.

    **Key Insight:** The fastest way to improve security is usually not adding complexity. It is making trust explicit and shrinking it.
    '''

    deep = f'''
    ## Deep Dive: How {title} Actually Breaks and How Defenders Respond

    The easiest mistake is to treat {title.lower()} as a niche topic. It is not. It is just security wearing different clothes. The same old problems keep showing up: weak identity, poor input handling, unsafe update paths, over-privileged integrations, and missing logs. The surface looks new. The failure pattern is ancient.

    ### 1) {lesson['deep_sections'][0].title()}
    Start with architecture. Every system in this lesson has assets, identities, trust boundaries, and update paths. If you cannot draw those four things, you do not understand the risk yet. For beginners, think of it like mapping a house: doors, windows, keys, and who gets to enter. For advanced work, add protocol details, firmware or model versions, external dependencies, and admin workflows.

    In practice, analysts should document:
    - the main components and where they live
    - who administers them
    - what data they handle
    - how updates arrive
    - what 'normal' traffic or behavior looks like

    A lot of ugly incidents happen because defenders only see the shiny interface, not the layers beneath it. A smart lock is not just a lock. It is a mobile app, a local wireless protocol, a cloud API, an account recovery flow, and a firmware update mechanism. An LLM chatbot is not just text generation. It is prompts, retrieval sources, tools, identity context, policies, logging, and output handling.

    ### 2) {lesson['deep_sections'][1].title()}
    Attackers usually pick the shortest path. That is why they love default credentials, exposed services, anonymous broker access, unsafe parsers, old libraries, hidden debug features, prompt confusion, poisoned data, or brittle classifiers. These are not glamorous bugs. They are just cheap leverage.

    Common weakness patterns in this lesson:
    - missing or weak authentication
    - trust in external content without inspection
    - too much privilege for services or tools
    - poor isolation between components
    - stale software, firmware, or model artifacts
    - no good way to reconstruct what happened after the fact

    If you remember one thing, remember this: systems fail where trust is broad and invisible. A device that trusts any nearby command source, a model that treats hostile text as trusted instruction, or a controller that accepts old unsigned updates are all doing the same stupid thing. They are treating input as authority.

    ### 3) {lesson['deep_sections'][2].title()}
    Defenders do better when they reduce assumptions. Start with least privilege. If a component only needs read access, do not give write access. If a device only needs to talk to one broker, block the rest. If a model should summarize a document, do not also let it freely call sensitive tools. Then add validation. Signed updates, strong auth, topic ACLs, prompt boundary checks, dataset lineage, output review, and alerting are all examples of earned trust.

    Monitoring matters because prevention fails in the real world. Good teams log version changes, administrative actions, unusual access patterns, failed auth, and high-risk operations. They also keep enough context to tell a story later. A raw alert with no surrounding evidence is a shrug, not a defense.

    **Real-World Example:**
    {lesson['case_study']}

    That incident pattern matters because it shows the difference between theoretical risk and operational pain. The compromise path was not magical. It was built from weak assumptions. That is exactly why disciplined baselines work.

    **Technical Details:**
    A practical review should check versions, exposed ports, trust relationships, update signing, role separation, logging coverage, and recovery steps. The analyst should be able to answer three questions fast: What can be reached? What can be changed? What evidence survives if something breaks?
    '''

    diagram = f'''
    ## Visual Architecture

    ```
        User/Admin
            |
            v
      [ Management Plane ]
            |
      +-----+-------------------+
      |                         |
      v                         v
    [ Core Service ] <-----> [ Update/Control Source ]
      |                         |
      v                         v
    [ Device/Model ] -----> [ Logs/Telemetry ]
      |
      v
    [ Physical / Business Impact ]
    ```

    **Key Components:**
    - Management Plane: Where accounts, policies, and admin actions live.
    - Core Service: The broker, API, controller, model app, or middleware that routes decisions.
    - Device/Model: The thing doing work in the real world.
    - Update/Control Source: Firmware server, dataset source, system prompt, or tool policy.
    - Logs/Telemetry: Your memory when things get weird.

    **Flow Explanation:**
    1. Admins and users send requests through the management plane.
    2. The core service translates those requests into actions or decisions.
    3. The device or model acts, which creates business impact.
    4. Updates and policies silently shape behavior, so they must be trusted carefully.
    5. Telemetry is what lets defenders catch abuse before it becomes a headline.
    '''

    memory = f'''
    ## Memory Techniques

    ### Mnemonic: TRUST

    **T.R.U.S.T.** is the quick review for {title.lower()}:
    - **T** – Track the assets and versions
    - **R** – Reduce privilege and reachability
    - **U** – Understand trust boundaries
    - **S** – Secure updates, secrets, and settings
    - **T** – Test what happens under abuse

    **Memory Hook:** Think of TRUST like checking a rental car before a road trip. You do not just assume the brakes, doors, and fuel gauge are fine because the paint looks nice.

    ### Alternative Mnemonic: MAPS

    - **M**ap components
    - **A**uthenticate strongly
    - **P**atch or pin versions
    - **S**ee the logs

    **Practice Technique:**
    - Say TRUST before any review.
    - Write MAPS at the top of your notes.
    - Use both on one real system today.
    - Explain the difference between them to a teammate.
    '''

    code = f'''
    ## Hands-On Exercise: First-Pass Review for {title}

    **Objective:** Build a simple workflow that turns a vague environment into something observable and reviewable.

    **Prerequisites:**
    - Shell access to a lab or sample environment
    - Permission to scan or inspect the target
    - Basic comfort reading command output

    **Step-by-Step Instructions:**

    ### Step 1: Identify what is there
    ```bash
    # Start with a safe inventory pass
    {lesson['exercise_cmds'][0]}

    # Expected output:
    # A list of hosts, ports, banners, and sometimes OS guesses
    ```

    ### Step 2: Inspect one target more closely
    ```bash
    # Probe a relevant service or host
    {lesson['exercise_cmds'][1]}

    # What to look for:
    # Server headers, open topics, obvious defaults, or missing protections
    ```

    ### Step 3: Validate one security control
    ```bash
    # Check encryption, signatures, or parsed traffic depending on the lab
    {lesson['exercise_cmds'][2]}

    # What to look for:
    # Certificate details, protocol behavior, or validation success/failure
    ```

    ### Step 4: Analyze
    Write down:
    1. what you discovered
    2. what trust assumption each item depends on
    3. the cheapest hardening step you would take next

    **Common Issues:**
    - Error: permission denied → Fix: run in a lab or with approved access only.
    - Problem: noisy or incomplete output → Troubleshoot: narrow the target and rerun with notes.
    - Problem: you found something but do not know if it is bad → Compare against vendor docs, secure baselines, and expected behavior.

    **Challenge:** Can you turn your findings into three risk statements written in plain English?

    **Success Criteria:**
    ✓ You can name the assets or services you inspected
    ✓ You can explain one trust boundary clearly
    ✓ You can propose one practical fix with evidence
    '''

    real_world = f'''
    ## Case Study: What This Looks Like in the Real World

    **Background:**
    {lesson['case_study']}

    **The Incident Pattern:**
    Attackers did not need perfection. They found an exposed or weakly protected path, used it to gain a foothold, then expanded trust from there. That could mean issuing device commands, joining a botnet, exfiltrating data, abusing tools, or triggering unsafe model behavior.

    **Technical Details:**
    - Vulnerability exploited: weak auth, unsafe defaults, missing validation, or brittle trust separation
    - Attack vector used: reachable service, hostile content, poisoned artifact, or crafted input
    - Tools or techniques employed: public scanners, simple scripts, stolen creds, or iterative prompt/model abuse
    - Timeline of events: reconnaissance → foothold → misuse of trust → expanded impact

    **What Went Wrong:**
    1. The environment trusted something it should have verified.
    2. Visibility was too thin to catch the problem early.
    3. Recovery planning lagged behind deployment speed.

    **Lessons Learned:**
    - Inventory is not paperwork. It is defensive eyesight.
    - Strong defaults beat heroic cleanup.
    - Logging without context is barely logging.

    **How This Relates to {title}:**
    The lesson is not “be afraid.” It is “design for abuse.” If you assume weird input, stale software, and credential mistakes will happen, your controls become much saner.

    **Prevention:**
    If the team had applied the basics from this lesson — version awareness, least privilege, safer update trust, and meaningful telemetry — the blast radius would likely have been smaller and the response much faster.

    **Additional Examples:**
    - Small office routers compromised because remote admin was exposed with reused credentials.
    - AI assistants leaking data because untrusted documents were treated like trusted instructions.
    - Industrial gear left with flat network access, letting a simple foothold expand toward sensitive controllers.

    **Your Turn:**
    Pick one system you know. Where is it trusting too much right now?
    '''

    quiz = f'''
    ## Knowledge Check: Spot the Dangerous Assumption

    **Challenge:** Test your understanding before moving forward.

    ### Question 1
    A team says, “It is on the internal network, so we are safe.”
    What should you do?
    A) Accept that because internal networks are trusted
    B) Ask who can reach it, how it authenticates, and what happens if one internal host is compromised
    C) Focus only on branding and user experience
    D) Disable logging to reduce noise

    **Think it through:** Internal is a location, not a security property.

    ### Question 2
    You find outdated software, weak defaults, and poor logs. Which one matters most?
    A) Only the outdated software
    B) Only the weak defaults
    C) Only the poor logs
    D) All of them, because attackers chain weaknesses

    ### Question 3
    You have budget for one first improvement. Which choice is strongest?
    A) Add inventory plus least privilege plus update discipline
    B) Ignore basics and buy the fanciest dashboard
    C) Hide the system name and hope attackers miss it
    D) Wait for a vendor webinar

    **Discuss:** If you picked B, C, or D, the system is probably choosing vibes over security.
    '''

    simulation = f'''
    ## Advanced Lab: Investigate and Contain a Suspicious Change

    **Scenario:**
    You are the security analyst for an environment using {title.lower()}. The team reports strange behavior: unexpected commands, odd outputs, or traffic that does not match the normal pattern.

    **Your Mission:**
    Confirm what changed, contain the risk safely, and produce a clear short report.

    **Available Resources:**
    - Inventory or architecture notes
    - Recent logs and version history
    - Access to a test or staging environment

    **Step 1: Initial Assessment**
    Check the obvious first: versions, recent changes, new integrations, unexpected network peers, and privileged actions.

    ```bash
    # Commands you might use:
    journalctl -n 200
    grep -R "error\|warning\|denied" logs/ -n
    diff -u known_good.conf current.conf
    ```

    **Step 2: Investigation**
    Compare current behavior to a known-good baseline. Ask whether the issue follows content, a configuration change, an update, or a specific account.

    **Step 3: Action**
    Contain safely. Restrict access, roll back bad changes if appropriate, rotate exposed secrets, and preserve evidence.

    **Step 4: Documentation**
    Record what happened, what evidence supports it, what you changed, and what follow-up control should prevent a repeat.

    **Debrief Questions:**
    - What assumption failed first?
    - Which log or artifact was most valuable?
    - What would you automate next time?

    **Bonus Challenge:**
    Write a one-paragraph incident summary that a manager and engineer could both understand.
    '''

    prior = f'''
    ## Building on What You Know

    **Remember from {lesson['prereq_hint']}:**
    You already know that systems need identity, boundaries, patching, and monitoring.

    **Now We're Adding:**
    {title} applies those same ideas to an environment with different constraints: lightweight devices, safety-sensitive operations, model behavior, hidden internals, or cloud-linked consumer workflows.

    **The Connection:**
    Basic security + better trust mapping = strong first-pass defense.

    Think of it like building a house:
    - Previous knowledge = foundation
    - This lesson = walls and wiring
    - Next lesson = the tricky stuff hidden behind the drywall

    **Similar Concepts:**
    This is similar to checking kitchen hygiene. A clean counter is good, but you also need to know where the food came from, who touched it, and whether the fridge is lying.

    **Analogy:**
    Just like a good airport separates passengers, baggage, crew, and maintenance areas, a secure technical system separates users, control paths, updates, and high-risk actions.
    '''

    defender_playbook = f'''
    ## Defender Playbook: What Good Looks Like in Daily Work

    A lot of teams learn the theory, nod politely, then go back to chaos. Do not do that. Good defense for {title.lower()} is a repeatable routine.

    ### Daily Habits
    - Review important alerts instead of collecting them like sad digital baseball cards.
    - Track version changes, admin actions, and new integrations.
    - Check whether anything new can suddenly reach the system.

    ### Weekly Habits
    - Compare running state to known-good configuration.
    - Review exposed accounts, keys, topics, prompts, or management paths.
    - Test one assumption on purpose: a bad input, a denied action, a rollback, a log query.

    ### Monthly Habits
    - Patch or update with a documented rollback path.
    - Re-score the top risks using real evidence, not stale fear.
    - Remove one thing that no longer needs access.

    ### Questions Mature Teams Ask
    1. If this component lies to us, how would we know?
    2. If this dependency is hostile, how much damage can it do?
    3. If an admin account gets popped, what blast radius remains?
    4. Can we recover fast without guessing?

    ### Short Hardening Checklist
    - Strong identity for admins and services
    - Tight network or tool access boundaries
    - Signed, verified, or otherwise controlled updates and artifacts
    - Useful logs tied to time, actor, version, and outcome
    - A rollback or containment plan that was tested once, not imagined once

    Good teams are boring in the best way. They know what they run, they know what changed, and they do not confuse hope with control.
    '''

    mistakes = f'''
    ## Common Mistakes and Why They Keep Happening

    **Mistake 1: Treating deployment as the finish line**
    Teams rush to install the thing, connect the cloud account, or enable the new model workflow. Then they stop. But deployment is when risk starts, not when it ends.

    **Mistake 2: Letting convenience outrank containment**
    Flat networks, broad tool permissions, shared admin credentials, and wide-open broker topics feel easy. They are easy right up until incident response starts.

    **Mistake 3: No clear owner**
    If nobody owns updates, logs, and review, the system becomes a ghost ship. It is technically present and socially abandoned.

    **Mistake 4: Believing hidden means secure**
    Hidden prompts, unpublished APIs, private firmware formats, and obscure radio protocols are speed bumps, not walls. Attackers reverse engineer weird stuff for fun.

    **Mistake 5: Measuring maturity by purchase count**
    A shelf full of tools does not prove security. Evidence does. Can the team detect misuse? Can they explain trust boundaries? Can they contain a bad change? That is maturity.

    **Mistake 6: Ignoring recovery**
    Teams love prevention. Fair. Prevention feels heroic. Recovery feels like homework. Then the bad day arrives and everyone learns homework mattered.

    **How to Break the Pattern:**
    Write down ownership, log what matters, reduce permissions, test one ugly scenario, and keep a known-good baseline. None of this is glamorous. All of it works.
    '''

    field_guide = f'''
    ## Field Guide: Fast Questions for a Real Review

    Use this when you have 15 minutes, a messy environment, and no patience for fluff.

    ### Asset Questions
    - What exactly is the thing I am reviewing?
    - What version is it on?
    - What other systems does it talk to?
    - What breaks if it fails or lies?

    ### Identity Questions
    - Who can administer it?
    - Are accounts shared, local, federated, or embedded?
    - Are default or weak credentials still possible?
    - Can one account do far more than it should?

    ### Trust Questions
    - What input is treated like authority?
    - What data source, prompt, broker, firmware image, or control message is assumed safe?
    - Is there signature validation, policy enforcement, or contextual filtering?
    - If the source is malicious, what is the maximum damage?

    ### Visibility Questions
    - Do I have logs for authentication, configuration changes, update attempts, and unusual actions?
    - Can I tie logs to a time, actor, source, and version?
    - Will evidence survive long enough for investigation?

    ### Recovery Questions
    - Can I isolate the component without blowing up the whole service?
    - Do I have a known-good configuration or artifact?
    - Can I revoke keys, roll back updates, or disable risky features quickly?

    ### Decision Rule
    If you cannot answer these questions, the next step is not clever analysis. The next step is visibility and ownership. People skip this because it feels basic. Basic is exactly why it works.

    ### Plain-English Risk Statement Template
    "This system trusts **X** without verifying **Y**, which means an attacker who can control **Z** may cause **impact**. The fastest fix is **control**."

    Example:
    "This system trusts inbound MQTT clients without strong topic authorization, which means a compromised internal host may publish fake commands to production devices. The fastest fix is per-device authentication and broker ACLs."

    That template works because it forces clarity. No buzzwords. No smoke machine. Just the path, the trust failure, the impact, and the fix.
    '''

    glossary = f'''
    ## Teach It Like You're 10: Tiny Glossary for {title}

    Here is the simple-language version you can use when your brain is tired.

    - **Asset**: the thing you care about. A device, a model, a broker, a controller, a dataset.
    - **Identity**: the proof of who or what is talking. User login, API key, cert, service account, device credential.
    - **Trust boundary**: the line where you should stop assuming and start checking.
    - **Telemetry**: the breadcrumbs a system leaves behind.
    - **Least privilege**: give the smallest useful power, not the biggest possible power.
    - **Baseline**: your picture of normal.
    - **Containment**: stopping the mess from spreading.

    Think of a school building:
    - The asset is the classroom and the students.
    - Identity is the badge on the teacher and the key on the ring.
    - The trust boundary is the locked door.
    - Telemetry is the camera or sign-in sheet.
    - Least privilege is the janitor opening maintenance rooms but not the principal's safe.
    - Baseline is what a normal school day looks like.
    - Containment is closing one hallway when something bad happens instead of evacuating the whole city.

    Why this matters: when the words get simpler, the logic gets sharper. If you cannot explain a control simply, there is a decent chance you do not understand it cleanly yet. That is not an insult. That is a useful alarm.

    Try this drill:
    1. Pick one system from your environment.
    2. Name its asset, identity, trust boundary, telemetry, and containment step.
    3. If you get stuck, that is the gap to fix.

    Experts sometimes drown themselves in terms. Do not copy that habit. Simple language is not childish. It is precise.
    '''

    reflection = f'''
    ## Reflection: Learning About Learning

    **Pause and Think:**

    ### About the Content
    - Which weakness pattern felt most familiar?
    - Which control seems easiest to apply this week?
    - Which part still feels fuzzy: architecture, detection, or response?
    - Which idea from this lesson would have prevented the real-world incident fastest?

    ### About Your Learning Process
    - Did the analogy, commands, or case study help most?
    - When you got stuck, was it because of jargon or because the system itself is messy?
    - What short note would help future-you remember this lesson in 30 days?
    - Could you explain this lesson to a junior teammate without using buzzwords?

    ### Application Planning
    - Name one real system where you can use TRUST and MAPS.
    - Who could you teach this lesson to in under five minutes?
    - What evidence would prove you improved security, not just documentation?
    - What one risky trust assumption will you test first?

    ### Next Steps
    - [ ] Review the mnemonic daily for 3 days
    - [ ] Repeat the hands-on exercise in a real or lab environment
    - [ ] Draw one trust-boundary diagram from memory
    - [ ] Explain one risk to a teammate in plain language
    - [ ] Revisit your notes in two weeks
    - [ ] Turn one lesson idea into a checklist or detection rule

    **Journal Prompt:**
    Write three sentences: what assumption did this lesson break for you, what will you check differently now, and what proof will show the change actually helped?
    '''

    mindset1 = f'''
    ## Mindset Coach: Start Smaller Than Your Fear

    {title} can look big because the system has many moving parts. That does not mean you need to understand everything at once. You do not. You need one clean first pass. Map it. Shrink trust. Verify one claim. Then another. That is how real expertise grows.

    **Reframe Common Fears:**
    ❌ "I need to master every protocol, model detail, or embedded trick before I can help."
    ✅ "I need to spot the first dangerous assumption and test it."

    ❌ "If the vendor built it, the hard parts are handled."
    ✅ "Vendor work reduces effort, not responsibility."

    ❌ "This topic is too niche."
    ✅ "This is classic security logic in a new wrapper."
    '''

    video = block('video', lesson['video'])

    mindset2 = f'''
    ## Mindset Coach: You Are Building Good Instincts

    You just learned how to ask sharper questions about {title.lower()}. That matters more than memorizing trivia.

    **Celebrate Your Progress:**
    - ✓ You can name the main attack surface
    - ✓ You can spot broad or invisible trust
    - ✓ You can suggest at least one control that lowers real risk

    **Growth Reminder:**
    Strong defenders are not people who know every buzzword. They are people who keep making the system simpler to reason about. Do that and you will outperform a lot of noisy experts.

    **Next Session:**
    1. Recall TRUST from memory.
    2. Redraw the architecture in 60 seconds.
    3. Teach one case study to someone else.

    **Remember:** progress beats drama. Security is usually won by teams that keep doing the boring right things.
    '''

    whats_next = f'''
    ## What's Next: Level Up

    **Congratulations.** You completed {title}. You are now ready for:

    ### Next Lesson Preview
    **{lesson['next_title']}**
    The next lesson builds on this one and gets more specific about how attackers abuse trust and how defenders respond cleanly.

    ### Advanced Topics to Explore
    1. **{lesson['advanced_topics'][0]}** — deeper technical validation work
    2. **{lesson['advanced_topics'][1]}** — useful when you move from theory to investigation
    3. **{lesson['advanced_topics'][2]}** — where mature teams turn reviews into durable controls

    ### Skills You Unlocked
    - ✅ Architecture reading: you can sketch the important parts fast
    - ✅ First-pass triage: you can find cheap attacker wins
    - ✅ Practical hardening: you can recommend fixes without hand-wavy nonsense

    ### Your Learning Path
    ```
    Basics → {title} → {lesson['next_title']} → Advanced practice
              ✅           ⬆️ next
    ```

    ### Continue the Journey
    - **Immediate:** take the post-assessment
    - **This Week:** run the exercise on a real or lab target
    - **This Month:** document one review using TRUST and MAPS
    - **This Quarter:** teach the lesson to a teammate

    ### Track Your Progress
    You've earned **{100 + lesson['difficulty']*25} XP** for completing this lesson.
    '''

    content_blocks = [
        block('mindset_coach', mindset1),
        block('explanation', opening),
        video,
        block('explanation', deep),
        block('diagram', diagram),
        block('memory_aid', memory),
        block('code_exercise', code),
        block('real_world', real_world),
        block('quiz', quiz),
        block('simulation', simulation),
        block('explanation', defender_playbook),
        block('explanation', mistakes),
        block('explanation', field_guide),
        block('teach_like_10', glossary),
        block('explanation', prior),
        block('reflection', reflection),
        block('mindset_coach', mindset2),
        block('explanation', whats_next),
    ]

    lesson_json = {
        'lesson_id': str(uuid.uuid4()),
        'domain': domain,
        'title': title,
        'subtitle': lesson['subtitle'],
        'difficulty': lesson['difficulty'],
        'estimated_time': lesson['estimated_time'],
        'order_index': lesson['order_index'],
        'prerequisites': [],
        'concepts': concepts,
        'learning_objectives': [
            f"Analyze the main attack surfaces and trust boundaries involved in {title.lower()}",
            f"Apply practical review steps to identify common weaknesses in {title.lower()}",
            f"Evaluate mitigation choices and prioritize the fixes that reduce risk fastest",
            f"Create a short, evidence-based hardening plan for a real environment using {title.lower()}"
        ],
        'post_assessment': q,
        'jim_kwik_principles': JIM,
        'content_blocks': content_blocks,
        'tags': lesson['tags']
    }

    fn = OUT / f"lesson_{domain}_{lesson['order_index']}_{lesson['slug']}_RICH.json"
    fn.write_text(json.dumps(lesson_json, indent=2, ensure_ascii=False) + "\n", encoding='utf-8')
    json.loads(fn.read_text(encoding='utf-8'))
    print(fn.name)
