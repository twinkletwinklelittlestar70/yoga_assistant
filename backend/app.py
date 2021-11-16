from flask import Flask, render_template, request, jsonify
import os
from .utils import gen_uuid, get_ext_name, get_save_path, filepath2url, url2filepath
from .error import InvalidAPIError
from .api.YogaModel import yoga_pose

app = Flask(
    __name__,
    static_folder="./static",
    static_url_path="/",
    template_folder="./static")

# Error Handler
@app.errorhandler(InvalidAPIError)
def invalid_api_usage(e):
    return jsonify(e.to_dict())

@app.route('/')
def index():
    '''
        When browser access this page, use render_template to render index.html
        Router should be handled in front end
    '''
    return render_template("index.html")

# 用户上传图片保存到静态服务目录，并返回给前端可以使用的url
@app.route('/api/upload', methods=['POST', 'PUT'])
def image_upload():
    # get upload image and save
    try:
        root = request.url_root
        image = request.files['file']
        new_name = gen_uuid() + get_ext_name(image.filename)
        save_file_path = get_save_path(new_name)

        print('[File Path] ', save_file_path)
        image.save(save_file_path)
        
        url = filepath2url(root, save_file_path)
        print('[Http url] ', url)
    except:
        print("An exception occurred")
        raise InvalidAPIError("upload error", status_code=1)

    return jsonify({"url": url}) # http://localhost:5000/images/aaba390a-d1dd-47af-adc3-b2e0c6df2fde.jpg

# Start analysis the image
@app.route('/api/analyse', methods=['POST'])
def image_analyse():
    try:
        data = request.json
        url = data['url']
        root = request.url_root

        filepath = url2filepath(url)
        
        # Do pose estimation
        keypoints_data, lm_image_path = yoga_pose.mediapipe(filepath)
        lm_image_url = filepath2url(root, lm_image_path, subpath='/anno_images/')
        
        # Do the classification
        pose_name = yoga_pose.predictPoseClass(keypoints_data)

        # Get the standard pose
        standard_filepath = yoga_pose.getStandardPose(pose_name)
        standard_url = filepath2url(root, standard_filepath, subpath=os.path.join('/standard/', pose_name))
        
        # Do the scoring
        score = yoga_pose.evaluatePose(filepath, standard_filepath)

    except Exception as e:
        print('Error: ', e)
        raise InvalidAPIError("analyse error", status_code=2)

    return jsonify({
        "mediapipe_image": lm_image_url,
        "keypoints": keypoints_data,
        "pose_name": pose_name,
        "score": score,
        "standar_pose": standard_url,
    })
    

if __name__ == '__main__':
    app.run()