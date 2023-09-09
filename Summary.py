from transformers import MBartTokenizer, MBartForConditionalGeneration

class Summary:
    def __init__(self) -> None:
        self.model_name = "IlyaGusev/mbart_ru_sum_gazeta"
        self.tokenizer = MBartTokenizer.from_pretrained(self.model_name)
        self.model = MBartForConditionalGeneration.from_pretrained(self.model_name)
    
    def tokenize_summary(self, article_text: str) -> str:
        input_ids = self.tokenizer(
            [article_text],
            max_length=600,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        )["input_ids"]

        output_ids = self.model.generate(
            input_ids=input_ids,
            no_repeat_ngram_size=4
        )[0]
        return self.tokenizer.decode(output_ids, skip_special_tokens=True)