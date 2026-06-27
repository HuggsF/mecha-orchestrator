import os
import json
from pathlib import Path

def generate_mecha_ontology(root_dir: str) -> dict:
    root_path = Path(root_dir)
    if not root_path.exists():
        return {"error": "Root directory does not exist"}

    ontology = {
        "name": "MECHA Multi-Agent Orchestrator Ontology",
        "version": "1.0.0",
        "root": str(root_path),
        "domains": []
    }

    # Core domains in the MECHA architecture
    expected_domains = [
        "ops", "squads", "rag-dojo", "kernel", "behavior", 
        "intelligence", "foundation", "governance", "test_db", "docs", "CORE"
    ]

    for domain in expected_domains:
        domain_path = root_path / domain
        if domain_path.is_dir():
            domain_info = {
                "id": domain,
                "type": "Core Domain",
                "path": f".mecha/{domain}",
                "description": _extract_description(domain_path),
                "components": _scan_components(domain_path)
            }
            ontology["domains"].append(domain_info)

    return ontology

def _extract_description(domain_path: Path) -> str:
    readme = domain_path / "README.md"
    if readme.exists():
        try:
            with open(readme, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        return line[:150] + ("..." if len(line) > 150 else "")
        except Exception:
            pass
    return f"Domínio responsável pelos fluxos de {domain_path.name}"

def _scan_components(domain_path: Path) -> list:
    components = []
    try:
        for file in domain_path.iterdir():
            if file.is_file() and file.suffix in [".py", ".js", ".ts", ".md"]:
                components.append({
                    "name": file.name,
                    "type": "Module" if file.suffix != ".md" else "Documentation"
                })
    except Exception:
        pass
    return components

if __name__ == "__main__":
    import sys
    # default to .mecha in the same directory as the script's parent parent
    script_dir = Path(__file__).resolve().parent
    default_root = script_dir.parent
    
    root_dir = sys.argv[1] if len(sys.argv) > 1 else str(default_root)
    topology = generate_mecha_ontology(root_dir)
    
    output_file = default_root / "mecha_ontology.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(topology, f, indent=2, ensure_ascii=False)
    
    print(f"Ontologia estrutural do MECHA gerada com sucesso em: {output_file}")
