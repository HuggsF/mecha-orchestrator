# ==============================================================================
# 🎨 VS CODE WEBVIEW UI TOOLKIT MCP SERVER
# ==============================================================================
# Exposes components documentation, templates, and styles for VS Code Webviews.
# Built with Model Context Protocol (FastMCP) Python SDK.
# ==============================================================================

import os
import sys
from typing import Dict, Any, List, Optional

from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("Webview UI Toolkit Helper")

# Database of vscode-webview-ui-toolkit components
COMPONENTS = {
    "vscode-button": {
        "description": "A button component representing a state or action.",
        "html_snippet": '<vscode-button appearance="primary">Click Me</vscode-button>',
        "attributes": {
            "appearance": "primary | secondary | icon",
            "disabled": "boolean",
            "autofocus": "boolean"
        },
        "css_variables": [
            "--vscode-button-background",
            "--vscode-button-foreground",
            "--vscode-button-hoverBackground"
        ],
        "events": ["click"],
        "example": """<!-- Primary Button -->
<vscode-button appearance="primary" id="btn-submit">Submit</vscode-button>

<!-- Secondary Button -->
<vscode-button appearance="secondary">Cancel</vscode-button>

<!-- Icon Button -->
<vscode-button appearance="icon" aria-label="Confirm">
    <span class="codicon codicon-check"></span>
</vscode-button>"""
    },
    "vscode-checkbox": {
        "description": "A checkbox component designed to select binary choices.",
        "html_snippet": '<vscode-checkbox checked>I agree to terms</vscode-checkbox>',
        "attributes": {
            "checked": "boolean",
            "disabled": "boolean",
            "readonly": "boolean"
        },
        "css_variables": [
            "--vscode-checkbox-background",
            "--vscode-checkbox-border",
            "--vscode-checkbox-foreground"
        ],
        "events": ["change"],
        "example": """<vscode-checkbox id="chk-remember" checked>Remember me</vscode-checkbox>"""
    },
    "vscode-text-field": {
        "description": "A text entry field for inputting short string values.",
        "html_snippet": '<vscode-text-field placeholder="Enter your name">Name:</vscode-text-field>',
        "attributes": {
            "placeholder": "string",
            "value": "string",
            "disabled": "boolean",
            "readonly": "boolean",
            "type": "text | password | email | number"
        },
        "css_variables": [
            "--vscode-input-background",
            "--vscode-input-foreground",
            "--vscode-input-border"
        ],
        "events": ["input", "change"],
        "example": """<vscode-text-field id="txt-username" placeholder="eg. john_doe">
    Username
</vscode-text-field>"""
    },
    "vscode-text-area": {
        "description": "A multi-line text input container for longer entries.",
        "html_snippet": '<vscode-text-area placeholder="Describe the issue..."></vscode-text-area>',
        "attributes": {
            "placeholder": "string",
            "value": "string",
            "cols": "number",
            "rows": "number",
            "resize": "none | both | horizontal | vertical"
        },
        "css_variables": [
            "--vscode-input-background",
            "--vscode-input-foreground"
        ],
        "events": ["input", "change"],
        "example": """<vscode-text-area id="txt-details" rows="5" resize="vertical">
    Detailed Description
</vscode-text-area>"""
    },
    "vscode-dropdown": {
        "description": "A selection dropdown menu to pick from a list of options.",
        "html_snippet": """<vscode-dropdown>
    <vscode-option>Option 1</vscode-option>
    <vscode-option>Option 2</vscode-option>
</vscode-dropdown>""",
        "attributes": {
            "disabled": "boolean",
            "value": "string"
        },
        "css_variables": [
            "--vscode-dropdown-background",
            "--vscode-dropdown-foreground",
            "--vscode-dropdown-border"
        ],
        "events": ["change"],
        "example": """<vscode-dropdown id="dd-env" value="prod">
    <vscode-option value="dev">Development</vscode-option>
    <vscode-option value="staging">Staging</vscode-option>
    <vscode-option value="prod">Production</vscode-option>
</vscode-dropdown>"""
    },
    "vscode-panels": {
        "description": "A tab container grouping views with headers.",
        "html_snippet": """<vscode-panels>
    <vscode-panel-tab id="tab-1">Tab 1</vscode-panel-tab>
    <vscode-panel-tab id="tab-2">Tab 2</vscode-panel-tab>
    <vscode-panel-view id="view-1">Content 1</vscode-panel-view>
    <vscode-panel-view id="view-2">Content 2</vscode-panel-view>
</vscode-panels>""",
        "attributes": {
            "activeid": "string"
        },
        "css_variables": [
            "--vscode-panel-background",
            "--vscode-panel-border",
            "--vscode-panelTitle-activeBorder"
        ],
        "events": ["change"],
        "example": """<vscode-panels activeid="tab-config">
    <vscode-panel-tab id="tab-config">Configuration</vscode-panel-tab>
    <vscode-panel-tab id="tab-logs">System Logs</vscode-panel-tab>
    
    <vscode-panel-view id="view-config">
        <h3>App Configuration</h3>
        <vscode-text-field>API Key</vscode-text-field>
    </vscode-panel-view>
    <vscode-panel-view id="view-logs">
        <pre>Service running on port 8080...</pre>
    </vscode-panel-view>
</vscode-panels>"""
    },
    "vscode-data-grid": {
        "description": "A grid component to display tabular data structured in columns and rows.",
        "html_snippet": """<vscode-data-grid id="grid" generate-header="default">
</vscode-data-grid>""",
        "attributes": {
            "generate-header": "none | default | sticky",
            "grid-template-columns": "string"
        },
        "css_variables": [
            "--vscode-list-hoverBackground",
            "--vscode-list-focusBackground"
        ],
        "events": [],
        "example": """<!-- HTML Structure -->
<vscode-data-grid id="my-grid"></vscode-data-grid>

<!-- Javascript Ingestion -->
<script>
    const grid = document.getElementById("my-grid");
    grid.rowsData = [
        { "ID": "1", "Status": "Active", "Name": "CodeSquad Runner" },
        { "ID": "2", "Status": "Offline", "Name": "RAG Analyzer" },
        { "ID": "3", "Status": "Success", "Name": "FinOps Guard" }
    ];
</script>"""
    },
    "vscode-progress-ring": {
        "description": "A circular loading and progress indicator.",
        "html_snippet": '<vscode-progress-ring></vscode-progress-ring>',
        "attributes": {
            "value": "number"
        },
        "css_variables": [
            "--vscode-progressBar-background"
        ],
        "events": [],
        "example": """<!-- Indeterminate Ring -->
<vscode-progress-ring></vscode-progress-ring>

<!-- Determinate Ring (50%) -->
<vscode-progress-ring value="50"></vscode-progress-ring>"""
    },
    "vscode-tag": {
        "description": "A tag/badge component used for metadata or categorizations.",
        "html_snippet": '<vscode-tag>Beta</vscode-tag>',
        "attributes": {},
        "css_variables": [
            "--vscode-badge-background",
            "--vscode-badge-foreground"
        ],
        "events": [],
        "example": """<vscode-tag>production</vscode-tag>
<vscode-tag>v1.2.0</vscode-tag>"""
    }
}

