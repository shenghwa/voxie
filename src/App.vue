<template>
  <div id="app">
    <div class="tabbar">
	  <select v-model="selectedLanguage" @change="changeLanguage">
		  <option value="en">English</option>
		  <option value="zh">中文</option>
	  </select>
      <router-link to="/components/login" tag="div" class="tabbar-item">{{ $t('login') }}</router-link>
      <router-link to="/components/register" tag="div" class="tabbar-item">{{ $t('register') }}</router-link>
	  <router-link to="/components/contact" tag="div" class="tabbar-item">{{ $t('service') }}</router-link>
      <div class="tabbar-bg"></div>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
	data() {
	    return {
	      selectedLanguage: 'en',
	    }
	  },
	methods: {
	    changeLanguage() {
	      this.$i18n.locale = this.selectedLanguage;
	    }
	  }
}
</script>

<style>
.tabbar {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  height: 50px;
  background-color: #007bff;
  position: relative;
  overflow: hidden;
}

.tabbar-item {
  color: #fff;
  font-size: 18px;
  font-weight: bold;
  margin: 0 20px;
  cursor: pointer;
}

.tabbar-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: #007bff;
  border-top-left-radius: 20px;
  border-top-right-radius: 20px;
  transform: translateY(-50%);
  z-index: -1;
}
</style>
