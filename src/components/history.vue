<template>
    <div class="chat-window">
      <div class="message-container" v-for="message in messages" :key="message.id">
        <div class="message" :class="{ 'left-message': message.sender === 'bot', 'right-message': message.sender === 'user' }">
			<span style="float: left; cursor: pointer; width: 300px;">{{ message.text }}</span>	
        </div>
      </div>
    </div>
	<div class="chat-input">
	  <button @click="chat" class="start_chat">{{ $t('chat') }}</button>
	  <button @click="upgrade" class="start_chat">{{ $t('upgrade') }}</button>
	</div>
</template>

<script>
import { useRoute } from 'vue-router';

export default {
    setup() {
      const route=useRoute()
      return {
		  token: route.query.token,
	  }
    },
  data() {
    return {
      messages: [

      ],
    }
  },
  mounted() {
      this.getMessage()
    },
  methods: {
	  upgrade () {
		  fetch(`http://192.168.18.2:5000/api/user/upgrade_role?token=${this.token}`, {
		    method: 'POST',
		  })
	  },
	chat () {
		window.location.href = `http://127.0.0.1:7860?token=${this.token}`
	},
    getMessage() {
	  const route=useRoute();
      setTimeout(() => {
		fetch(`http://192.168.18.2:5000/api/record/record_list?token=${this.token}`)
		.then(response => response.json())
		.then(data => {
			for (let i = 0; i < data.data.items.length; i++) {
			  if (i % 2 == 0){
				  this.messages.push({
				    id: this.messages.length + 1,
				    text: data.data.items[i].content,
				    sender: 'user'
				  });
			  }
			  else {
				  this.messages.push({
				    id: this.messages.length + 1,
				    text: data.data.items[i].content,
				    sender: 'bot'
				  });
			  }
			}
		}).catch(error => {
		  console.error(error)
		})
        
      }, 1000);
    },
  }
}
</script>

<style>
.chat-window {
  height: 800px;
  overflow-y: auto;
}

.message-container {
  display: flex;
  flex-direction: column;
  margin-bottom: 16px;
}

.message {
  max-width: 60%;
  padding: 8px;
  border-radius: 8px;
  white-space: pre-wrap;
}

.left-message {
  align-self: flex-start;
  background-color: #f1f0f0;
  white-space: pre-wrap;
}

.right-message {
  align-self: flex-end;
  background-color: #0084ff;
  color: white;
  white-space: pre-wrap;
}
.chat-input {
  display: flex;
  justify-content: space-between;
  margin-top: 16px;
}

.chat-input input {
  width: 80%;
  margin-right: 16px;
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

.chat-input button {
  background-color: #0084ff;
  color: white;
  padding: 8px 16px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
}

.start_chat {
  margin: auto;
  display: block;
  padding: 0.5rem 1rem;
  font-size: 1.2rem;
  font-weight: bold;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
}

</style>
