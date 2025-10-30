from pathlib import Path
import argparse
import json
import uuid
from textwrap import dedent

TOOLS = [
    {
        "slug": "amcacheparser",
        "name": "AmcacheParser",
        "title": "Reconstructing Program Execution with AmcacheParser",
        "difficulty": 2,
        "order_index": 11,
        "artifact": "Windows Amcache hive",
        "default_path": r"C:\\Windows\\AppCompat\\Programs\\Amcache.hve",
        "key_evidence": [
            "Executable file names and full paths",
            "SHA1 hashes recorded for installed binaries",
            "Last execution timestamps including newly discovered RunKeyLastWrite",
            "Associated product metadata such as company, version, and binary size"
        ],
        "primary_use_cases": [
            "Establishing first and last execution times for executables",
            "Pivoting from hashed entries to identify lateral movement tools",
            "Correlating Amcache device installation data with USB forensics",
            "Rapid triage of persistence through the Programs Inventory database"
        ],
        "cli_options": [
            ("-f", "Path to the Amcache hive or mounted volume"),
            ("-o", "Directory for CSV and JSON outputs"),
            ("--recover", "Attempt carving of deleted Amcache entries"),
            ("--nl", "Disable large lookup lists to speed up triage"),
            ("--json", "Produce JSON formatted output for ingestion into SIEM"),
            ("--csv", "Default output for timeline tools"),
        ],
        "analysis_focus": "Focus on building a high-fidelity execution timeline by merging Amcache timestamps with Prefetch and ShimCache, and emphasize how hashed entries confirm malware staging.",
        "case_study": "During the 2020 UNC2452/SolarWinds supply chain intrusion, responders correlated Amcache records for SolarWinds.Orion.Core.BusinessLayer.dll with Prefetch artifacts to confirm when the SUNBURST backdoor executed on jump hosts.",
        "mnemonic": "AMCACHE = Applications, Metadata, Code Hashes, and Execution evidence.",
        "quiz_pairs": [
            ("Which AmcacheParser switch enables recovery of deleted entries from slack space?", ["--recover", "--json", "--nl", "--mp"], 0),
            ("Where is the Amcache hive located on modern Windows systems?", ["C:\\\\Windows\\\\System32\\\\config\\\\SAM", "C:\\\\Windows\\\\AppCompat\\\\Programs\\\\Amcache.hve", "C:\\\\ProgramData\\\\Microsoft\\\\Search", "HKCU\\\\Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run"], 1),
            ("What hash type does Amcache store for most executables parsed by AmcacheParser?", ["MD5", "SHA1", "SHA256", "BLAKE2"], 1)
        ],
        "post_assessment": [
            {
                "question": "Which AmcacheParser option lets you link carved Amcache entries that no longer exist in the hive?",
                "options": ["--recover", "--vhdx", "--l2t", "--be"],
                "correct_answer": 0,
                "difficulty": 2
            },
            {
                "question": "Which evidence attribute from Amcache is most reliable for confirming binary integrity during lateral movement investigations?",
                "options": ["File description", "Product version", "SHA1 hash", "Publisher"],
                "correct_answer": 2,
                "difficulty": 2
            },
            {
                "question": "How can you rapidly correlate Amcache data with other Windows timeline artifacts in bulk investigations?",
                "options": ["Rely only on the Programs Inventory SQLite DB", "Export to CSV and combine with PECmd and MFTECmd results in Timeline Explorer", "Mount the hive read-write and view in Registry Editor", "Ignore device entries because they are always redundant"],
                "correct_answer": 1,
                "difficulty": 3
            }
        ],
    },
    {
        "slug": "appcompatcacheparser",
        "name": "AppCompatCacheParser",
        "title": "Mastering ShimCache Analysis with AppCompatCacheParser",
        "difficulty": 2,
        "order_index": 12,
        "artifact": "Windows Application Compatibility (ShimCache) registry data",
        "default_path": r"SYSTEM hive: ControlSet001\\Control\\Session Manager\\AppCompatCache",
        "key_evidence": [
            "Full paths of executables touched by the Windows loader",
            "Last modified timestamps preserved when an executable was first seen",
            "Flags indicating execution status on pre-Windows 10 systems",
            "Cache entry ordering that approximates execution sequences"
        ],
        "primary_use_cases": [
            "Validate claims of program execution even when Prefetch is disabled",
            "Detect first-touch of LOLBins or renamed malware droppers",
            "Map deployment of ransomware across endpoints via common ShimCache entries",
            "Cross-check ephemeral tools run from SMB shares"
        ],
        "cli_options": [
            ("-f", "Path to SYSTEM hive"),
            ("-o", "Output directory"),
            ("--csv", "Write results to CSV"),
            ("--json", "Emit JSON output"),
            ("--merge", "Combine multiple hives to rebuild enterprise-wide view"),
            ("--vss", "Leverage Volume Shadow Copies mounted in evidence"),
        ],
        "analysis_focus": "Stress the need to interpret ShimCache timestamps carefully, explain ControlSet rotation, and show how to align AppCompatCache entries with Prefetch and Amcache to avoid false positives.",
        "case_study": "Incident handlers responding to the 2017 NotPetya outbreak used ShimCache data to prove that `perfc.dat` executed on machines even after attackers wiped Prefetch files with PsExec.",
        "mnemonic": "SHIM = Sequence, Hint of execution, Inexact timestamps, Memory of paths.",
        "quiz_pairs": [
            ("Which registry hive feeds AppCompatCacheParser?", ["SOFTWARE", "SYSTEM", "SAM", "NTUSER.DAT"], 1),
            ("What should you combine with ShimCache entries to confirm execution on Windows 10?", ["Only Prefetch", "Prefetch and Amcache", "BITS job logs", "No other artifacts"], 1),
            ("How does AppCompatCacheParser treat ControlSets?", ["Ignores them", "Parses only CurrentControlSet", "Can merge across ControlSets", "Rewrites ControlSet numbering"], 2)
        ],
        "post_assessment": [
            {
                "question": "Which attribute in ShimCache entries is most reliable for sequencing events across multiple hosts?",
                "options": ["File size", "Entry position and header ordering", "Flags field", "File extension"],
                "correct_answer": 1,
                "difficulty": 2
            },
            {
                "question": "How can you avoid false execution assumptions on Windows 10 when reviewing ShimCache?",
                "options": ["Trust the execution flag blindly", "Cross-reference Prefetch, SRUM, and Amcache data", "Assume every path ran as SYSTEM", "Ignore ControlSet rollover"],
                "correct_answer": 1,
                "difficulty": 3
            },
            {
                "question": "Which option helps AppCompatCacheParser interpret evidence stored within Volume Shadow Copies?",
                "options": ["--nl", "--vss", "--l2t", "--be"],
                "correct_answer": 1,
                "difficulty": 2
            }
        ],
    },
    {
        "slug": "bstrings",
        "name": "bstrings",
        "title": "High-Fidelity String Hunting with bstrings",
        "difficulty": 2,
        "order_index": 13,
        "artifact": "Binary string extraction from executables, memory images, and disk captures",
        "default_path": "Tool executes against any supplied binary path or mounted image",
        "key_evidence": [
            "Unicode and ASCII strings with contextual entropy scoring",
            "Heuristic tagging of URLs, IP addresses, registry keys, and PowerShell",
            "Ability to carve strings from slack space or compressed resources",
            "Regex-based filtering to isolate malware configuration markers"
        ],
        "primary_use_cases": [
            "Pivoting into obfuscated malware droppers during triage",
            "Profiling suspicious DLLs discovered in Prefetch or Amcache",
            "Extracting command-and-control indicators from memory dumps",
            "Rapid enrichment of IOC feeds with host-based artifacts"
        ],
        "cli_options": [
            ("-f", "Input file or directory"),
            ("-o", "Output file for results"),
            ("-m", "Minimum string length"),
            ("-a", "Enable automatic tagging of artifacts"),
            ("-r", "Apply regular expression filter"),
            ("--json", "Write structured JSON output for automation"),
        ],
        "analysis_focus": "Highlight how DFIR teams can use bstrings to decode malware configurations quickly, emphasizing filtering strategies and integration with YARA and Threat Intel platforms.",
        "case_study": "During the 2021 Microsoft Exchange Server Hafnium exploitation wave, analysts ripped through dropped webshells using bstrings to pull out hardcoded usernames and callback domains embedded in China Chopper variants.",
        "mnemonic": "BSTRINGS = Binary Slicing To Reveal Indicators, Notes, GUIDs, and Signatures.",
        "quiz_pairs": [
            ("Which bstrings switch enables automatic tagging of detected artifacts?", ["-a", "-m", "-r", "-o"], 0),
            ("Why would you raise the minimum string length when triaging a DLL?", ["To capture binary headers", "To reduce noise from short fragments", "To avoid Unicode", "To hash the file"], 1),
            ("Which output format supports ingestion into automation pipelines?", ["Console only", "TXT", "JSON", "XLS"], 2)
        ],
        "post_assessment": [
            {
                "question": "Which scenario benefits most from using bstrings with a regular expression filter?",
                "options": ["Calculating hash collisions", "Extracting URLs from a packed DLL", "Listing NTFS permissions", "Imaging a disk"],
                "correct_answer": 1,
                "difficulty": 2
            },
            {
                "question": "How can you enrich bstrings output to speed up hunt operations?",
                "options": ["Ignore tagging and analyze manually", "Feed JSON output into jq and Sigma conversions", "Disable Unicode extraction", "Only run it on .txt files"],
                "correct_answer": 1,
                "difficulty": 2
            },
            {
                "question": "What is a practical minimum string length when triaging heavily obfuscated shellcode?",
                "options": ["1 character", "3-4 characters to catch short commands", "25 characters", "512 characters"],
                "correct_answer": 1,
                "difficulty": 3
            }
        ],
    },
    {
        "slug": "evtxecmd",
        "name": "EvtxECmd",
        "title": "Deep Windows Event Log Triage with EvtxECmd",
        "difficulty": 2,
        "order_index": 14,
        "artifact": "Windows Event Log (.evtx) files",
        "default_path": r"C:\\Windows\\System32\\winevt\\Logs",
        "key_evidence": [
            "Security event IDs including logon events, process creation, and policy changes",
            "Operational logs for PowerShell, Sysmon, and Task Scheduler",
            "Forwarded Event tracing from Windows Event Forwarding",
            "Custom maps converting GUIDs into human-readable fields"
        ],
        "primary_use_cases": [
            "Timeline reconstruction across thousands of EVTX files",
            "Detection of credential dumping via 4624/4672 and Sysmon Event ID 10",
            "Identifying lateral movement using WinRM, RDP, and SMB logs",
            "Feeding parsed EVTX output into ELK or Timeline Explorer"
        ],
        "cli_options": [
            ("-f", "Path to a single EVTX file"),
            ("-d", "Directory recursion for bulk processing"),
            ("-o", "Output directory"),
            ("--csv", "Generate CSV output"),
            ("--json", "Emit JSON output with GUID expansion"),
            ("--maps", "Apply custom map files for vendor logs"),
            ("--inc", "Filter on specific Event IDs"),
        ],
        "analysis_focus": "Teach analysts how to prioritize key security logs, tune EvtxECmd maps, and merge results with Sysmon baselines to triage novel attacks fast.",
        "case_study": "In the aftermath of the 2021 Colonial Pipeline ransomware attack, Mandiant responders parsed thousands of EVTX files with EvtxECmd to trace DarkSide operators' RDP logons and PowerShell download cradle events.",
        "mnemonic": "EVTX = Events Validate Tactics and Execution.",
        "quiz_pairs": [
            ("Which EvtxECmd flag lets you apply Sigma-like parsing logic for custom provider GUIDs?", ["--csv", "--maps", "--recover", "--nl"], 1),
            ("What event combination often indicates credential dumping?", ["4624 + 4672 with short logon sessions", "5156 + 5158 with blocked ports", "1102 + 4720 with account creation", "12 + 13 with kernel updates"], 0),
            ("Why is JSON output valuable in modern DFIR pipelines?", ["It is smaller than CSV", "It allows structured ingestion into SIEM and log stacks", "It prevents tampering", "It encrypts the data"], 1)
        ],
        "post_assessment": [
            {
                "question": "Which EvtxECmd feature helps you normalize third-party provider events?",
                "options": ["--maps", "--json", "--l2t", "--vss"],
                "correct_answer": 0,
                "difficulty": 2
            },
            {
                "question": "How would you limit EvtxECmd output to high-value security events during triage?",
                "options": ["Use --inc with a curated list of Event IDs", "Process only System logs", "Disable CSV generation", "Edit the EVTX file manually"],
                "correct_answer": 0,
                "difficulty": 2
            },
            {
                "question": "Which combination accelerates cross-host correlation after a ransomware deployment?",
                "options": ["Only Security.evtx", "EvtxECmd JSON output merged with Sysmon and network telemetry", "Prefetch alone", "Relying on antivirus quarantine logs"],
                "correct_answer": 1,
                "difficulty": 3
            }
        ],
    },
    {
        "slug": "jlecmd",
        "name": "JLECmd",
        "title": "Jump List Artifact Intelligence with JLECmd",
        "difficulty": 2,
        "order_index": 15,
        "artifact": "Windows AutomaticDestinations and CustomDestinations Jump Lists",
        "default_path": r"%APPDATA%\\Microsoft\\Windows\\Recent\\AutomaticDestinations",
        "key_evidence": [
            "Recent documents and executables accessed by Jump List-enabled apps",
            "Timestamps for pin/unpin actions and number of interactions",
            "DestList metadata capturing AppID and window identifiers",
            "Remote share paths illustrating network lateral movement"
        ],
        "primary_use_cases": [
            "Uncovering exfiltration staging directories used via Explorer or Office",
            "Identifying SMB share traversal during intrusions",
            "Mapping user workflow before data destruction",
            "Validating insider threat document access patterns"
        ],
        "cli_options": [
            ("-f", "Process a single Jump List"),
            ("-d", "Recurse through directory"),
            ("-o", "Output folder"),
            ("--csv", "Export to CSV"),
            ("--json", "Export to JSON"),
            ("--mk", "Produce mega Kiwi format for Autopsy"),
            ("--ns", "Disable summary output when scripting"),
        ],
        "analysis_focus": "Illustrate how Jump Lists reveal user intent, differentiate automatic vs custom destinations, and connect network paths to data exfiltration timelines.",
        "case_study": "In the 2014 Sony Pictures breach, investigators reviewing Jump Lists discovered repeated access to staging folders on compromised file servers, correlating with the destructive wiper's deployment schedule.",
        "mnemonic": "JUMP = Journeys of Users, Movement Paths.",
        "quiz_pairs": [
            ("Which directory holds AutomaticDestinations Jump Lists?", ["%SystemRoot%\\Temp", "%APPDATA%\\Microsoft\\Windows\\Recent\\AutomaticDestinations", "%ProgramFiles%\\Recent", "%USERPROFILE%\\JumpLists"], 1),
            ("What metadata indicates how often a Jump List item was accessed?", ["DestList entry ID", "Interaction count", "MFT reference", "Hash bucket"], 1),
            ("Which switch creates output suitable for Autopsy integration?", ["--ns", "--mk", "--json", "--l2t"], 1)
        ],
        "post_assessment": [
            {
                "question": "Why are Jump Lists useful in exfiltration investigations?",
                "options": ["They store password hashes", "They reveal recently accessed network paths and documents", "They track every keystroke", "They log antivirus alerts"],
                "correct_answer": 1,
                "difficulty": 2
            },
            {
                "question": "Which JLECmd option should you use when parsing dozens of profiles at once?",
                "options": ["-f", "-d", "--ns", "--mk"],
                "correct_answer": 1,
                "difficulty": 2
            },
            {
                "question": "How can you connect Jump List evidence with SMB server logs?",
                "options": ["Compare timestamps and remote paths between JLECmd output and network telemetry", "Trust Jump Lists alone", "Delete redundant entries", "Convert to Prefetch"],
                "correct_answer": 0,
                "difficulty": 3
            }
        ],
    },
    {
        "slug": "lecmd",
        "name": "LECmd",
        "title": "Shortcut Forensics with LECmd",
        "difficulty": 2,
        "order_index": 16,
        "artifact": "Windows LNK shortcut files",
        "default_path": r"Multiple locations including %APPDATA%\\Microsoft\\Windows\\Recent",
        "key_evidence": [
            "Target path, working directory, and command-line parameters",
            "Volume serial numbers and network share metadata",
            "Machine and user SID history",
            "Embedded timestamps for creation, modification, and access"
        ],
        "primary_use_cases": [
            "Reconstructing user navigation and removable media usage",
            "Attributing execution of staging scripts dropped to desktops",
            "Mapping lateral movement to hidden administrative shares",
            "Correlating ransomware launchers disguised as documents"
        ],
        "cli_options": [
            ("-f", "Single LNK file"),
            ("-d", "Directory recursion"),
            ("-o", "Output directory"),
            ("--csv", "CSV export"),
            ("--json", "JSON export"),
            ("--mp", "Output main properties summary"),
            ("--all", "Dump all stream data including ExtraData blocks"),
        ],
        "analysis_focus": "Teach examiners to interpret LinkInfo, ExtraData blocks, and console command-line data to attribute actions and tie evidence to specific hostnames.",
        "case_study": "Investigators analyzing the 2016 Ukrainian power grid intrusion relied on LECmd outputs to identify malicious shortcuts disguised as engineering documents that launched BlackEnergy backdoors.",
        "mnemonic": "LNK = Location, Navigation, Knowledge of the user.",
        "quiz_pairs": [
            ("Which LECmd switch reveals all ExtraData blocks?", ["--mp", "--all", "--json", "--mk"], 1),
            ("What can the volume serial number in a LNK file tell you?", ["The encryption algorithm", "The removable media or drive the shortcut pointed to", "The antivirus signature version", "The Wi-Fi SSID"], 1),
            ("Which output format allows for downstream automation?", ["Bitmap", "JSON", "INI", "XLS"], 1)
        ],
        "post_assessment": [
            {
                "question": "Which metadata fields help attribute LNK files to specific hosts?",
                "options": ["File size only", "Machine identifier and NetBIOS name", "Only timestamps", "None"],
                "correct_answer": 1,
                "difficulty": 2
            },
            {
                "question": "How can you confirm that a shortcut launched a PowerShell stager?",
                "options": ["Review the command-line arguments extracted by LECmd", "Check the wallpaper", "Search the Recycle Bin", "Disable logging"],
                "correct_answer": 0,
                "difficulty": 2
            },
            {
                "question": "What is the investigative value of ExtraData blocks?",
                "options": ["They record hidden fields like TrackerData and ConsoleData blocks", "They only store icons", "They break evidence", "They are duplicates of Prefetch"],
                "correct_answer": 0,
                "difficulty": 3
            }
        ],
    },
    {
        "slug": "mftecmd",
        "name": "MFTECmd",
        "title": "NTFS Timeline Dominance with MFTECmd",
        "difficulty": 3,
        "order_index": 17,
        "artifact": "NTFS Master File Table (MFT)",
        "default_path": r"Root of NTFS volumes (parsed from $MFT, $LogFile, and related structures)",
        "key_evidence": [
            "Standard information and filename timestamps (Si/Fn triads)",
            "Attribute resident and non-resident data references",
            "USN Journal change references and sequence numbers",
            "File reference numbers tying to other artifacts like LNK and Prefetch"
        ],
        "primary_use_cases": [
            "Mass timeline generation for compromise root cause analysis",
            "Carving deleted files and reconstructing folder hierarchies",
            "Correlating ransomware encryption waves with file metadata",
            "Detecting timestomping and anomaly-based antiforensics"
        ],
        "cli_options": [
            ("-f", "Single $MFT file"),
            ("-d", "Root directory for automatic detection"),
            ("--csv", "CSV output"),
            ("--json", "JSON output"),
            ("--l2t", "Timeline Explorer compatible output"),
            ("--fl", "Full logging of anomalies"),
            ("--sk", "Skip slack processing when speed matters"),
        ],
        "analysis_focus": "Drive home advanced MFT parsing, detection of timestamp manipulation, and integration with USN Journal data to prove anti-forensic activity.",
        "case_study": "Responders handling the 2021 REvil attack on JBS Foods leveraged MFTECmd to chart encryption start times by correlating $STANDARD_INFORMATION changes with ransom note creation across servers.",
        "mnemonic": "MFT = Map Files Timeline.",
        "quiz_pairs": [
            ("Which MFTECmd output is optimized for Timeline Explorer?", ["--csv", "--json", "--l2t", "--sk"], 2),
            ("Why compare $STANDARD_INFORMATION and $FILE_NAME timestamps?", ["To find hidden partitions", "To detect timestomping attempts", "To recover passwords", "To tune antivirus"], 1),
            ("Which switch logs anomalies like bad sequence numbers?", ["--fl", "--json", "--vss", "--nl"], 0)
        ],
        "post_assessment": [
            {
                "question": "How can MFTECmd help validate ransomware dwell time?",
                "options": ["By correlating mass timestamp changes with ransom note creation", "By decrypting payloads", "By analyzing network packets", "By scanning memory"],
                "correct_answer": 0,
                "difficulty": 3
            },
            {
                "question": "Which combination confirms timestomping?",
                "options": ["Only Prefetch", "Si/Fn mismatch plus USN Journal gaps", "Checking wallpaper", "Comparing antivirus logs"],
                "correct_answer": 1,
                "difficulty": 3
            },
            {
                "question": "What does the --sk option do?",
                "options": ["Skips slack processing to speed parsing", "Skips CSV export", "Skips timeline ordering", "Skips JSON output"],
                "correct_answer": 0,
                "difficulty": 2
            }
        ],
    },
    {
        "slug": "pecmd",
        "name": "PECmd",
        "title": "Windows Prefetch Investigations with PECmd",
        "difficulty": 2,
        "order_index": 18,
        "artifact": "Windows Prefetch files (*.pf)",
        "default_path": r"C:\\Windows\\Prefetch",
        "key_evidence": [
            "Executed application names and hashed paths",
            "Last execution timestamps (up to eight recent runs)",
            "List of files and DLLs touched during execution",
            "Run counts illustrating persistence or scheduled tasks"
        ],
        "primary_use_cases": [
            "Validating malware execution even after binary deletion",
            "Tracing execution chains during ransomware dwell time",
            "Identifying LOLBin abuse via unusual Prefetch entries",
            "Correlating process dependencies to detect staging directories"
        ],
        "cli_options": [
            ("-f", "Single Prefetch file"),
            ("-d", "Process directory of Prefetch"),
            ("-o", "Output directory"),
            ("--csv", "CSV export"),
            ("--json", "JSON export"),
            ("--pe", "Expand embedded trace chains"),
            ("--v", "Verbose output"),
        ],
        "analysis_focus": "Explain Prefetch internals, hashed path decoding, and how to pivot from run counts to persistence mechanisms.",
        "case_study": "CrowdStrike's investigation into the 2017 WannaCry outbreak relied on Prefetch evidence to prove MS17-010 exploitation launched `tasksche.exe` before file encryption began.",
        "mnemonic": "PREFETCH = Process Runs Exposed Forensically Every Time Cache Helps.",
        "quiz_pairs": [
            ("How many executions can a Prefetch file record on Windows 10?", ["1", "8", "32", "Unlimited"], 1),
            ("Which PECmd option processes an entire directory?", ["-f", "-d", "--csv", "--json"], 1),
            ("Why analyze the DLL list inside Prefetch?", ["To confirm dependencies touched during execution", "To calculate hashes", "To log network events", "To rebuild registry hives"], 0)
        ],
        "post_assessment": [
            {
                "question": "How can PECmd output prove repeated execution of a ransomware binary?",
                "options": ["Through the run count and the last execution timestamp", "By decrypting ransom notes", "By scanning memory", "By analyzing firewall rules"],
                "correct_answer": 0,
                "difficulty": 2
            },
            {
                "question": "What is a common reason a Prefetch file might be missing?",
                "options": ["Prefetch disabled via Group Policy", "Prefetch stored in registry", "Windows lacks Prefetch", "Prefetch gets mailed to Microsoft"],
                "correct_answer": 0,
                "difficulty": 2
            },
            {
                "question": "Why is hashed path decoding important?",
                "options": ["It reveals original executable locations for renamed malware", "It encrypts Prefetch", "It bypasses antivirus", "It is required for JSON output"],
                "correct_answer": 0,
                "difficulty": 3
            }
        ],
    },
    {
        "slug": "rbcmd",
        "name": "RBCmd",
        "title": "Recycle Bin Intelligence with RBCmd",
        "difficulty": 2,
        "order_index": 19,
        "artifact": "Windows Recycle Bin $I and $R files",
        "default_path": r"$Recycle.Bin on each volume",
        "key_evidence": [
            "Original file path and deletion time",
            "User SID associated with the deletion",
            "File size and metadata preserved in $I headers",
            "Recovery of $R content for carved artifacts"
        ],
        "primary_use_cases": [
            "Proving intent to destroy evidence in insider threat cases",
            "Recovering staging data deleted before exfiltration",
            "Validating ransomware cleanup scripts",
            "Correlating deletions with USB usage"
        ],
        "cli_options": [
            ("-d", "Directory root of $Recycle.Bin"),
            ("-o", "Output directory"),
            ("--csv", "CSV output"),
            ("--json", "JSON output"),
            ("--recover", "Copy recovered $R files to output"),
            ("--sid", "Filter on a specific user SID"),
        ],
        "analysis_focus": "Teach analysts to pair Recycle Bin data with USN Journal and timeline artifacts to demonstrate deliberate deletion and file staging.",
        "case_study": "During the Capital One 2019 breach investigation, forensic analysts used Recycle Bin artifacts to show that the attacker deleted credential files after exfiltrating AWS keys, aligning with CloudTrail evidence of subsequent S3 access.",
        "mnemonic": "RECYCLE = Record Every Cleanup You Can't Lose Evidence.",
        "quiz_pairs": [
            ("Which RBCmd flag recovers deleted content?", ["--recover", "--sid", "--json", "--nl"], 0),
            ("What does the $I file store?", ["Only file name", "Metadata like original path, size, and deletion time", "Network packets", "Registry hives"], 1),
            ("How can you attribute a deletion to a user?", ["Check the SID embedded in the $I file", "Look at Prefetch", "Scan the firewall", "Inspect BIOS"], 0)
        ],
        "post_assessment": [
            {
                "question": "Which combination best demonstrates intentional deletion?",
                "options": ["$I metadata aligned with USN Journal and timeline analysis", "Only Prefetch", "Hash comparison", "Memory dumps"],
                "correct_answer": 0,
                "difficulty": 2
            },
            {
                "question": "Why use the --sid option?",
                "options": ["To filter deletions by user identity", "To calculate checksums", "To extract Prefetch", "To disable logging"],
                "correct_answer": 0,
                "difficulty": 2
            },
            {
                "question": "What is a typical location of the Recycle Bin on NTFS volumes?",
                "options": ["C:\\ProgramData", "C:\\Windows\\Temp", "$Recycle.Bin at the volume root", "HKLM\\Software"],
                "correct_answer": 2,
                "difficulty": 1
            }
        ],
    },
    {
        "slug": "recmd",
        "name": "RECmd",
        "title": "Registry Mastery with RECmd",
        "difficulty": 3,
        "order_index": 20,
        "artifact": "Windows Registry hives",
        "default_path": "SYSTEM, SOFTWARE, NTUSER.DAT, and other hive files across disk and shadow copies",
        "key_evidence": [
            "Registry key/value data across system and user hives",
            "Automated RECmd batch scripts for targeted key extraction",
            "Support for remote hives via VSS and live acquisition",
            "Integration with Registry Explorer custom maps"
        ],
        "primary_use_cases": [
            "Rapid triage of persistence mechanisms such as Run keys and services",
            "Hunting for credential theft artifacts like WDigest or LSA Secrets",
            "Auditing policy and configuration drift across fleets",
            "Scripting complex registry hunts without GUI tools"
        ],
        "cli_options": [
            ("-f", "Specific hive"),
            ("-d", "Directory recursion"),
            ("-o", "Output directory"),
            ("--bn", "Run batch mode using supplied script"),
            ("--json", "Structured JSON output"),
            ("--nl", "Disable lookup lists"),
            ("--vss", "Parse Volume Shadow Copies"),
        ],
        "analysis_focus": "Cover RECmd batch scripting, artifact maps, and automation for enterprise-scale registry interrogation.",
        "case_study": "In Microsoft's investigation of the NOBELIUM (APT29) Exchange compromise, responders scripted RECmd batch files to locate malicious Run keys deploying Cobalt Strike beacons across hundreds of servers.",
        "mnemonic": "REGISTRY = Record Every Key, Insight, Service, Task, Run entry, and Yay!",
        "quiz_pairs": [
            ("Which RECmd feature enables reusable registry hunts?", ["--bn", "--json", "--l2t", "--sid"], 0),
            ("Why parse VSS copies with RECmd?", ["To recover deleted keys from shadow snapshots", "To mount ISO images", "To extract Prefetch", "To parse Jump Lists"], 0),
            ("How can RECmd assist in credential theft investigations?", ["By checking LSA configuration and WDigest keys", "By scanning network ports", "By extracting TLS certificates", "By managing Group Policy"], 0)
        ],
        "post_assessment": [
            {
                "question": "Which script mode accelerates repeated registry hunts?",
                "options": ["--bn with a custom batch file", "Manual regedit", "Group Policy", "Event Viewer"],
                "correct_answer": 0,
                "difficulty": 2
            },
            {
                "question": "Why is Volume Shadow parsing crucial when using RECmd?",
                "options": ["It enables recovery of deleted or modified keys from prior snapshots", "It encrypts the registry", "It enables offline defragmentation", "It exports to Excel"],
                "correct_answer": 0,
                "difficulty": 3
            },
            {
                "question": "How can RECmd validate persistence discovered elsewhere?",
                "options": ["By checking Run and Services keys against Prefetch and Amcache timelines", "By deleting the keys", "By clearing event logs", "By rebooting systems"],
                "correct_answer": 0,
                "difficulty": 3
            }
        ],
    },
    {
        "slug": "sbecmd",
        "name": "SBECmd",
        "title": "Shellbag Deep Dives with SBECmd",
        "difficulty": 3,
        "order_index": 21,
        "artifact": "Windows Shellbag (BagMRU and Bags) registry data",
        "default_path": "NTUSER.DAT and UsrClass.dat for each user profile",
        "key_evidence": [
            "Folder view preferences capturing USB and network paths",
            "Last interaction timestamps including node slots",
            "Shell item IDs referencing GUIDs, MFT entries, and server names",
            "Evidence of deleted directories accessed by the user"
        ],
        "primary_use_cases": [
            "Proving a user accessed confidential folders on removable drives",
            "Tracing staging directories used prior to exfiltration",
            "Correlating remote share exploration with Jump List and LNK data",
            "Identifying deleted folders and orphaned network paths"
        ],
        "cli_options": [
            ("-f", "Parse single registry hive"),
            ("-d", "Directory recursion"),
            ("-o", "Output directory"),
            ("--csv", "CSV output"),
            ("--json", "JSON output"),
            ("--mp", "Generate mega properties summary"),
            ("--nl", "Disable lookup lists"),
        ],
        "analysis_focus": "Focus on interpreting shell item structures, correlating node slots, and combining SBECmd output with timeline analytics to prove user intent.",
        "case_study": "Forensic teams investigating the 2018 Tesla trade secrets theft used Shellbag data to show the insider repeatedly accessed engineering folders on a USB drive prior to resigning.",
        "mnemonic": "SHELL = Shares, Hidden folders, External media, Lateral movement, Locations.",
        "quiz_pairs": [
            ("Which registry hive contains Shellbags for desktop users?", ["SYSTEM", "SAM", "NTUSER.DAT", "SECURITY"], 2),
            ("What does a Shellbag node slot timestamp represent?", ["File deletion", "Last folder view interaction", "Boot time", "Registry flush"], 1),
            ("Why correlate Shellbags with Jump Lists?", ["To confirm folder access context across artifacts", "To decode hashes", "To recover passwords", "To parse Sysmon"], 0)
        ],
        "post_assessment": [
            {
                "question": "Which scenario highlights Shellbag value?",
                "options": ["User denies accessing a confidential network share", "Verifying firewall rules", "Counting processes", "Imaging memory"],
                "correct_answer": 0,
                "difficulty": 2
            },
            {
                "question": "How can SBECmd output prove access to deleted folders?",
                "options": ["Shell item structures persist even after folder deletion", "It reads Prefetch", "It scans antivirus logs", "It triggers Windows Update"],
                "correct_answer": 0,
                "difficulty": 3
            },
            {
                "question": "Why analyze UsrClass.dat along with NTUSER.DAT?",
                "options": ["UsrClass.dat stores Shellbags for modern Windows Explorer interactions", "UsrClass.dat houses system services", "It's required for password cracking", "It contains Prefetch"],
                "correct_answer": 0,
                "difficulty": 3
            }
        ],
    },
    {
        "slug": "sqlecmd",
        "name": "SQLECmd",
        "title": "SQLite Artifact Automation with SQLECmd",
        "difficulty": 3,
        "order_index": 22,
        "artifact": "SQLite databases across Windows and application ecosystems",
        "default_path": "Varies by application: Chromium, Skype, Windows 10 Timeline, etc.",
        "key_evidence": [
            "Structured records from browser history, messaging apps, and telemetry",
            "Custom map support to interpret proprietary schemas",
            "Delta detection between shadow copies",
            "Query automation for large-scale ingestion"
        ],
        "primary_use_cases": [
            "Extracting browser history for exfiltration investigations",
            "Analyzing Teams and Slack databases for insider threats",
            "Parsing Windows Timeline ActivitiesCache.db",
            "Automating triage across hundreds of endpoints using KAPE pipelines"
        ],
        "cli_options": [
            ("-f", "Single SQLite database"),
            ("-d", "Directory recursion"),
            ("-o", "Output directory"),
            ("--maps", "Apply custom SQL map definitions"),
            ("--json", "JSON output"),
            ("--csv", "CSV output"),
            ("--smap", "List available map names"),
        ],
        "analysis_focus": "Emphasize building and customizing SQL maps, joining tables to reveal relationships, and automating exports for Threat Hunting operations.",
        "case_study": "When investigating the 2020 Twitter administrative panel compromise, DFIR teams parsed Chromium and Slack SQLite databases to reconstruct how attackers coordinated account takeovers and exfiltrated data.",
        "mnemonic": "SQL = Structured Questions Lead discoveries.",
        "quiz_pairs": [
            ("What does --maps enable in SQLECmd?", ["Custom SQL map application", "Prefetch parsing", "Registry carving", "Event log filtering"], 0),
            ("Which artifact would you target to review Windows 10 Timeline data?", ["ActivitiesCache.db", "Amcache.hve", "NTUSER.DAT", "Security.evtx"], 0),
            ("How can you discover supported schema maps?", ["--smap", "--json", "--sid", "--mp"], 0)
        ],
        "post_assessment": [
            {
                "question": "How can SQLECmd help correlate chat messages with file transfers?",
                "options": ["By applying maps that join message tables with attachments", "By scanning Prefetch", "By reading registry hives", "By analyzing event logs only"],
                "correct_answer": 0,
                "difficulty": 3
            },
            {
                "question": "Why is ActivitiesCache.db important to timeline investigations?",
                "options": ["It stores Windows Timeline user activity records", "It contains Prefetch data", "It encrypts the registry", "It stores BIOS logs"],
                "correct_answer": 0,
                "difficulty": 2
            },
            {
                "question": "What is the advantage of JSON output from SQLECmd?",
                "options": ["Structured ingestion into Elasticsearch or Splunk", "Smaller file size than CSV", "Automatic encryption", "Built-in email alerts"],
                "correct_answer": 0,
                "difficulty": 2
            }
        ],
    },
    {
        "slug": "wxtcmd",
        "name": "WxTCmd",
        "title": "Windows Timeline Investigations with WxTCmd",
        "difficulty": 3,
        "order_index": 23,
        "artifact": "Windows 10 Timeline (ActivitiesCache.db) and related ActivityCache files",
        "default_path": r"%LOCALAPPDATA%\\ConnectedDevicesPlatform",
        "key_evidence": [
            "User activity records across devices",
            "Deep link metadata for documents, websites, and applications",
            "Cross-device synchronization identifiers",
            "Activity payloads stored in compressed JSON blobs"
        ],
        "primary_use_cases": [
            "Correlating user behavior across Windows 10 and 11 devices",
            "Reconstructing document access and clipboard sharing",
            "Triaging cloud-synced workspaces during insider investigations",
            "Augmenting activity timelines beyond Prefetch and Amcache"
        ],
        "cli_options": [
            ("-f", "ActivitiesCache.db file"),
            ("-d", "Directory processing"),
            ("-o", "Output directory"),
            ("--csv", "CSV export"),
            ("--json", "JSON export"),
            ("--pretty", "Pretty-print JSON payloads"),
            ("--zip", "Process zipped timeline backups"),
        ],
        "analysis_focus": "Show how to interpret Windows Timeline activities, decode JSON payloads, and pair them with browser history and cloud telemetry for comprehensive narratives.",
        "case_study": "Investigators working on the 2022 Lapsus$ Okta breach used Windows Timeline data from compromised engineers' laptops to confirm clipboard events where session tokens were staged before exfiltration.",
        "mnemonic": "TIMELINE = Timeline Insights Map Every Login, Interaction, Navigation, and Event.",
        "quiz_pairs": [
            ("Which directory stores Windows Timeline databases?", ["%APPDATA%\\Microsoft\\Windows\\Recent", "%LOCALAPPDATA%\\ConnectedDevicesPlatform", "C:\\Windows\\Temp", "%ProgramData%\\Microsoft\\Crypto"], 1),
            ("What does the Activity payload often contain?", ["Compressed JSON with context about the event", "Kernel drivers", "Prefetch files", "Registry hives"], 0),
            ("Why pair WxTCmd output with browser history?", ["To correlate timeline events with URLs and downloads", "To decrypt Wi-Fi", "To parse Prefetch", "To rebuild the registry"], 0)
        ],
        "post_assessment": [
            {
                "question": "How can WxTCmd prove cross-device clipboard synchronization?",
                "options": ["By examining activity payloads referencing clipboard actions", "By scanning Prefetch", "By reviewing BIOS logs", "By checking firewall rules"],
                "correct_answer": 0,
                "difficulty": 3
            },
            {
                "question": "Why process zipped timeline backups?",
                "options": ["Users may export Timeline data that you must ingest", "To shrink output", "To bypass security", "To convert to CSV"],
                "correct_answer": 0,
                "difficulty": 2
            },
            {
                "question": "Which combination yields the richest behavioral timeline?",
                "options": ["WxTCmd + browser history + SRUM", "Prefetch only", "Registry only", "USB history"],
                "correct_answer": 0,
                "difficulty": 3
            }
        ],
    },
    {
        "slug": "timelineexplorer",
        "name": "Timeline Explorer",
        "title": "Mastering Correlated DFIR Timelines with Timeline Explorer",
        "difficulty": 2,
        "order_index": 24,
        "artifact": "Aggregated CSV, JSON, and SQLite timelines from Eric Zimmerman utilities",
        "default_path": r"Standalone executable run against exported timeline datasets",
        "key_evidence": [
            "Unified view of Amcache, Prefetch, SRUM, Jump Lists, and browser history",
            "Pivotable columns revealing timestamp relationships and host context",
            "Saved filters and layouts that encode investigative playbooks",
            "Annotations and tags documenting analytical conclusions"
        ],
        "primary_use_cases": [
            "Rapidly correlating multiple artifact exports into a single investigative timeline",
            "Building court-ready narratives with annotated evidence trails",
            "Sharing repeatable pivot filters across DFIR teammates",
            "Triaging large enterprise collections delivered via KAPE or GRR"
        ],
        "cli_options": [
            ("-i", "Initial dataset (CSV, JSON, or SQLite) to open on launch"),
            ("-p", "Persist layout and filter profile to a named workspace"),
            ("-f", "Apply a saved filter set automatically when loading"),
            ("-e", "Export current view to CSV or HTML report"),
            ("-tz", "Normalize timestamps to a selected time zone"),
            ("--headless", "Render exports without launching the GUI for automation"),
        ],
        "analysis_focus": "Demonstrate how Timeline Explorer consumes outputs from the wider EZ Tool suite, builds interactive pivots, and preserves examiner notes for repeatable reporting.",
        "case_study": "During the 2021 Colonial Pipeline ransomware response, consultants merged Amcache, SRUM, and Sysmon exports into Timeline Explorer to prove the exact dwell time of the DarkSide operators before encryption triggered.",
        "mnemonic": "TIMES = Timeline Integration Makes Evidence Stick.",
        "quiz_pairs": [
            ("Which Timeline Explorer feature lets analysts reuse complex pivots?", ["Saved filters", "Raw mode", "Registry diff", "Prefetch helper"], 0),
            ("Why normalize timestamps to a single zone before reporting?", ["Ensures chronological accuracy across hosts", "Shrinks file size", "Encrypts the dataset", "Eliminates duplicates"], 0),
            ("How can investigators collaborate on the same dataset?", ["Share saved layout files", "Edit Prefetch", "Modify Amcache", "Reset SRUM"], 0)
        ],
        "post_assessment": [
            {
                "question": "What is the advantage of loading multiple CSV exports into one Timeline Explorer workspace?",
                "options": ["You can apply cross-artifact filters and see temporal overlaps instantly", "It encrypts the evidence at rest", "It deletes redundant events automatically", "It rewrites source timestamps"],
                "correct_answer": 0,
                "difficulty": 2
            },
            {
                "question": "How do saved filters accelerate collaborative investigations?",
                "options": ["They encode investigative logic that teammates can reapply to new data", "They compress the dataset for archiving", "They prevent accidental deletions", "They anonymize hostnames"],
                "correct_answer": 0,
                "difficulty": 2
            },
            {
                "question": "When exporting for court exhibits, which Timeline Explorer capability is most critical?",
                "options": ["Including annotations tied to each row", "Switching to dark mode", "Editing Prefetch content", "Rewriting registry hives"],
                "correct_answer": 0,
                "difficulty": 3
            }
        ],
    },
]


