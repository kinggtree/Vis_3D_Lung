// 对用户输入的数据进行验证，表单验证等示例代码


const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const PORT = process.env.PORT || 8000;

// 使用body-parser中间件解析请求体
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// 模拟一个用户数据库，通常应该使用数据库来存储和验证用户信息
const users = [
  { id: 1, username: 'user1', email: 'user1@example.com', password: 'password1' },
  { id: 2, username: 'user2', email: 'user2@example.com', password: 'password2' }
];

// 登录验证路由
app.post('/login', (req, res) => {
  const { username, password } = req.body;
  // 在实际应用中，应该查询数据库来验证用户信息
  const user = users.find(u => u.username === username && u.password === password);
  if (user) {
    res.status(200).json({ message: '登录成功', user });
  } else {
    res.status(401).json({ message: '用户名或密码错误' });
  }
});

// 注册验证路由
app.post('/register', (req, res) => {
  const { username, email, password } = req.body;
  // 在实际应用中，应该进行更严格的输入验证，并且检查用户名或邮箱是否已经存在
  if (!username || !email || !password) {
    res.status(400).json({ message: '请填写完整的注册信息' });
  } else {
    // 在这里执行注册逻辑，通常是将用户信息存储到数据库中
    // 这里只是简单地返回成功消息
    res.status(200).json({ message: '注册成功' });
  }
});

// 启动服务器
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
