---
name: project-continuity-check
description: >-
  Use this BEFORE starting substantial work in any git repository or new project idea — at the
  start of a session, whenever the user mentions starting/creating/resuming a project or repo, or
  whenever it's unclear if related prior work exists. Applies equally when this session has direct
  access to the user's own local PC, not just cloud git sessions — unpushed local work forks from
  the shared GitHub state exactly like a stray cloud branch does. Trigger even without an explicit
  ask: "let's start a new project for X", "create a repo for Y", "leg mir ein neues Projekt an",
  opening an unfamiliar repo, opening a repo on the user's local machine, or picking up a task that
  might already exist elsewhere. Skipping this causes silent, costly duplication — isolated work
  starts on something already underway elsewhere, diverging until a hard-to-untangle mess surfaces
  later. This has happened repeatedly to this user; treat it as a standing priority.
---

# Project Continuity Check

## Why this exists

GitHub (or whichever remote the project uses) is the single central sync instance across every way this user works — cloud sessions, a session on their phone, and sessions with direct access to their own local PC and the software on it. Any of these can independently touch the same project. The moment one of them holds state the others can't see — a cloud session on its own branch, or a local working copy with commits or edits that haven't been pushed yet — that copy is, functionally, a fork, whether or not it ever gets a distinct branch name.

Each new Claude Code / Claude session that touches a git repository tends to create its own isolated branch, or — when working directly on the user's local machine — simply accumulates local changes that stay local. If that session doesn't know a related branch, repo, or local working copy already has newer or more complete work, it quietly starts from scratch — or from a stale snapshot — and builds forward independently. Nobody notices until much later, when two (or more) divergent versions of "the same project" have to be reconciled, and work gets lost or duplicated in the process.

This is not a one-off bug to patch — it is a structural risk any time: a new repo is created, an existing repo is opened without context, the user picks up a project from a different device or a different conversation, or work happens locally on the user's own machine instead of through a cloud session. The fix is the same cheap, proactive habit everywhere: look before you leap, and push what you have before you leave it, every time, not just when something has already gone wrong.

## When you're about to create a brand-new project/repo

Before scaffolding anything:

1. Call `list_repos` (or the equivalent repo-listing tool available in this session) and scan the results for names or descriptions that sound related to what the user is describing — not just exact matches. A user rarely remembers to mention "oh, I actually started this three weeks ago under a different name."
2. If anything looks even loosely related, surface it to the user directly before proceeding: name the repo, say why it looks related, and ask whether this new work should go there instead. Do not silently proceed past a plausible match.
3. If nothing related turns up, say so briefly ("checked your repos, nothing related exists yet") and proceed — the point is to make the check visible, not to interrogate the user every time.

## When you're opening an existing repo cold (new session, possibly on a different device)

0. **Do this before you say anything substantive about the project** — not just before you edit a file. It's tempting to answer a vague opening message ("let's keep working on X", "I want to create Y") from whatever feels familiar about the topic, especially if the project has come up before in training or in a pattern you recognize. Don't. Any claim about where the project currently stands, what's "next", or what's already been done must come from actually reading this session's live state (`CLAUDE.md`, a status/progress note it points to, recent commits) — not from assumption, memory, or pattern-matching on the topic. A confident-sounding but stale answer is worse than a brief "let me check the current state first," because the user has no way to tell it's wrong until they notice the mismatch themselves.
1. Check for a `CLAUDE.md` at the repo root first. If one exists and names a canonical branch, don't just read it for reference while quietly working on whatever branch this session happens to have been given — **actively move your own work onto that named branch** (check it out, or make sure every commit you make this session lands there) before touching anything. If this session's platform doesn't let you control which branch you commit to, say that plainly and immediately, and tell the user this session's work will not land on the canonical branch unless something changes, rather than silently proceeding on the wrong one.
2. If there's no `CLAUDE.md`, or it's silent on this, run `git branch -a` and `git log --all --oneline -20` (or the equivalent) to see whether other branches have recent activity. A repo with several `claude/<adjective>-<noun>-<hash>`-style branches is a strong signal that multiple independent sessions have touched this project before — don't assume the branch you happen to be on is the only or the latest one.
3. Compare timestamps and content breadth across candidate branches (a quick `git log -1 --format=%ci <branch>` per branch, or a `git diff --stat` between the two most plausible candidates) rather than assuming whichever branch you started on is current. Shallower, older-looking branches are not automatically wrong, but a branch that is a strict subset of another's content, or that still contains known-fixed errors, is a strong tell that it is the stale one.
4. If you find a genuine fork — real, divergent work on both sides — don't silently pick one. Tell the user what you found (branch names, what's unique to each, how recent each is) and let them decide, the same way you would flag any other consequential, hard-to-reverse decision.

