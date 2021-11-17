<template>
  <div class="result-container">
    <div>Yoga Pose Name: {{result.poseName}}</div>
    <div class="pose-container">
      <div class="pose-display student-pose">
        <span>Your pose</span>
        <img :src=result.mediapipeImage />
        <span>Score: {{(result.score * 100).toFixed(2)}}</span>
      </div>
      <div class="pose-display standard-pose">
        <span>Standard pose</span>
        <img :src=result.standardImage />
        <span>&nbsp;</span>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'Result',
  props: {
    result: Object,
  },
  data () {
    return {
      mediapipeImage: ''
    }
  },
  components: {
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.result-container {
  margin-top: 20px;
}
.pose-container {
  display: flex;
  justify-content: space-between;
}
.pose-display {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
}
.pose-display span {
  margin: 10px auto;
}
img {
  width: 80%;
  max-width: 350px;
  border: solid black 1px;
}
</style>
