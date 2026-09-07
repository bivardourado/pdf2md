import os
import streamlit as st
import pymupdf4llm

def count_words(text: str) -> int:
    """Conta as palavras de um texto."""
    return len(text.split())

def chunk_markdown_smart(text: str, max_words: int = 450000, margin: int = 50000) -> list[str]:
    """
    Divide o Markdown de forma inteligente baseando-se em tags de título (# ou ##).
    O corte preferencialmente ocorre quando o bloco atinge (max_words - margin) palavras 
    e encontramos um novo título. Se atingir max_words sem achar um título, corta de forma segura.
    """
    lines = text.split('\n')
    chunks = []
    current_chunk_lines = []
    current_word_count = 0
    
    threshold = max_words - margin if max_words > margin else max_words
    
    for line in lines:
        line_words = count_words(line)
        
        is_heading = line.strip().startswith('# ') or line.strip().startswith('## ')
        
        # Se ultrapassou o limite máximo absoluto ou 
        # (se está acima do threshold e achamos um heading)
        if (current_word_count + line_words > max_words) or (current_word_count > threshold and is_heading):
            if current_chunk_lines:
                chunks.append('\n'.join(current_chunk_lines))
                current_chunk_lines = []
                current_word_count = 0
        
        current_chunk_lines.append(line)
        current_word_count += line_words
        
    # Adiciona o restante
    if current_chunk_lines:
        chunks.append('\n'.join(current_chunk_lines))
        
    return chunks

def main():
    st.set_page_config(
        page_title="pdf2md - Conversor Inteligente", 
        page_icon="📄", 
        layout="centered"
    )

    st.title("📄 pdf2md")
    st.subheader("Conversor Inteligente de PDF/DOCX para Markdown")
    st.write("Extraia o texto de documentos grandes mantendo a estrutura (títulos, listas, tabelas) pronta para LLMs e Google Gemini Notebook.")

    uploaded_files = st.file_uploader("Escolha um ou mais arquivos PDF ou DOCX", type=["pdf", "docx"], accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            with st.expander(f"📄 {uploaded_file.name}", expanded=True):
                temp_filename = f"temp_{uploaded_file.name}"
                
                # Salvar o arquivo temporário
                try:
                    with open(temp_filename, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                        
                    md_text = ""
                    
                    if uploaded_file.name.lower().endswith('.pdf'):
                        import pymupdf
                        with st.spinner(f"🔄 Extraindo texto de {uploaded_file.name}..."):
                            doc = pymupdf.open(temp_filename)
                            num_pages = len(doc)
                            
                        progress_bar = st.progress(0, text=f"Convertendo página 0 de {num_pages} (0%)")
                        
                        for i in range(num_pages):
                            md_text += pymupdf4llm.to_markdown(doc, pages=[i])
                            progress = (i + 1) / num_pages
                            progress_bar.progress(progress, text=f"Convertendo página {i+1} de {num_pages} ({int(progress * 100)}%)")
                            
                        doc.close()
                        progress_bar.empty() # Remove a barra ao finalizar
                    
                    elif uploaded_file.name.lower().endswith('.docx'):
                        import mammoth
                        import markdownify
                        with st.spinner(f"🔄 Extraindo texto de {uploaded_file.name}..."):
                            with open(temp_filename, "rb") as docx_file:
                                result = mammoth.convert_to_html(docx_file)
                                html = result.value
                                md_text = markdownify.markdownify(html, heading_style="ATX")
                                
                    word_count = count_words(md_text)
                    
                    st.success("✅ Conversão concluída com sucesso!")
                    
                    col1, col2 = st.columns(2)
                    col1.metric(label="Total de Palavras", value=f"{word_count:,}")
                    
                    GEMINI_NOTEBOOK_LIMIT = 450000 # Margem de segurança pro limite de 500k
                    base_name, _ = os.path.splitext(uploaded_file.name)
                    
                    if word_count <= GEMINI_NOTEBOOK_LIMIT:
                        col2.metric(label="Status Gemini Notebook", value="Aprovado (1 arquivo)")
                        
                        st.download_button(
                            label="📥 Baixar Arquivo .md Único",
                            data=md_text,
                            file_name=f"{base_name}.md",
                            mime="text/markdown",
                            key=f"dl_single_{uploaded_file.name}"
                        )
                    else:
                        col2.metric(label="Status Gemini Notebook", value="Requer Divisão", delta="- Limite Excedido", delta_color="inverse")
                        st.warning(f"⚠️ O arquivo possui {word_count:,} palavras. Será dividido inteligentemente mantendo capítulos e títulos agrupados.")
                        
                        chunks = chunk_markdown_smart(md_text, max_words=GEMINI_NOTEBOOK_LIMIT)
                        
                        st.write("### Arquivos Gerados:")
                        for idx, chunk in enumerate(chunks, 1):
                            chunk_words = count_words(chunk)
                            st.download_button(
                                label=f"📥 Baixar Parte {idx} ({chunk_words:,} palavras)",
                                data=chunk,
                                file_name=f"{base_name}_parte_{idx}.md",
                                key=f"dl_part_{uploaded_file.name}_{idx}",
                                mime="text/markdown"
                            )
                            
                except Exception as e:
                    st.error(f"Erro ao processar o arquivo {uploaded_file.name}: {e}")
                    
                finally:
                    if os.path.exists(temp_filename):
                        try:
                            os.remove(temp_filename)
                        except Exception as cleanup_error:
                            st.warning(f"Não foi possível remover o arquivo temporário: {cleanup_error}")

if __name__ == "__main__":
    main()
