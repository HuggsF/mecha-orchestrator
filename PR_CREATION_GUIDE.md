# Manual PR Creation Guide — Sprint S1-S5

## Problem Context

The `feat/sendspeed-absorption-s1-s5` branch has unrelated git history from `master`. This prevents automated PR creation via `gh pr create`. Git refuses to merge unrelated histories by default.

**Branch Status:**
- `feat/sendspeed-absorption-s1-s5`: 10 commits (includes completion report)
- `master`: Different lineage (DOE UI/Personas focus)
- Remote: Both branches pushed ✅

---

## Manual PR Creation Steps

### Option 1: Create PR via GitHub Web UI (Recommended)

1. **Open GitHub:** https://github.com/HuggsF/mecha-orchestrator

2. **Click "Compare & pull request"** (if button appears) or go to:
   ```
   https://github.com/HuggsF/mecha-orchestrator/compare/master...feat/sendspeed-absorption-s1-s5
   ```

3. **Fill PR Details:**

   **Title:**
   ```
   feat: sprint sendspeed s1-s5 — absorção completa do domínio + rpg_cortex MCP
   ```

   **Description:**
   ```
   ## Sprint SendSpeed S1-S5 — Absorção Completa

   Absorção ratificada do domínio SendSpeed (debate O6 #2) e MCP read-only rpg_cortex.

   ### ✅ Deliverables

   **S1 — MCP Foundation + Security**
   - sendspeed_mcp_server.py: 17 tools in 5 modules (read-only)
   - sendspeed_squad.json: 6 specialized bots
   - sendspeed_workflows.json: 4 linear journeys
   - ide_backend.py: Security hardening (bind 127.0.0.1 + BusTokenMiddleware)
   - ORCH-14: Dedicated routing rule

   **S2 — Ontology v2.2.0 + Curation**
   - mecha_ontology.json v2.2.0: 11 domains, 28 subdomains
   - 6 curated CORE/sendspeed docs (callbacks, journeys, channels, integrations, contracts, userin_platform)
   - neo4j_sendspeed_ingest.py: 13 nodes + 13 relationships

   **S3 — Deep Journeys + AgentBus Bridge**
   - +2 new pipelines (batch_trigger, otp_fallback)
   - sendspeed_journey_handler.py: Journey → Pipeline bridge
   - workflow.started/completed emitted on AgentBus

   **S4 — UserIn Platform**
   - userin_rbac_spec: 10 user stories (SEND-367)
   - smartflow_dashboard_spec: Export inconsistency flags
   - billing_reporting_spec: 3 performance SLA risks

   **S5 — External Integrations (Blocked)**
   - igaming_webhook_pattern: Generic spec (NGX + FastTrack)
   - webhook_security_spec: NGX confirmed, FastTrack blocked
   - crm_adapter_registry: pending_fasttrack_doc

   **RPG Cortex MCP (Bonus)**
   - rpg_cortex_mcp_server.py: 4 tools (status, hardware_spec, integration_contract, gaps)
   - 4 known gaps documented with provenance

   ### 📊 Quality Metrics
   - ✅ 66/66 tests green
   - ✅ 21 MCP tools total
   - ✅ 6 docs curated
   - ✅ .gitignore sanitized
   - ✅ Guards intact (anti-clobber, write restrictions)
   - ✅ Zero secrets in history

   ### 🏗️ Squads Deployed
   1. dev_squad (Uncle Bob, Linus, Kent Beck, Mitnick)
   2. qa_squad (Sonar, Fowler, Locust)
   3. tribunal_squad (Warlock vs Amanda)
   4. devops_squad (Infrastructure)
   5. sendspeed_squad (6 bots)
   6. product_squad (Planning)

   ### 📌 Branch Info
   - Commits: 10 (S1 + S2 + S3 + S4 + S5 + RPG + report)
   - Files Modified: 47
   - Files Added: 18
   - Files Deleted: 12 (for security)

   **Note:** This branch has unrelated history with master. Recommend:
   - Merge with `--allow-unrelated-histories` flag
   - Run full test suite post-merge
   - Verify all MCP tools accessible

   Closes: (link any related issues if applicable)
   ```

4. **Click "Create pull request"**

5. **GitHub will prompt:**
   ```
   This branch has some commits with a different history than master.
   ```
   ✅ **Click "Create anyway"** or "Force create"

---

### Option 2: Command-Line Merge + PR (If Web UI Fails)

If the web UI doesn't allow creation:

```bash
# 1. Fetch latest
git fetch origin

# 2. Check out master
git checkout master

# 3. Merge with allow-unrelated-histories
git merge --no-ff --allow-unrelated-histories origin/feat/sendspeed-absorption-s1-s5 \
  -m "Merge feat/sendspeed-absorption-s1-s5: Sprint S1-S5 + RPG Cortex MCP

Absorção SendSpeed (S1-S5) + RPG Cortex MCP read-only.
Tests: 66/66 green. Tools: 21 MCP total.
See SPRINT_S1_S5_COMPLETION.md for details."

# 4. Resolve conflicts (if any) — see section below
# ... (edit files)
# git add .
# git commit

# 5. Push to master
git push origin master

# 6. Create PR from GitHub UI pointing to this merge
```

---

## Handling Merge Conflicts

If step 3 encounters conflicts, you'll see:
```
Auto-merging .agents/AGENTS.md
CONFLICT (add/add): Merge conflict in .agents/AGENTS.md
...
```

**Resolution Strategy:**

```bash
# View conflicts
git status

# For each conflicted file, choose resolution:
# Option A: Keep sendspeed changes (ours = origin/feat/sendspeed-s1-s5)
git checkout --theirs <file>

# Option B: Keep master changes (theirs = master)
git checkout --ours <file>

# Option C: Manual merge (edit file, remove conflict markers)
# Conflict markers look like:
# <<<<<<<< HEAD
# ... master version
# ========
# ... sendspeed version
# >>>>>>>> origin/feat/sendspeed-absorption-s1-s5

# After resolving all
git add .
git commit

# Continue merge
git push origin master
```

**Key Conflict Files (likely):**
- `.agents/AGENTS.md` — Choose `theirs` (sendspeed squad defs)
- `.gitignore` — Merge both (union of rules)
- `package.json` — Review manually (dependencies)
- `README.md` — Merge both (docs)

---

## Post-PR Validation Checklist

After PR is created (or merged):

- [ ] All 66 tests pass on CI
- [ ] MCP tools accessible from sendspeed_mcp_server
- [ ] Neo4j ingestors work with v2.2.0 ontology
- [ ] Squad orchestration functional in merged context
- [ ] Guard integrity verified (anti-clobber active)
- [ ] Zero secrets detected in history scan
- [ ] Workflow engine handles new pipelines (batch_trigger, otp_fallback)

---

## Critical Decisions

### Why Not Rebase?

Rebasing onto master would:
- Flatten 10 commits into linear history
- Require resolving conflicts for each commit
- Lose semantic commit grouping (S1, S2, S3, S4, S5, RPG)
- Risk losing git bisect context

❌ **Not recommended**

### Why Allow Unrelated Histories?

- Preserves both git lineages (master's UI work + sendspeed's backend work)
- Single merge commit documents integration point
- Can be reverted if needed (single `git revert -m 1 <merge-commit>`)
- Allows faster merge with manual conflict resolution

✅ **Recommended**

### Alternative: Cherry-Pick Key Commits

If you want to selectively integrate only SendSpeed S1-S5 (skipping ops/governance):

```bash
git checkout master
git cherry-pick 61d67ff..ed79173  # Pick S1 → S3
git cherry-pick ed79173           # Pick RPG
git push origin master
```

⚠️ **Complex but surgical** — only if master needs specific features

---

## Next Actions After PR Merge

1. **Close feature branch** (after code review approval)
   ```bash
   git push origin --delete feat/sendspeed-absorption-s1-s5
   ```

2. **Delete local branch**
   ```bash
   git branch -d feat/sendspeed-absorption-s1-s5
   ```

3. **Sync local master**
   ```bash
   git fetch origin
   git checkout master
   git pull origin master
   ```

4. **Verify SendSpeed tools on merged main**
   ```bash
   pytest tests/ -v
   # Should show 66+ tests passing
   ```

---

## Support

**If PR creation fails:**
1. Check GitHub auth: `gh auth status`
2. Verify branch exists: `git branch -r | grep sendspeed`
3. Try force create: `gh pr create --base master --head feat/sendspeed-absorption-s1-s5 --fill`

**If merge conflicts are complex:**
- Contact DX team for merge strategy guidance
- Consider creating **release branch** instead: `release/s1-s5` with cherry-picked commits

---

**Status:** Ready for manual PR creation  
**Estimated Merge Time:** 15-30 mins (including conflict resolution)  
**Risk Level:** Low (isolated feature, comprehensive tests, well-documented)  

---

*Generated: 2026-07-02*
*Reference: SPRINT_S1_S5_COMPLETION.md*