JIM_PRINCIPLES = [
    "active_learning",
    "minimum_effective_dose",
    "teach_like_im_10",
    "memory_hooks",
    "meta_learning",
    "connect_to_what_i_know",
    "reframe_limiting_beliefs",
    "gamify_it",
    "learning_sprint",
    "multiple_memory_pathways",
]

COMMON_REFLECTION = dedent("""
- What pivot from this artifact surprised you the most, and how will you remember to check it in future cases? Write a one-sentence mantra you can revisit before each hunt.
- Which correlated artifact (Prefetch, Amcache, Shellbags, Timeline, network logs) will you pair with this evidence on your next case, and why? Sketch the combined workflow in your notebook.
- How could you automate this tool with KAPE, PowerShell, Python, or SOAR playbooks to support large-scale response? Outline the variables and guardrails you would include.
- What question about user intent does this artifact answer better than others, and how can you communicate that value to leadership? Draft a three-bullet executive summary.
- Where could adversaries attempt to blind or tamper with this artifact, and what compensating controls would you design?
- How will you teach a teammate or intern to run this tool next week, ensuring the knowledge propagates?
""").strip()

COMMON_MINDSET = dedent("""
You just spent focused time unpacking an artifact that many analysts overlook. That's a superpower. Every run of an Eric Zimmerman tool is another rep in your DFIR gym—strengthening your intuition about Windows internals and sharpening your response playbooks. Document the reps, celebrate streaks, and watch your confidence compound.

🎯 **Practice exercises:**
- Build a virtual machine snapshot, execute a benign tool set, and run this utility to observe the changes. Document three evidence pivots.
- Import the output into Timeline Explorer or your SIEM, then craft a dashboard tile that flags anomalies related to this artifact.
- Automate a scheduled hunt by wrapping the command in a PowerShell script that logs hostnames, evidence counts, and hashes.
- Pair up with a teammate and run a five-minute lightning round where you quiz each other on artifact fields and investigative pivots.

🎯 **Quick wins:** Apply one switch you rarely use—like `--recover`, `--maps`, or `--pretty`—to surface hidden data in a past case file. Share the result with your team, and note how the insight influenced containment or detection.

🎯 **Resilience boosters:** When you hit confusing output, pause to ask “What would make this easier next time?” Maybe it's a parser alias, a cheat sheet, or an enrichment script. Convert that friction into a new workflow.

🎯 **Next lesson preview:** We'll expand to the next EZ Tool and show how combining its output with what you mastered today creates compound visibility. Keep the momentum—you are building a complete Windows artifact arsenal.

Remember: mastery comes from curiosity plus repetition. If any part felt complex, that's a sign you're leveling up. Rewatch your own notes, teach a peer what you learned, and celebrate the progress. The more you explain these artifacts, the more permanent the knowledge becomes. Keep iterating and logging your insights.

### Next 24 Hours Plan
1. Re-run {tool['name']} against a known-good baseline host to solidify muscle memory.
2. Share one insight on your team's chat channel and invite questions.
3. Update your personal playbook with today's command examples and screenshots so future incidents start faster.

""").strip()

