# test_workspace_root_contract.py — contrato de resolucao do WORKSPACE_ROOT
# (MECHA-S1-01, P0 ratificado pelo debate O6)
#
# Bug corrigido: mecha_mcp_server.py resolvia WORKSPACE_ROOT como .mecha
# (3 dirnames sobre o abspath do arquivo), mas SquadOrchestrator monta
# <workspace_root>/.mecha/intelligence/squads/... — resultado: paths tipo
# .mecha/.mecha/... e _load_json retornava {} EM SILENCIO.
#
# Este teste prova que:
#   (a) WORKSPACE_ROOT aponta para um dir contendo .mecha/intelligence/squads;
#   (b) o loader interno (SquadOrchestrator.load_squad_config) carrega o
#       dev_squad.json real (nao-vazio, com agentes);
#   (c) idem para sendspeed_squad.json e sendspeed_workflows.json.
#
# Paths de import resolvidos via conftest.py (padrao da suite).
import os

import mecha_mcp_server
from squad_orchestrator import SquadOrchestrator


def _orchestrator():
    return SquadOrchestrator(mecha_mcp_server.WORKSPACE_ROOT)


# ------------------------------------------------------------------
# (a) WORKSPACE_ROOT aponta para o dir certo
# ------------------------------------------------------------------

def test_workspace_root_is_parent_of_mecha():
    root = mecha_mcp_server.WORKSPACE_ROOT
    assert os.path.isdir(root), f"WORKSPACE_ROOT nao existe: {root}"
    # SquadOrchestrator monta <root>/.mecha/... — logo o root NAO pode ser o
    # proprio .mecha (regressao do bug original).
    assert os.path.basename(root) != ".mecha", (
        f"WORKSPACE_ROOT resolveu para o proprio .mecha: {root}"
    )
    squads_dir = os.path.join(root, ".mecha", "intelligence", "squads")
    assert os.path.isdir(squads_dir), (
        f"Dir de squads nao encontrado a partir de WORKSPACE_ROOT: {squads_dir}"
    )


def test_workspace_root_matches_ide_backend_resolution():
    # ide_backend.py e a referencia correta: patterns/../../.. => workspace
    expected = os.path.normpath(
        os.path.join(
            os.path.dirname(os.path.abspath(mecha_mcp_server.__file__)),
            "..", "..", "..",
        )
    )
    assert os.path.normcase(mecha_mcp_server.WORKSPACE_ROOT) == os.path.normcase(expected)


# ------------------------------------------------------------------
# (b) loader interno carrega dev_squad.json real
# ------------------------------------------------------------------

def test_loader_loads_dev_squad_with_agents():
    cfg = _orchestrator().load_squad_config("dev_squad")
    assert isinstance(cfg, dict)
    assert cfg, "dev_squad.json carregou vazio — regressao do bug WORKSPACE_ROOT"
    # Agentes conhecidos do dev squad
    assert "Uncle Bob" in cfg
    assert "Linus" in cfg
    assert len(cfg) >= 2, f"dev_squad deveria ter multiplos agentes, veio: {list(cfg)}"


# ------------------------------------------------------------------
# (c) idem para sendspeed_squad.json e sendspeed_workflows.json
# ------------------------------------------------------------------

def test_loader_loads_sendspeed_squad_with_agents():
    cfg = _orchestrator().load_squad_config("sendspeed_squad")
    assert isinstance(cfg, dict)
    assert cfg, "sendspeed_squad.json carregou vazio"
    assert "CatalogBot" in cfg
    assert len(cfg) >= 2, f"sendspeed_squad deveria ter multiplos agentes, veio: {list(cfg)}"


def test_loader_loads_sendspeed_workflows():
    cfg = _orchestrator().load_workflow_config("sendspeed_workflows")
    assert isinstance(cfg, dict)
    assert cfg, "sendspeed_workflows.json carregou vazio"
    assert "journey_recuperacao_cadastro_userin" in cfg
