"""
Git status utilities for checking repository update status.
"""

import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
import json


class GitStatus:
    """Utility class for git operations"""

    def __init__(self):
        self.git_info_file = Path('.git_info.json')

    def get_last_pull_time(self) -> Optional[datetime]:
        """Get timestamp of last git pull"""
        try:
            if self.git_info_file.exists():
                with open(self.git_info_file, 'r') as f:
                    data = json.load(f)
                    return datetime.fromisoformat(data.get('last_pull', ''))
        except:
            pass
        return None

    def update_pull_time(self):
        """Update the last pull timestamp"""
        try:
            data = {'last_pull': datetime.now().isoformat()}
            with open(self.git_info_file, 'w') as f:
                json.dump(data, f)
        except:
            pass

    def check_for_updates(self) -> Dict:
        """
        Check if there are updates available on remote.
        Returns dict with: {
            'has_updates': bool,
            'local_commit': str,
            'remote_commit': str,
            'behind_by': int,
            'error': Optional[str]
        }
        """
        result = {
            'has_updates': False,
            'local_commit': '',
            'remote_commit': '',
            'behind_by': 0,
            'error': None
        }

        try:
            # Get current branch
            branch_result = subprocess.run(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                capture_output=True,
                text=True,
                timeout=5
            )

            if branch_result.returncode != 0:
                result['error'] = 'Not a git repository'
                return result

            branch = branch_result.stdout.strip()

            # Get local commit
            local_result = subprocess.run(
                ['git', 'rev-parse', 'HEAD'],
                capture_output=True,
                text=True,
                timeout=5
            )
            result['local_commit'] = local_result.stdout.strip()[:7]

            # Fetch remote (without pulling)
            subprocess.run(
                ['git', 'fetch', 'origin', branch],
                capture_output=True,
                timeout=10
            )

            # Get remote commit
            remote_result = subprocess.run(
                ['git', 'rev-parse', f'origin/{branch}'],
                capture_output=True,
                text=True,
                timeout=5
            )
            result['remote_commit'] = remote_result.stdout.strip()[:7]

            # Check how many commits behind
            behind_result = subprocess.run(
                ['git', 'rev-list', '--count', f'HEAD..origin/{branch}'],
                capture_output=True,
                text=True,
                timeout=5
            )

            if behind_result.returncode == 0:
                behind_count = int(behind_result.stdout.strip())
                result['behind_by'] = behind_count
                result['has_updates'] = behind_count > 0

        except subprocess.TimeoutExpired:
            result['error'] = 'Git command timeout'
        except Exception as e:
            result['error'] = str(e)

        return result

    def get_last_commit_info(self) -> Dict:
        """Get information about the last local commit"""
        try:
            # Get commit hash
            hash_result = subprocess.run(
                ['git', 'rev-parse', '--short', 'HEAD'],
                capture_output=True,
                text=True,
                timeout=5
            )

            # Get commit date
            date_result = subprocess.run(
                ['git', 'log', '-1', '--format=%ci'],
                capture_output=True,
                text=True,
                timeout=5
            )

            # Get commit message
            msg_result = subprocess.run(
                ['git', 'log', '-1', '--format=%s'],
                capture_output=True,
                text=True,
                timeout=5
            )

            return {
                'hash': hash_result.stdout.strip(),
                'date': date_result.stdout.strip(),
                'message': msg_result.stdout.strip()
            }
        except:
            return {
                'hash': 'unknown',
                'date': 'unknown',
                'message': 'Could not retrieve commit info'
            }
