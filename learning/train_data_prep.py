"""
TRAINING DATA PREPARATION MODULE
=================================

This module handles:
1. Loading unknown queries from logs
2. Creating input-output training pairs
3. Data cleaning and preprocessing
4. Train/validation/test split
5. Dataset statistics and analysis

MATHEMATICAL CONCEPTS:
======================
Data Distribution: We use stratified sampling to ensure training data reflects
real-world query patterns. The goal is to create a representative sample.

If we have 10,000 unknown queries with distribution:
- Greetings: 20%
- Questions: 60%
- Commands: 15%
- Other: 5%

After train/val/test split (70/15/15):
- Train: 7000 examples (maintains 20/60/15/5 ratio)
- Val: 1500 examples
- Test: 1500 examples

This prevents data bias where one category dominates training.
"""

import json
import os
from pathlib import Path
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional
import random
from dataclasses import dataclass, asdict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _default_data_dir() -> str:
    repo = Path(__file__).resolve().parent.parent
    return str(repo / "src" / "Asuna_data" / "server") + os.sep


@dataclass
class TrainingExample:
    """
    A single training example with input and target output.
    
    Attributes:
        input_text: User query/unmatched input
        output_text: Desired bot response or cleaned query
        intent: Classified intent (optional, for intent classification)
        confidence: Human annotator confidence in label (0-1)
        source: Where this example came from (log_file, manual, etc)
    """
    input_text: str
    output_text: str
    intent: Optional[str] = None
    confidence: float = 1.0
    source: str = "unknown_logs"


