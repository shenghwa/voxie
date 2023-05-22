<template>
  <div class="login">
    <h1 class="login__title">{{ $t('new_account') }}</h1>
    <form class="login__form">
	  <div class="login__form-item">
	    <label class="login__form-label">{{ $t('email') }}：</label>
	    <input type="text" v-model="email" class="login__form-input">
	  </div>
      <div class="login__form-item">
        <label class="login__form-label">{{ $t('username') }}：</label>
        <input type="text" v-model="username" class="login__form-input">
      </div>
      <div class="login__form-item">
        <label class="login__form-label">{{ $t('password') }}：</label>
        <input type="password" v-model="password" class="login__form-input">
      </div>
      <button @click.prevent="register" class="login__form-submit">{{ $t('register') }}</button>
    </form>
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
    register() {
      fetch('http://192.168.18.2:5000/api/user/register', {
        method: 'POST',
        body: new URLSearchParams({
          'username': this.username,
          'password': this.password,
		  'email': this.email
        })
      })
	  .then(response => response.json())
      .then(data => {
        if (data.status == 201) {
          this.message = 'Success'
        } else {
          this.message = 'Username is existed'
        }
      })
      .catch(error => {
        console.error(error)
        this.message = 'Fail to register'
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
}

.login__title {
  font-size: 2rem;
  margin-bottom: 1rem;
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
