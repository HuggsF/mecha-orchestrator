import os
import sys
import json
import hashlib
import argparse
from typing import Dict, List, Tuple, Optional

try:
    from pydantic import BaseModel, Field
    HAS_PYDANTIC = True
except ImportError:
    HAS_PYDANTIC = False

# --- Configurar UTF-8 no stdout/stderr no Windows ---
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')


# --- Pydantic Data Models ---
if HAS_PYDANTIC:
    class TransitionAction(BaseModel):
        action_type: str = "click"
        target_relative_coord: Tuple[int, int]
        description: str

    class GraphNode(BaseModel):
        state_id: str
        window_title: str
        controls_found: List[dict]
        visual_path: Optional[str] = None

    class NavigationGraph(BaseModel):
        nodes: Dict[str, GraphNode] = Field(default_factory=dict)
        edges: Dict[str, Dict[str, TransitionAction]] = Field(default_factory=dict) # state_from -> {state_to: action}
else:
    class TransitionAction:
        def __init__(self, action_type, target_relative_coord, description):
            self.action_type = action_type
            self.target_relative_coord = target_relative_coord
            self.description = description
        def model_dump(self):
            return {
                "action_type": self.action_type,
                "target_relative_coord": self.target_relative_coord,
                "description": self.description
            }

    class GraphNode:
        def __init__(self, state_id, window_title, controls_found, visual_path=None):
            self.state_id = state_id
            self.window_title = window_title
            self.controls_found = controls_found
            self.visual_path = visual_path
        def model_dump(self):
            return {
                "state_id": self.state_id,
                "window_title": self.window_title,
                "controls_found": self.controls_found,
                "visual_path": self.visual_path
            }

    class NavigationGraph:
        def __init__(self):
            self.nodes = {}
            self.edges = {}
        def model_dump(self):
            nodes_dump = {k: v.model_dump() if hasattr(v, 'model_dump') else v for k, v in self.nodes.items()}
            edges_dump = {}
            for k, connections in self.edges.items():
                edges_dump[k] = {tk: tv.model_dump() if hasattr(tv, 'model_dump') else tv for tk, tv in connections.items()}
            return {"nodes": nodes_dump, "edges": edges_dump}


