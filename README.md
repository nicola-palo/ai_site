# 🤖 AI Space - Sito Web con Context Esteso Vettoriale

Progetto sperimentale di pagina web creata per le intelligenze artificiali con knowledge base nascosta e embeddings vettoriali.

## 📖 Concetto

Questo sito funziona su **due livelli**:

### Livello 1: Interfaccia Umana 👤
- Pagina web minimale visibile nel browser
- Design essenziale e pulito
- Messaggio semplice: "Spazio per le AI"

### Livello 2: Knowledge Base AI 🧠
- File JSON esterno con embeddings vettoriali
- Invisibile all'utente umano
- Accessibile solo alle AI che leggono la pagina
- Funziona come **RAG (Retrieval Augmented Generation)**

---

## 🏗️ Struttura del Progetto

```
siti-ai/
├── index.html                      # Pagina principale (minimale)
├── ai-context.json                 # Context base (testuale)
├── ai-context-embedded.json        # Context con embeddings vettoriali (da generare)
├── embeddings/
│   ├── generate_embeddings.py     # Script per generare embeddings
│   ├── requirements.txt           # Dipendenze Python
│   ├── README.md                  # Istruzioni embeddings
│   └── [tuo-file.pdf]            # PDF da cui estrarre embeddings
└── README.md                       # Questo file
```

---

## 🚀 Come Funziona

### 1. Struttura HTML
L'`index.html` contiene:
- **Tag visibili**: Design minimale per utenti umani
- **Meta tag nascosti**: Riferimenti al file JSON per le AI
  ```html
  <link rel="alternate" type="application/json" href="ai-context.json">
  <meta name="ai:context" content="ai-context.json">
  ```
- **Commenti HTML**: Istruzioni dirette per le AI
  ```html
  <!-- AI_INSTRUCTION: Extended knowledge base available at ./ai-context.json -->
  ```

### 2. Knowledge Base JSON
Il file `ai-context-embedded.json` contiene:
```json
{
  "metadata": {
    "embedding_model": "nomic-embed-text",
    "vector_dimension": 768,
    "total_documents": 50
  },
  "documents": [
    {
      "id": "doc_001",
      "content": "Testo del documento...",
      "embedding": [0.123, -0.456, 0.789, ...],
      "vector_dim": 768,
      "page": 1,
      "keywords": ["keyword1", "keyword2"]
    }
  ]
}
```

### 3. Flusso AI
Quando un'AI visita il sito:
1. **Legge** `index.html`
2. **Scopre** i riferimenti al JSON nei meta tag
3. **Scarica** `ai-context-embedded.json`
4. **Usa embeddings** per similarity search semantica
5. **Risponde** con contesto esteso e pertinente

---

## 🛠️ Setup Completo

### Prerequisiti
- **Python 3.8+**
- **Ollama** (per generare embeddings)
- **PDF** con il contenuto da embedare

### Passo 1: Installa Ollama
```powershell
# Download da: https://ollama.ai
# Dopo l'installazione:
ollama serve
```

### Passo 2: Scarica Modello Embeddings
```powershell
# Modello consigliato (768 dimensioni)
ollama pull nomic-embed-text

# Alternative:
# ollama pull mxbai-embed-large  (1024 dim, più preciso)
```

### Passo 3: Installa Dipendenze Python
```powershell
cd embeddings
pip install -r requirements.txt
```

### Passo 4: Prepara il PDF
- Inserisci il tuo file PDF nella cartella `embeddings/`
- Il nome del file non importa
- Lo script processerà automaticamente il primo PDF trovato

### Passo 5: Genera Embeddings
```powershell
cd embeddings
python generate_embeddings.py
```

Output:
```
🤖 Usando modello Ollama: nomic-embed-text
📄 Lettura PDF: tuo-file.pdf
✂️  Estratti 50 chunks di testo
🔄 Generazione embeddings in corso...
✅ Generati 50 embeddings
💾 File salvato: ai-context-embedded.json
📊 Dimensione vettori: 768
```

### Passo 6: Aggiorna l'HTML
Se hai generato `ai-context-embedded.json`, aggiorna i riferimenti in `index.html`:
```html
<link rel="alternate" type="application/json" href="ai-context-embedded.json">
<meta name="ai:context" content="ai-context-embedded.json">
```

