# GitHub Mirror: agentic-framework-mirror

This repository is a mirror of the original Gitea repository: [https://gitea.deepcredit.ai/tvi/agentic-framework.git](https://gitea.deepcredit.ai/tvi/agentic-framework.git)

## 📦 Initial Setup

Clone the Gitea repository and add GitHub as a remote:

```bash
git clone https://gitea.deepcredit.ai/tvi/agentic-framework.git
cd agentic-framework
git remote add github git@github.com:v-dc/agentic-framework-mirror.git
```

## 🚀 Push Full Mirror to GitHub

```bash
git push github --mirror
```

## 🔄 Update GitHub Mirror (Repeat When Needed)

```bash
git fetch origin --prune
git push github --mirror
```

## 🔐 Notes

Ensure the SSH key from the server is added to your GitHub account and that `~/.ssh/config` has the correct entry for GitHub:

```ssh
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/tux
  IdentitiesOnly yes
```

