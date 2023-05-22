<template>
  <div>
    <div class="chat-window">
	  <div class="message-container" v-if="this.$i18n.locale=='en'" v-for="question in questions" :key="question.id">
	    <div class="message" :class="{ 'left-message': question.sender === 'bot', 'right-message': question.sender === 'user' }">
	  			<span style="float: left; cursor: pointer; width: 300px;" @click="sendDefaultMessage(question.text)">{{ question.text }}</span>	
	    </div>
	  </div>
	  <div class="message-container" v-if="this.$i18n.locale=='zh'" v-for="question in cn_questions" :key="question.id">
	    <div class="message" :class="{ 'left-message': question.sender === 'bot', 'right-message': question.sender === 'user' }">
	  			<span style="float: left; cursor: pointer; width: 300px;" @click="sendDefaultMessage(question.text)">{{ question.text }}</span>	
	    </div>
	  </div>
      <div class="message-container" v-if="this.$i18n.locale=='en'" v-for="message in messages" :key="message.id">
        <div class="message" :class="{ 'left-message': message.sender === 'bot', 'right-message': message.sender === 'user' }">
			<span style="float: left; cursor: pointer; width: 300px;" @click="sendDefaultMessage(message.text)">{{ message.text }}</span>	
        </div>
      </div>
    </div>
    <div class="chat-input">
      <input type="text" v-model="inputText" @keyup.enter="sendMessage">
      <button @click="sendMessage">{{ $t('send') }}</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
		cn_questions: [
			  {
				id: 0,
				text: '开始使用Voxie',
				sender: 'bot'
			  },
			  {
				id: 1,
				text: '为什么我一天只能问五个问题?',
				sender: 'bot'
			  },
			  {
				id: 2,
				text: '我可以问什么样的问题捏?',
				sender: 'bot'
			  },
			  {
				id: 3,
				text: '为什么有的问题没有回答捏?',
				sender: 'bot'
			  },
			  {
				id: 4,
				text: '注册新用户时的限制',
				sender: 'bot'
			  },
			  {
				id: 1,
				text: '您好，有什么可以帮您的吗?',
				sender: 'bot'
			  }
		],
	  questions: [
		  {
		    id: 0,
		    text: 'Getting start with Voxie.',
		    sender: 'bot'
		  },
		  {
		    id: 1,
		    text: 'Why can I only ask 15 questions in one day?',
		    sender: 'bot'
		  },
		  {
		    id: 2,
		    text: 'Which kind of question can I ask?',
		    sender: 'bot'
		  },
		  {
		    id: 3,
		    text: 'Why can\'t I get answers to some question?',
		    sender: 'bot'
		  },
		  {
		    id: 4,
		    text: 'Precautions for registration.',
		    sender: 'bot'
		  },
		  {
		    id: 1,
		    text: 'Hi, how can I help you? You can try to ask the quetions above.',
		    sender: 'bot'
		  }
	  ],
      messages: [],
      inputText: '',
	  question_index: '5',
	  answer: '',
    }
  },
  methods: {
	
    sendMessage() {
      if (!this.inputText) {
        return;
      }
      this.messages.push({
        id: this.messages.length + 1,
        text: this.inputText,
        sender: 'user'
      });
	  if (this.inputText == 'Getting start with Voxie.') {
		  this.question_index = '0';
	  }
	  else if (this.inputText == 'Why can I only ask 15 questions in one day?') {
	  		  this.question_index = '1';
	  }
	  else if (this.inputText == 'Which kind of question can I ask?') {
	  		  this.question_index = '2';
	  }
	  else if (this.inputText == 'Why can\'t I get answers to some question?') {
	  		  this.question_index = '3';
	  }
	  else if (this.inputText == 'Precautions for registration.') {
	  		  this.question_index = '4';
	  }
	  else {
		  this.question_index = '5';
	  };
      this.inputText = '';
      setTimeout(() => {
		fetch(`http://192.168.18.2:5000/api/contact/answer?question_index=${this.question_index}`)
		.then(response => response.json())
		.then(data => {
			this.answer = data.data.answer;
			this.messages.push({
			  id: this.messages.length + 1,
			  text: this.answer,
			  sender: 'bot'
			});
		}).catch(error => {
		  console.error(error)
		})
        
      }, 1000);
    },
	sendDefaultMessage(message) {
		this.messages.push({
		  id: this.messages.length + 1,
		  text: message,
		  sender: 'user'
		});
		if (message == 'Getting start with Voxie.') {
				  this.question_index = '0';
		};
		if (message == 'Why can I only ask 15 questions in one day?') {
				  this.question_index = '1';
		};
		if (message == 'Which kind of question can I ask?') {
				  this.question_index = '2';
		};
		if (message == 'Why can\'t I get answers to some question?') {
				  this.question_index = '3';
		};
		if (message == 'Precautions for registration.') {
				  this.question_index = '4';
		};
		message = '';
		setTimeout(() => {
				fetch(`http://192.168.18.2:5000/api/contact/answer?question_index=${this.question_index}`)
				.then(response => response.json())
				.then(data => {
					this.answer = data.data.answer;
					this.messages.push({
					  id: this.messages.length + 1,
					  text: this.answer,
					  sender: 'bot'
					});
				}).catch(error => {
				  console.error(error)
				})
		  
		}, 1000);
	}
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
</style>
