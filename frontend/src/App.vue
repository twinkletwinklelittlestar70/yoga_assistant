<template>
  <div>
    <Title msg="Welcome to Your Yoga Assitant"/>
    <!-- <p>Pose we support: ["adho mukha svanasana","ananda balasana","ardha matsyendrasana","ardha uttanasana","baddha konasana","bakasana","balasana","bhujapidasana","bitilasana","camatkarasana","chaturanga dandasana","garudasana","gomukhasana","halasana","makarasana","malasana","matsyasana","natarajasana","padmasana","paripurna navasana","parivrtta trikonasana","parsva bakasana","paschimottanasana","prasarita padottanasana","purvottanasana","salabhasana","salamba sarvangasana","savasana","supta baddha konasana","supta matsyendrasana","supta padangusthasana","supta virasana","tittibhasana","upavistha konasana","urdhva dhanurasana","urdhva prasarita eka padasana","ustrasana","utkatasana","utthita hasta padangustasana","utthita parsvakonasana","utthita trikonasana","vasisthasana","virabhadrasana ii","virabhadrasana iii","vriksasana"]</p> -->
    <Upload @onload="imageLoad" @onremove="removeImage"/>
    <el-button class="start-btn" type="success" @click="startAnalyse">Start Analyse</el-button>
    <Result v-if="result.mediapipeImage" :result="result"/>
  </div>
</template>

<script>
import Title from './components/Title.vue'
import Upload from './components/Upload.vue'
import Result from './components/Result.vue'
import { doAnalyse } from './api/api'

export default {
  name: 'App',
  components: {
    Title,
    Upload,
    Result
  },
  data () {
    return {
      originImage: '',
      result: {
        mediapipeImage: '',
        poseName: '',
        score: 0,
        standardImage: '',
        keypoints: []
      }
    }
  },
  methods: {
    imageLoad(url) {
      this.originImage = url
      console.log('emit success!', url)
    },
    startAnalyse() {
      if (!this.originImage) {
        return
      }

      doAnalyse(this.originImage).then((data) => {
        console.log('analyse!', data)
        this.result.mediapipeImage = data.mediapipe_image
        this.result.poseName = data.pose_name
        this.result.keypoints = data.keypoints
        this.result.score = data.score
        this.result.standardImage = data.standar_pose
      })
    },
    removeImage() {
      this.originImage = ''
      this.result = {
        mediapipeImage: '',
        poseName: '',
        score: 0,
        standardImage: '',
        keypoints: []
      }
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 20px;
}
.el-button.el-button--success.start-btn {
  margin-top: 30px;
}
</style>