## Working directly on the user's local machine is not exempt

When this session has direct access to the user's own computer and its installed software (rather than an isolated cloud checkout), the same risk shows up in a different shape — and it needs the same proactive check, every time:

1. **At the start of local work**, before editing anything, check whether the local working copy is in sync with GitHub: `git fetch`, then compare local `HEAD` against `origin/<branch>`. If local is behind, there's newer work upstream (from a cloud session, another local session, or the user on another device) that hasn't been pulled in yet — surface this before proceeding, the same way you'd surface a stray branch. If local is ahead with unpushed commits, that's work from a previous local session that the rest of the world — any cloud session, any other device — cannot see yet; say so plainly.
2. **Don't let local work sit unpushed.** Push promptly after meaningful changes rather than batching everything for "later" — every commit that stays local-only for an extended stretch is, in effect, a silent fork that only resolves itself if nothing else touches the project in the meantime. If a push genuinely can't happen right now (offline, mid-experiment, explicit instruction to hold off), say so explicitly, so the user knows this state exists and is unprotected until it's pushed.
3. **Treat "local, not yet on GitHub" as the same category of risk as "a divergent branch nobody mentioned"** — because it is one. The fix in both cases is the same: make the shared remote (GitHub) reflect reality as soon as possible, and be explicit the moment it doesn't.

## Making future sessions less likely to fork in the first place

Once you've confirmed which branch/state is canonical for a given project (whether you just resolved a fork or you're starting fresh), make that durable, not just something you and the current user happen to know:

- Write or update a `CLAUDE.md` at the repo root naming the canonical branch explicitly, and instructing any future session to fetch and read it before doing anything else. This is read automatically by future sessions in this repo, so it is the single highest-leverage thing you can do.
- If you have the access to do so, set the repository's actual default branch to the canonical one, so a plain clone or a session that doesn't read CLAUDE.md still lands in the right place. If your access is blocked at the platform/proxy level (this is common — repo admin settings are often restricted even when code pushes are allowed), say so plainly and give the user the exact manual steps (which settings page, which field) rather than quietly giving up on the idea.
- **Be explicit about what the default-branch fix does and doesn't do.** It fixes the *content* a brand-new session starts from — it does not stop a brand-new session from being handed its own fresh branch by the platform, which is a separate, structural behavior of how these sessions get created (e.g. on a phone, or any new chat on this repo). Don't let the user believe "I changed the default branch" is a full fix for forking; say clearly that a new session will still fork onto its own branch, just from the right starting point, and that branch still needs to be found and reconciled later.
- If the user works across multiple devices or sessions on the same project (as is common — e.g. switching from a desktop session to their phone mid-project), mention once, briefly: resuming the *same* session/conversation avoids this problem more completely than any amount of branch hygiene, because a fresh "new chat" on a repo creates a fresh branch almost by design, even with the default branch fixed. If the user says they're opening the project on another device, ask directly whether that's the same session continuing or a new one — the answer changes what you should expect to find.

## Keep it proportionate

This check should take seconds, not minutes — a repo listing call, maybe a `git branch -a`. Don't turn it into a research project or demand the user confirm trivial non-findings. The goal is to replace silent, unexamined forking with a quick, visible "I checked, here's what I found," so that when there genuinely is something to catch, it gets caught.
