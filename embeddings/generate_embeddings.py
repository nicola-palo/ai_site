"""
Script per generare embeddings da file PDF usando Ollama
Genera un file JSON con embeddings vettoriali pronti per l'uso

Requisiti:
- pip install ollama pypdf2
- Ollama installato e in esecuzione (ollama serve)
- Un modello con supporto embeddings (es: nomic-embed-text, mxbai-embed-large)
"""

import json
import os
from pathlib import Path
from typing import List, Dict
import ollama
from PyPDF2 import PdfReader


class EmbeddingGenerator:
    def __init__(self, model_name: str = "nomic-embed-text"):
        """
        Inizializza il generatore di embeddings
        
        Args:
            model_name: Nome del modello Ollama da usare
                       - nomic-embed-text (consigliato, dimensione 768)
                       - mxbai-embed-large (dimensione 1024)
        """
        self.model_name = model_name
        print(f"🤖 Usando modello Ollama: {model_name}")
        
    def extract_text_from_pdf(self, pdf_path: str) -> List[str]:
        """Estrae il testo dal PDF e lo divide in chunks"""
        print(f"📄 Lettura PDF: {pdf_path}")
        reader = PdfReader(pdf_path)
        
        chunks = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text.strip():
                # Dividi per paragrafi/sezioni
                paragraphs = text.split('\n\n')
                for para in paragraphs:
                    clean_para = para.strip()
                    if len(clean_para) > 50:  # Ignora testi troppo corti
                        chunks.append({
                            "page": i + 1,
                            "content": clean_para
                        })
        
        print(f"✂️  Estratti {len(chunks)} chunks di testo")
        return chunks
    
    def generate_embedding(self, text: str) -> List[float]:
        """Genera embedding per un singolo testo usando Ollama"""
        try:
            response = ollama.embeddings(
                model=self.model_name,
                prompt=text
            )
            return response['embedding']
        except Exception as e:
            print(f"❌ Errore generazione embedding: {e}")
            return []
    
    def process_pdf(self, pdf_path: str, output_json: str = "ai-context-embedded.json"):
        """Processa il PDF e genera il file JSON con embeddings"""
        
        # Estrai chunks dal PDF
        chunks = self.extract_text_from_pdf(pdf_path)
        
        if not chunks:
            print("❌ Nessun testo estratto dal PDF")
            return
        
        # Genera embeddings per ogni chunk
        print(f"🔄 Generazione embeddings in corso...")
        embedded_documents = []
        
        for idx, chunk in enumerate(chunks, 1):
            print(f"   Processing {idx}/{len(chunks)}...", end='\r')
            
            embedding = self.generate_embedding(chunk['content'])
            
            if embedding:
                embedded_documents.append({
                    "id": f"doc_{idx:03d}",
                    "page": chunk['page'],
                    "content": chunk['content'],
                    "embedding": embedding,
                    "vector_dim": len(embedding),
                    "keywords": self._extract_keywords(chunk['content'])
                })
        
        print(f"\n✅ Generati {len(embedded_documents)} embeddings")
        
        # Crea la struttura JSON finale
        output_data = {
            "metadata": {
                "version": "1.0",
                "purpose": "AI Extended Context with Vector Embeddings",
                "source_file": os.path.basename(pdf_path),
                "embedding_model": self.model_name,
                "vector_dimension": embedded_documents[0]['vector_dim'] if embedded_documents else 0,
                "total_documents": len(embedded_documents),
                "encoding": "utf-8"
            },
            "instructions": {
                "for_ai": "Questo file contiene embeddings vettoriali. Usa similarity search per trovare contenuti rilevanti basandoti sulla query dell'utente.",
                "usage": "Calcola la distanza coseno tra query embedding e document embeddings per recuperare i chunk più pertinenti."
            },
            "documents": embedded_documents
        }
        
        # Salva il JSON
        output_path = Path(__file__).parent / output_json
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 File salvato: {output_path}")
        print(f"📊 Dimensione vettori: {output_data['metadata']['vector_dimension']}")
        
    def _extract_keywords(self, text: str, max_keywords: int = 5) -> List[str]:
        """Estrae keywords semplici dal testo (puoi migliorare con NLP)"""
        # Implementazione base: parole più lunghe
        words = text.lower().split()
        # Filtra parole comuni italiane
        stop_words = {'per', 'con', 'del', 'della', 'dei', 'delle', 'che', 'questo', 'questa', 'sono', 'essere'}
        keywords = [w for w in words if len(w) > 5 and w not in stop_words]
        return list(set(keywords))[:max_keywords]


def main():
    """Funzione principale"""
    print("=" * 60)
    print("🚀 Generatore Embeddings per AI Context")
    print("=" * 60)
    
    # Configura il modello
    model = "nomic-embed-text"  # Cambia se necessario
    
    # Cerca file PDF nella cartella corrente
    pdf_files = list(Path(__file__).parent.glob("*.pdf"))
    
    if not pdf_files:
        print("❌ Nessun file PDF trovato nella cartella 'embeddings'")
        print("   Inserisci un file PDF nella stessa cartella di questo script")
        return
    
    print(f"\n📁 File PDF trovati:")
    for i, pdf in enumerate(pdf_files, 1):
        print(f"   {i}. {pdf.name}")
    
    # Usa il primo PDF (o chiedi all'utente)
    pdf_path = pdf_files[0]
    print(f"\n✅ Processando: {pdf_path.name}")
    
    # Genera embeddings
    generator = EmbeddingGenerator(model_name=model)
    generator.process_pdf(str(pdf_path))
    
    print("\n✅ Processo completato!")
    print("📌 Prossimi passi:")
    print("   1. Copia 'ai-context-embedded.json' nella cartella principale del sito")
    print("   2. Aggiorna index.html per puntare al nuovo file JSON")


if __name__ == "__main__":
    main()
