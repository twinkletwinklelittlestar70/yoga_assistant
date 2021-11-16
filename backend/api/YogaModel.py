import tensorflow as tf
import numpy as np
import cv2
import mediapipe as mp
import joblib
import os
from .. import config
from ..models import scorer

# import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class YogaModel():
    def __init__(self):
        # Load the model
        # self.model = tf.keras.models.load_model(config.CLASSIFICATION_MODEL_PATH)
        self.classifier = joblib.load(config.CLASSIFICATION_MODEL_PATH)
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose_scorer = scorer.load_model(os.path.join(BASE_DIR, config.SCORING_MODEL_PATH))

        pass
    
    def mediapipe(self, filepath, ifdraw=True):
        '''
        Applying mediapipe to do pose estimation for one image
        
        Args:
            filepath
        Returns:
            33 normalized keypoints
        '''

        # Apply mediapipe to do the pose estimation
        pose = self.mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)
        image = cv2.imread(filepath)
        image_hight, image_width, _ = image.shape
        print('img shape===>', image_hight, image_width)

        pose_results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        print('pose result====>', len(pose_results.pose_landmarks.landmark))
        keypoints_data = []
        for _, lm in enumerate(pose_results.pose_landmarks.landmark):
            # print('lanmark', id, lm)
            keypoints_data.append([lm.x, lm.y, lm.z, lm.visibility])
        
        if ifdraw == False:
            return keypoints_data
        
        # Draw pose landmark on image
        annotated_image = image.copy()
        self.mp_drawing.draw_landmarks(annotated_image, pose_results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
        annotated_image_path = filepath.replace('/static/images/', '/static/anno_images/')
        cv2.imwrite(annotated_image_path, annotated_image)

        return keypoints_data, annotated_image_path

    def predictPoseClass(self, keypoints):
        '''
        Predic yoga pose for one image with 33 keypoins

        Args:
            keypoints
        
        Returns:
            pose name
        '''
        print('\n\nstart predictPoseClass!')
        
        # 预处理数据
        input_data = []
        for lm in keypoints:
            input_data.append(lm[0]) # x
            input_data.append(lm[1]) # y
        
        # print('\n input data ', input_data)
        y_pred = self.classifier.predict([input_data])
        print('\n posture predict result: ', y_pred[0])

        return y_pred[0]
    
    def getStandardPose(self, posename):
        '''
        get standard pose filepath by posename

        Args:
            keypoints
        
        Returns:
            pose name
        '''
        basedir = os.path.abspath(os.path.dirname(__name__))
        filepath = basedir + "/static/standard/" + posename
        file_list = os.listdir(filepath)
        
        # Random pick or the first one?
        return os.path.join(filepath, file_list[0])
    
    def _preprocess_keypoints(self, list_33_data):
        input_data_x = []
        input_data_y = []
        for lm in list_33_data:
            input_data_x.append(lm[0])
            input_data_y.append(lm[1])
        input_data = np.array([input_data_x, input_data_y], dtype=np.float32)
    
        print('=====> shape of input', input_data.shape, input_data.dtype)
        return input_data
    
    def evaluatePose(self, user_path, standard_path):
        '''
        evaluate the pose image and return score

        Args:
            user_path: user pose image file path
            standard_path: standard pose image file path
        
        Returns:
            score {int} the evaluated score
        '''
        print('calling evaluatePose', user_path, standard_path)
        user_keyoints = self.mediapipe(user_path, ifdraw=False)
        standard_keyponits = self.mediapipe(standard_path,  ifdraw=False)
        
        input_1 = self._preprocess_keypoints(user_keyoints)
        input_2 = self._preprocess_keypoints(standard_keyponits)

        score = float(scorer.inference(self.pose_scorer, input_1, input_2))

        print('evaluatePose result ===> ', score)
        return score

    
yoga_pose = YogaModel()
