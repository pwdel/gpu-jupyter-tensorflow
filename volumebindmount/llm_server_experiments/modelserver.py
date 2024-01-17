import argparse
import cherrypy
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class ResponseServer:

    def __init__(self, model_identifier):
        self.tokenizer = AutoTokenizer.from_pretrained(model_identifier)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_identifier,
            device_map="auto", # map device to GPU, then CPU, then RAM
            torch_dtype=torch.bfloat16, # use half precision
            trust_remote_code=True
        )

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def api(self):
        try:
            data = cherrypy.request.json
            prompt = data.get("prompt")
            response_text = self.generate_response(prompt)
            return {"response": response_text}
        except Exception as e:
            cherrypy.log(f"Error: {str(e)}", severity=40)
            cherrypy.response.status = 500
            return {"message": "Internal Server Error"}

    def generate_response(self, prompt):
        inputs = self.tokenizer.encode(
            prompt, 
            return_tensors='pt',
            add_special_tokens=True
        )

        if not torch.cuda.is_available():
            raise RuntimeError("CUDA is not available. Please check your GPU settings.")
        inputs = inputs.to("cuda")

        outputs = self.model.generate(
            inputs,
            max_length=300,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.7
        )
        
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--model',
        help='--model [ARG] is the model identifier or the full path name to the model dir',
        type=str,
        required=True
    )
    args = parser.parse_args()

    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 8080,
        'server.environment': 'production'
        # Add other configurations as needed
    })

    # passing the --model arg to the class constructor, passing arg to init
    cherrypy.quickstart(ResponseServer(args.model))
