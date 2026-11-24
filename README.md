# 📄 pdf2md - Conversor Inteligente de PDF/DOCX para Markdown

Conversor moderno de documentos grandes (**PDF** e **DOCX**) para **Markdown (`.md`)** otimizado para Large Language Models (LLMs), Google NotebookLM e Gemini.

## ✨ Recursos
- 🚀 **100% In-Memory (`io.BytesIO`):** Nenhum arquivo é salvo em disco, garantindo velocidade, segurança e isolamento contra concorrência multiusuário.
- 📦 **Download em Lote (.ZIP):** Faça upload de dezenas ou centenas de arquivos de uma vez e baixe todos os `.md` compactados em um único clique.
- 🧠 **Smart Chunking (Divisão Inteligente):** Documentos gigantes (>450.000 palavras) são automaticamente fatiados em seções lógicas respeitando cabeçalhos de capítulos (`#` ou `##`).
- 📝 **Preservação de Estrutura:** Mantém tabelas, listas, ênfases e formatações prontas para IAs.

## 🛠️ Como rodar localmente

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar a aplicação
streamlit run app.py
```