# --- Metroidvania Map Manager ---
class MetroidvaniaMap:
    def __init__(self, storage_path: str = "c:/Users/huggs/OneDrive/Documentos/workspace/.mecha/ops/maps/navigation_graph.json"):
        self.storage_path = storage_path
        if HAS_PYDANTIC:
            self.graph = NavigationGraph()
        else:
            self.graph = NavigationGraph()
        self.load_graph()

    def load_graph(self) -> None:
        """Carrega o grafo de navegacao de forma segura."""
        if not os.path.exists(self.storage_path):
            # Assegura diretorio pai
            out_dir = os.path.dirname(self.storage_path)
            if out_dir and not os.path.exists(out_dir):
                os.makedirs(out_dir, exist_ok=True)
            return

        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            if HAS_PYDANTIC:
                # Carrega no Pydantic
                nodes = {k: GraphNode(**v) for k, v in data.get("nodes", {}).items()}
                edges = {}
                for k, conn in data.get("edges", {}).items():
                    edges[k] = {tk: TransitionAction(**tv) for tk, tv in conn.items()}
                self.graph.nodes = nodes
                self.graph.edges = edges
            else:
                for k, v in data.get("nodes", {}).items():
                    self.graph.nodes[k] = GraphNode(
                        state_id=v.get("state_id"),
                        window_title=v.get("window_title"),
                        controls_found=v.get("controls_found"),
                        visual_path=v.get("visual_path", None)
                    )
                for k, conn in data.get("edges", {}).items():
                    self.graph.edges[k] = {}
                    for tk, tv in conn.items():
                        self.graph.edges[k][tk] = TransitionAction(**tv)
            self.last_ocr_text = data.get("last_ocr_text", "")
        except Exception as e:
            print(f"[!] Erro ao carregar grafo do disco: {e}. Iniciando novo grafo.")

    def save_graph(self) -> None:
        """Persiste o grafo estruturado em disco no formato JSON."""
        try:
            if HAS_PYDANTIC:
                data = {
                    "nodes": {k: v.model_dump() for k, v in self.graph.nodes.items()},
                    "edges": {k: {tk: tv.model_dump() for tk, tv in conn.items()} for k, conn in self.graph.edges.items()},
                    "last_ocr_text": getattr(self, "last_ocr_text", "")
                }
            else:
                data = self.graph.model_dump()
                data["last_ocr_text"] = getattr(self, "last_ocr_text", "")

            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[!] Erro ao salvar o grafo no disco: {e}")

    def add_state(self, window_title: str, controls: list, visual_path: Optional[str] = None) -> str:
        """Gera um hash MD5 unico para o estado e o registra no grafo."""
        # Cria chave baseada no titulo e controles
        controls_str = json.dumps(controls, sort_keys=True)
        raw_key = f"{window_title}-{controls_str}"
        state_id = hashlib.md5(raw_key.encode('utf-8')).hexdigest()

        if state_id not in self.graph.nodes:
            if HAS_PYDANTIC:
                node = GraphNode(state_id=state_id, window_title=window_title, controls_found=controls, visual_path=visual_path)
            else:
                node = GraphNode(state_id, window_title, controls, visual_path)
            self.graph.nodes[state_id] = node
            self.save_graph()
        else:
            # Se o nó já existe mas agora temos a imagem e antes não tínhamos, atualiza visual_path
            node = self.graph.nodes[state_id]
            current_visual = node.visual_path if HAS_PYDANTIC else node.visual_path
            if visual_path and current_visual is None:
                if HAS_PYDANTIC:
                    node.visual_path = visual_path
                else:
                    node.visual_path = visual_path
                self.save_graph()
            
        return state_id

    def add_transition(self, state_from_id: str, state_to_id: str, action_type: str, coord: Tuple[int, int], desc: str) -> None:
        """Cria uma aresta direcional de transicao entre dois estados."""
        if HAS_PYDANTIC:
            action = TransitionAction(action_type=action_type, target_relative_coord=coord, description=desc)
        else:
            action = TransitionAction(action_type=action_type, target_relative_coord=coord, description=desc)

        # Adiciona no dicionario de arestas
        edges = self.graph.edges
        if state_from_id not in edges:
            edges[state_from_id] = {}
        
        edges[state_from_id][state_to_id] = action
        self.save_graph()

    def get_backtrack_route(self, current_state_id: str, target_state_id: str) -> List[dict]:
        """Calcula o caminho mais curto usando busca em largura (BFS)."""
        if current_state_id == target_state_id:
            return []

        # Fila para BFS contendo (no_atual, caminho_de_acoes_ate_aqui)
        queue = [(current_state_id, [])]
        visited = {current_state_id}

        edges = self.graph.edges

        while queue:
            node, path = queue.pop(0)

            # Obtem as conexoes de saida do no atual
            connections = edges.get(node, {})
            for neighbor, action in connections.items():
                if neighbor == target_state_id:
                    # Converte para dicionario para retorno consistente
                    act_dump = action.model_dump() if hasattr(action, 'model_dump') else action.model_dump() if HAS_PYDANTIC else action.model_dump()
                    return path + [act_dump]

                if neighbor not in visited:
                    visited.add(neighbor)
                    act_dump = action.model_dump() if hasattr(action, 'model_dump') else action.model_dump() if HAS_PYDANTIC else action.model_dump()
                    queue.append((neighbor, path + [act_dump]))

        return [] # Retorna vazio se nao houver rota de retorno

    def sync_to_obsidian(self, vault_path: str = "c:/Users/huggs/OneDrive/Documentos/workspace/Obsidian/Topologia_Omega") -> None:
        """
        Sincroniza o estado atual do grafo gerando notas markdown individuais no cofre do Obsidian.
        Garante links wiki [[Window_Target]] para reconstrução de grafo de conhecimento.
        """
        if not os.path.exists(vault_path):
            try:
                os.makedirs(vault_path, exist_ok=True)
            except Exception as e:
                print(f"[!] Erro ao criar diretorio do Obsidian: {e}")
                return

        # 1. Obter dados do grafo
        if HAS_PYDANTIC:
            nodes = {k: v.model_dump() for k, v in self.graph.nodes.items()}
            edges = {k: {tk: tv.model_dump() for tk, tv in conn.items()} for k, conn in self.graph.edges.items()}
        else:
            nodes = {}
            for k, v in self.graph.nodes.items():
                nodes[k] = v.model_dump() if hasattr(v, 'model_dump') else v
            edges = {}
            for k, conn in self.graph.edges.items():
                edges[k] = {}
                for tk, tv in conn.items():
                    edges[k][tk] = tv.model_dump() if hasattr(tv, 'model_dump') else tv

        # Guardar lista de arquivos criados para poder remover notas antigas órfãs
        created_files = set()

        # 2. Escrever notas de cada nó
        for state_id, node in nodes.items():
            win_title = node.get("window_title", "Sem_Titulo")
            safe_name = "".join([c if c.isalnum() or c in " _-" else "_" for c in win_title]).strip()
            safe_name = safe_name[:80].strip()
            file_name = f"Window_{safe_name}.md"
            file_path = os.path.join(vault_path, file_name)
            
            created_files.add(file_path)
            
            # Gerar conteúdo da nota
            lines = []
            lines.append("---")
            lines.append(f'id: "{state_id}"')
            lines.append(f'window_title: "{win_title}"')
            lines.append('type: "claw_navigation_state"')
            lines.append("---")
            lines.append("")
            lines.append(f"# {win_title}")
            lines.append("")
            
            # Anexar miniatura de imagem se configurada
            v_path = node.get("visual_path")
            if v_path and os.path.exists(v_path):
                attachments_dir = os.path.join(vault_path, "attachments")
                try:
                    os.makedirs(attachments_dir, exist_ok=True)
                    dest_image = os.path.join(attachments_dir, f"Window_{state_id}.png")
                    import shutil
                    shutil.copy2(v_path, dest_image)
                    lines.append(f"![Captura de Tela](attachments/Window_{state_id}.png)")
                    lines.append("")
                except Exception as img_err:
                    print(f"[!] Erro ao copiar imagem para o Obsidian: {img_err}")
            
            lines.append(f"**Estado ID**: `{state_id}`")
            lines.append("")
            lines.append("## Controles Encontrados")
            controls = node.get("controls_found", [])
            if not controls:
                lines.append("*Nenhum controle detectado.*")
            else:
                for idx, ctrl in enumerate(controls):
                    lines.append(f"- Control {idx+1}: `{ctrl.get('type', 'desconhecido')}` em coordenadas {ctrl.get('relative_bounds', '')}")
            lines.append("")
            lines.append("## Transições e Rotas de Conexão")
            
            # Encontrar conexões de saída
            connections = edges.get(state_id, {})
            if not connections:
                lines.append("*Nenhuma transição de saída mapeada.*")
            else:
                for target_id, action in connections.items():
                    target_node = nodes.get(target_id)
                    if target_node:
                        t_title = target_node.get("window_title", "Sem_Titulo")
                        t_safe = "".join([c if c.isalnum() or c in " _-" else "_" for c in t_title]).strip()[:80].strip()
                        lines.append(f"- **[[Window_{t_safe}]]**: {action.get('description', '')} via `{action.get('action_type', '')}` em {action.get('target_relative_coord', '')}")
            lines.append("")
            
            # Encontrar conexões de entrada (backlinks)
            back_transitions = []
            for from_id, conn in edges.items():
                if state_id in conn:
                    from_node = nodes.get(from_id)
                    if from_node:
                        f_title = from_node.get("window_title", "Sem_Titulo")
                        f_safe = "".join([c if c.isalnum() or c in " _-" else "_" for c in f_title]).strip()[:80].strip()
                        back_transitions.append(f"- **[[Window_{f_safe}]]** (Retorno de transição)")
            
            if back_transitions:
                lines.append("## Entradas / Backlinks")
                lines.extend(back_transitions)
                lines.append("")
                
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(lines))
            except Exception as e:
                print(f"[!] Erro ao salvar nota do Obsidian {file_path}: {e}")

        # 3. Remover arquivos markdown antigos órfãos
        try:
            for item in os.listdir(vault_path):
                if item.startswith("Window_") and item.endswith(".md"):
                    full_p = os.path.join(vault_path, item)
                    if full_p not in created_files:
                        os.remove(full_p)
        except Exception as e:
            print(f"[!] Erro ao limpar notas antigas do Obsidian: {e}")