THEME_VARIABLES = {
    "Backgrounds & Panels": {
        "--vscode-editor-background": "Editor default background color.",
        "--vscode-sideBar-background": "Sidebar panel background color.",
        "--vscode-panel-background": "Bottom panels (Terminal, Output) background color.",
        "--vscode-menu-background": "Dropdown menus background color."
    },
    "Foregrounds & Text": {
        "--vscode-foreground": "Primary default font color.",
        "--vscode-editor-foreground": "Editor default text font color.",
        "--vscode-descriptionForeground": "Description/muted text font color.",
        "--vscode-errorForeground": "Error message font color."
    },
    "Buttons": {
        "--vscode-button-background": "Primary action button background.",
        "--vscode-button-foreground": "Primary button font color.",
        "--vscode-button-hoverBackground": "Primary button background on hover.",
        "--vscode-button-secondaryBackground": "Secondary action button background.",
        "--vscode-button-secondaryForeground": "Secondary button font color."
    },
    "Inputs & Borders": {
        "--vscode-input-background": "Text field and text area background.",
        "--vscode-input-foreground": "Input text font color.",
        "--vscode-input-border": "Border line around inputs.",
        "--vscode-focusBorder": "Border line when element is selected/focused."
    }
}


@mcp.tool()
def list_components() -> List[str]:
    """Retorna a lista de todos os componentes disponíveis no VS Code Webview UI Toolkit."""
    return list(COMPONENTS.keys())


