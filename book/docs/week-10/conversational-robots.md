---
sidebar_position: 29
---

# Week 10: Conversational Robotics and Natural Language Interaction

Welcome to Week 10 of our Physical AI & Humanoid Robotics journey! This week, we'll explore conversational robotics, which enables robots to interact with humans through natural language. This capability is essential for creating intuitive, accessible robotic systems that can collaborate effectively with humans.

## Learning Objectives

By the end of this week, you will be able to:

1. Understand the architecture of conversational robotics systems
2. Implement speech recognition and synthesis for robots
3. Design natural language understanding pipelines
4. Create dialogue management systems for robots
5. Integrate language with robot actions and perception
6. Evaluate conversational robot performance and usability

## Introduction to Conversational Robotics

Conversational robotics combines natural language processing with robotic control to enable human-like interactions. This field encompasses several key components:

- **Automatic Speech Recognition (ASR)**: Converting speech to text
- **Natural Language Understanding (NLU)**: Interpreting user intent
- **Dialogue Management**: Maintaining conversation context
- **Natural Language Generation (NLG)**: Creating appropriate responses
- **Text-to-Speech (TTS)**: Converting text to speech
- **Action Execution**: Performing robot actions based on language commands

### Why Conversational Robotics Matters

Conversational interfaces are crucial for Physical AI systems because they:

- **Enable Natural Interaction**: Allow humans to communicate using familiar language
- **Reduce Training Requirements**: No need to learn robot-specific commands
- **Increase Accessibility**: Make robotics technology accessible to non-experts
- **Improve Collaboration**: Facilitate human-robot teamwork
- **Enhance Adaptability**: Allow for flexible, context-aware interactions

## Speech Recognition and Synthesis

### Automatic Speech Recognition (ASR)

ASR converts spoken language to text, forming the foundation of conversational robotics:

```python
import numpy as np
import torch
import torch.nn as nn
import librosa
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

class SpeechRecognizer:
    def __init__(self, model_name="facebook/wav2vec2-large-960h"):
        """
        Automatic Speech Recognition system using wav2vec 2.0
        
        Args:
            model_name: Pre-trained model name from Hugging Face
        """
        self.processor = Wav2Vec2Processor.from_pretrained(model_name)
        self.model = Wav2Vec2ForCTC.from_pretrained(model_name)
        self.model.eval()
    
    def preprocess_audio(self, audio_file_path, target_sr=16000):
        """
        Preprocess audio file for ASR
        
        Args:
            audio_file_path: Path to audio file
            target_sr: Target sampling rate
            
        Returns:
            Processed audio tensor
        """
        # Load audio
        audio, sr = librosa.load(audio_file_path, sr=target_sr)
        
        # Normalize audio
        audio = audio / np.max(np.abs(audio))
        
        return audio
    
    def recognize_speech(self, audio_file_path):
        """
        Recognize speech from audio file
        
        Args:
            audio_file_path: Path to audio file
            
        Returns:
            Recognized text
        """
        # Preprocess audio
        audio = self.preprocess_audio(audio_file_path)
        
        # Process with tokenizer
        inputs = self.processor(
            audio, 
            sampling_rate=16000, 
            return_tensors="pt", 
            padding=True
        )
        
        # Perform inference
        with torch.no_grad():
            logits = self.model(inputs.input_values).logits
        
        # Decode predictions
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.processor.batch_decode(predicted_ids)[0]
        
        return transcription

# Example usage (would require an audio file in practice)
# recognizer = SpeechRecognizer()
# text = recognizer.recognize_speech("example_speech.wav")
# print(f"Recognized text: {text}")
```

### Text-to-Speech (TTS)

TTS converts text responses to natural-sounding speech:

```python
import torch
from TTS.api import TTS

class TextToSpeech:
    def __init__(self, model_name="tts_models/en/ljspeech/tacotron2-DDC"):
        """
        Text-to-Speech system using Coqui TTS
        
        Args:
            model_name: Pre-trained TTS model name
        """
        # Initialize TTS model
        self.tts = TTS(model_name)
    
    def synthesize_speech(self, text, output_file_path):
        """
        Synthesize speech from text
        
        Args:
            text: Input text to convert to speech
            output_file_path: Path to save synthesized audio
            
        Returns:
            Path to saved audio file
        """
        # Generate speech
        self.tts.tts_to_file(text=text, file_path=output_file_path)
        
        return output_file_path

# Example usage
# tts = TextToSpeech()
# tts.synthesize_speech("Hello, I am a conversational robot.", "output_speech.wav")
```

### Real-time Speech Processing

For interactive conversations, we need real-time processing:

