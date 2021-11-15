<template>
  <el-upload
    class="yoga-uploader"
    :class="{disabled: uploadDisabled}"
    :action="logoImageUploadUrl"
    list-type="picture-card"
    :file-list="imagelist"
    :headers="headers"
    :limit="1"
    :on-exceed="handleExceed"
    :on-success="handleyogaSuccess"
    :on-remove="handleRemove">
  </el-upload>
</template>

<script>
export default {
  data() {
    return {
      imageUrl: '',
      logoImageUploadUrl: 'http://localhost:8080/api/upload',
      imagelist: [],
    }
  },
  computed: {
    uploadDisabled () {
        return !!this.imageUrl
    },
  },
  emits: ["onload"],
  methods: {
    handleyogaSuccess(res, file) {
      console.log('handleyogaSuccess', res, file)
      this.imageUrl = res.url
      this.$emit("onload", res.url);
    },
    handleRemove(file, fileList) {
      console.log('handleRemove', file, fileList)
      this.imageUrl = ''
      this.$emit("onremove");
    },
    handleExceed() {
      this.$message.warning(
        'Only one image'
      )
    },
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style >
.disabled .el-upload--picture-card {
    display: none;
}
</style>