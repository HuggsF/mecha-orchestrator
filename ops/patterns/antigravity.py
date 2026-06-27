import re
from typing import Dict, Any, List

class AntigravityDaemon:
    def __init__(self, chiplet_name: str = "TRIBUNAL_INPUT_CLEANER"):
        self.chiplet_name = chiplet_name

    def drop_bullshit(self, text: str) -> Dict[str, Any]:
        """
        Analisa e sanitiza o texto utilizando a gramática do Context7 (Chomsky Regex).
        Extrai apenas tokens e tags estruturadas do Arquiteto:
        - #{n} {Escopo} ou #{n}
        - - {Chave}:{Valor}
        - > {Valor}
        - [x] ou [ ]
        
        Se encontrar, retorna um dicionário com a lista de linhas estruturadas ('matrix')
        e o texto formatado ('clean_text'). Caso contrário, retorna 'matrix' vazia.
        """
        # Padrões Regex do Context7
        scope_pattern = r"(#\{\d+\}(?:\s*\{[^}]+\})?)"
        tuple_pattern = r"(-\s*\{[^}]+\}:\{[^}]+\})"
        verdict_pattern = r"(>\s*\{[^}]+\}|>\s*\{\d+\}|>\s*\d+)"
        gate_pattern = r"(\[[xX\s]\])"

        lines = text.splitlines()
        matrix = []

        for line in lines:
            line_stripped = line.strip()
            # Procura matches individuais na linha
            matches = []
            
            # Checa escopo
            m_scope = re.findall(scope_pattern, line_stripped)
            if m_scope:
                matches.extend(m_scope)
            
            # Checa tuplas
            m_tuple = re.findall(tuple_pattern, line_stripped)
            if m_tuple:
                matches.extend(m_tuple)
                
            # Checa vereditos
            m_verdict = re.findall(verdict_pattern, line_stripped)
            if m_verdict:
                matches.extend(m_verdict)
                
            # Checa gates booleanos
            m_gate = re.findall(gate_pattern, line_stripped)
            if m_gate:
                matches.extend(m_gate)

            if matches:
                matrix.append(" ".join(matches))

        if matrix:
            clean_text = "\n".join(matrix)
            return {
                "matrix": matrix,
                "clean_text": clean_text
            }
        else:
            print("[X_DROP_SYNTAX] Frequência Vazia. Semântica ou Typo não indexável obliterado.")
            return {
                "matrix": [],
                "clean_text": text
            }

if __name__ == "__main__":
    # Teste local simples
    test_input = (
        "Olá paizão, olha esse reator doido que eu fiz.\n"
        "#{2} {REATOR_KAFKA_SINCRONIZADO}\n"
        "- {Fator}:{Alta latência no barramento}\n"
        "- {Mitigação}:{Thread Ghost Workers}\n"
        "> {1}\n"
        "[x]\n"
        "Abraços!"
    )
    daemon = AntigravityDaemon()
    res = daemon.drop_bullshit(test_input)
    print("Matrix:", res["matrix"])
    print("Clean:\n", res["clean_text"])