class TrainingDataset:
    """
    Manages training data loading, preprocessing, and splitting.
    """
    
    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = data_dir if data_dir is not None else _default_data_dir()
        self.examples: List[TrainingExample] = []
        self.stats = {
            'total_examples': 0,
            'avg_input_length': 0,
            'avg_output_length': 0,
            'intent_distribution': {},
            'unique_intents': 0,
        }
    
    def load_unknown_queries(self, filepath: str = "unknown query.txt") -> int:
        """
        Load unknown queries from log file.
        
        File format expected:
        ['user_input', 'some_context']
        ['another_input', 'more_context']
        ...
        
        Returns:
            Number of examples loaded
        """
        full_path = os.path.join(self.data_dir, filepath)
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError:
            logger.error(f"File not found: {full_path}")
            return 0
        
        loaded = 0
        for line in lines:
            try:
                # Parse the format: ['input', 'context']
                if line.strip().startswith("['"):
                    # Remove brackets and split by ', '
                    line = line.strip()
                    # Extract strings from list format
                    parts = eval(line)  # Safe here since it's our own log format
                    
                    if isinstance(parts, list) and len(parts) >= 2:
                        input_text = parts[0].strip()
                        # context_text = parts[1].strip()
                        
                        # Create a training example
                        if input_text:  # Only if input is not empty
                            example = TrainingExample(
                                input_text=input_text,
                                output_text=input_text,  # Initially same, needs human labeling
                                source="unknown_logs"
                            )
                            self.examples.append(example)
                            loaded += 1
            except Exception as e:
                logger.debug(f"Could not parse line: {line[:50]}... Error: {e}")
                continue
        
        logger.info(f"Loaded {loaded} examples from {filepath}")
        return loaded
    
    def load_manual_training_data(self, filepath: str) -> int:
        """
        Load manually created training data from JSON file.
        
        Expected format:
        [
            {
                "input": "what time is it",
                "output": "It's currently ...",
                "intent": "time_query",
                "confidence": 1.0
            },
            ...
        ]
        """
        full_path = os.path.join(self.data_dir, filepath)
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            logger.error(f"File not found: {full_path}")
            return 0
        
        loaded = 0
        for item in data:
            example = TrainingExample(
                input_text=item.get('input', '').strip(),
                output_text=item.get('output', '').strip(),
                intent=item.get('intent'),
                confidence=float(item.get('confidence', 1.0)),
                source=item.get('source', 'manual')
            )
            if example.input_text and example.output_text:
                self.examples.append(example)
                loaded += 1
        
        logger.info(f"Loaded {loaded} manually annotated examples from {filepath}")
        return loaded
    
    def remove_duplicates(self) -> int:
        """
        Remove duplicate examples while keeping highest confidence version.
        
        MATHEMATICAL CONCEPT - Deduplication:
        If we have duplicates with different outputs:
            Input: "hello"
            Output1: "Hi there!" (confidence: 0.9)
            Output2: "Hello!" (confidence: 1.0)
        
        We keep the one with highest confidence (1.0).
        This prevents conflicting training signals where the model learns:
        P(output1 | input) and P(output2 | input) simultaneously.
        """
        before = len(self.examples)
        
        # Group by input_text
        input_groups = defaultdict(list)
        for example in self.examples:
            input_groups[example.input_text].append(example)
        
        # Keep only highest confidence example for each input
        deduplicated = []
        for input_text, examples in input_groups.items():
            best_example = max(examples, key=lambda x: x.confidence)
            deduplicated.append(best_example)
        
        self.examples = deduplicated
        removed = before - len(self.examples)
        
        logger.info(f"Removed {removed} duplicate examples")
        return removed
    
    def _tokenize_for_stats(self, text: str) -> List[str]:
        """Simple tokenization for statistics."""
        return text.lower().split()
    
    def calculate_statistics(self):
        """
        Calculate and store dataset statistics.
        
        STATISTICAL CONCEPTS:
        - Mean: Average length of inputs/outputs
        - Distribution: How many examples per intent
        - Variance: How much inputs vary in length
        """
        if not self.examples:
            logger.warning("No examples to calculate statistics")
            return
        
        input_lengths = []
        output_lengths = []
        intents = []
        
        for example in self.examples:
            input_lengths.append(len(self._tokenize_for_stats(example.input_text)))
            output_lengths.append(len(self._tokenize_for_stats(example.output_text)))
            if example.intent:
                intents.append(example.intent)
        
        # Calculate mean
        mean_input = sum(input_lengths) / len(input_lengths) if input_lengths else 0
        mean_output = sum(output_lengths) / len(output_lengths) if output_lengths else 0
        
        # Calculate variance (measure of spread)
        # Variance = mean((x - mean)^2)
        var_input = sum((x - mean_input) ** 2 for x in input_lengths) / len(input_lengths) if input_lengths else 0
        var_output = sum((x - mean_output) ** 2 for x in output_lengths) / len(output_lengths) if output_lengths else 0
        
        intent_dist = Counter(intents)
        
        self.stats = {
            'total_examples': len(self.examples),
            'avg_input_length': round(mean_input, 2),
            'avg_output_length': round(mean_output, 2),
            'var_input_length': round(var_input, 2),
            'var_output_length': round(var_output, 2),
            'max_input_length': max(input_lengths) if input_lengths else 0,
            'max_output_length': max(output_lengths) if output_lengths else 0,
            'min_input_length': min(input_lengths) if input_lengths else 0,
            'min_output_length': min(output_lengths) if output_lengths else 0,
            'intent_distribution': dict(intent_dist),
            'unique_intents': len(intent_dist),
        }
        
        logger.info(f"Dataset Statistics:\n{json.dumps(self.stats, indent=2)}")
    
    def train_val_test_split(
        self, 
        train_ratio: float = 0.7,
        val_ratio: float = 0.15,
        test_ratio: float = 0.15,
        seed: int = 42,
        stratify_by_intent: bool = True
    ) -> Tuple[List[TrainingExample], List[TrainingExample], List[TrainingExample]]:
        """
        Split data into training, validation, and test sets.
        
        MATHEMATICAL CONCEPT - Stratified Train/Val/Test Split:
        
        Goal: Ensure all sets have similar class distribution
        
        Example with two intents:
        - Greetings: 60% of data
        - Questions: 40% of data
        
        Without stratification (random split):
        - Train: 63% greetings, 37% questions (BIASED!)
        - Val: 58% greetings, 42% questions
        - Test: 55% greetings, 45% questions
        
        With stratification:
        - Train: 60% greetings, 40% questions (SAME!)
        - Val: 60% greetings, 40% questions
        - Test: 60% greetings, 40% questions
        
        This prevents model from learning intent distribution as a proxy.
        """
        random.seed(seed)
        
        if stratify_by_intent and any(ex.intent for ex in self.examples):
            # Group by intent
            intent_groups = defaultdict(list)
            for example in self.examples:
                intent = example.intent or "unknown"
                intent_groups[intent].append(example)
            
            train, val, test = [], [], []
            
            # Split each intent group separately
            for intent, examples in intent_groups.items():
                random.shuffle(examples)
                
                n = len(examples)
                train_n = int(n * train_ratio)
                val_n = int(n * val_ratio)
                
                train.extend(examples[:train_n])
                val.extend(examples[train_n:train_n + val_n])
                test.extend(examples[train_n + val_n:])
        else:
            # Simple random split
            examples = self.examples.copy()
            random.shuffle(examples)
            
            n = len(examples)
            train_n = int(n * train_ratio)
            val_n = int(n * val_ratio)
            
            train = examples[:train_n]
            val = examples[train_n:train_n + val_n]
            test = examples[train_n + val_n:]
        
        logger.info(f"Split sizes - Train: {len(train)}, Val: {len(val)}, Test: {len(test)}")
        return train, val, test
    
    def save_to_jsonl(self, examples: List[TrainingExample], filepath: str):
        """
        Save examples to JSONL format (one JSON per line).
        
        This is the standard format for HuggingFace transformers training.
        
        Example output file:
        {"input": "hello", "output": "hi there", "intent": "greeting"}
        {"input": "what time", "output": "it is ...", "intent": "time"}
        """
        full_path = os.path.join(self.data_dir, filepath)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            for example in examples:
                json_line = json.dumps(asdict(example), ensure_ascii=False)
                f.write(json_line + '\n')
        
        logger.info(f"Saved {len(examples)} examples to {filepath}")
    
    def save_all_splits(self, train: List[TrainingExample], val: List[TrainingExample], test: List[TrainingExample]):
        """Save all three splits to JSONL files."""
        self.save_to_jsonl(train, "train.jsonl")
        self.save_to_jsonl(val, "val.jsonl")
        self.save_to_jsonl(test, "test.jsonl")
        
        logger.info("All splits saved successfully")


# Example usage
if __name__ == "__main__":
    # Initialize dataset
    dataset = TrainingDataset()
    
    # Load data
    dataset.load_unknown_queries("unknown query.txt")
    
    # Optionally load manually annotated data
    # dataset.load_manual_training_data("training_data.json")
    
    # Clean data
    dataset.remove_duplicates()
    
    # Analyze data
    dataset.calculate_statistics()
    
    # Split data
    train, val, test = dataset.train_val_test_split()
    
    # Save splits
    dataset.save_all_splits(train, val, test)
    
    print("✓ Data preparation complete!")
    print(f"Total examples: {len(dataset.examples)}")
    print(f"Train: {len(train)}, Val: {len(val)}, Test: {len(test)}")