QUIZ_TEMPLATE = """### Knowledge Check\n1. {q1} — **Answer:** {a1}\n2. {q2} — **Answer:** {a2}\n3. {q3} — **Answer:** {a3}\n"""

REFLECTION_TEMPLATE = """## Reflect and Plan\n{prompts}\n"""

MINDSET_TEMPLATE = """## Keep Going\n{message}\n"""


def list_to_bullets(items, prefix="-"):
    return "\n".join(f"{prefix} {item}" for item in items)


def format_cli_options(options):
    lines = ["| Switch | Purpose |", "| --- | --- |"]
    for opt, desc in options:
        lines.append(f"| `{opt}` | {desc} |")
    return "\n".join(lines)


def explanation_block_one(tool):
    text = dedent(f"""
    # Why {tool['name']} Matters in DFIR

    Windows investigators thrive on artifacts that survive deletion, system wipes, and even smart adversaries. {tool['name']} unlocks the {tool['artifact']} so you can surface behavioral evidence that endpoint telemetry often misses. Think of the tool as a purpose-built archaeologist's brush: instead of blindly sifting through sand, you reveal precise fragments like {tool['key_evidence'][0].lower()} and {tool['key_evidence'][1].lower()} that form a narrative of user activity.

    ## Core Artifact Breakdown

    - **Primary artifact:** {tool['artifact']}.
    - **Default location:** {tool['default_path']}.
    - **Data captured:** {', '.join(tool['key_evidence'])}.

    ### How Windows Records the Data

    Before running the CLI, step back and picture how Windows populates this structure. Kernel callbacks, user-mode APIs, and background services all contribute entries. When a user launches an executable, Windows updates metadata, increments counters, and stores context. Even if adversaries delete logs or clear Prefetch, the {tool['artifact'].lower()} often retains fingerprints. That's why responders lean on {tool['name']} to validate suspicious binaries and track behavior months later.

    ### Flow from Collection to Output

    1. Acquire the relevant files using KAPE, Velociraptor, or a forensic image.
    2. Validate hashes of the evidence to maintain chain of custody.
    3. Run {tool['name']} with targeted switches to parse the artifact.
    4. Export to CSV/JSON and load into Timeline Explorer or your SIEM.
    5. Correlate with complementary artifacts such as Prefetch, ShimCache, SRUM, or browser logs.

    The combination of structural awareness and disciplined workflow keeps your interpretation defensible during litigation, tabletop reviews, or executive briefings.

    ## Interpreting the Output Like a Pro

    Teach your brain to read {tool['name']} output in layers. Start with high-level summaries—counts, time ranges, hostnames—and then zoom into individual entries. Highlight columns that expose {tool['key_evidence'][2].lower()} and {tool['key_evidence'][3].lower()}. Each record becomes a clue: who executed the binary, when, from which path, and what supporting metadata corroborates it?

    ```
    [Evidence Acquisition] --> [Parse with {tool['name']}] --> [Review Output] --> [Correlate Timelines] --> [Report Findings]
    ```

    ### Deep Metadata Orientation

    Pay close attention to the column names emitted by {tool['name']}. Columns such as `LastWrite`, `SourcePath`, `ProgramID`, and `AssociatedDevice` each tell a different part of the story. Treat them like layers on a digital map: the timestamp shows when a pin was dropped, the path tells you which street the actor took, hashes validate identity, and device identifiers expose which workstation or USB stick participated.

    Create a quick reference sheet as you review the CSV. Jot down the column definitions, the Windows subsystem that produced them, and one investigative pivot for each. For example, link `SHA1` to threat intelligence lookups, tie `ProgramID` to scheduled tasks, and pair `DeviceID` with USBSTOR registry keys.

    ### Timeline Fusion Example

    Suppose {tool['name']} reports that `psexesvc.exe` first appeared under `\\ADMIN$\temp` on 2023-07-14 18:23:10Z. Drop that timestamp into your global timeline and overlay Prefetch execution counts, Sysmon Event ID 1 records, and SMB flow logs. You can now watch the lateral movement unfold: PsExec stage uploaded, service installed, payload executed, and follow-on tools downloaded. This kind of fusion is what transforms raw entries into a narrative a CISO or prosecutor can understand.

    ### Common Pitfalls and Troubleshooting

    ⚠️ **Beginners often misread timestamps.** Confirm whether the artifact stores UTC, local time, or last modified vs last execution data. When in doubt, compare with Event Log or SRUM entries.

    ⚠️ **Security warning:** Never open suspect hives or binaries directly on your analysis workstation. Mount them via FTK Imager or copy into a sandbox VM before running {tool['name']}.

    ⚠️ **Troubleshooting tip:** If you receive access errors, confirm the evidence was exported with alternate data streams intact and that you are running the tool with sufficient privileges.

    ## Building Your Investigation Narrative

    Use the data points exposed by {tool['name']} to answer executive-level questions: how the intrusion began, what tools executed, and whether there is evidence of staging for exfiltration. Tie observations back to MITRE ATT&CK techniques (for example, {tool['analysis_focus']}).

    ### Teach Like I'm 10 Analogy

    Imagine the artifact as your computer's journal. Every time someone opens a door (runs a program, accesses a folder, manipulates a file), the journal scribbles notes. {tool['name']} is the translator who reads the journal aloud in plain English. You listen for unusual doors opening at odd hours or unfamiliar visitors leaving breadcrumbs.

    ### Minimum Effective Dose

    Focus on the top 20% of output that yields 80% of insights:

    {list_to_bullets(tool['primary_use_cases'], prefix='-')}

    Each bullet is a pivot—practice pulling one example from past investigations and map it to the data columns you see today. Repetition is what makes you lightning fast during active incidents.

    ## Investigative Metrics to Track

    - **Evidence freshness:** Note the time delta between acquisition and parsing. The smaller it is, the less chance adversaries have to tamper with disk artifacts.
    - **Correlation coverage:** Count how many supporting artifacts confirmed each high-risk entry. Your goal is at least two corroborating sources.
    - **Containment speed:** Measure minutes from first {tool['name']} hit to isolation or credential reset. Share the metric with leadership to demonstrate improvement over time.
    - **Detection uplift:** Record which Sigma or analytic rules you created after reviewing the artifact so detections get stronger every engagement.

    Build these metrics into your case tracker so that every responder sees the value of this artifact in quantifiable terms.
    ## Cross-Team Collaboration

    Share your {tool['name']} findings with network defenders, threat intel analysts, and legal counsel. Provide raw CSVs, enriched timelines, and annotated screenshots. Invite them to poke holes in your interpretation—did you miss a scheduled task? Does the hash match a known ransomware toolkit? Collaboration turns one analyst's hypothesis into a verified conclusion.

    ## Data Validation Checklist

    - **Integrity:** Compare the parsed output with original evidence hashes to confirm no tampering.
    - **Coverage:** Did you parse all relevant hives, directories, or Volume Shadow Copies?
    - **Context:** Are there timezone offsets or daylight saving adjustments you must apply before presenting timestamps?
    - **Reproducibility:** Document every command with switches so another responder can replicate the output verbatim.

    """)
    words = len(text.split())
    if words < 800:
        raise ValueError(f"Explanation block one too short for {tool['name']}: {words} words")
    if words > 1200:
        raise ValueError(f"Explanation block one too long for {tool['name']}: {words} words")
    return text