```python
import pyaudio
import wave
import threading
import queue
import time

class RealTimeSpeechProcessor:
    def __init__(self, speech_recognizer, text_to_speech):
        """
        Real-time speech processing system
        
        Args:
            speech_recognizer: ASR system
            text_to_speech: TTS system
        """
        self.sr = speech_recognizer
        self.tts = text_to_speech
        
        # Audio parameters
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.record_seconds = 5
        
        # Audio queue for processing
        self.audio_queue = queue.Queue()
        self.listening = False
        
        # Initialize PyAudio
        self.audio = pyaudio.PyAudio()
    
    def record_audio(self, duration=5):
        """
        Record audio for specified duration
        
        Args:
            duration: Recording duration in seconds
            
        Returns:
            Audio data
        """
        stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )
        
        print("Recording...")
        frames = []
        
        for i in range(0, int(self.rate / self.chunk * duration)):
            data = stream.read(self.chunk)
            frames.append(data)
        
        print("Finished recording")
        
        stream.stop_stream()
        stream.close()
        
        return b''.join(frames)
    
    def save_audio(self, audio_data, file_path):
        """
        Save recorded audio to file
        
        Args:
            audio_data: Raw audio data
            file_path: Path to save audio file
        """
        wf = wave.open(file_path, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.audio.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(audio_data)
        wf.close()
    
    def start_conversation(self):
        """
        Start a conversation loop
        """
        print("Starting conversation. Press Ctrl+C to stop.")
        
        try:
            while True:
                # Record user speech
                audio_data = self.record_audio(duration=5)
                temp_file = "temp_recording.wav"
                self.save_audio(audio_data, temp_file)
                
                # Recognize speech
                recognized_text = self.sr.recognize_speech(temp_file)
                print(f"Recognized: {recognized_text}")
                
                # Process with dialogue manager (simplified)
                response = self.generate_response(recognized_text)
                print(f"Robot response: {response}")
                
                # Synthesize speech
                output_file = "robot_response.wav"
                self.tts.synthesize_speech(response, output_file)
                
                # Play response (simplified)
                self.play_audio(output_file)
                
        except KeyboardInterrupt:
            print("\nConversation ended.")
    
    def generate_response(self, user_input):
        """
        Generate a simple response to user input
        
        Args:
            user_input: Recognized user speech
            
        Returns:
            Response text
        """
        # This is a simplified response generator
        # In practice, this would use more sophisticated NLU/NLG
        user_input_lower = user_input.lower()
        
        if "hello" in user_input_lower or "hi" in user_input_lower:
            return "Hello! How can I assist you today?"
        elif "how are you" in user_input_lower:
            return "I'm functioning well, thank you for asking!"
        elif "what" in user_input_lower and "your name" in user_input_lower:
            return "I am a conversational robot designed to assist you."
        elif "help" in user_input_lower:
            return "I can help with various tasks. What would you like assistance with?"
        else:
            return f"I heard you say: '{user_input}'. How can I help you with that?"
    
    def play_audio(self, file_path):
        """
        Play audio file
        
        Args:
            file_path: Path to audio file to play
        """
        wf = wave.open(file_path, 'rb')
        
        stream = self.audio.open(
            format=self.audio.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True
        )
        
        data = wf.readframes(self.chunk)
        while data:
            stream.write(data)
            data = wf.readframes(self.chunk)
        
        stream.stop_stream()
        stream.close()
        wf.close()

# Example usage
# sr = SpeechRecognizer()
# tts = TextToSpeech()
# processor = RealTimeSpeechProcessor(sr, tts)
# processor.start_conversation()
```

## Natural Language Understanding (NLU)

### Intent Recognition

Identifying user intents from natural language:

```python
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

class IntentRecognizer:
    def __init__(self):
        """
        Recognize user intents from natural language
        """
        self.intents = {
            'greeting': ['hello', 'hi', 'hey', 'good morning', 'good afternoon'],
            'navigation': ['go to', 'move to', 'navigate to', 'walk to', 'drive to'],
            'grasp': ['pick up', 'take', 'grasp', 'hold', 'grab', 'lift'],
            'place': ['put', 'place', 'set down', 'release', 'drop'],
            'question': ['what', 'where', 'when', 'who', 'how', 'why'],
            'confirmation': ['yes', 'yeah', 'sure', 'okay', 'ok', 'affirmative'],
            'negation': ['no', 'nope', 'negative', 'cancel', 'stop'],
            'information_request': ['tell me', 'explain', 'describe', 'show me', 'what is']
        }
        
        # Create training data for ML model
        self.training_phrases = []
        self.training_labels = []
        
        for intent, phrases in self.intents.items():
            for phrase in phrases:
                self.training_phrases.append(phrase)
                self.training_labels.append(intent)
        
        # Create and train ML model
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(lowercase=True, ngram_range=(1, 2))),
            ('classifier', MultinomialNB())
        ])
        
        # Train the model
        self.model.fit(self.training_phrases, self.training_labels)
    
    def recognize_intent(self, text):
        """
        Recognize intent from text
        
        Args:
            text: Input text
            
        Returns:
            Recognized intent and confidence score
        """
        # Use rule-based approach first for exact matches
        text_lower = text.lower()
        
        for intent, phrases in self.intents.items():
            for phrase in phrases:
                if phrase in text_lower:
                    return intent, 1.0
        
        # Use ML model for more complex understanding
        predicted_intent = self.model.predict([text])[0]
        prediction_proba = self.model.predict_proba([text])[0]
        confidence = max(prediction_proba)
        
        return predicted_intent, confidence

# Example usage
intent_recognizer = IntentRecognizer()

test_sentences = [
    "Hello there!",
    "Please go to the kitchen",
    "Can you pick up the red cup?",
    "What time is it?",
    "Yes, that's correct"
]

print("Intent Recognition Examples:")
for sentence in test_sentences:
    intent, confidence = intent_recognizer.recognize_intent(sentence)
    print(f"  '{sentence}' -> Intent: {intent}, Confidence: {confidence:.2f}")
```

