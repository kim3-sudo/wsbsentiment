from aitextgen import aitextgen

class wsbgenerate:
  """
  wsbgenerate
  
  A class for text generation based on r/wallstreetbets
  
  No defaults.
  """
  def textgen():
    """
    Generate a text sample using the trained aitextgen model.
    
    Parameters
    ----------
    None
    
    Returns
    str : A single string with a sample text
    """
    ai = aitextgen(model_folder="trained_model",
               tokenizer_file="aitextgen.tokenizer.json",
               to_gpu=True)
    return ai.generate_one(temperature = 0.5, top_p = 0.9)