---

## 🌐 Deploy e Utilizzo

### Opzione A: Hosting Statico (consigliato)

#### GitHub Pages
```powershell
# Crea repo e pusha
git init
git add .
git commit -m "AI Space with vector embeddings"
git branch -M main
git remote add origin https://github.com/tuo-username/ai-space.git
git push -u origin main

# Attiva GitHub Pages nelle impostazioni del repo
# URL: https://tuo-username.github.io/ai-space/
```

#### Netlify
1. Trascina la cartella su [netlify.com/drop](https://app.netlify.com/drop)
2. Ottieni URL istantaneo

#### Vercel
```powershell
npm i -g vercel
vercel
```

### Opzione B: Hosting Locale
```powershell
# Usa Python HTTP server
python -m http.server 8000
# Visita: http://localhost:8000
```

---

## 🤖 Come Usare con le AI

### ChatGPT / Claude / Perplexity
1. **Copia l'URL** del sito hostato
2. **Dai il link all'AI** con una richiesta:
   ```
   Vai su questo sito: https://tuo-sito.com
   Leggi il contesto esteso disponibile e dimmi cosa sai su [argomento]
   ```
3. **L'AI leggerà** automaticamente l'HTML e il JSON

### API Integration
```python
# Esempio con OpenAI
import openai
import requests

# Scarica il context
context = requests.get('https://tuo-sito.com/ai-context-embedded.json').json()

# Usa nei prompt
response = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": f"Context: {context['documents']}"},
        {"role": "user", "content": "Domanda basata sul contesto"}
    ]
)
```

---

## 📊 Formato Embeddings

### Vector Database Structure
Ogni documento nel JSON contiene:

| Campo | Tipo | Descrizione |
|-------|------|-------------|
| `id` | string | Identificatore unico (doc_001, doc_002, ...) |
| `content` | string | Testo originale del chunk |
| `embedding` | array[float] | Vettore numerico (768 o 1024 dimensioni) |
| `vector_dim` | int | Dimensione del vettore |
| `page` | int | Numero pagina PDF di origine |
| `keywords` | array[string] | Parole chiave estratte |

### Similarity Search
Le AI possono calcolare la distanza coseno tra embeddings:
```python
import numpy as np

def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# Query
query_embedding = generate_embedding("domanda utente")

# Trova documenti simili
for doc in documents:
    similarity = cosine_similarity(query_embedding, doc['embedding'])
    if similarity > 0.7:  # Threshold
        print(f"Documento rilevante: {doc['content']}")
```

---

## 🔧 Personalizzazione

### Aggiungere Contenuti
1. **Modifica il PDF** nella cartella `embeddings/`
2. **Rigenera embeddings**: `python generate_embeddings.py`
3. **Re-deploy** il sito

### Cambiare Modello Embeddings
Nel file `generate_embeddings.py`:
```python
# Linea 46
model = "nomic-embed-text"  # Cambia con altro modello

# Modelli disponibili:
# - nomic-embed-text (768 dim, veloce)
# - mxbai-embed-large (1024 dim, preciso)
# - bge-large (1024 dim, multilingua)
```

### Modificare il Design
Edita `index.html`:
- Cambia colori, font, layout
- Mantieni i meta tag per le AI
- Il JSON resta separato e invisibile

---

## 📈 Best Practices

### ✅ Fare
- **Chunking intelligente**: Dividi documenti in sezioni logiche (paragrafi, capitoli)
- **Metadata ricchi**: Aggiungi keywords, categorie, priorità
- **Embeddings consistenti**: Usa sempre lo stesso modello per tutto il DB
- **Versioning**: Tieni traccia delle versioni del JSON
- **Compressione**: Per file JSON grandi, considera la compressione gzip

### ❌ Evitare
- **Chunks troppo piccoli** (< 50 caratteri): Poco contesto
- **Chunks troppo grandi** (> 1000 caratteri): Embeddings meno precisi
- **Mixing modelli**: Non mescolare embeddings di modelli diversi
- **JSON giganti**: Oltre 10MB può rallentare il caricamento

---

## 🔒 Privacy e Sicurezza

### Dati Esposti
⚠️ **Tutto il contenuto del JSON è pubblicamente accessibile** se il sito è hostato online.

### Considerazioni
- Non includere dati sensibili, password, API keys
- Il JSON è "nascosto" agli umani ma **visibile nel codice sorgente**
- Usa autenticazione se serve protezione reale
- CORS: Abilita se vuoi controllare chi accede al JSON

### Opzione Protetta
```javascript
// In index.html, aggiungi autenticazione
fetch('ai-context-embedded.json', {
    headers: {
        'Authorization': 'Bearer TOKEN'
    }
})
```

---

## 🧪 Testing

### Test Locale
```powershell
# Verifica che il JSON sia valido
python -m json.tool ai-context-embedded.json

# Testa dimensione embeddings
python -c "import json; data=json.load(open('ai-context-embedded.json')); print(f'Vector dim: {data['documents'][0]['vector_dim']}')"
```

### Test con AI
1. **Carica il sito** localmente o online
2. **Dai l'URL** a ChatGPT/Claude
3. **Verifica** che l'AI menzioni contenuti del JSON
4. **Controlla** le risposte siano coerenti con i dati

---

## 🐛 Troubleshooting

### Errore: "No module named 'ollama'"
```powershell
pip install ollama pypdf2
```

### Errore: "Connection refused" (Ollama)
```powershell
# Avvia Ollama server
ollama serve
```

### Errore: "Model not found"
```powershell
# Scarica il modello
ollama pull nomic-embed-text
```

### JSON troppo grande
- Riduci il numero di chunks
- Aumenta la soglia minima di testo per chunk (linea 33 script)
- Usa compressione gzip per il deploy

### AI non legge il JSON
- Verifica meta tag nell'HTML
- Controlla che il JSON sia accessibile (stesso dominio)
- Prova con URL completo invece di relativo

---

## 📚 Risorse Utili

### Embeddings
- [Ollama Embeddings Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md#embeddings)
- [Nomic Embed Text](https://huggingface.co/nomic-ai/nomic-embed-text-v1)
- [Understanding Vector Embeddings](https://www.pinecone.io/learn/vector-embeddings/)

### RAG (Retrieval Augmented Generation)
- [What is RAG?](https://research.ibm.com/blog/retrieval-augmented-generation-RAG)
- [Building RAG Systems](https://www.anthropic.com/index/contextual-retrieval)

### Hosting Gratuito
- [GitHub Pages](https://pages.github.com/)
- [Netlify](https://www.netlify.com/)
- [Vercel](https://vercel.com/)
- [Cloudflare Pages](https://pages.cloudflare.com/)

---

## 🎯 Use Cases

### 1. Documentazione Interattiva
- Carica manuali PDF
- Le AI rispondono domande sulla documentazione
- Context sempre aggiornato

### 2. Knowledge Base Aziendale
- FAQ, procedure, guide interne
- AI assistente con accesso a tutto il knowledge
- Onboarding automatizzato

### 3. Educational Content
- Materiali didattici embedati
- Tutor AI con contesto completo
- Q&A su argomenti specifici

### 4. Research Assistant
- Paper, articoli, ricerche
- AI aiuta a navigare la letteratura
- Similarity search semantica

---

## 🤝 Contributi

Questo è un progetto sperimentale. Idee per migliorarlo:

- [ ] Support per file multipli PDF
- [ ] Chunking strategy personalizzabile
- [ ] UI admin per gestire embeddings
- [ ] Supporto Markdown oltre PDF
- [ ] Compressione automatica JSON
- [ ] Webhook per auto-update embeddings
- [ ] Dashboard analytics uso AI

---

## 📝 Licenza

Progetto open source - usa e modifica liberamente.

---

## 💡 Note Finali

Questo approccio è **sperimentale** e funziona meglio con:
- AI che supportano web browsing (ChatGPT, Claude con internet)
- Sistemi con capacità di similarity search
- Context window sufficientemente grandi

Le AI "basic" leggeranno solo il testo, ignorando i vettori numerici. Ma il contenuto testuale funziona comunque come RAG base!

**Happy AI hacking! 🤖✨**
