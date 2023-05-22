<template>
  <div class="login">
	<div class="login__container">
		<form class="login__form">
		  <div class="login__form-item">
			<label class="login__form-label">{{ $t('email') }}：</label>
			<input type="text" v-model="email" class="login__form-input">
		  </div>
		  <div class="login__form-item">
			<label class="login__form-label">{{ $t('password') }}：</label>
			<input type="password" v-model="password" class="login__form-input">
		  </div>
		  <button @click.prevent="login" class="login__form-submit">{{ $t('login') }}</button>
		</form>
	</div>
	<div v-if="message" class="login__message">{{ message }}</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      password: '',
	  email: '',
      message: ''
    }
  },
  methods: {
		
    login() {
      fetch('http://192.168.18.2:5000/api/user/login', {
        method: 'POST',
        body: new URLSearchParams({
          'email': this.email,
          'password': this.password
        })
      })
	  .then(response => response.json())
      .then(data => {
		  console.log(data)
		  if (data.status == 200){
			  this.message = 'Successed',
			  this.$router.push({
			        name: 'history',
			        query: { token: data.data.token }
			      });
			  // window.location.href = `http://127.0.0.1:7860?token=${data.data.token}`
		  }
		  else{
			  this.message = 'Failed'
		  }
		
      })
      .catch(error => {
        console.error(error)
        this.message = 'Failed'
      })
    },
  }
}
</script>

<style scoped>
.login {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: url("../static/wordCloud.jpg");
  background-repeat: no-repeat;
  background-size: 100% 100%;
}

.login__container {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  background-color: white;
}

.login__image {
  margin-right: 2rem;
}

.login__form {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 0.5rem;
}

.login__form-item {
  display: flex;
  flex-direction: row;
  align-items: center;
  margin-bottom: 1rem;
}

.login__form-label {
  margin-right: 0.5rem;
  font-weight: bold;
}

.login__form-input {
  border: none;
  border-bottom: 1px solid #ccc;
  margin-left: 0.5rem;
  padding: 0.5rem;
  font-size: 1rem;
}

.login__form-submit {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  font-size: 1.2rem;
  font-weight: bold;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
}

.login__message {
  margin-top: 1rem;
  color: red;
  font-weight: bold;
}
</style>