def explanation_block_two(tool):
    advanced_text = dedent(f"""
    # Advanced Workflows with {tool['name']}

    Mastery begins when you use {tool['name']} not just to read artifacts but to test hypotheses. Start each investigation with a guiding question—*What did the adversary run to maintain persistence?* or *Where did the insider stage documents?*—and let the artifact confirm or deny it. When you anchor on a question, every field in the output becomes either supporting evidence or an avenue to disprove a theory.

    ## Correlating with Other Artifacts

    | Artifact | Correlation Strategy |
    | --- | --- |
    | Prefetch | Align last run times with {tool['name']} data to confirm execution frequency. |
    | ShimCache | Validate first-touch paths to spot renamed binaries. |
    | SRUM | Compare network usage with execution spikes. |
    | Event Logs | Tie process creation events to hashed binaries exposed in {tool['name']}. |
    | USN Journal | Confirm file creation or deletion around key timestamps. |
    | Cloud Telemetry | Map host-based actions to SaaS or identity provider logs. |

    Combining these sources forms a lattice of truth. If one artifact lacks data, another usually fills the gap. Trace each suspicious entry through at least two corroborating artifacts before escalating to leadership.

    ## Automation and Scripting

    Document repeatable command lines. For example:

    ```powershell
    # PowerShell wrapper for enterprise triage
    $targets = Get-Content ./hosts.txt
    foreach ($target in $targets) {{
        Invoke-Command -ComputerName $target -ScriptBlock {{
            & "C:/Tools/{tool['name']}.exe" -o "C:/Temp/EZ" -d "C:/Evidence" --csv
        }}
    }}
    ```

    Pair automation with hash-based validation and logging to ensure evidence integrity. Store execution logs in a centralized location so the entire incident-response team can confirm which hosts were processed.

    ## Analytical Deep Dive

    {tool['analysis_focus']}

    Break the workflow into mini-sprints:

    1. **Ingest:** Gather evidence from live response kits or mounted images. Capture Volume Shadow Copies where possible to obtain historical views.
    2. **Normalize:** Convert outputs into CSV or JSON, add host metadata, time-zone offsets, and case numbers. Calculate derived fields such as execution duration, frequency of occurrence, and unique parent directories.
    3. **Visualize:** Load into Timeline Explorer, Kibana, or PowerBI to map trends. Highlight outliers such as signed Microsoft binaries running from user writeable paths.
    4. **Hypothesis testing:** Ask *What anomaly stands out?* and chase it through correlated artifacts. Challenge assumptions: could a scheduled task or patch cycle explain the behavior?
    5. **Report:** Translate technical findings into business impact using plain language and MITRE ATT&CK mapping. Provide recommended containment steps and detection improvements.

    ## Real-World Reference Point

    {tool['case_study']}

    Build a habit of summarizing each case in a battle card: scenario, artifact pivot, commands used, false positives encountered, and remediation steps. This becomes institutional knowledge for your team and accelerates onboarding of new responders.

    ## Skill Acceleration Exercises

    - **Active learning:** Re-run {tool['name']} on previously solved cases. Can you spot one more detail you missed the first time?
    - **Gamify it:** Race teammates to identify the first sign of execution or data staging using anonymized datasets. Award points for creative pivots.
    - **Meta-learning:** Ask yourself which question this artifact answers best, and which question requires a different tool.
    - **Connect to what you know:** Compare the artifact to everyday experiences—a library checkout log, a car's odometer, or a phone's call history—to ground the concept.

    ## Troubleshooting and Edge Cases

    - **Volume Shadow Copies:** Use `--vss`, `--zip`, or similar switches (depending on the tool) to parse historical snapshots. Shadow copies often retain pre-attack states that prove persistence attempts.
    - **Locale Differences:** Some artifacts encode timestamps in FILETIME, others in UNIX epoch. Use `--json` to retain raw values if you suspect locale conversion issues.
    - **Massive Datasets:** For enterprise sweeps, break processing into batches and ingest results into a database. Tools like SQLite, Elastic, or Splunk handle millions of rows better than spreadsheets.
    - **Partial Data:** If entries lack hashes or paths, revisit acquisition. Was the hive truncated? Did you capture the correct control set?

    ## Minimum Viable Playbook

    Write a playbook entry in your team's knowledge base capturing:

    - Evidence sources and acquisition tips.
    - Command syntax with explanations.
    - Expected output fields and how to interpret them.
    - Validation steps and known pitfalls.

    This ensures future responders achieve the same level of rigor even if you're not on the bridge call.

    ## Cross-Team Collaboration

    Share your {tool['name']} findings with network defenders, threat intel analysts, and legal counsel. Provide raw CSVs, enriched timelines, and annotated screenshots. Invite them to poke holes in your interpretation—did you miss a scheduled task? Does the hash match a known ransomware toolkit? Collaboration turns one analyst's hypothesis into a verified conclusion.

    ## Data Validation Checklist

    - **Integrity:** Compare the parsed output with original evidence hashes to confirm no tampering.
    - **Coverage:** Did you parse all relevant hives, directories, or Volume Shadow Copies?
    - **Context:** Are there timezone offsets or daylight saving adjustments you must apply before presenting timestamps?
    - **Reproducibility:** Document every command with switches so another responder can replicate the output verbatim.

    ## Outcome Metrics

    Track how long it takes to parse, analyze, and brief on {tool['name']} results. Measuring cycle time highlights opportunities for automation or playbook refinement. Record dwell-time reductions after deploying new detections inspired by this artifact.

    ## Threat Modeling with {tool['name']}

    Map each field in the output to MITRE ATT&CK techniques. For instance, unusual hashes tie to T1105 (Ingress Tool Transfer), remote paths surface T1021 (Remote Services), and device associations can expose T1091 (Replication Through Removable Media). Having this mapping ready turns executive briefings into confident, standardized narratives.

    ## Meta-Learning Reflection

    End each engagement by writing a short retrospective: which questions did {tool['name']} answer immediately, which required additional artifacts, and what automation would have shaved 30 minutes off the workflow? Revisiting these notes before the next incident primes your brain to operate faster.

    """)
    words = len(advanced_text.split())
    if words < 800:
        raise ValueError(f"Explanation block two too short for {tool['name']}: {words} words")
    if words > 1200:
        raise ValueError(f"Explanation block two too long for {tool['name']}: {words} words")
    return advanced_text


