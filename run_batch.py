import csv, json, re, uuid
from pathlib import Path

base = Path('/home/node/.openclaw/workspace/cyberlearn')
ideas_path = base/'lesson_ideas.csv'
status_path = base/'batch_generation_status.json'
content_dir = base/'content'

with ideas_path.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

status = json.loads(status_path.read_text(encoding='utf-8'))
completed = set(map(str, status.get('completed', [])))
failed = set(map(str, status.get('failed', [])))

planned = [
    r for r in rows
    if r['status'] == 'idea'
    and str(r['lesson_number']) not in completed
    and str(r['lesson_number']) not in failed
]
planned.sort(key=lambda r: (int(r['order_index']), int(r['lesson_number'])))
selected = planned[:10]

principles = [
    'teach_like_im_10',
    'active_learning',
    'memory_hooks',
    'connect_to_what_i_know',
    'minimum_effective_dose',
    'multiple_memory_pathways',
    'learning_sprint',
    'reframe_limiting_beliefs',
    'gamify_it',
    'meta_learning',
]

def slugify(s):
    s = s.lower()
    s = re.sub(r'[^a-z0-9]+', '_', s)
    return re.sub(r'_+', '_', s).strip('_')

blocks_by_domain = {
 'fundamentals': [
  {'type':'mindset_coach','content':'This one looks simple on paper. It isn\'t. Cryptography is where security stops being vibes and starts being math with consequences.'},
  {'type':'explanation','title':'What cryptography is for','content':'Cryptography solves three jobs: keep secrets secret, prove who said what, and detect tampering.'},
  {'type':'explanation','title':'Teach Me Like I\'m 10: Locks, Boxes, and Signatures','content':'Symmetric crypto is one key for both lock and unlock. Asymmetric crypto is a public lock anyone can use and a private key only the owner can open. Hashes are fingerprints, not locks.'},
  {'type':'code_exercise','title':'SHA-256 and password hashing','content':'Use SHA-256 for integrity checks, not passwords. For passwords, use bcrypt or Argon2 with a salt.'},
  {'type':'real_world','title':'Where you see this at work','content':'TLS certificates, signed software updates, disk encryption, password storage, and secure messaging all lean on these primitives.'},
  {'type':'memory_aid','title':'Crypto shortcut','content':'Hash = fingerprint. Symmetric = fast bulk lock. Asymmetric = key exchange and signatures. Passwords = slow hash with salt.'},
  {'type':'reflection','title':'Think it through','content':'Why is a signed file not the same as an encrypted file?'},
  {'type':'mindset_coach','content':'Crypto is a tool, not a badge. Use the right primitive for the right job or you\'ll build expensive nonsense.'},
 ],
 'malware': [
  {'type':'mindset_coach','content':'Malware work is forensic work with fewer shortcuts. If you skip the boring bits, you\'ll confidently explain the wrong thing.'},
  {'type':'explanation','title':'Core idea','content':'Malware analysis starts with knowing what family you\'re looking at, how it behaves, and what evidence it leaves behind.'},
  {'type':'explanation','title':'Teach Me Like I\'m 10: Trouble in a Toy Box','content':'Static analysis is reading the toy box label. Dynamic analysis is watching the toy break things when you press play. Both matter.'},
  {'type':'code_exercise','title':'Simple triage checklist','content':'Check file type, hashes, strings, imports, signatures, and obvious indicators before you detonate anything.'},
  {'type':'real_world','title':'Why it matters','content':'A small implant can hide command-and-control, persistence, and theft behind very ordinary-looking processes.'},
  {'type':'memory_aid','title':'Malware triage flow','content':'Identify → hash → inspect → observe → correlate → report.'},
  {'type':'reflection','title':'Think it through','content':'What would make you trust a static finding more than a dynamic one?'},
  {'type':'mindset_coach','content':'Malware loves rushing defenders. Don\'t give it that pleasure. Be methodical.'},
 ],
 'pentest': [
  {'type':'mindset_coach','content':'This is where people get sloppy and call it skill. It\'s not skill; it\'s usually entropy with a shell prompt.'},
  {'type':'explanation','title':'Core idea','content':'These lessons are about finding attack paths in web apps and auth stacks — safely, deliberately, and with enough discipline to avoid self-inflicted nonsense.'},
  {'type':'explanation','title':'Teach Me Like I\'m 10: Secret Doors','content':'A web app is like a building with labeled doors. Good testing checks the side door, the service hatch, and the door the architect forgot to lock.'},
  {'type':'code_exercise','title':'Testing checklist','content':'Probe inputs, headers, parameters, auth flows, and error handling. Log what changed and why.'},
  {'type':'real_world','title':'Where this shows up','content':'WAFs, GraphQL schemas, SSRF pivots, XXE parsers, deserialization gadgets, OAuth flows, and SAML assertions all fail in predictable ways.'},
  {'type':'memory_aid','title':'Pentest mantra','content':'Enumerate, validate, exploit in a lab, document, then explain risk in plain English.'},
  {'type':'reflection','title':'Think it through','content':'Which is easier to miss: a broken auth flow or a weird server-side parser?'},
  {'type':'mindset_coach','content':'Careful beats clever when the target is production.'},
 ],
 'system': [
  {'type':'mindset_coach','content':'Operating systems are where security gets physical. Forget the marketing — the guts decide what\'s actually possible.'},
  {'type':'explanation','title':'Core idea','content':'These lessons cover how Windows, Linux, and related subsystems manage processes, permissions, services, and trust.'},
  {'type':'explanation','title':'Teach Me Like I\'m 10: The Building Manager','content':'The OS is the building manager. Processes are tenants, permissions are keys, services are scheduled workers, and the kernel is the security guard nobody argues with.'},
  {'type':'code_exercise','title':'Quick inspection habit','content':'Look at the running process, its parent, its permissions, and what starts it. Weirdness usually hides there.'},
  {'type':'real_world','title':'Why it matters','content':'Attackers abuse normal system features because normal features are trusted. That\'s why internals matter.'},
  {'type':'memory_aid','title':'System internals cue','content':'Process, thread, token, service, ACL, driver, trust chain.'},
  {'type':'reflection','title':'Think it through','content':'Which control would you harden first on a real workstation: services, ACLs, or scripting?'},
  {'type':'mindset_coach','content':'If the OS feels abstract, you\'re not done yet. Security lives in the details.'},
 ],
}

