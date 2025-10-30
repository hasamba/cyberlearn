#!/bin/bash
# Run this once on dev machine to mark shell scripts as executable
# Git will remember the executable bit and preserve it when pushing/pulling

echo "Setting executable permissions on shell scripts..."

chmod +x setup.sh
chmod +x start.sh
chmod +x update_vm.sh
chmod +x pull_fresh.sh
chmod +x set_executable_permissions.sh

echo ""
echo "✓ Executable permissions set for:"
echo "  - setup.sh"
echo "  - start.sh"
echo "  - update_vm.sh"
echo "  - pull_fresh.sh"
echo "  - set_executable_permissions.sh"

echo ""
echo "Now commit these changes:"
echo "  git add setup.sh start.sh update_vm.sh pull_fresh.sh set_executable_permissions.sh"
echo "  git commit -m \"Set executable permissions on shell scripts\""
echo "  git push"

echo ""
echo "After pushing, these scripts will be executable on VM after git pull!"