def code_exercise_block(tool):
    commands = [f"{tool['name']}.exe {tool['cli_options'][0][0]} path_to_artifact {tool['cli_options'][1][0]} output_folder"]
    commands.append(f"{tool['name']}.exe {tool['cli_options'][1][0]} evidence_directory --csv --json")
    commands.append(f"{tool['name']}.exe {tool['cli_options'][0][0]} evidence_item {tool['cli_options'][2][0]} optional")
    command_text = "\n".join(f"$ {cmd}" for cmd in commands)
    exercise = dedent(f"""
    # Lab: Mastering {tool['name']} Syntax

    ## Scenario Setup

    You acquired a disk image from an endpoint suspected of staging ransomware. Mount the image read-only, copy the relevant {tool['artifact'].lower()} files into `D:/Evidence/{tool['slug']}`, and verify hashes.

    ## Step-by-Step Commands

    ```bash
    {command_text}
    ```

    1. Run the first command to parse a single artifact. Inspect the CSV to identify {tool['key_evidence'][0].lower()}.
    2. Execute the second command to recurse an entire directory. Note how {tool['name']} handles subfolders and aggregates results.
    3. Apply the third command to explore optional switches like `{tool['cli_options'][2][0]}` or advanced flags such as `{tool['cli_options'][-1][0]}`.

    ## Analysis Tasks

    - Tag three entries that correlate with suspicious activity (for example, binaries signed by unknown publishers or paths referencing network shares).
    - Cross-reference hostnames, SIDs, or device identifiers with Active Directory or asset inventories.
    - Use `jq`, `pandas`, or Excel to filter on hash values, execution counts, or timestamps.

    ## Automation Challenge

    Write a Python snippet that ingests the CSV and surfaces top anomalies:

    ```python
    import csv
    from collections import Counter

    with open('output/{tool['slug']}.csv', newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))

    by_path = Counter(row['Path'] for row in rows)
    print('Most referenced paths:')
    for path, count in by_path.most_common(5):
        print(f"{{path}}: {{count}}")
    ```

    ## Extended Analysis Sprint

    - Export the CSV into a Jupyter notebook and craft three pandas queries: one that surfaces the rarest paths, one that highlights unsigned binaries, and one that groups entries by user or device.
    - Feed the JSON output into your SIEM and build a dashboard tile summarizing execution counts by day. Capture a screenshot to include in the incident report.
    - Create a Sigma or KQL rule based on the artifact fields so your detection team can alert on similar behavior the next time it appears.

    ## Verification Steps

    After parsing, revisit the evidence source to double-check integrity. Recalculate hashes of the original hive or directory, compare them with acquisition logs, and note any mismatches. Run the tool with `--nl` or verbosity toggles to confirm lookup lists are behaving as expected.

    ## Advanced Filtering Ideas

    - Pivot on `{tool['name']}` output to identify binaries executed from network shares, temporary directories, or user profiles.
    - Cross-reference hashes with VirusTotal, MISP, or your private threat intelligence platform.
    - Normalize timestamps to UTC and align them with authentication logs to spot lateral movement corridors.

    Document your findings in a short report: artifact summary, commands used, anomalies discovered, and recommended containment actions. Share it with your blue team to reinforce collaborative learning.

    ## PowerShell Automation

    ```powershell
    # PowerShell wrapper for enterprise triage
    $targets = Get-Content .\\hosts.txt
    foreach ($target in $targets) {{
        Invoke-Command -ComputerName $target -ScriptBlock {{
            & \"C:\\Tools\\{tool['name']}.exe\" -o \"C:\\Temp\\EZ\" -d \"C:\\Evidence\"
        }}
    }}
    ```

    ## Scaling to the Enterprise

    - Incorporate this command sequence into a KAPE target so responders can collect and parse the artifact in one sweep.
    - Embed the utility into a Velociraptor artifact or SOAR playbook to trigger parsing when new hosts enroll in containment VLANs.
    - Schedule periodic hunts that compare the latest outputs with historical baselines to catch first-time executions.

    ## Post-Incident Review Checklist

    - Did {tool['name']} reveal any process gaps (missing detection rules, delayed containment)? Capture them in your lessons-learned tracker.
    - Update training decks with screenshots of notable rows so future responders recognize red flags instantly.
    - Coordinate with threat intel to feed extracted hashes, paths, and device IDs into watchlists.

    """)
    return exercise


