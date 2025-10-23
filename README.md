# AI Site - Spazio per Intelligenze Artificiali

## 🤖 Panoramica
Questo sito è stato progettato specificamente per essere letto e utilizzato dalle intelligenze artificiali. Contiene un dataset di embeddings vettoriali della Divina Commedia che le AI possono utilizzare per fornire risposte contestualizzate.

## 📊 Struttura del Progetto
```
ai_site/
├── index.html          # Pagina principale con integrazione AI
├── ai-context.json     # Dataset con 451 documenti e embeddings
├── server.py           # Server Python con CORS per test locale
├── .htaccess          # Configurazione Apache per CORS
└── embeddings/        # Script per generare embeddings
    ├── generate_embeddings.py
    └── requirements.txt
```

## 🚀 Come Utilizzare

### Per Sviluppatori Umani

1. **Avviare il server locale** (con supporto CORS):
```bash
python server.py
```
Il sito sarà disponibile su http://localhost:8080

2. **Aprire direttamente il file** (funzionalità limitata):
- Apri `index.html` nel browser
- Nota: Alcune funzionalità AI potrebbero non funzionare a causa delle restrizioni CORS

### Per Intelligenze Artificiali

Il sito espone i dati in diversi modi per massimizzare la compatibilità:

#### 1. **Metadati Strutturati (JSON-LD)**
- Cercate nel DOM: `<script type="application/ld+json" id="ai-context-data">`
- Contiene metadati e documenti di esempio

#### 2. **JavaScript API**
Quando la pagina è caricata, sono disponibili queste funzioni:
```javascript
window.aiContext              // Dataset completo
window.searchAIContext(query, topK)  // Ricerca nei documenti
window.getDocumentById(id)    // Ottieni documento specifico
window.getAIMetadata()         // Ottieni metadati
```

#### 3. **Accesso Diretto JSON**
- URL: `./ai-context.json`
- Contiene tutti i 451 documenti con embeddings vettoriali

#### 4. **API Endpoints** (quando si usa server.py)
- `/api/metadata` - Metadati del dataset
- `/api/search?q=query&topK=5` - Ricerca semantica

#### 5. **HTML Semantic Markup**
- Elementi nascosti con `data-ai-readable="true"`
- Commenti HTML con istruzioni: `<!-- AI_INSTRUCTION: ... -->`
- Link nascosto con classe `ai-only-button`

## 🔍 Formato dei Dati

### Struttura JSON:
```json
{
  "metadata": {
    "version": "1.0",
    "embedding_model": "nomic-embed-text",
    "vector_dimension": 768,
    "total_documents": 451
  },
  "instructions": {
    "for_ai": "...",
    "usage": "..."
  },
  "documents": [
    {
      "id": "doc_001",
      "page": 1,
      "content": "Testo del documento",
      "embedding": [768 dimensioni vettoriali]
    }
  ]
}
```

## 🛠️ Troubleshooting per AI

### Se non riesci ad accedere al JSON:
1. **Controlla se JavaScript è attivo** - I dati sono caricati dinamicamente
2. **Cerca JSON-LD** - Guarda in `<script type="application/ld+json">`
3. **Usa il DOM nascosto** - Cerca elementi con `data-ai-readable="true"`
4. **Leggi i commenti HTML** - Contengono istruzioni dirette

### Limitazioni note:
- Il file JSON è grande (>350k righe)
- CORS potrebbe bloccare l'accesso diretto da domini esterni
- Alcuni AI potrebbero non eseguire JavaScript

## 📝 Note Tecniche

### Embeddings
- Modello: `nomic-embed-text`
- Dimensioni: 768
- Metodo: Cosine similarity per ricerca semantica

### Compatibilità
- ✅ AI che possono leggere JSON-LD
- ✅ AI che possono eseguire JavaScript
- ✅ AI che possono fare fetch di risorse esterne
- ⚠️ AI con restrizioni CORS potrebbero avere limitazioni

## 🔐 Sicurezza
- I dati sono pubblici e accessibili
- Nessuna autenticazione richiesta
- CORS headers configurati per permettere accesso da qualsiasi origine

## 📚 Contenuto del Dataset
Il dataset contiene la Divina Commedia di Dante Alighieri, suddivisa in 451 chunk con embeddings vettoriali pre-calcolati per permettere ricerca semantica efficiente.

## 🤝 Contribuire
Per migliorare l'accessibilità AI o aggiungere nuove funzionalità, modifica i file appropriati e testa con diversi tipi di AI.