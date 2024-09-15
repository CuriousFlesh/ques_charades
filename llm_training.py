import pandas as pd
import ast
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments

# Load the CSV file
df = pd.read_csv('cleaned_movies_updated.csv')

# Convert stringified lists to actual lists
def convert_stringified_lists(row):
    for col in ['cast', 'directors', 'genres', 'movie_tone', 'plot_keywords']:
        if isinstance(row[col], str):
            try:
                row[col] = ast.literal_eval(row[col])
                if not isinstance(row[col], list):
                    row[col] = [row[col]]
            except (ValueError, SyntaxError):
                row[col] = [row[col]]
        else:
            if not isinstance(row[col], list):
                row[col] = [row[col]]
    return row

df = df.apply(convert_stringified_lists, axis=1)

# Convert the DataFrame into a list of dictionaries
data_dict = df.to_dict(orient='records')

# Create a Dataset from the entire data
dataset = Dataset.from_dict({'text': data_dict})

# Load the tokenizer and model
model_name = 'EleutherAI/gpt-neo-125M'
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Set the padding token if needed
if tokenizer.pad_token is None:
    if tokenizer.eos_token:
        tokenizer.pad_token = tokenizer.eos_token
    else:
        tokenizer.add_special_tokens({'pad_token': '[PAD]'})
        tokenizer.pad_token = '[PAD]'

model = AutoModelForCausalLM.from_pretrained(model_name)

# Tokenize the dataset
def preprocess_function(examples):
    texts = [str(item) for item in examples['text']]  # Ensure all text is stringified
    encodings = tokenizer(texts, padding="max_length", truncation=True)
    encodings['labels'] = encodings['input_ids']  # Set the labels to be the same as input_ids
    return encodings

# Tokenize the entire dataset
tokenized_dataset = dataset.map(preprocess_function, batched=True)

# Define training arguments
training_args = TrainingArguments(
    output_dir='./fine_tuned_llama_model',
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir='./logs',
    use_mps_device=False,  # Ensure this is correctly set for your hardware
    report_to="none"  # Suppress report logging if needed
)

# Initialize the Trainer using the entire tokenized dataset
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,  # Using the entire dataset for training
)

# Train the model
trainer.train()

# Save the model and tokenizer
model.save_pretrained('./fine_tuned_llama_model')
tokenizer.save_pretrained('./fine_tuned_llama_model')