### Entity Extraction

Identifying important entities from user utterances:

```python
import spacy
import re
from datetime import datetime

class EntityExtractor:
    def __init__(self):
        """
        Extract named entities and other important information from text
        """
        # Load spaCy model (install with: python -m spacy download en_core_web_sm)
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("spaCy model not found. Please install with: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        # Define patterns for specific entities
        self.location_patterns = [
            r'\b(kitchen|living room|bedroom|office|bathroom|garage|garden|dining room|hallway|entrance)\b',
            r'\b(room|area|space|zone)\b',
        ]
        
        self.object_patterns = [
            r'\b(cup|bottle|book|phone|box|chair|table|pen|notebook|laptop)\b',
            r'\b(item|object|thing|article|product)\b',
        ]
        
        self.color_patterns = [
            r'\b(red|blue|green|yellow|purple|orange|pink|brown|black|white|gray|grey)\b'
        ]
    
    def extract_entities(self, text):
        """
        Extract entities from text
        
        Args:
            text: Input text
            
        Returns:
            Dictionary of extracted entities
        """
        entities = {
            'locations': [],
            'objects': [],
            'colors': [],
            'persons': [],
            'quantities': [],
            'times': [],
            'spans': []  # Raw spaCy entities
        }
        
        # Use spaCy for general entity recognition
        if self.nlp:
            doc = self.nlp(text)
            for ent in doc.ents:
                entities['spans'].append({
                    'text': ent.text,
                    'label': ent.label_,
                    'start': ent.start_char,
                    'end': ent.end_char
                })
                
                # Categorize entities
                if ent.label_ == "PERSON":
                    entities['persons'].append(ent.text)
                elif ent.label_ in ["TIME", "DATE"]:
                    entities['times'].append(ent.text)
        
        # Use regex patterns for specific entities
        text_lower = text.lower()
        
        # Extract locations
        for pattern in self.location_patterns:
            matches = re.findall(pattern, text_lower)
            entities['locations'].extend(matches)
        
        # Extract objects
        for pattern in self.object_patterns:
            matches = re.findall(pattern, text_lower)
            entities['objects'].extend(matches)
        
        # Extract colors
        for pattern in self.color_patterns:
            matches = re.findall(pattern, text_lower)
            entities['colors'].extend(matches)
        
        # Extract quantities (numbers)
        quantity_matches = re.findall(r'\b\d+\b', text)
        entities['quantities'] = [int(q) for q in quantity_matches]
        
        return entities

# Example usage
entity_extractor = EntityExtractor()

test_sentences = [
    "Bring me the red cup from the kitchen",
    "Go to John's office and wait there",
    "Pick up three books from the table",
    "Meet me at 3 PM in the conference room"
]

print("\nEntity Extraction Examples:")
for sentence in test_sentences:
    entities = entity_extractor.extract_entities(sentence)
    print(f"  Sentence: '{sentence}'")
    for entity_type, entity_list in entities.items():
        if entity_list:
            print(f"    {entity_type}: {entity_list}")
```

## Dialogue Management

### State-Based Dialogue Manager

Managing conversation flow and context:

```python
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional

class DialogueState:
    def __init__(self):
        """
        Represent the state of a dialogue
        """
        self.session_id = str(uuid.uuid4())
        self.turn_count = 0
        self.context = {}
        self.user_goals = []
        self.robot_goals = []
        self.history = []
        self.current_intent = None
        self.pending_confirmation = None
        self.timestamp = datetime.now()
    
    def update_context(self, key, value):
        """Update dialogue context"""
        self.context[key] = value
    
    def add_to_history(self, speaker, text, metadata=None):
        """Add utterance to dialogue history"""
        turn = {
            'turn_id': self.turn_count,
            'speaker': speaker,
            'text': text,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        self.history.append(turn)
        self.turn_count += 1

class DialogueManager:
    def __init__(self):
        """
        Manage dialogue flow and context
        """
        self.current_state = DialogueState()
        self.intent_recognizer = IntentRecognizer()
        self.entity_extractor = EntityExtractor()
        
        # Define dialogue policies
        self.policies = {
            'greeting': self.handle_greeting,
            'navigation': self.handle_navigation,
            'grasp': self.handle_grasp,
            'place': self.handle_place,
            'question': self.handle_question,
            'confirmation': self.handle_confirmation,
            'negation': self.handle_negation,
            'information_request': self.handle_information_request
        }
    
    def process_user_input(self, user_input: str) -> str:
        """
        Process user input and generate response
        
        Args:
            user_input: Text from user
            
        Returns:
            Response text
        """
        # Add user input to history
        self.current_state.add_to_history('user', user_input)
        
        # Recognize intent
        intent, confidence = self.intent_recognizer.recognize_intent(user_input)
        self.current_state.current_intent = intent
        
        # Extract entities
        entities = self.entity_extractor.extract_entities(user_input)
        
        # Update context with entities
        for entity_type, entity_list in entities.items():
            if entity_list:
                self.current_state.update_context(entity_type, entity_list)
        
        # Generate response based on intent
        if intent in self.policies:
            response = self.policies[intent](user_input, entities, confidence)
        else:
            response = self.handle_unknown_intent(user_input)
        
        # Add robot response to history
        self.current_state.add_to_history('robot', response)
        
        return response
    
    def handle_greeting(self, user_input: str, entities: Dict, confidence: float) -> str:
        """Handle greeting intent"""
        greetings = ["Hello!", "Hi there!", "Greetings!", "Nice to meet you!"]
        import random
        return random.choice(greetings)
    
    def handle_navigation(self, user_input: str, entities: Dict, confidence: float) -> str:
        """Handle navigation intent"""
        locations = entities.get('locations', [])
        if locations:
            location = locations[0]
            return f"Okay, I will navigate to the {location}."
        else:
            return "Where would you like me to go?"
    
    def handle_grasp(self, user_input: str, entities: Dict, confidence: float) -> str:
        """Handle grasp intent"""
        objects = entities.get('objects', [])
        colors = entities.get('colors', [])
        
        if objects:
            obj = objects[0]
            if colors:
                color = colors[0]
                return f"Okay, I will pick up the {color} {obj}."
            else:
                return f"Okay, I will pick up the {obj}."
        else:
            return "What would you like me to pick up?"
    
    def handle_place(self, user_input: str, entities: Dict, confidence: float) -> str:
        """Handle place intent"""
        locations = entities.get('locations', [])
        if locations:
            location = locations[0]
            return f"Okay, I will place the object in the {location}."
        else:
            return "Where would you like me to place the object?"
    
    def handle_question(self, user_input: str, entities: Dict, confidence: float) -> str:
        """Handle question intent"""
        # This is a simplified response - in practice, this would connect to a knowledge base
        return "That's an interesting question. Could you provide more details?"
    
    def handle_confirmation(self, user_input: str, entities: Dict, confidence: float) -> str:
        """Handle confirmation intent"""
        if self.current_state.pending_confirmation:
            # Process the confirmed action
            action = self.current_state.pending_confirmation
            self.current_state.pending_confirmation = None
            return f"Proceeding with {action}."
        else:
            return "I understand. How can I assist you further?"
    
    def handle_negation(self, user_input: str, entities: Dict, confidence: float) -> str:
        """Handle negation intent"""
        if self.current_state.pending_confirmation:
            # Cancel the pending action
            self.current_state.pending_confirmation = None
            return "Action cancelled. How else can I help?"
        else:
            return "I understand. What would you like to do instead?"
    
    def handle_information_request(self, user_input: str, entities: Dict, confidence: float) -> str:
        """Handle information request intent"""
        # This would connect to a knowledge base in practice
        return "I can provide information about various topics. What would you like to know?"
    
    def handle_unknown_intent(self, user_input: str) -> str:
        """Handle unknown intent"""
        return f"I'm not sure I understand. Could you rephrase that?"
    
    def get_dialogue_state(self) -> Dict:
        """Get current dialogue state"""
        return {
            'session_id': self.current_state.session_id,
            'turn_count': self.current_state.turn_count,
            'context': self.current_state.context,
            'history': self.current_state.history[-5:]  # Last 5 turns
        }

# Example usage
dialogue_manager = DialogueManager()

print("\nDialogue Management Examples:")
test_inputs = [
    "Hello, robot!",
    "Please go to the kitchen",
    "Can you pick up the red cup?",
    "What time is it?",
    "Yes, that's correct"
]

for user_input in test_inputs:
    response = dialogue_manager.process_user_input(user_input)
    print(f"User: {user_input}")
    print(f"Robot: {response}\n")

# Print dialogue state
state = dialogue_manager.get_dialogue_state()
print(f"Current dialogue state: Session ID {state['session_id']}, {state['turn_count']} turns")
```

### Context-Aware Dialogue

Maintaining context across multiple turns:

```python
class ContextualDialogueManager(DialogueManager):
    def __init__(self):
        """
        Enhanced dialogue manager with context awareness
        """
        super().__init__()
        self.long_term_memory = {}  # Store persistent information
        self.short_term_context = {}  # Current conversation context
        self.user_preferences = {}  # Remember user preferences
    
    def process_user_input(self, user_input: str) -> str:
        """
        Process user input with enhanced context awareness
        """
        # Add user input to history
        self.current_state.add_to_history('user', user_input)
        
        # Recognize intent and extract entities
        intent, confidence = self.intent_recognizer.recognize_intent(user_input)
        entities = self.entity_extractor.extract_entities(user_input)
        
        # Resolve references in context (e.g., "it", "that", "the object")
        resolved_entities = self.resolve_references(entities, user_input)
        
        # Update context
        self.update_context_with_entities(resolved_entities)
        
        # Determine if this is a follow-up to previous intent
        follow_up_action = self.is_follow_up(intent, user_input)
        
        # Generate response
        if follow_up_action:
            response = self.handle_follow_up(follow_up_action, user_input, resolved_entities)
        elif intent in self.policies:
            response = self.policies[intent](user_input, resolved_entities, confidence)
        else:
            response = self.handle_unknown_intent(user_input)
        
        # Add robot response to history
        self.current_state.add_to_history('robot', response)
        
        return response
    
    def resolve_references(self, entities: Dict, user_input: str) -> Dict:
        """
        Resolve pronouns and references in user input
        
        Args:
            entities: Extracted entities
            user_input: Original user input
            
        Returns:
            Entities with resolved references
        """
        # Check for pronouns that refer to previous entities
        user_input_lower = user_input.lower()
        
        # Resolve "it", "that", "the object" based on previous context
        if any(pronoun in user_input_lower for pronoun in ["it", "that", "the object"]):
            # Look for previously mentioned objects
            if 'objects' in self.short_term_context:
                last_objects = self.short_term_context['objects']
                if last_objects:
                    entities['objects'] = entities.get('objects', []) + [last_objects[-1]]
        
        # Resolve "there", "that place" based on previous locations
        if any(word in user_input_lower for word in ["there", "that place", "the location"]):
            if 'locations' in self.short_term_context:
                last_locations = self.short_term_context['locations']
                if last_locations:
                    entities['locations'] = entities.get('locations', []) + [last_locations[-1]]
        
        return entities
    
    def update_context_with_entities(self, entities: Dict):
        """
        Update dialogue context with new entities
        """
        for entity_type, entity_list in entities.items():
            if entity_list:
                # Store in short-term context
                self.short_term_context[entity_type] = entity_list
                
                # Update long-term memory if appropriate
                if entity_type in ['persons', 'preferences']:
                    for entity in entity_list:
                        if entity_type not in self.long_term_memory:
                            self.long_term_memory[entity_type] = []
                        if entity not in self.long_term_memory[entity_type]:
                            self.long_term_memory[entity_type].append(entity)
    
    def is_follow_up(self, current_intent: str, user_input: str) -> Optional[str]:
        """
        Determine if this is a follow-up to a previous intent
        
        Args:
            current_intent: Current recognized intent
            user_input: User input
            
        Returns:
            Previous intent if this is a follow-up, None otherwise
        """
        # Check if user is confirming or negating a previous suggestion
        if self.current_state.pending_confirmation:
            if current_intent in ['confirmation', 'negation']:
                return self.current_state.pending_confirmation
        
        # Check for follow-up questions
        if current_intent == 'question' and self.short_term_context.get('recent_action'):
            return 'follow_up_question'
        
        return None
    
    def handle_follow_up(self, follow_up_type: str, user_input: str, entities: Dict) -> str:
        """
        Handle follow-up to previous action
        """
        if follow_up_type == 'confirmation':
            # Process the confirmed action
            action = self.current_state.pending_confirmation
            self.current_state.pending_confirmation = None
            return f"Proceeding with {action}."
        elif follow_up_type == 'negation':
            # Cancel the pending action
            self.current_state.pending_confirmation = None
            return "Action cancelled. How else can I help?"
        elif follow_up_type == 'follow_up_question':
            # Answer question about recent action
            recent_action = self.short_term_context.get('recent_action', 'previous action')
            return f"Regarding the {recent_action}, what would you like to know?"
        else:
            return "I'm not sure how this relates to our previous conversation."

# Example usage
contextual_dm = ContextualDialogueManager()

print("\nContextual Dialogue Examples:")
conversation = [
    "I need to move somewhere",
    "Go to the kitchen",  # Navigation intent
    "Can you pick up something?",  # Grasp intent
    "Take the red cup",  # Specify object
    "Put it on the table",  # Place intent, "it" refers to cup
    "How do you know my name?"  # Question about context
]

for user_input in conversation:
    response = contextual_dm.process_user_input(user_input)
    print(f"User: {user_input}")
    print(f"Robot: {response}\n")
```

## Integration with Robot Actions

### Action Planning from Language

Converting natural language commands to robot actions:

