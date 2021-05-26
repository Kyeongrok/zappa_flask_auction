var app5 = new Vue({
  el: '#app-5',
  data: {
    input: '롬5:1',
    history:[],
    message: '이곳에 결과가 나옵니다.'
  },
  methods: {
    callApi: function () {
        const input = this.input
        fetch('https://2kstde4150.execute-api.ap-northeast-1.amazonaws.com/dev/v1/find/single/'+input)
        .then(res => {
            return res.json()
        }).then(data => {
            console.log(data)
            this.history.push({'text':data[0]['text'], 'index':data[0]['index']})
        })
    }
  }
})