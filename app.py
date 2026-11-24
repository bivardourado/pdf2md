import io
import os
import zipfile
import streamlit as st
import pymupdf
import pymupdf4llm
import mammoth
import markdownify

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
        
        if (current_word_count + line_words > max_words) or (current_word_count > threshold and is_heading):
            if current_chunk_lines:
                chunks.append('\n'.join(current_chunk_lines))
                current_chunk_lines = []
                current_word_count = 0
        
        current_chunk_lines.append(line)
        current_word_count += line_words
        
    if current_chunk_lines:
        chunks.append('\n'.join(current_chunk_lines))
        
    return chunks

def convert_pdf_to_md(file_bytes: bytes) -> str:
    """Converte PDF diretamente da memória para Markdown."""
    doc = pymupdf.open(stream=file_bytes, filetype="pdf")
    md_text = pymupdf4llm.to_markdown(doc)
    doc.close()
    return md_text

def convert_docx_to_md(file_bytes: bytes) -> str:
    """Converte DOCX diretamente da memória para Markdown."""
    docx_stream = io.BytesIO(file_bytes)
    result = mammoth.convert_to_html(docx_stream)
    html = result.value
    md_text = markdownify.markdownify(html, heading_style="ATX")
    return md_text

def create_zip_archive(files_data: dict[str, str]) -> io.BytesIO:
    """Cria um arquivo .ZIP em memória contendo todos os arquivos .md."""
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for file_name, text_content in files_data.items():
            zip_file.writestr(file_name, text_content)
    zip_buffer.seek(0)
    return zip_buffer

def main():
    st.set_page_config(
        page_title="pdf2md - Conversor Inteligente", 
        page_icon="📄", 
        layout="centered"
    )

    st.title("📄 pdf2md")
    st.subheader("Conversor Inteligente de PDF/DOCX para Markdown")
    st.write("Extraia o texto de documentos grandes mantendo a formatação e estrutura prontas para LLMs e Google Gemini Notebook.")

    uploaded_files = st.file_uploader(
        "Escolha um ou mais arquivos PDF ou DOCX", 
        type=["pdf", "docx"], 
        accept_multiple_files=True
    )

    if uploaded_files:
        st.write(f"📁 **Total de arquivos selecionados:** `{len(uploaded_files)}`")
        
        converted_files: dict[str, str] = {}
        GEMINI_NOTEBOOK_LIMIT = 450000

        with st.spinner("⚡ Processando e convertendo arquivos em memória..."):
            for uploaded_file in uploaded_files:
                base_name, ext = os.path.splitext(uploaded_file.name)
                ext = ext.lower()
                file_bytes = uploaded_file.getvalue()
                
                try:
                    if ext == '.pdf':
                        md_text = convert_pdf_to_md(file_bytes)
                    elif ext == '.docx':
                        md_text = convert_docx_to_md(file_bytes)
                    else:
                        continue

                    word_count = count_words(md_text)

                    # Verifica limite do Gemini Notebook
                    if word_count <= GEMINI_NOTEBOOK_LIMIT:
                        converted_files[f"{base_name}.md"] = md_text
                    else:
                        chunks = chunk_markdown_smart(md_text, max_words=GEMINI_NOTEBOOK_LIMIT)
                        for idx, chunk in enumerate(chunks, 1):
                            converted_files[f"{base_name}_parte_{idx}.md"] = chunk
                            
                except Exception as e:
                    st.error(f"Erro ao converter `{uploaded_file.name}`: {e}")

        # Se houver múltiplos arquivos convertidos, exibe o botão Mestre de Download ZIP
        if len(converted_files) > 1:
            st.success(f"🎉 **{len(uploaded_files)} arquivo(s)** processados com sucesso! Gerados `{len(converted_files)}` arquivos .md.")
            
            zip_data = create_zip_archive(converted_files)
            st.download_button(
                label=f"📦 Baixar TODOS os arquivos em um único .ZIP ({len(converted_files)} arquivos)",
                data=zip_data,
                file_name="discursos_markdown.zip",
                mime="application/zip",
                type="primary",
                use_container_width=True
            )
            st.markdown("---")
        elif len(converted_files) == 1:
            st.success("✅ Conversão concluída com sucesso!")

        # Exibição individual dos arquivos
        st.write("### 📂 Arquivos Convertidos:")
        for file_name, text_content in converted_files.items():
            words = count_words(text_content)
            with st.expander(f"📄 {file_name} ({words:,} palavras)", expanded=(len(converted_files) == 1)):
                st.download_button(
                    label=f"📥 Baixar {file_name}",
                    data=text_content,
                    file_name=file_name,
                    mime="text/markdown",
                    key=f"dl_{file_name}"
                )

if __name__ == "__main__":
    main()