```python
from dataclasses import dataclass
from typing import List, Dict, Any
import json

@dataclass
class RobotAction:
    """Represents a robot action"""
    action_type: str  # 'navigation', 'grasp', 'place', 'speak', etc.
    parameters: Dict[str, Any]
    priority: int = 1
    duration_estimate: float = 1.0  # Estimated time in seconds

class LanguageToActionConverter:
    def __init__(self):
        """
        Convert natural language commands to robot actions
        """
        self.action_templates = {
            'navigation': {
                'keywords': ['go to', 'move to', 'navigate to', 'walk to', 'drive to', 'reach'],
                'template': self.create_navigation_action
            },
            'grasp': {
                'keywords': ['pick up', 'take', 'grasp', 'hold', 'grab', 'lift', 'get'],
                'template': self.create_grasp_action
            },
            'place': {
                'keywords': ['put', 'place', 'set down', 'release', 'drop', 'set'],
                'template': self.create_place_action
            },
            'speak': {
                'keywords': ['say', 'tell', 'speak', 'repeat'],
                'template': self.create_speak_action
            }
        }
    
    def convert_to_actions(self, user_input: str, entities: Dict) -> List[RobotAction]:
        """
        Convert user input to a sequence of robot actions
        
        Args:
            user_input: Natural language command
            entities: Extracted entities
            
        Returns:
            List of robot actions
        """
        actions = []
        user_lower = user_input.lower()
        
        # Identify action type based on keywords
        for action_type, config in self.action_templates.items():
            for keyword in config['keywords']:
                if keyword in user_lower:
                    action = config['template'](user_input, entities)
                    if action:
                        actions.append(action)
                    break  # Only create one action per keyword match
        
        # Handle compound commands (e.g., "Go to kitchen and pick up cup")
        if 'and' in user_lower or ',' in user_lower:
            actions.extend(self.handle_compound_command(user_input, entities))
        
        return actions
    
    def create_navigation_action(self, user_input: str, entities: Dict) -> RobotAction:
        """Create navigation action from input"""
        locations = entities.get('locations', [])
        location = locations[0] if locations else 'unknown location'
        
        return RobotAction(
            action_type='navigation',
            parameters={
                'destination': location,
                'avoid_obstacles': True,
                'speed': 'medium'
            },
            duration_estimate=10.0
        )
    
    def create_grasp_action(self, user_input: str, entities: Dict) -> RobotAction:
        """Create grasp action from input"""
        objects = entities.get('objects', [])
        colors = entities.get('colors', [])
        
        obj = objects[0] if objects else 'unknown object'
        color = colors[0] if colors else None
        
        return RobotAction(
            action_type='grasp',
            parameters={
                'object': obj,
                'color': color,
                'grasp_type': 'precision',
                'force_limit': 10.0
            },
            duration_estimate=5.0
        )
    
    def create_place_action(self, user_input: str, entities: Dict) -> RobotAction:
        """Create place action from input"""
        locations = entities.get('locations', [])
        location = locations[0] if locations else 'unknown location'
        
        return RobotAction(
            action_type='place',
            parameters={
                'destination': location,
                'placement_type': 'careful'
            },
            duration_estimate=5.0
        )
    
    def create_speak_action(self, user_input: str, entities: Dict) -> RobotAction:
        """Create speak action from input"""
        # Extract the text to speak (everything after the speaking verb)
        import re
        speak_match = re.search(r'(say|tell|speak|repeat)\s+(.+)', user_input, re.IGNORECASE)
        text_to_speak = speak_match.group(2) if speak_match else user_input
        
        return RobotAction(
            action_type='speak',
            parameters={
                'text': text_to_speak,
                'voice_type': 'neutral'
            },
            duration_estimate=2.0
        )
    
    def handle_compound_command(self, user_input: str, entities: Dict) -> List[RobotAction]:
        """Handle compound commands separated by 'and' or ','"""
        actions = []
        
        # Split on 'and' or ','
        parts = re.split(r'\band\b|,', user_input, flags=re.IGNORECASE)
        
        for part in parts:
            part = part.strip()
            if part:
                # Extract entities for this part
                part_entities = self.extract_entities_for_part(part, entities)
                part_actions = self.convert_to_actions(part, part_entities)
                actions.extend(part_actions)
        
        return actions
    
    def extract_entities_for_part(self, part: str, all_entities: Dict) -> Dict:
        """Extract entities relevant to a specific part of a compound command"""
        # This is a simplified implementation
        # In practice, this would use more sophisticated coreference resolution
        return all_entities

# Example usage
converter = LanguageToActionConverter()

test_commands = [
    "Go to the kitchen",
    "Pick up the red cup",
    "Place it on the table",
    "Say hello to everyone",
    "Go to the living room and pick up the book"
]

print("\nLanguage to Action Conversion Examples:")
for command in test_commands:
    entities = entity_extractor.extract_entities(command)
    actions = converter.convert_to_actions(command, entities)
    
    print(f"Command: '{command}'")
    for action in actions:
        print(f"  -> Action: {action.action_type}, Params: {action.parameters}")
    print()
```

### Robot Action Executor

Executing robot actions based on language commands:

