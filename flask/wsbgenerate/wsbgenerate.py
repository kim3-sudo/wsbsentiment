from aitextgen import aitextgen

class wsbgenerate:
  def textgen():
    ai = aitextgen(model_folder="trained_model",
               tokenizer_file="aitextgen.tokenizer.json",
               to_gpu=True)
    return ai.generate_one(temperature = 0.5, top_p = 0.9)
