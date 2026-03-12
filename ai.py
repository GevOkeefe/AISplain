from llama_cpp import Llama
import logging
import os

class AIDoc:

    def __init__(self, doc):
        self.llm = Llama(
            model_path='model/your_model_name',
            n_ctx=32192,  # Context window
            n_threads=16,  # CPU threads
            n_gpu_layers=-1,  # Set to -1 for GPU acceleration if available
            verbose=False
        )
        self.conversation_history = []
        self.doc_store = doc
        self.document_context = ""
        self.documents_loaded = False

    def load_documents(self, file_paths):
        """Load multiple documents"""
        if isinstance(file_paths, str):
            file_paths = [file_paths]

        for path in file_paths:
            if os.path.exists(path):
                self.doc_store.load_document(path)
            else:
                logging.error(f"File not found: {path}")

        with open('a.txt', 'w', encoding='utf-8') as f:
            for chunk in self.doc_store.chunks:
                f.write(chunk)
        if self.doc_store.chunks:
            self.doc_store.build_index()
            self.documents_loaded = True

    def chat(self, user_message, max_tokens=512, temperature=1.2, stream=True):
        context = ""

        # Retrieve relevant document chunks if available
        if self.doc_store.index is not None:
            results = self.doc_store.search(user_message, k=3)

            if results:
                context = "Relevant information from documents:\n\n"
                for i, result in enumerate(results, 1):
                    context += f"[{i}] {result['text']}...\n\n"
                context += "---\n\n"

        # Build prompt from conversation history
        prompt = self._build_prompt(user_message, context)
        logging.error(prompt)

        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        self._trim_history()

        if stream:
            return self._chat_stream(prompt, max_tokens, temperature)

        # Generate response
        response = self.llm(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            stop=["User:", "\n\n\n"],
            echo=False
        )

        assistant_message = response["choices"][0]["text"].strip()

        return assistant_message

    def _build_prompt(self, user_message, context=''):
        """Build a prompt from conversation history"""
        prompt = "You are a helpful AI assistant. "

        if self.documents_loaded:
            prompt += "You have access to document knowledge. "

        prompt += "Respond clearly and concisely and make it as short as possible.\n\n"

        # Add permanent document context (only if documents are loaded)
        if self.documents_loaded and self.document_context:
            prompt += self.document_context

        if context:
            prompt += context

        if len(self.conversation_history) > 0:
            prompt += f"Previous messages:\n"
            for msg in self.conversation_history:
                if msg["role"] == "user":
                    prompt += f"User: {msg['content']}\n"
                else:
                    prompt += f"Assistant: {msg['content']}\n"

        prompt += f"Current message:\nUser: {user_message}\nAssistant:"

        return prompt

    def _trim_history(self):
        """Keep only the most recent conversation exchanges"""
        max_messages = 10

        if len(self.conversation_history) > max_messages:
            self.conversation_history = self.conversation_history[-max_messages:]

    def _chat_stream(self, prompt, max_tokens, temperature):
        """Generator for streaming responses"""
        full_response = ""

        # Stream tokens one by one
        for output in self.llm(
                prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                stop=["User:", "\n\n\n"],
                echo=False,
                stream=True
        ):
            token = output["choices"][0]["text"]
            full_response += token
            yield token

        self.conversation_history.append({
            "role": "assistant",
            "content": full_response
        })

    def show_sources(self, query):
        """Show document sources for a query"""
        results = self.doc_store.search(query, k=5)
        if not results:
            logging.error("No relevant documents found.")
            return

        logging.warning("\nTop relevant document chunks:")
        logging.warning("=" * 60)
        for i, result in enumerate(results, 1):
            logging.warning(f"\n[{i}] Source: {result['source']}")
            logging.warning(f"Score: {result['score']:.4f}")
            logging.warning(f"Text: {result['text'][:200]}...")
        logging.warning("=" * 60 + "\n")

    def reset(self):
        """Clear conversation history"""
        self.conversation_history = []
        logging.info("Conversation history cleared.\n")
