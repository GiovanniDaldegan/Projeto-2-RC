#!/bin/bash

# Script para compilar e validar o documento LaTeX main.tex
# Autor: ChatWeb 2.0 Project
# Data: 7 de junho de 2025

set -e  # Sair em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Diretórios
LATEX_DIR="latex"
MAIN_TEX="main.tex"
MAIN_PDF="main.pdf"
LOG_FILE="main.log"
AUX_FILE="main.aux"

# Função para limpar arquivos auxiliares
cleanup_aux_files() {
    echo -e "${YELLOW}🧹 Limpando arquivos auxiliares...${NC}"
    rm -f *.aux *.log *.out *.toc *.lof *.lot *.bbl *.blg *.fls *.fdb_latexmk *.synctex.gz
}

# Função para verificar dependências
check_dependencies() {
    echo -e "${BLUE}🔍 Verificando dependências...${NC}"
    
    if ! command -v pdflatex &> /dev/null; then
        echo -e "${RED}❌ pdflatex não encontrado! Instale texlive-basic.${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ pdflatex encontrado${NC}"
}

# Função para compilar o documento
compile_document() {
    echo -e "${BLUE}⚙️  Compilando documento LaTeX...${NC}"
    
    # Primeira compilação
    echo -e "${YELLOW}📝 Primeira compilação...${NC}"
    if pdflatex -interaction=nonstopmode "$MAIN_TEX" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Primeira compilação concluída${NC}"
    else
        echo -e "${RED}❌ Erro na primeira compilação!${NC}"
        show_errors
        return 1
    fi
    
    # Segunda compilação (para resolver referências)
    echo -e "${YELLOW}📝 Segunda compilação (referências)...${NC}"
    if pdflatex -interaction=nonstopmode "$MAIN_TEX" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Segunda compilação concluída${NC}"
    else
        echo -e "${RED}❌ Erro na segunda compilação!${NC}"
        show_errors
        return 1
    fi
}

# Função para mostrar erros do log
show_errors() {
    if [ -f "$LOG_FILE" ]; then
        echo -e "${RED}📋 Erros encontrados no log:${NC}"
        grep -n "^!" "$LOG_FILE" | head -10
        echo -e "\n${YELLOW}💡 Verifique o arquivo $LOG_FILE para detalhes completos.${NC}"
    fi
}

# Função para mostrar avisos importantes
show_warnings() {
    if [ -f "$LOG_FILE" ]; then
        echo -e "${YELLOW}⚠️  Verificando avisos importantes...${NC}"
        
        # Contar underfull/overfull boxes
        underfull_count=$(grep -c "Underfull" "$LOG_FILE" 2>/dev/null || echo "0")
        overfull_count=$(grep -c "Overfull" "$LOG_FILE" 2>/dev/null || echo "0")
        
        if [ "$underfull_count" -gt 0 ] || [ "$overfull_count" -gt 0 ]; then
            echo -e "${YELLOW}📏 Problemas de formatação encontrados:${NC}"
            echo -e "   • Underfull boxes: $underfull_count"
            echo -e "   • Overfull boxes: $overfull_count"
            echo -e "${YELLOW}💡 Estes avisos são geralmente cosméticos e não impedem a geração do PDF.${NC}"
        fi
        
        # Verificar citações indefinidas
        if grep -q "Citation.*undefined" "$LOG_FILE"; then
            echo -e "${YELLOW}📚 Citações indefinidas encontradas. Execute bibtex se necessário.${NC}"
        fi
        
        # Verificar referências indefinidas
        if grep -q "Reference.*undefined" "$LOG_FILE"; then
            echo -e "${YELLOW}🔗 Referências indefinidas encontradas.${NC}"
        fi
    fi
}

# Função para validar o PDF gerado
validate_pdf() {
    echo -e "${BLUE}🔍 Validando PDF gerado...${NC}"
    
    if [ ! -f "$MAIN_PDF" ]; then
        echo -e "${RED}❌ PDF não foi gerado!${NC}"
        return 1
    fi
    
    # Verificar tamanho do arquivo
    pdf_size=$(stat -f%z "$MAIN_PDF" 2>/dev/null || stat -c%s "$MAIN_PDF" 2>/dev/null)
    if [ "$pdf_size" -lt 1000 ]; then
        echo -e "${RED}❌ PDF parece estar corrompido (muito pequeno: ${pdf_size} bytes)${NC}"
        return 1
    fi
    
    # Verificar se é um PDF válido
    if command -v file &> /dev/null; then
        if file "$MAIN_PDF" | grep -q "PDF"; then
            echo -e "${GREEN}✅ PDF válido gerado: ${pdf_size} bytes${NC}"
        else
            echo -e "${RED}❌ Arquivo gerado não é um PDF válido${NC}"
            return 1
        fi
    else
        echo -e "${GREEN}✅ PDF gerado: ${pdf_size} bytes${NC}"
    fi
    
    # Contar páginas se possível
    if command -v pdfinfo &> /dev/null; then
        pages=$(pdfinfo "$MAIN_PDF" 2>/dev/null | grep "Pages:" | awk '{print $2}')
        if [ -n "$pages" ]; then
            echo -e "${GREEN}📄 Número de páginas: $pages${NC}"
        fi
    fi
}