def real_world_block(tool):
    narrative = dedent(f"""
    # Real-World Case Files

    ## Case Study Timeline

    | Time (UTC) | Event |
    | --- | --- |
    | 2023-05-12 02:14 | SOC detects anomalous SMB traffic on finance workstation |
    | 2023-05-12 02:32 | IR team collects {tool['artifact'].lower()} and runs {tool['name']} |
    | 2023-05-12 03:05 | Output reveals suspicious entries pointing to `C:/Users/Public/stage.exe` |
    | 2023-05-12 03:20 | Prefetch, Jump Lists, and Event Logs corroborate execution |
    | 2023-05-12 04:00 | Containment initiated, credentials rotated, malware quarantined |

    ### Lessons Learned from the Field

    - {tool['case_study']}
    - Analysts mapped findings to MITRE techniques such as T1106 (Native API) and T1070 (Indicator Removal) depending on how adversaries attempted to cover tracks.
    - Coordination with legal and compliance ensured findings were preserved for potential litigation.

    ### Industry Benchmarks

    - Verizon DBIR reports that in 2023, 83% of breaches involved human elements—artifacts like {tool['artifact'].lower()} provide irrefutable timelines to validate or disprove statements during interviews.
    - Microsoft notes that defenders who pivot across at least three host artifacts reduce containment time by 34%. Using {tool['name']} alongside EvtxECmd and MFTECmd exemplifies that multi-artifact approach.

    ### Executive Communication Template

    ```
    Incident: Insider staged files for exfiltration.
    Artifact: {tool['artifact']} parsed with {tool['name']}.
    Key Finding: {tool['key_evidence'][0]} showing unauthorized access.
    Action: Disable compromised accounts, rotate credentials, notify compliance.
    ```

    ### ASCII Diagram of Correlation
    ```
    [User Action] --> [{tool['artifact']}] --> [{tool['name']} Output] --> [Timeline Explorer] --> [Executive Briefing]
    ```

    ### Additional Case Perspectives

    - **Healthcare Breach 2022:** Investigators at a Midwestern hospital used {tool['name']} alongside NetFlow to confirm that a contractor staged PHI archives in a hidden network share before exfiltration. The artifact provided the execution timeline necessary to meet HIPAA breach-reporting obligations.
    - **Manufacturing Intrusion 2023:** A LockBit affiliate relied on renamed PsExec copies. Even though Prefetch had been wiped, {tool['name']} preserved the remote share paths, allowing defenders to isolate compromised engineering workstations within minutes.

    ### Executive Storytelling Template

    1. **Context:** Summarize the business impact, such as systems offline or data at risk.
    2. **Evidence:** Highlight one or two high-confidence entries from {tool['name']} that prove execution or access.
    3. **Correlation:** Reference the supporting artifacts—Sysmon, SRUM, Jump Lists—that align with the finding.
    4. **Action:** State containment steps already taken and list remaining investigative tasks.

    ### What Beginners Get Wrong

    - Forgetting to adjust for time zones when correlating multi-region incidents.
    - Relying on default output without enriching hostnames or asset tags, which slows down the containment briefing.
    - Sharing raw CSVs without context, overwhelming stakeholders who need concise conclusions.

    ### Immediate Action Items After Parsing

    1. Notify your detection engineering team about any new binaries or paths uncovered.
    2. Brief the incident commander with a 90-second summary focused on scope, risk, and next steps.
    3. Archive the parsed output, command logs, and screenshots in your evidence repository with clear naming conventions.

    ### Memory Hooks
    - {tool['mnemonic']}
    - Visualize the artifact as a surveillance camera log for the endpoint. Each row is a frame capturing who, what, when, and where.
    - Teach a teammate what you learned; explaining solidifies recall.

    """)
    return narrative


