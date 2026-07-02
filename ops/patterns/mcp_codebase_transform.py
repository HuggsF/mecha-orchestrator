# DEPRECATED: Pendente re-arquitetura na Mecha V3
from mcp.server.fastmcp import FastMCP
import os

mcp = FastMCP("MechaCodebaseTransform")

def read_file_safe(path: str) -> str:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    return f"[Arquivo não encontrado: {path}]"

def build_tree(startpath: str, max_depth: int = 3) -> str:
    tree = []
    base_depth = startpath.rstrip(os.sep).count(os.sep)
    for root, dirs, files in os.walk(startpath):
        # Exclude hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        level = root.count(os.sep) - base_depth
        if level > max_depth:
            continue
        
        indent = ' ' * 4 * level
        tree.append(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            if not f.startswith('.'):
                tree.append(f"{subindent}{f}")
    return "\n".join(tree)

@mcp.tool()
def prepare_debate_context(target_dir: str = ".") -> str:
    """
    Extracts the MECHA Ontology, the directory tree, and the 3 Persona DNAs
    (Hiansen, Henrique, Rodolfo) to build the context for a multi-agent
    topology debate.
    """
    workspace_root = r"c:\Users\huggs\OneDrive\Documentos\workspace\.mecha"
    
    ontology_path = os.path.join(workspace_root, "mecha_ontology.json")
    hiansen_path = os.path.join(workspace_root, "rag-dojo", "codebase-transform", "references", "personas", "hiansen.md")
    henrique_path = os.path.join(workspace_root, "rag-dojo", "codebase-transform", "references", "personas", "henrique.md")
    rodolfo_path = os.path.join(workspace_root, "rag-dojo", "codebase-transform", "references", "personas", "rodolfo.md")
    
    ontology_content = read_file_safe(ontology_path)
    hiansen_dna = read_file_safe(hiansen_path)
    henrique_dna = read_file_safe(henrique_path)
    rodolfo_dna = read_file_safe(rodolfo_path)
    
    abs_target = os.path.abspath(target_dir)
    tree_content = build_tree(abs_target, max_depth=3)
    
    context = f"""
# MULTI-AGENT TOPOLOGY DEBATE CONTEXT

You are the Orquestrador-Mestre (Mecha). You must now simulate a debate between 3 personas to evaluate and perform a codebase transformation on the directory: `{abs_target}`

## 1. PERSONA DNAs
The following are the core directives for the 3 agents. Internalize them before simulating their responses.

--- HIANSEN ---
{hiansen_dna}

--- HENRIQUE ---
{henrique_dna}

--- RODOLFO ---
{rodolfo_dna}

## 2. CURRENT ONTOLOGY (mecha_ontology.json)
{ontology_content}

## 3. FACTUAL DIRECTORY TREE (Max Depth 3)
```text
{tree_content}
```

## INSTRUCTIONS
1. Read the provided Ontology and compare it to the Factual Directory Tree.
2. Simulate a debate where Hiansen points out structural/canonical issues, Henrique focuses on the reality of the code and prevents over-engineering, and Rodolfo looks for contradictions, missing tests, and security risks.
3. Consolidate their findings into a prioritized matrix.
4. Output a `synthesis_report.md` detailing the actions required to harmonize the directory tree with the ontology (Codebase Transform Phase 0/1).
"""
    return context

if __name__ == "__main__":
    mcp.run()
