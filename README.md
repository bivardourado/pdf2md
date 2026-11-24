<div align="center">

# 📄 pdf2md

### Conversor Inteligente de Documentos para Markdown & Otimizador para LLMs

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://pdf2md2docx.streamlit.app/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/bivardourado/pdf2md)

**Converta dezenas ou centenas de documentos PDF e Word (DOCX) em Markdown estruturado e limpo, pronto para RAG, Google NotebookLM e Modelos de Linguagem de Grande Porte (LLMs).**

[🌐 Acessar Aplicação Online](https://pdf2md2docx.streamlit.app/) • [✨ Recursos](#-principais-recursos) • [🚀 Como Usar](#-como-usar-localmente) • [🧠 Smart Chunking](#-smart-chunking-para-llms)

---

</div>

## 📌 Visão Geral

O **pdf2md** resolve um problema crítico no fluxo de trabalho com Inteligência Artificial: **a perda de formatação e o excesso de contexto ao converter documentos complexos**. 

Ao contrário de extratores simples que apenas jogam o texto bruto, o **pdf2md** preserva tabelas, hierarquias de títulos (`#`, `##`), ênfases e listas, preparando os arquivos no formato ideal para consumo por ferramentas como **Google Gemini Notebook**, **ChatGPT**, **Claude** e **NotebookLM**.

---

## ✨ Principais Recursos

- ⚡ **Processamento 100% em Memória (`io.BytesIO`):** Zero gravação física em disco temporário. Mais rápido, totalmente seguro contra *path traversal* e sem risco de concorrência ou conflito de arquivos.
- 📦 **Download em Lote (.ZIP):** Faça upload de 10, 50 ou 200 arquivos simultâneos (ex: coleções de discursos, contratos ou relatórios) e baixe tudo com um único clique em um arquivo compactado `.zip`.
- 🧠 **Smart Chunking (Divisão Inteligente de Capítulos):** Documentos gigantes com mais de **450.000 palavras** são divididos automaticamente sem quebrar frases ou parágrafos ao meio — o fatiamento respeita as quebras lógicas de capítulos e seções.
- 📑 **Suporte Multi-Formato:**
  - **PDF:** Renderização via `PyMuPDF` + `PyMuPDF4LLM` com preservação visual e estrutural.
  - **DOCX:** Conversão semântica via `Mammoth` + `Markdownify` garantindo tabelas e listas limpas.
- 📊 **Contador de Palavras & Verificador Gemini:** Diagnóstico imediato do tamanho do documento e compatibilidade de janela de contexto.

---

## 🚀 Como Usar Localmente

### 1. Clonar o repositório
```bash
git clone https://github.com/bivardourado/pdf2md.git
cd pdf2md
```

### 2. Criar e ativar o ambiente virtual (Recomendado)
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux / Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Executar a aplicação
```bash
streamlit run app.py
```

Acesse em seu navegador no endereço: `http://localhost:8501`

---

## 🧠 Smart Chunking para LLMs

Janelas de contexto em LLMs (como o limite de 500k palavras no Gemini Notebook) exigem divisão cirúrgica. 

O algoritmo do **pdf2md** opera com uma margem de segurança programada:

```
[Início do Documento]
       │
       ▼
Acumula palavras linha a linha
       │
       ├──> Total < 400.000 palavras? ────> Continua agrupando
       │
       └──> Total > 400.000 palavras E encontrou '# ' ou '## '?
               │
               ▼
       [Corte Seguro no Título do Capítulo] ───> Salva Parte N
               │
               ▼
       Reinicia contagem no novo capítulo ────> Salva Parte N+1
```

---

## 🛠️ Stack Tecnológica

| Tecnologia | Função no Projeto |
| :--- | :--- |
| **[Streamlit](https://streamlit.io/)** | Interface web interativa reativa e moderna |
| **[PyMuPDF / PyMuPDF4LLM](https://pymupdf.readthedocs.io/)** | Motor de alta velocidade para extração de PDF estruturado |
| **[Mammoth](https://github.com/mwilliamson/python-mammoth)** | Conversor semântico de documentos Word (.docx) |
| **[Markdownify](https://github.com/matthewwithanm/python-markdownify)** | Transformação de HTML intermediário em Markdown puro |

---

## 📄 Licença

Distribuído sob a licença **MIT**. Veja `LICENSE` para mais informações.

---

<div align="center">
Desenvolvido por <a href="https://github.com/bivardourado">Bivar Dourado</a> 🚀
</div>