```python
import asyncio
import time
from typing import Callable, Optional

class RobotActionExecutor:
    def __init__(self, robot_interface):
        """
        Execute robot actions based on language commands
        
        Args:
            robot_interface: Interface to control the physical robot
        """
        self.robot = robot_interface
        self.is_executing = False
        self.action_queue = []
        self.current_action = None
        
        # Action execution handlers
        self.action_handlers = {
            'navigation': self.execute_navigation,
            'grasp': self.execute_grasp,
            'place': self.execute_place,
            'speak': self.execute_speak
        }
    
    async def execute_action(self, action: RobotAction) -> bool:
        """
        Execute a single robot action
        
        Args:
            action: RobotAction to execute
            
        Returns:
            True if successful, False otherwise
        """
        if action.action_type not in self.action_handlers:
            print(f"Unknown action type: {action.action_type}")
            return False
        
        self.current_action = action
        self.is_executing = True
        
        try:
            print(f"Executing {action.action_type} action...")
            handler = self.action_handlers[action.action_type]
            success = await handler(action.parameters)
            
            if success:
                print(f"Successfully completed {action.action_type} action")
            else:
                print(f"Failed to complete {action.action_type} action")
            
            return success
            
        except Exception as e:
            print(f"Error executing {action.action_type} action: {e}")
            return False
        finally:
            self.is_executing = False
            self.current_action = None
    
    async def execute_navigation(self, params: Dict) -> bool:
        """
        Execute navigation action
        
        Args:
            params: Navigation parameters
            
        Returns:
            True if successful, False otherwise
        """
        destination = params.get('destination', 'unknown')
        speed = params.get('speed', 'medium')
        
        print(f"Navigating to {destination} at {speed} speed")
        
        # Simulate navigation
        await asyncio.sleep(3)  # Simulate travel time
        
        # In practice, this would call robot navigation functions
        # self.robot.navigate_to(destination, speed)
        
        return True
    
    async def execute_grasp(self, params: Dict) -> bool:
        """
        Execute grasp action
        
        Args:
            params: Grasp parameters
            
        Returns:
            True if successful, False otherwise
        """
        obj = params.get('object', 'unknown')
        color = params.get('color')
        grasp_type = params.get('grasp_type', 'precision')
        force_limit = params.get('force_limit', 10.0)
        
        print(f"Attempting to grasp {f'{color} ' if color else ''}{obj} with {grasp_type} grasp, force limit {force_limit}N")
        
        # Simulate grasp
        await asyncio.sleep(2)  # Simulate grasp time
        
        # In practice, this would call robot manipulation functions
        # self.robot.grasp_object(obj, grasp_type, force_limit)
        
        # Simulate success/failure
        import random
        return random.random() > 0.2  # 80% success rate
    
    async def execute_place(self, params: Dict) -> bool:
        """
        Execute place action
        
        Args:
            params: Place parameters
            
        Returns:
            True if successful, False otherwise
        """
        destination = params.get('destination', 'unknown')
        placement_type = params.get('placement_type', 'careful')
        
        print(f"Placing object at {destination} with {placement_type} placement")
        
        # Simulate placement
        await asyncio.sleep(2)  # Simulate placement time
        
        # In practice, this would call robot manipulation functions
        # self.robot.place_object(destination, placement_type)
        
        return True
    
    async def execute_speak(self, params: Dict) -> bool:
        """
        Execute speak action
        
        Args:
            params: Speak parameters
            
        Returns:
            True if successful, False otherwise
        """
        text = params.get('text', '')
        voice_type = params.get('voice_type', 'neutral')
        
        print(f"Speaking: '{text}' with {voice_type} voice")
        
        # Simulate speech
        await asyncio.sleep(len(text) / 10)  # Simulate speech duration
        
        # In practice, this would call TTS functions
        # self.robot.speak(text, voice_type)
        
        return True
    
    async def execute_action_sequence(self, actions: List[RobotAction]) -> List[bool]:
        """
        Execute a sequence of actions
        
        Args:
            actions: List of RobotAction to execute in sequence
            
        Returns:
            List of success/failure for each action
        """
        results = []
        
        for i, action in enumerate(actions):
            print(f"Executing action {i+1}/{len(actions)}: {action.action_type}")
            success = await self.execute_action(action)
            results.append(success)
            
            if not success:
                print(f"Stopping execution due to failure in action {i+1}")
                break
        
        return results

# Mock robot interface for demonstration
class MockRobotInterface:
    def __init__(self):
        pass

# Example usage
async def run_action_execution_demo():
    mock_robot = MockRobotInterface()
    executor = RobotActionExecutor(mock_robot)
    
    # Create some test actions
    actions = [
        RobotAction('navigation', {'destination': 'kitchen', 'speed': 'medium'}),
        RobotAction('grasp', {'object': 'cup', 'color': 'red', 'grasp_type': 'precision', 'force_limit': 10.0}),
        RobotAction('navigation', {'destination': 'table', 'speed': 'slow'}),
        RobotAction('place', {'destination': 'table', 'placement_type': 'careful'})
    ]
    
    print("Executing action sequence...")
    results = await executor.execute_action_sequence(actions)
    
    print(f"\nExecution results: {results}")
    print(f"Success rate: {sum(results)}/{len(results)}")

# Run the demo
# asyncio.run(run_action_execution_demo())
```

## Evaluation of Conversational Systems

### Usability Metrics

Evaluating conversational robot performance:

```python
import time
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class ConversationMetrics:
    """Metrics for evaluating conversational systems"""
    task_success_rate: float
    response_time_avg: float
    response_time_std: float
    user_satisfaction: float
    misunderstanding_rate: float
    conversation_length_avg: float
    context_preservation_score: float

class ConversationalEvaluator:
    def __init__(self):
        """
        Evaluate conversational robot performance
        """
        self.interactions = []
        self.start_times = {}
    
    def start_interaction(self, session_id: str):
        """Mark start of an interaction"""
        self.start_times[session_id] = time.time()
    
    def end_interaction(self, session_id: str, success: bool, user_satisfaction: float = 3.0):
        """Record end of an interaction"""
        if session_id in self.start_times:
            duration = time.time() - self.start_times[session_id]
            
            interaction = {
                'session_id': session_id,
                'duration': duration,
                'success': success,
                'user_satisfaction': user_satisfaction,  # 1-5 scale
                'timestamp': time.time()
            }
            
            self.interactions.append(interaction)
            del self.start_times[session_id]
    
    def add_misunderstanding(self, session_id: str, user_utterance: str, robot_response: str):
        """Record when robot misunderstands user"""
        for interaction in reversed(self.interactions):
            if interaction['session_id'] == session_id:
                if 'misunderstandings' not in interaction:
                    interaction['misunderstandings'] = []
                interaction['misunderstandings'].append({
                    'user_utterance': user_utterance,
                    'robot_response': robot_response
                })
                break
    
    def calculate_metrics(self) -> ConversationMetrics:
        """Calculate conversation metrics"""
        if not self.interactions:
            return ConversationMetrics(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        
        durations = [i['duration'] for i in self.interactions]
        successes = [i['success'] for i in self.interactions]
        satisfactions = [i.get('user_satisfaction', 3.0) for i in self.interactions]
        
        # Count misunderstandings
        total_misunderstandings = sum(
            len(i.get('misunderstandings', [])) for i in self.interactions
        )
        total_interactions = len(self.interactions)
        
        task_success_rate = sum(successes) / len(successes) if successes else 0
        response_time_avg = sum(durations) / len(durations) if durations else 0
        response_time_std = (sum((d - response_time_avg)**2 for d in durations) / len(durations))**0.5 if durations else 0
        user_satisfaction = sum(satisfactions) / len(satisfactions) if satisfactions else 3.0
        misunderstanding_rate = total_misunderstandings / total_interactions if total_interactions > 0 else 0
        conversation_length_avg = sum(len(i.get('misunderstandings', [])) + 1 for i in self.interactions) / total_interactions if total_interactions > 0 else 1
        
        # Context preservation is a more complex metric, simplified here
        context_preservation_score = self.estimate_context_preservation()
        
        return ConversationMetrics(
            task_success_rate=task_success_rate,
            response_time_avg=response_time_avg,
            response_time_std=response_time_std,
            user_satisfaction=user_satisfaction,
            misunderstanding_rate=misunderstanding_rate,
            conversation_length_avg=conversation_length_avg,
            context_preservation_score=context_preservation_score
        )
    
    def estimate_context_preservation(self) -> float:
        """Estimate how well context is preserved (simplified)"""
        # This would be more sophisticated in practice
        # For now, return a placeholder based on misunderstanding rate
        if not self.interactions:
            return 0.0
        
        misunderstanding_rate = sum(
            len(i.get('misunderstandings', [])) for i in self.interactions
        ) / len(self.interactions) if self.interactions else 0
        
        # Lower misunderstanding rate indicates better context preservation
        return max(0.0, 1.0 - misunderstanding_rate)

# Example evaluation
evaluator = ConversationalEvaluator()

# Simulate some interactions
for i in range(10):
    session_id = f"session_{i}"
    evaluator.start_interaction(session_id)
    
    # Simulate conversation
    time.sleep(0.5 + i * 0.1)  # Simulate processing time
    
    # Random success/failure
    import random
    success = random.random() > 0.2  # 80% success rate
    satisfaction = random.uniform(3.0, 5.0)  # Satisfaction rating
    
    evaluator.end_interaction(session_id, success, satisfaction)
    
    # Sometimes add misunderstandings
    if random.random() < 0.3:  # 30% chance of misunderstanding
        evaluator.add_misunderstanding(
            session_id, 
            "Can you pick up the red cup?", 
            "I heard: Can you pick up the blue book?"
        )

# Calculate metrics
metrics = evaluator.calculate_metrics()

print("\nConversational System Evaluation Metrics:")
print(f"  Task Success Rate: {metrics.task_success_rate:.2f}")
print(f"  Avg Response Time: {metrics.response_time_avg:.2f}s (±{metrics.response_time_std:.2f}s)")
print(f"  User Satisfaction: {metrics.user_satisfaction:.2f}/5.0")
print(f"  Misunderstanding Rate: {metrics.misunderstanding_rate:.2f}")
print(f"  Avg Conversation Length: {metrics.conversation_length_avg:.2f} exchanges")
print(f"  Context Preservation: {metrics.context_preservation_score:.2f}")
```

## Best Practices for Conversational Robotics

### 1. System Design
- Use modular architecture for easy updates and maintenance
- Implement fallback strategies for misunderstood inputs
- Design for graceful degradation when components fail
- Include logging and monitoring for system debugging

### 2. Natural Language Processing
- Combine rule-based and ML-based approaches
- Handle ambiguity and uncertainty in user input
- Implement context-aware understanding
- Use appropriate models for your specific domain

### 3. Interaction Design
- Provide clear feedback about system state
- Confirm critical actions before execution
- Handle interruptions and corrections gracefully
- Maintain natural conversation flow

### 4. Evaluation and Improvement
- Continuously collect user feedback
- Monitor system performance metrics
- Update models based on usage patterns
- Test with diverse user populations

## Looking Ahead

This week we explored conversational robotics, which enables natural human-robot interaction. Next week, we'll dive into LLM-based planning, where we'll explore how large language models can be used for high-level task planning and reasoning in robotic systems.

## Exercises

1. Implement a complete speech recognition and synthesis pipeline
2. Create a dialogue manager with context awareness
3. Develop a system that converts natural language to robot actions
4. Design an evaluation framework for conversational robots
5. Integrate conversational capabilities with navigation and manipulation

## Further Reading

- "Spoken Language Processing" by Huang, Acero, and Hon
- "Natural Language Processing with Python" by Bird, Klein, and Loper
- "Human-Robot Interaction" by Goodrich and Schultz
- "Conversational AI" by Bental et al.