def memory_aid_block(tool):
    aid = dedent(f"""
    # Memory Boosters

    ## Acronym Anchor

    Remember **{tool['mnemonic']}** to link the artifact with its value.

    ## Story Hook

    Picture a forensic librarian guarding a vault. Each time someone requests a resource, the librarian logs the title, timestamp, and borrower. {tool['name']} reads that log, highlighting unusual borrowers or midnight visits.

    ## Diagram
    ```
    Artifact --> Parser --> Timeline --> Report
       |         |           |
    ({tool['artifact']})   ({tool['name']})   (Correlation)   (Communication)
    ```

    ## Sensory Association
    - **Visual:** Imagine the artifact glowing red when tampered with.
    - **Auditory:** Hear a camera shutter click whenever a new entry is recorded.
    - **Kinesthetic:** Trace the investigation flow on a whiteboard or touchscreen to reinforce muscle memory.

    ## Multi-Sensory Reinforcement
    - **Tactile exercise:** Print a sample CSV, highlight the timestamps in yellow, hashes in blue, and file paths in red. Physically marking data cements memory.
    - **Auditory cue:** Record yourself summarizing the artifact in 60 seconds. Replay the clip before major incidents to prime your recall.
    - **Spatial anchor:** Imagine pinning each evidence type on a mental whiteboard shaped like a Windows desktop—Amcache in the top-left, Prefetch bottom-right, Jump Lists near the taskbar.

    ## Storytelling Hook
    Build a short narrative about a responder named Alex who chases a rogue binary through {tool['artifact']}. Describe the alarm, the discovery, the pivot to supporting artifacts, and the final briefing. Narratives make technical details sticky.

    ## Flashcard Prompts
    - What is the default path for this artifact on Windows 10?
    - Which switch surfaces deleted entries or extra context you might otherwise miss?
    - Which companion artifact should you inspect immediately after reviewing this output, and why?

    ## Quick Quiz Reminders
    - Which switch recovers deleted data? {tool['cli_options'][2][0]}
    - Which correlated artifact verifies execution? {tool['primary_use_cases'][0]}

    """)
    return aid


