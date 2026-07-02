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

def _resolve_domain_dir(root_path: Path, declared_path: str) -> Path:
    """Resolve o path declarado de um dominio (suporta '../X' e prefixo '.mecha/')."""
    cleaned = declared_path.replace("\\", "/")
    if cleaned.startswith(".mecha/"):
        cleaned = cleaned[len(".mecha/"):]
    return (root_path / cleaned).resolve()


def validate_ontology(ontology: dict, root_dir: str) -> list:
    """
    Validacao contra o filesystem (debate O6, item 9 / finding R2).
    Recusa componentes que nao existem fisicamente ('hallucinated components').
    Componentes com 'defined_in' sao logicos e validados no diretorio indicado.
    """
    errors = []
    root_path = Path(root_dir).resolve()
    for domain in ontology.get("domains", []):
        ddir = _resolve_domain_dir(root_path, domain.get("path", domain.get("id", "")))
        if not ddir.is_dir():
            errors.append(f"[{domain.get('id')}] path nao existe: {ddir}")
            continue
        for comp in domain.get("components", []):
            name = comp.get("name", "").rstrip("/")
            base = _resolve_domain_dir(root_path, comp["defined_in"]) if comp.get("defined_in") else ddir
            if name and not (base / name).exists():
                errors.append(f"[{domain.get('id')}] componente inexistente: {name}")
        for sub in domain.get("subdomains", []):
            sdir = _resolve_domain_dir(root_path, sub.get("id", ""))
            if not sdir.is_dir():
                errors.append(f"[{sub.get('id')}] subdomain path nao existe: {sdir}")
                continue
            for comp in sub.get("components", []):
                name = comp.get("name", "").rstrip("/")
                if name and not (sdir / name).exists():
                    errors.append(f"[{sub.get('id')}] componente inexistente: {name}")
    return errors


def _version_tuple(version: str) -> tuple:
    try:
        return tuple(int(p) for p in str(version).split("."))
    except ValueError:
        return (0,)


if __name__ == "__main__":
    import shutil
    import sys

    force = "--force" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--force"]

    script_dir = Path(__file__).resolve().parent
    default_root = script_dir.parent
    root_dir = args[0] if args else str(default_root)

    topology = generate_mecha_ontology(root_dir)

    # Gate 1 — validacao estrutural do que foi gerado
    errors = validate_ontology(topology, root_dir)
    if errors and not force:
        print("ERRO: ontologia gerada nao passou na validacao (use --force para ignorar):")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)

    # Gate 2 — protecao anti-clobber de versao curada mais nova
    output_file = default_root / "mecha_ontology.json"
    if output_file.exists():
        try:
            with open(output_file, "r", encoding="utf-8") as f:
                existing = json.load(f)
            if _version_tuple(existing.get("version", "0")) > _version_tuple(topology.get("version", "0")) and not force:
                print(
                    f"ERRO: mecha_ontology.json existente (v{existing.get('version')}) e mais novo que o gerado "
                    f"(v{topology.get('version')}). Curadoria manual seria destruida. Use --force se tiver certeza."
                )
                sys.exit(1)
        except (json.JSONDecodeError, OSError):
            pass
        shutil.copy2(output_file, str(output_file) + ".bak")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(topology, f, indent=2, ensure_ascii=False)

    print(f"Ontologia estrutural do MECHA gerada com sucesso em: {output_file}")
    if errors:
        print(f"AVISO: escrita forcada com {len(errors)} erro(s) de validacao.")