# Função para mostrar estatísticas
show_statistics() {
    echo -e "\n${BLUE}📊 Estatísticas do documento:${NC}"
    
    if [ -f "$MAIN_TEX" ]; then
        lines=$(wc -l < "$MAIN_TEX")
        words=$(wc -w < "$MAIN_TEX")
        chars=$(wc -c < "$MAIN_TEX")
        
        echo -e "   • Linhas: $lines"
        echo -e "   • Palavras: $words"
        echo -e "   • Caracteres: $chars"
    fi
    
    if [ -f "$MAIN_PDF" ]; then
        pdf_size=$(stat -f%z "$MAIN_PDF" 2>/dev/null || stat -c%s "$MAIN_PDF" 2>/dev/null)
        pdf_size_kb=$((pdf_size / 1024))
        echo -e "   • Tamanho do PDF: ${pdf_size_kb}KB"
    fi
}

# Função principal
main() {
    # Verificar dependências
    check_dependencies
    
    # Limpar arquivos auxiliares antigos
    cleanup_aux_files
    
    # Compilar documento
    if compile_document; then
        echo -e "\n${GREEN}🎉 Compilação concluída com sucesso!${NC}"
        
        # Validar PDF
        if validate_pdf; then
            # Mostrar avisos
            show_warnings
            
            # Mostrar estatísticas
            show_statistics
            
            echo -e "\n${GREEN}✅ Processo concluído! PDF disponível em: $LATEX_DIR/$MAIN_PDF${NC}"
            
            # Sugerir visualização
            echo -e "\n${BLUE}💡 Para visualizar o PDF:${NC}"
            echo -e "   xdg-open $LATEX_DIR/$MAIN_PDF"
            echo -e "   ou"
            echo -e "   evince $LATEX_DIR/$MAIN_PDF"
            
        else
            echo -e "\n${RED}❌ Falha na validação do PDF${NC}"
            exit 1
        fi
    else
        echo -e "\n${RED}❌ Falha na compilação${NC}"
        exit 1
    fi
}

echo -e "${BLUE}=== ChatWeb 2.0 - Compilador LaTeX ===${NC}"
echo -e "Data: $(date)"
echo -e "Diretório: $(pwd)\n"

# Verificar argumentos da linha de comando primeiro
case "${1:-}" in
    --clean)
        echo -e "${YELLOW}🧹 Modo limpeza: removendo arquivos auxiliares...${NC}"
        # Verificar se o diretório latex existe
        if [ ! -d "$LATEX_DIR" ]; then
            echo -e "${RED}❌ Erro: Diretório '$LATEX_DIR' não encontrado!${NC}"
            exit 1
        fi
        # Mudar para o diretório latex
        cd "$LATEX_DIR"
        cleanup_aux_files
        echo -e "${GREEN}✅ Limpeza concluída${NC}"
        exit 0
        ;;
    --help|-h)
        echo -e "${BLUE}ChatWeb 2.0 - Compilador LaTeX${NC}"
        echo -e "\nUso: $0 [opção]"
        echo -e "\nOpções:"
        echo -e "  (sem argumentos)  Compilar e validar o documento"
        echo -e "  --clean          Limpar arquivos auxiliares"
        echo -e "  --help, -h       Mostrar esta ajuda"
        exit 0
        ;;
    "")
        # Continuar com a compilação normal
        ;;
    *)
        echo -e "${RED}❌ Opção inválida: $1${NC}"
        echo -e "Use '$0 --help' para ver as opções disponíveis."
        exit 1
        ;;
esac

# Verificar se o diretório latex existe
if [ ! -d "$LATEX_DIR" ]; then
    echo -e "${RED}❌ Erro: Diretório '$LATEX_DIR' não encontrado!${NC}"
    exit 1
fi

# Mudar para o diretório latex
cd "$LATEX_DIR"

# Verificar se o arquivo main.tex existe
if [ ! -f "$MAIN_TEX" ]; then
    echo -e "${RED}❌ Erro: Arquivo '$MAIN_TEX' não encontrado!${NC}"
    exit 1
fi

echo -e "${BLUE}📄 Arquivo encontrado: $MAIN_TEX${NC}"

# Executar função principal (só chega aqui se não foi --clean ou --help)
main