@mcp.tool()
def get_component_details(component_name: str) -> Optional[Dict[str, Any]]:
    """Retorna detalhes específicos de um componente (exemplo, atributos, variáveis CSS).
    
    Args:
        component_name: O nome do componente (ex: 'vscode-button', 'vscode-dropdown').
    """
    return COMPONENTS.get(component_name)


@mcp.tool()
def get_theme_css_variables() -> Dict[str, Dict[str, str]]:
    """Retorna a lista de variáveis CSS nativas do VS Code para manter o design sincronizado com o tema ativo."""
    return THEME_VARIABLES


@mcp.tool()
def generate_webview_template(
    title: str,
    components: List[str],
    include_messaging: bool = True
) -> Dict[str, str]:
    """Gera um boilerplate completo de arquivos HTML, CSS e JS pré-configurados com o Toolkit.
    
    Args:
        title: O título da Webview.
        components: Lista dos componentes do toolkit que deseja incluir (ex: ['vscode-button', 'vscode-text-field']).
        include_messaging: Se deve incluir código de envio/recebimento de mensagens com a extensão (padrão: True).
    """
    # Build CDN scripts
    cdn_script = '<script type="module" src="https://unpkg.com/@vscode/webview-ui-toolkit@latest/dist/toolkit.min.js"></script>'
    codicon_css = '<link rel="stylesheet" href="https://unpkg.com/@vscode/codicons@latest/dist/codicon.css">'
    
    # Build components body
    body_elements = []
    for c in components:
        if c in COMPONENTS:
            body_elements.append(f"    <!-- Component: {c} -->\n    <div class=\"component-row\">\n        {COMPONENTS[c]['html_snippet']}\n    </div>")
            
    body_html = "\n\n".join(body_elements)
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    {cdn_script}
    {codicon_css}
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h2>{title}</h2>
    </header>

    <main>
{body_html}
    </main>

    <script src="main.js"></script>
</body>
</html>"""

    css_content = """body {
    padding: 15px;
    color: var(--vscode-foreground);
    font-family: var(--vscode-font-family, sans-serif);
    font-size: var(--vscode-font-size, 13px);
    background-color: var(--vscode-editor-background);
}

header {
    border-bottom: 1px solid var(--vscode-panel-border);
    margin-bottom: 20px;
    padding-bottom: 8px;
}

h2 {
    margin: 0;
    font-weight: 500;
}

main {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.component-row {
    display: flex;
    flex-direction: column;
    gap: 6px;
    padding: 10px;
    border-radius: 4px;
    background-color: var(--vscode-sideBar-background);
    border: 1px solid var(--vscode-panel-border);
}
"""

    js_messaging = """
    // Obter o objeto da API do VS Code para comunicação
    const vscode = acquireVsCodeApi();

    // Guardar estado anterior caso queira restaurar
    const previousState = vscode.getState();

    // Exemplo de envio de dados para o host da extensão
    document.querySelectorAll('vscode-button').forEach(btn => {
        btn.addEventListener('click', () => {
            vscode.postMessage({
                command: 'button-clicked',
                text: btn.textContent,
                time: new Date().toISOString()
            });
        });
    });

    // Ouvir mensagens enviadas da extensão para a Webview
    window.addEventListener('message', event => {
        const message = event.data; // Dados da mensagem
        console.log("Mensagem recebida da extensão:", message);
        
        switch (message.command) {
            case 'update-theme':
                document.body.style.setProperty('--current-theme', message.theme);
                break;
        }
    });
"""

    js_content = f"""// ==============================================================================
// 🎮 WEBVIEW LOGIC - {title}
// ==============================================================================
(function () {{
    console.log("Webview UI Toolkit initialized successfully.");
{js_messaging if include_messaging else ""}
}})();
"""

    return {
        "index.html": html_content,
        "style.css": css_content,
        "main.js": js_content
    }


if __name__ == "__main__":
    mcp.run()