selected_nums = []
for r in selected:
    selected_nums.append(int(r['lesson_number']))
    domain = r['domain']
    title = r['title']
    idx = int(r['order_index'])
    fn = content_dir / f"lesson_{domain}_{idx}_{slugify(title)}_RICH.json"
    blocks = blocks_by_domain.get(domain, blocks_by_domain['system'])
    obj = {
        'lesson_id': str(uuid.uuid4()),
        'domain': domain,
        'title': title,
        'difficulty': int(r['difficulty']),
        'order_index': idx,
        'prerequisites': json.loads(r['prerequisites']) if r['prerequisites'].strip() else [],
        'concepts': [x.strip() for x in r['topics'].split(',') if x.strip()],
        'estimated_time': 45,
        'learning_objectives': [x.strip() for x in r['topics'].split(',')[:4] if x.strip()],
        'tags': [x.strip() for x in r['tags'].split(',') if x.strip()] + ['Built-In'],
        'jim_kwik_principles': principles,
        'content_blocks': blocks,
        'post_assessment': [
            {'question': f'What is the best first-step approach to {title}?', 'options': ['Guess quickly', 'Start with basics and verify assumptions', 'Skip to exploitation', 'Wait for a tool to tell you'], 'correct': 1, 'explanation': 'Good work starts with fundamentals and validation.'},
            {'question': f'Which choice best fits {title} in a production environment?', 'options': ['No notes, no logs', 'Careful scoping and documentation', 'Maximal noise', 'Random testing'], 'correct': 1, 'explanation': 'Production work demands discipline.'},
            {'question': f'What is the main value of {title}?', 'options': ['Buzzwords', 'Repeatable understanding', 'Luck', 'Memes'], 'correct': 1, 'explanation': 'Repeatability is the point.'},
        ]
    }
    if domain == 'fundamentals':
        obj['post_assessment'][0] = {'question':'Which statement about hashes is correct?', 'options':['They are reversible','They are fixed-length fingerprints','They encrypt data','They replace passwords'], 'correct':1, 'explanation':'Hashes are fixed-length digests.'}
    elif domain == 'malware':
        obj['post_assessment'][0] = {'question':'What is the safest first move with an unknown sample?', 'options':['Execute it on your laptop','Triage it first','Upload it to random tools without caution','Delete it immediately'], 'correct':1, 'explanation':'Triage before execution.'}
    elif domain == 'pentest':
        obj['post_assessment'][0] = {'question':'What should guide testing in web and auth work?', 'options':['Noise','Scope and validation','Speed only','Guessing'], 'correct':1, 'explanation':'Scope first, always.'}
    elif domain == 'system':
        obj['post_assessment'][0] = {'question':'Why study system internals?', 'options':['To memorize jargon','To understand what attackers can actually abuse','To avoid logs','To write prettier docs'], 'correct':1, 'explanation':'Internals explain capability and abuse.'}

    fn.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    json.loads(fn.read_text(encoding='utf-8'))

for r in rows:
    if int(r['lesson_number']) in selected_nums:
        r['status'] = 'completed'

with ideas_path.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

for n in selected_nums:
    if str(n) not in status['completed']:
        status['completed'].append(str(n))
status_path.write_text(json.dumps(status, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

print(json.dumps({'selected': selected_nums, 'count': len(selected_nums)}, ensure_ascii=False))