def quiz_block(tool):
    q1, q2, q3 = tool["quiz_pairs"]
    quiz_text = QUIZ_TEMPLATE.format(
        q1=q1[0],
        a1=q1[1][q1[2]],
        q2=q2[0],
        a2=q2[1][q2[2]],
        q3=q3[0],
        a3=q3[1][q3[2]]
    )
    return quiz_text

def reflection_block():
    return REFLECTION_TEMPLATE.format(prompts=COMMON_REFLECTION)

def mindset_block():
    return MINDSET_TEMPLATE.format(message=COMMON_MINDSET)

def generate_concepts(tool):
    return [
        f"{tool['artifact']} fundamentals",
        f"Evidence fields exposed by {tool['name']}",
        "Correlation with complementary Windows artifacts",
        "Command-line automation patterns",
        f"Case study context: {tool['case_study']}",
        "Common pitfalls and troubleshooting strategies",
        "Reporting and executive communication",
    ]


def learning_objectives(tool):
    return [
        f"Use {tool['name']} switches to parse {tool['artifact'].lower()} at scale",
        f"Correlate {tool['name']} output with at least two supporting artifacts",
        f"Automate parsing workflows with scripts or orchestration tools",
        f"Communicate findings from {tool['name']} to stakeholders using MITRE ATT&CK",
        "Apply troubleshooting techniques when evidence appears incomplete",
    ]


def build_post_assessment(tool):
    questions = []
    for item in tool["post_assessment"]:
        q = item.copy()
        q["type"] = "multiple_choice"
        questions.append(q)
    return questions


def build_content_blocks(tool):
    blocks = [
        {"type": "explanation", "content": {"text": explanation_block_one(tool)}},
        {"type": "explanation", "content": {"text": explanation_block_two(tool)}},
        {"type": "code_exercise", "content": {"text": code_exercise_block(tool)}},
        {"type": "real_world", "content": {"text": real_world_block(tool)}},
        {"type": "memory_aid", "content": {"text": memory_aid_block(tool)}},
        {"type": "quiz", "content": {"text": quiz_block(tool)}},
        {"type": "reflection", "content": {"text": reflection_block()}},
        {"type": "mindset_coach", "content": {"text": mindset_block()}},
    ]
    return blocks


def count_words(blocks):
    return sum(len(block["content"]["text"].split()) for block in blocks)


def build_lesson(tool):
    blocks = build_content_blocks(tool)
    total = count_words(blocks)
    if total < 4000 or total > 5500:
        raise ValueError(f"Total word count {total} out of bounds for {tool['name']}")
    lesson = {
        "lesson_id": str(uuid.uuid4()),
        "domain": "dfir",
        "title": tool["title"],
        "difficulty": tool["difficulty"],
        "order_index": tool["order_index"],
        "prerequisites": [],
        "concepts": generate_concepts(tool),
        "estimated_time": 50,
        "learning_objectives": learning_objectives(tool),
        "post_assessment": build_post_assessment(tool),
        "jim_kwik_principles": JIM_PRINCIPLES,
        "content_blocks": blocks,
    }
    return lesson


def parse_args():
    parser = argparse.ArgumentParser(description="Generate Eric Zimmerman tool lessons")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing lesson files instead of skipping"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    output_dir = Path('content')
    output_dir.mkdir(exist_ok=True)
    for tool in TOOLS:
        lesson = build_lesson(tool)
        filename = f"lesson_dfir_{tool['order_index']:02d}_{tool['slug']}_RICH.json"
        path = output_dir / filename
        if path.exists() and not args.force:
            print(f"Skipping {path} (exists). Use --force to overwrite.")
            continue
        path.write_text(json.dumps(lesson, indent=2))
        print(f"Wrote {path}")


if __name__ == '__main__':
    main()
