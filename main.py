from flask import Flask, request, jsonify, render_template
from flask.globals import request
from flask.json import jsonify
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc
import fs
stub = service_pb2_grpc.V2Stub(ClarifaiChannel.get_grpc_channel())

from clarifai_grpc.grpc.api import service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2


import base64




# with open("C:/Users/adams/Downloads/Eq_it-na_pizza-margherita_sep2005_sml.jpg", "rb") as img_file:
#     my_string = base64.b64encode(img_file.read())

filename = 'pizza.jpg'  # I assume you have a way of picking unique filenames



def convert(my_string):
    imgdata = base64.b64decode(my_string)
    # print(imgdata)
    with open(filename, 'wb') as f:
        f.write(imgdata)
    with open(filename, "rb") as f:
        file_bytes = f.read()

    # print(file_bytes)
    print(1)
    metadata = (('authorization', 'Key 69afe5ce2e5246f8b733fd3213dd7d33'),)
    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            model_id="9504135848be0dd2c39bdab0002f78e9",
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        image=resources_pb2.Image(
                            base64=file_bytes
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )

    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

    # Since we have one input, one output will exist here.
    output = post_model_outputs_response.outputs[0]
    print(output.data.concepts[0])
    y = []
    for x in output.data.concepts:
        if x.value >= 0.1:
            y.append(x.name)
        else:
            break
    return y


app = Flask(__name__)


@app.route('/')
def main():
    return render_template("main.html")


@app.route('/img/', methods=['GET', 'POST'])
def index():
    content = request.json
    img = content['image_base64']
    result = convert(img)
    return {"food": result}


if __name__ == '__main__':
    app.run(debug=True)