def run_mock_test():
    print("[*] Iniciando teste unitario do Grafo de Navegacao (BFS Backtrack)...")
    # Usa um caminho de arquivo temporario para teste
    test_file = "c:/Users/huggs/OneDrive/Documentos/workspace/.mecha/ops/maps/navigation_graph_test.json"
    if os.path.exists(test_file):
        os.remove(test_file)

    mapper = MetroidvaniaMap(storage_path=test_file)

    # 1. Adicionando Estados mock
    # Janela A: Home Page
    state_a = mapper.add_state("Opera - Smartico Home", [{"type": "button", "relative_bounds": (10, 10, 40, 30)}])
    # Janela B: Login Form
    state_b = mapper.add_state("Opera - Smartico Login", [{"type": "input", "relative_bounds": (100, 100, 300, 130)}])
    # Janela C: Admin Dashboard
    state_c = mapper.add_state("Opera - Smartico Admin Dashboard", [{"type": "button", "relative_bounds": (500, 20, 600, 50)}])

    print(f" [+] Estado A (Home) registrado: {state_a}")
    print(f" [+] Estado B (Login) registrado: {state_b}")
    print(f" [+] Estado C (Admin) registrado: {state_c}")

    # 2. Adicionando transicoes (Home -> Login -> Admin)
    mapper.add_transition(state_a, state_b, "click", (25, 20), "Clicar no link de Login")
    mapper.add_transition(state_b, state_c, "click", (200, 115), "Enviar credenciais de acesso")
    
    # Criando aresta de backtrack para demonstrar o BFS (Admin -> Home)
    mapper.add_transition(state_c, state_a, "click", (550, 35), "Clicar no botao Logout")

    # 3. Calculando rota de retorno BFS (De Admin para Home)
    print("\n[*] Calculando rota de retorno BFS (De Admin para Home)...")
    route = mapper.get_backtrack_route(state_c, state_a)
    
    if route:
        print(f" [+] ROTA ENCONTRADA (Total de etapas: {len(route)}):")
        for idx, step in enumerate(route):
            print(f"    Passo {idx + 1}: {step['description']} em {step['target_relative_coord']} via {step['action_type']}")
    else:
        print(" [!] Rota nao encontrada.")

    # 4. Testando a exportação Obsidian
    print("\n[*] Testando exportacao Obsidian Sync...")
    test_vault = "c:/Users/huggs/OneDrive/Documentos/workspace/.mecha/ops/maps/obsidian_test_vault"
    if os.path.exists(test_vault):
        import shutil
        shutil.rmtree(test_vault, ignore_errors=True)
        
    mapper.sync_to_obsidian(vault_path=test_vault)
    
    # Valida criação das notas
    note_files = []
    if os.path.exists(test_vault):
        note_files = [f for f in os.listdir(test_vault) if f.endswith(".md")]
        
    if len(note_files) == 3:
        print(f" [+] Sincronizacao Obsidian validada com sucesso! {len(note_files)} notas criadas.")
        success = True
    else:
        print(f" [!] Falha na sincronizacao do Obsidian. Arquivos encontrados: {note_files}")
        success = False
        
    if os.path.exists(test_vault):
        import shutil
        shutil.rmtree(test_vault, ignore_errors=True)

    # Limpeza de arquivo de teste
    if os.path.exists(test_file):
        os.remove(test_file)
        
    if not success:
        print("[!] Teste do Grafo falhou no Obsidian Sync.")
        sys.exit(1)
        
    print("[+] Teste do Grafo concluido com sucesso!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MECHA Navigation Graph Engine")
    parser.add_argument("--test-graph", action="store_true", help="Executa o teste unitario BFS do grafo")
    parser.add_argument("--sync-obsidian", action="store_true", help="Forca a exportacao do grafo atual para o Obsidian")
    args = parser.parse_args()

    if args.test_graph:
        run_mock_test()
    elif args.sync_obsidian:
        mapper = MetroidvaniaMap()
        mapper.sync_to_obsidian()
        print("[+] Grafo sincronizado com o cofre do Obsidian com sucesso!")
    else:
        # Exibe informacoes basicas do grafo salvo
        mapper = MetroidvaniaMap()
        nodes_count = len(mapper.graph.nodes)
        edges_count = sum(len(conn) for conn in mapper.graph.edges.values())
        print(f"MECHA Navigation Graph:")
        print(f"  Total de Nos (Janelas): {nodes_count}")
        print(f"  Total de Conexoes: {edges_count}")
